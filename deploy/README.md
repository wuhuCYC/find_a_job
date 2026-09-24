# 部署到服务器

在自己电脑上 `python -m jobhunt web` 就够用了。部署到服务器的好处是：**每天自动抓两次职位，手机上随时看排名、改状态**。

两种方式：

- **A. 放在卖点 SaaS（sell_csgo_monitor）那台 VPS 上**，挂在 `https://<服务器 IP>/jobs/`，不需要新域名。一条命令部署。
- **B. 另开一台海外服务器 + 自己的域名**：能在网页上直接定制简历（调用 Claude）。

---

## A. 和 SaaS 同一台 VPS（`deploy_vps.sh`）

流程和 sell_csgo_monitor 一样：在 Mac 上 rsync 代码，再 ssh 上去安装。

### 第一次部署

```bash
# 1. 在 Mac 的仓库目录里写服务器地址（private/ 不进 git）
echo 'VPS_HOST=你的服务器IP' > private/deploy.env
#    如果 ssh 要指定密钥，再加一行：SSH_KEY=~/.ssh/id_ed25519

# 2. 部署（前提：ssh root@你的服务器IP 能免密登录，和你平时 rsync SaaS 用的是同一套）
bash deploy/deploy_vps.sh

# 3. 打开 https://你的服务器IP/jobs/ ，用户名和密码在 private/web_password.txt
```

浏览器如果提示证书和地址不匹配，和你现在用 IP 访问 SaaS 的情况一样（证书是签给域名的）。
等域名备案通过、恢复解析后，用域名加 `/jobs/` 访问就正常了（include 加在同一个 server 块里）。

### 脚本做了什么

| 步骤 | 内容 |
|---|---|
| 同步 | 代码 → `/opt/find_a_job`（不传 `private/ data/ output/ .env`）；另外上传 `private/profile.yaml` 和 `output/base/` 里的基础简历 |
| 隔离 | 新建系统用户 `jobhunt`；代码归 root 只读，`jobhunt` 只能写 `data/` 和 `output/`；systemd 加了 `ProtectSystem=strict`、内存上限 600M |
| 服务 | `jobhunt-web`（127.0.0.1:8765）+ `jobhunt-fetch.timer`（洛杉矶时间每天 7:00、17:00 抓取） |
| nginx | 装 `/etc/nginx/snippets/jobhunt.conf`，在 server_name 含你 IP 的 443 server 块里加**一行** `include`。<br>改之前备份到 `/var/backups/jobhunt-nginx/`；`nginx -t` 不过、或者 SaaS 的 `/` 和 `/api/` 返回码有任何变化，**自动回滚** |
| 密码 | 第一次生成随机密码，直接存进 Mac 的 `private/web_password.txt`（权限 600），不在终端显示 |

这些步骤在沙盒里用「certbot 风格的 SaaS nginx 配置 + 自签证书 + 假后端」完整演练过：
首次部署、重复部署、语法错误回滚、SaaS 返回码变化回滚、重置密码、卸载后配置逐字节恢复。

### 这台机器在国内：两个限制

1. **定制简历在 Mac 上做。** Claude API 在中国大陆不可用，所以服务器的 `.env` 里是 `JOBHUNT_TAILOR=0`，
   网页上的「定制简历」按钮换成了一条可复制的命令：
   ```bash
   python -m jobhunt run                  # Mac 上先抓一次（同一个职位的 uid 两边一样）
   python -m jobhunt tailor '<uid>'       # 从网页复制
   ```
2. **招聘网站从国内访问可能慢或不通。** 部署后先跑一次：
   ```bash
   bash deploy/deploy_vps.sh check        # 在服务器上逐个检查已配置的招聘接口
   ```
   如果很多家不通：在服务器的 `/opt/find_a_job/.env` 里加 `HTTPS_PROXY=http://你的代理:端口`
   （和 SaaS 的 `STEAM_PROXY` 同理，抓取用的 requests 会自动走它），或者抓取继续在 Mac 上做。

投递状态以服务器为准（在网页上改）；Mac 上的 `data/jobs.db` 是另一份，只用来定制简历。

### 常用命令

```bash
bash deploy/deploy_vps.sh            # 更新代码（改了素材库、配置、代码之后重新跑）
bash deploy/deploy_vps.sh status     # 服务状态 + 最近一次抓取的日志
bash deploy/deploy_vps.sh fetch      # 立刻抓一次
bash deploy/deploy_vps.sh check      # 招聘接口连通性
bash deploy/deploy_vps.sh logs       # 网站日志
bash deploy/deploy_vps.sh password   # 忘了密码：重新生成
bash deploy/deploy_vps.sh uninstall  # 停服务、去掉 nginx 那一行 include（代码和数据保留）
```

---

## B. 海外服务器 + 自己的域名

服务器在中国大陆以外时，网页上可以直接定制简历。

```bash
# 1. 代码和依赖
sudo useradd --system --home-dir /opt/find_a_job --shell /usr/sbin/nologin jobhunt
sudo git clone https://github.com/wuhuCYC/find_a_job /opt/find_a_job && cd /opt/find_a_job
sudo python3 -m venv venv && sudo venv/bin/pip install -r deploy/requirements-server.txt
sudo mkdir -p data output private && sudo chown -R jobhunt:jobhunt data output private

# 2. 私人信息从自己电脑拷过去（不进 git），API key 写进 .env
scp private/profile.yaml root@你的服务器:/opt/find_a_job/private/
echo "ANTHROPIC_API_KEY=..." | sudo tee /opt/find_a_job/.env >/dev/null
sudo chown root:jobhunt /opt/find_a_job/.env && sudo chmod 640 /opt/find_a_job/.env

# 3. 服务
sudo cp deploy/jobhunt-web.service deploy/jobhunt-fetch.service deploy/jobhunt-fetch.timer /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now jobhunt-web jobhunt-fetch.timer

# 4. nginx + 密码 + HTTPS：把 nginx.conf 里的 jobs.example.com 换成你的域名
printf 'me:%s\n' "$(openssl passwd -apr1)" | sudo tee /etc/nginx/.jobhunt_htpasswd >/dev/null
sudo cp deploy/nginx.conf /etc/nginx/sites-available/jobhunt
sudo ln -s /etc/nginx/sites-available/jobhunt /etc/nginx/sites-enabled/
sudo certbot --nginx -d jobs.example.com
sudo nginx -t && sudo systemctl reload nginx
```

---

## 安全要点

- **一定要有 nginx 密码**：页面里有你的简历素材、投递记录和签证时间线。
- 网站只监听 `127.0.0.1`，对外只能经过 nginx；nginx 转发时把 Host 设成 `127.0.0.1`，应用只接受本机 Host。
- 写操作要求 `X-Jobhunt` 请求头 + JSON，别的网站没法借你的登录状态替你操作。
- 服务器上不能「打开申请页预填」（`--server` 模式关掉了这个按钮）；投递那一步在自己电脑上做。
