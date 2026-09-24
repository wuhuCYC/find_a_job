#!/usr/bin/env bash
# 在 VPS 上以 root 运行（deploy_vps.sh 通过 ssh 调用，代码已经 rsync 到 /opt/find_a_job）。
# 可以重复运行。只新增东西：独立用户、独立端口、独立 systemd 服务；
# nginx 只在已有 HTTPS server 块里加一行 include，改之前备份，检查不过或 SaaS 返回码变了就自动回滚。
#
# 环境变量：VPS_HOST（必填，网站的 IP 或域名）、WEB_USER（网页登录名，默认 me）、SKIP_NGINX=1（只装服务）
set -euo pipefail

APP=${APP:-/opt/find_a_job}
APP_USER=${APP_USER:-jobhunt}
PORT=8765                                       # 和 jobhunt-web.service、nginx-jobs.conf 一致
SNIPPET=${SNIPPET:-/etc/nginx/snippets/jobhunt.conf}
HTPASSWD=/etc/nginx/.jobhunt_htpasswd           # 和 nginx-jobs.conf 一致
BACKUP_DIR=${BACKUP_DIR:-/var/backups/jobhunt-nginx}
NGINX_RELOAD=${NGINX_RELOAD:-systemctl reload nginx}
NGINX_DIRS=${NGINX_DIRS:-}                      # 空 = nginx_include.py 默认的 sites-enabled + conf.d
ONLY=${ONLY:-}                                  # 只跑某一步：app / nginx / password
VPS_HOST=${VPS_HOST:?需要 VPS_HOST}
WEB_USER=${WEB_USER:-me}

log() { printf '\n==> %s\n' "$*"; }
die() { printf '\n✗ %s\n' "$*" >&2; exit 1; }

[ "$(id -u)" = 0 ] || die "需要 root 运行"
cd "$APP"

setup_app() {
  log "1/5 系统用户 $APP_USER（不和 SaaS 共用用户）"
  id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --home-dir "$APP" --no-create-home --shell /usr/sbin/nologin "$APP_USER"

  log "2/5 目录和权限：代码归 root 只读，$APP_USER 只能写 data/ output/"
  mkdir -p data output private
  chown -R root:root "$APP"
  chmod -R u+rwX,go+rX,go-w "$APP"
  chown -R "$APP_USER:$APP_USER" data output private
  chmod 750 data output
  chmod 700 private
  find private -type f -exec chmod 600 {} +

  log "3/5 Python 虚拟环境（venv/）"
  python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))' || die "需要 Python 3.10 以上"
  [ -x venv/bin/python ] || python3 -m venv venv
  venv/bin/pip install -q --upgrade pip
  venv/bin/pip install -q -r deploy/requirements-server.txt
  runuser -u "$APP_USER" -- venv/bin/python -m jobhunt validate >/dev/null || die "素材库校验没通过"

  log "4/5 .env"
  if [ ! -f .env ]; then
    # systemd 的 EnvironmentFile 不支持行尾注释，注释要单独一行
    printf '%s\n' \
      '# 求职台服务器配置（不进 git）' \
      '# 国内服务器调不了 Claude API：关闭网页上的定制简历，改在自己电脑上运行 python -m jobhunt tailor' \
      'JOBHUNT_TAILOR=0' > .env
  fi
  chown "root:$APP_USER" .env
  chmod 640 .env

  log "5/5 systemd：jobhunt-web + 每天两次的抓取 timer"
  if ss -ltn "sport = :$PORT" | grep -q LISTEN && ! systemctl is-active --quiet jobhunt-web; then
    die "端口 $PORT 被别的程序占用了（ss -ltnp 查看）"
  fi
  install -m 644 deploy/jobhunt-web.service deploy/jobhunt-fetch.service deploy/jobhunt-fetch.timer /etc/systemd/system/
  systemctl daemon-reload
  systemctl enable --quiet jobhunt-web.service jobhunt-fetch.timer
  systemctl restart jobhunt-web.service jobhunt-fetch.timer
  local ok=0
  for _ in $(seq 1 30); do
    if curl -fs --noproxy '*' -o /dev/null "http://127.0.0.1:$PORT/api/data"; then ok=1; break; fi
    sleep 0.5
  done
  if [ "$ok" != 1 ]; then
    journalctl -u jobhunt-web -n 40 --no-pager || true
    die "jobhunt-web 没有起来（上面是日志）"
  fi
  echo "jobhunt-web 已在 127.0.0.1:$PORT 运行"
  if [ ! -s data/jobs.db ]; then
    systemctl start --no-block jobhunt-fetch.service
    echo "第一次抓取已在后台开始（deploy_vps.sh status 查看进度）"
  fi
}

# 生成网页登录密码写进 htpasswd；密码只打印这一次（deploy_vps.sh 会马上存到 Mac 的 private/）
new_password() {
  local password worker
  password=$(openssl rand -base64 24 | tr -dc 'A-Za-z0-9' | head -c 16)
  mkdir -p "$(dirname "$HTPASSWD")"
  printf '%s:%s\n' "$WEB_USER" "$(openssl passwd -apr1 "$password")" > "$HTPASSWD"
  # nginx 的 worker 用户要能读密码文件
  # shellcheck disable=SC2009
  worker=$(ps -o user= -C nginx 2>/dev/null | grep -vx root | head -n1 || true)
  if [ -n "$worker" ]; then
    chgrp "$(id -gn "$worker")" "$HTPASSWD" && chmod 640 "$HTPASSWD"
  else
    chmod 644 "$HTPASSWD"
  fi
  echo "@@WEB_PASSWORD@@ $WEB_USER $password" >&2
  echo "$password"
}

