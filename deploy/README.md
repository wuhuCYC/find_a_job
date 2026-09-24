# 部署到服务器（可选）

在自己电脑上 `python -m jobhunt web` 就够用了。部署到服务器的好处是：**每天自动抓两次职位，手机上随时看排名、改状态**。

## 先确认服务器位置

- 服务器需要在**中国大陆以外**（美国最好）：Anthropic API（定制简历）在大陆不可用，部分招聘网站在大陆访问也不稳定。
  如果你卖点 SaaS 的 VPS 在大陆（需要备案的那台），不要用它，另开一台海外的。
- 服务器上**不能**「打开申请页预填」（`--server` 模式会关掉这个按钮）；投递那一步在自己电脑上做。

## 步骤

```bash
# 1. 代码和依赖
sudo mkdir -p /opt/find_a_job && sudo chown deploy:deploy /opt/find_a_job
git clone https://github.com/wuhuCYC/find_a_job /opt/find_a_job && cd /opt/find_a_job
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 2. 私人信息从自己电脑拷过去（不进 git）
scp -r private/ deploy@你的服务器:/opt/find_a_job/private/
echo "ANTHROPIC_API_KEY=..." > /opt/find_a_job/.env && chmod 600 /opt/find_a_job/.env

# 3. 服务：改 jobhunt-web.service 里的域名
sudo cp deploy/jobhunt-web.service deploy/jobhunt-fetch.service deploy/jobhunt-fetch.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jobhunt-web jobhunt-fetch.timer

# 4. nginx + 密码 + HTTPS：改 nginx.conf 里的域名
sudo htpasswd -c /etc/nginx/.jobhunt_htpasswd yourname
sudo cp deploy/nginx.conf /etc/nginx/sites-available/jobhunt
sudo ln -s /etc/nginx/sites-available/jobhunt /etc/nginx/sites-enabled/
sudo certbot --nginx -d jobs.example.com
sudo nginx -t && sudo systemctl reload nginx
```

## 安全要点

- **一定要加 nginx 密码**：页面里有你的简历素材、投递记录和签证时间线。
- 网站只监听 `127.0.0.1`，对外只能经过 nginx；`--allow-host` 只放行你的域名。
- 写操作要求 `X-Jobhunt` 请求头 + JSON，别的网站没法借你的登录状态替你操作。
- `.env`（API key）和 `private/` 权限设成只有 deploy 用户可读。
