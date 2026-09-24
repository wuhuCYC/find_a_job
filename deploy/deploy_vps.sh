#!/usr/bin/env bash
# 在你的 Mac 上运行：把求职台部署到 VPS 的 /opt/find_a_job，网址是 https://<服务器>/jobs/（带密码）。
# 和 sell_csgo_monitor 一样：rsync 代码 → ssh 上去装 venv / systemd / nginx。可以重复运行（更新也用它）。
#
#   bash deploy/deploy_vps.sh            部署或更新
#   bash deploy/deploy_vps.sh status     服务状态 + 最近一次抓取的日志
#   bash deploy/deploy_vps.sh fetch      立刻抓一次职位
#   bash deploy/deploy_vps.sh check      在服务器上检查每家公司的招聘接口能不能连上
#   bash deploy/deploy_vps.sh logs       网站日志
#   bash deploy/deploy_vps.sh password   重新生成网页登录密码（存到 private/web_password.txt）
#   bash deploy/deploy_vps.sh uninstall  停掉服务、去掉 nginx 里的 include（代码和数据留在服务器上）
#
# 服务器信息写在 private/deploy.env（不进 git）：
#   VPS_HOST=1.2.3.4            # 必填：服务器 IP（或已经解析好的域名）
#   VPS_USER=root               # 可选，默认 root
#   SSH_KEY=~/.ssh/id_ed25519   # 可选，默认用 ssh 自己的配置
#   WEB_USER=me                 # 可选，网页登录名
set -euo pipefail
cd "$(dirname "$0")/.."

# shellcheck source=/dev/null
if [ -f private/deploy.env ]; then . private/deploy.env; fi
: "${VPS_HOST:?请先在 private/deploy.env 里写 VPS_HOST=你的服务器 IP}"
VPS_USER=${VPS_USER:-root}
WEB_USER=${WEB_USER:-me}
APP=/opt/find_a_job
TARGET="$VPS_USER@$VPS_HOST"
SSH_CMD="ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new"
if [ -n "${SSH_KEY:-}" ]; then SSH_CMD="$SSH_CMD -i ${SSH_KEY/#\~/$HOME}"; fi

remote() { $SSH_CMD "$TARGET" "$@"; }
push() { rsync -az -e "$SSH_CMD" "$@"; }

cmd_deploy() {
  local py=python3
  if [ -x .venv/bin/python ]; then py=.venv/bin/python; fi
  echo "==> 本地校验素材库"
  "$py" -m jobhunt validate

  echo "==> 同步代码到 $TARGET:$APP（不传 private/ data/ output/ .env）"
  remote "mkdir -p $APP"
  push --delete \
    --exclude='.git/' --exclude='.venv/' --exclude='venv/' --exclude='__pycache__/' --exclude='.pytest_cache/' \
    --exclude='/private/' --exclude='/data/' --exclude='/output/' --exclude='/.env' --exclude='*.db' \
    --exclude='rendercv_output/' --exclude='.DS_Store' \
    ./ "$TARGET:$APP/"

  if [ -f private/profile.yaml ]; then
    echo "==> 上传 private/profile.yaml（网站的签证时间线要用）"
    remote "mkdir -p $APP/private && chmod 700 $APP/private"
    push private/profile.yaml "$TARGET:$APP/private/profile.yaml"
  else
    echo "（没有 private/profile.yaml：网站照常运行，只是没有个人 OPT 时间线）"
  fi
  if [ -d output/base ]; then
    echo "==> 上传基础简历 PDF（output/base/）"
    remote "mkdir -p $APP/output/base"
    push output/base/ "$TARGET:$APP/output/base/"
  fi

  echo "==> 在服务器上安装"
  run_remote_setup ""
}

# 在服务器上跑 remote_setup.sh。网页密码（第一次部署或 password 命令生成）一出现就存到
# private/web_password.txt，不显示在终端；这样即使之后断线，密码也不会丢。
run_remote_setup() {
  local only=$1 status
  set +e
  remote "VPS_HOST='$VPS_HOST' WEB_USER='$WEB_USER' ONLY='$only' bash $APP/deploy/remote_setup.sh" 2>&1 |
    while IFS= read -r line; do
      case "$line" in
        @@WEB_PASSWORD@@*)
          read -r _ user pass <<< "$line"
          (umask 077; printf '网址：https://%s/jobs/\n用户名：%s\n密码：%s\n' "$VPS_HOST" "$user" "$pass" > private/web_password.txt)
          echo "==> 网页登录名和密码已保存到 private/web_password.txt（只生成这一次）" ;;
        *) printf '%s\n' "$line" ;;
      esac
    done
  status=${PIPESTATUS[0]}
  set -e
  return "$status"
}

case "${1:-deploy}" in
  deploy) cmd_deploy ;;
  password) run_remote_setup password ;;
  status) remote "systemctl --no-pager status jobhunt-web jobhunt-fetch.timer | head -n 20; echo; journalctl -u jobhunt-fetch --no-pager -n 30" ;;
  fetch) remote "systemctl start --no-block jobhunt-fetch && echo '已开始抓取，稍后运行 status 看结果'" ;;
  check) remote "cd $APP && runuser -u jobhunt -- env XDG_CACHE_HOME=$APP/data/.cache venv/bin/python -m jobhunt check" ;;
  logs) remote "journalctl -u jobhunt-web --no-pager -n 100" ;;
  uninstall)
    remote "systemctl disable --now jobhunt-web.service jobhunt-fetch.timer || true
      python3 $APP/deploy/nginx_include.py remove --snippet /etc/nginx/snippets/jobhunt.conf \
        && nginx -t && systemctl reload nginx && rm -f /etc/nginx/snippets/jobhunt.conf
      echo '已停止服务并去掉 nginx include；代码和数据还在 $APP'" ;;
  *) echo "用法：bash deploy/deploy_vps.sh [deploy|status|fetch|check|logs|password|uninstall]" >&2; exit 2 ;;
esac