# 从服务器本机按网站的 Host 访问自己，返回 HTTP 状态码
probe() {
  curl -sk --noproxy '*' -o /dev/null -w '%{http_code}' --max-time 10 --resolve "$VPS_HOST:443:127.0.0.1" "${@:2}" "https://$VPS_HOST$1" || true
}

# nginx 的 reload 是异步的：等 worker 换了一批再继续，否则检查可能打到旧配置
nginx_workers() {
  local master
  master=$(pgrep -o -f 'nginx: master' || true)
  if [ -n "$master" ]; then pgrep -P "$master" | sort | tr '\n' ' '; fi
}
reload_nginx() {
  local before
  before=$(nginx_workers)
  $NGINX_RELOAD
  for _ in $(seq 1 40); do
    sleep 0.25
    if [ "$(nginx_workers)" != "$before" ]; then sleep 0.5; return 0; fi
  done
  echo "⚠️ 10 秒内没等到 nginx 重载完成" >&2
}

setup_nginx() {
  log "nginx：/jobs/ 子路径 + 密码"
  command -v nginx >/dev/null || die "没找到 nginx"
  local conf="" saved="" out prev_snippet=""
  local dir_args=()
  for d in $NGINX_DIRS; do dir_args+=(--dir "$d"); done

  local before_root before_api
  before_root=$(probe /)
  before_api=$(probe /api/)
  echo "改之前：/ → $before_root，/api/ → $before_api"

  mkdir -p "$(dirname "$SNIPPET")" "$BACKUP_DIR"
  chmod 700 "$BACKUP_DIR"
  if [ -f "$SNIPPET" ]; then
    prev_snippet="$BACKUP_DIR/jobhunt.conf.prev"
    cp "$SNIPPET" "$prev_snippet"
  fi
  install -m 644 deploy/nginx-jobs.conf "$SNIPPET"

  local password=""
  if [ ! -s "$HTPASSWD" ]; then
    password=$(new_password)
  fi

  rollback() {
    echo "回滚 nginx 配置……"
    if [ -n "$saved" ]; then cp "$saved" "$conf"; fi
    if [ -n "$prev_snippet" ]; then cp "$prev_snippet" "$SNIPPET"; elif [ -n "$saved" ]; then rm -f "$SNIPPET"; fi
    if ! nginx -t 2>/dev/null; then
      echo "⚠️ 回滚后 nginx -t 仍然失败，请手动检查（原配置备份：${saved:-无}）" >&2
      return
    fi
    reload_nginx
    local now
    now=$(probe /)
    if [ "$now" = "$before_root" ]; then
      echo "原来的网站已恢复：/ → $now"
    else
      echo "⚠️ 回滚后 / 返回 $now（改之前是 $before_root），请检查。原配置备份：${saved:-无}" >&2
    fi
  }

  if ! out=$(python3 deploy/nginx_include.py add --host "$VPS_HOST" --snippet "$SNIPPET" --backup-dir "$BACKUP_DIR" "${dir_args[@]}"); then
    rollback
    die "没能自动加 include（原因见上）。nginx 没有改动"
  fi
  echo "$out"
  case "$out" in
    ADDED*) conf=$(echo "$out" | awk '{print $2}'); saved=$(echo "$out" | awk '{print $3}') ;;
  esac

  if ! nginx -t; then rollback; die "nginx -t 没通过，已恢复原配置"; fi
  reload_nginx

  local after_root after_api jobs_code
  after_root=$(probe /)
  after_api=$(probe /api/)
  echo "改之后：/ → $after_root，/api/ → $after_api"
  if [ "$before_root" != "$after_root" ] || [ "$before_api" != "$after_api" ]; then
    rollback
    die "原来网站的返回码变了，已回滚"
  fi
  jobs_code=$(probe /jobs/)
  if [ "$jobs_code" != 401 ]; then rollback; die "/jobs/ 应该要求密码（401），实际是 $jobs_code，已回滚"; fi
  if [ -n "$password" ]; then
    local authed
    authed=$(probe /jobs/api/data -u "$WEB_USER:$password")
    [ "$authed" = 200 ] || { rollback; die "带密码访问 /jobs/api/data 返回 $authed，已回滚"; }
  fi
  echo "✓ https://$VPS_HOST/jobs/ 已上线（不带密码 401，SaaS 不受影响）"
}

case "$ONLY" in
  "") setup_app; if [ "${SKIP_NGINX:-0}" != 1 ]; then setup_nginx; fi ;;
  app) setup_app ;;
  nginx) setup_nginx ;;
  password) new_password >/dev/null; echo "新密码已生成（nginx 每次请求都会读密码文件，不用重载）" ;;
  *) die "ONLY 只能是 app / nginx / password" ;;
esac
