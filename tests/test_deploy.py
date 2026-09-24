"""部署文件：nginx include 助手 + 各配置之间的一致性。"""
import importlib.util
import re
import shutil
import subprocess

import pytest

from jobhunt import config

DEPLOY = config.ROOT / "deploy"
spec = importlib.util.spec_from_file_location("nginx_include", DEPLOY / "nginx_include.py")
ni = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ni)

SNIPPET = "/etc/nginx/snippets/jobhunt.conf"

# certbot 改写过的典型站点配置（和 sell_csgo_monitor 的部署方式一致）
SAAS = """\
server {
    server_name 203.0.113.10 example.com www.example.com;

    location /api/ {
        proxy_pass http://127.0.0.1:5050/;
        proxy_set_header Host $host;
    }

    location ~* \\.(js|css|png)$ {   # 静态文件缓存 { 注释里的括号不算 }
        expires 7d;
    }

    location / {
        root /opt/app/frontend/dist;
        try_files $uri $uri/ /index.html;
        add_header X-Note "a { b } ; c";
        set $x "${host}-1";
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem; # managed by Certbot
}
server {
    if ($host = example.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
    listen 80;
    server_name 203.0.113.10 example.com www.example.com;
    return 404; # managed by Certbot
}
"""


def _site(tmp_path, text=SAAS, name="sell_monitor"):
    d = tmp_path / "sites-enabled"
    d.mkdir(exist_ok=True)
    (d / name).write_text(text)
    return d


def test_tokenizer_ignores_braces_in_comments_quotes_and_vars():
    nodes = ni.parse(SAAS)
    servers = list(ni.server_blocks(nodes))
    assert len(servers) == 2
    assert ni.is_https(servers[0]) and not ni.is_https(servers[1])
    assert "203.0.113.10" in ni.server_names(servers[0])


def test_add_then_remove_roundtrip(tmp_path):
    d = _site(tmp_path)
    backups = tmp_path / "bak"
    out = ni.cmd_add("203.0.113.10", SNIPPET, [str(d)], str(backups))
    assert out.startswith("ADDED ")
    text = (d / "sell_monitor").read_text()
    https_block = text[: text.index("server {", 10)]
    assert f"    include {SNIPPET};" in https_block             # 加在 443 块里
    assert text.count(f"include {SNIPPET};") == 1
    assert list(backups.iterdir()) and not list(d.glob("*.bak"))   # 备份不放在 sites-enabled
    assert ni.cmd_add("203.0.113.10", SNIPPET, [str(d)], str(backups)).startswith("ALREADY")

    assert ni.cmd_remove(SNIPPET, [str(d)], str(backups)).startswith("REMOVED")
    assert (d / "sell_monitor").read_text() == SAAS                 # 原样恢复
    assert ni.cmd_remove(SNIPPET, [str(d)], str(backups)) == "NOTHING"


def test_add_picks_default_server_when_no_name_matches(tmp_path):
    conf = "server {\n    listen 443 ssl default_server;\n    server_name _;\n}\n"
    d = _site(tmp_path, conf)
    assert ni.cmd_add("198.51.100.7", SNIPPET, [str(d)], str(tmp_path / "bak")).startswith("ADDED")


@pytest.mark.parametrize("conf", [
    "server {\n    listen 80;\n    server_name 203.0.113.10;\n}\n",                       # 没有 HTTPS
    SAAS + SAAS.split("server {\n    if")[0],                                             # 两个同名 HTTPS 块
])
def test_add_refuses_when_target_is_ambiguous(tmp_path, conf):
    d = _site(tmp_path, conf)
    with pytest.raises(ni.ConfError):
        ni.cmd_add("203.0.113.10", SNIPPET, [str(d)], str(tmp_path / "bak"))
    assert (d / "sell_monitor").read_text() == conf                  # 没改任何东西


def test_broken_config_is_reported_not_modified(tmp_path):
    conf = "server {\n    listen 443 ssl;\n    server_name 203.0.113.10;\n"
    d = _site(tmp_path, conf)
    assert ni.main(["add", "--host", "203.0.113.10", "--snippet", SNIPPET, "--dir", str(d),
                    "--backup-dir", str(tmp_path / "bak")]) == 2
    assert (d / "sell_monitor").read_text() == conf


def test_conf_d_only_loads_dot_conf(tmp_path):
    d = tmp_path / "conf.d"
    d.mkdir()
    (d / "site.conf.disabled").write_text(SAAS)
    with pytest.raises(ni.ConfError):
        ni.cmd_add("203.0.113.10", SNIPPET, [str(d)], str(tmp_path / "bak"))


# ---------------------------------------------------------------- 配置一致性
def _lines(path):
    return {ln.strip() for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith("#")}


def test_server_requirements_subset_of_main():
    server = _lines(DEPLOY / "requirements-server.txt")
    main = _lines(config.ROOT / "requirements.txt")
    assert server <= main
    assert not any(r.startswith(("playwright", "pytest")) for r in server)


def test_ports_paths_and_users_agree():
    web = (DEPLOY / "jobhunt-web.service").read_text()
    fetch = (DEPLOY / "jobhunt-fetch.service").read_text()
    snippet = (DEPLOY / "nginx-jobs.conf").read_text()
    setup = (DEPLOY / "remote_setup.sh").read_text()
    port = re.search(r"--port (\d+)", web).group(1)
    assert f"proxy_pass http://127.0.0.1:{port}/;" in snippet
    assert f"PORT={port}" in setup
    htpasswd = re.search(r"auth_basic_user_file (\S+);", snippet).group(1)
    assert f"HTPASSWD={htpasswd}" in setup
    assert "location ^~ /jobs/" in snippet and "proxy_set_header Host 127.0.0.1;" in snippet
    for unit in (web, fetch):
        assert "User=jobhunt" in unit and "/opt/find_a_job/venv/bin/python" in unit
        assert "ReadWritePaths=/opt/find_a_job/data /opt/find_a_job/output" in unit
    assert "APP_USER=${APP_USER:-jobhunt}" in setup and "python3 -m venv venv" in setup


def test_env_file_has_no_inline_comments():
    """systemd 的 EnvironmentFile 不支持行尾注释：JOBHUNT_TAILOR=0 后面不能跟 # 说明。"""
    setup = (DEPLOY / "remote_setup.sh").read_text()
    assert "'JOBHUNT_TAILOR=0'" in setup
    assert not re.search(r"JOBHUNT_TAILOR=0\s+#", setup)


@pytest.mark.skipif(not shutil.which("bash"), reason="没有 bash")
@pytest.mark.parametrize("script", ["deploy_vps.sh", "remote_setup.sh"])
def test_shell_scripts_parse(script):
    assert subprocess.run(["bash", "-n", str(DEPLOY / script)]).returncode == 0
    if shutil.which("shellcheck"):
        assert subprocess.run(["shellcheck", "-s", "bash", str(DEPLOY / script)]).returncode == 0


@pytest.mark.skipif(not shutil.which("nginx"), reason="没有 nginx")
def test_snippet_passes_nginx_t(tmp_path):
    d = _site(tmp_path, SAAS.replace("ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem; # managed by Certbot", ""))
    snippet = tmp_path / "jobhunt.conf"
    snippet.write_text((DEPLOY / "nginx-jobs.conf").read_text().replace("/etc/nginx/.jobhunt_htpasswd", str(tmp_path / "pw")))
    ni.cmd_add("203.0.113.10", str(snippet), [str(d)], str(tmp_path / "bak"))
    site = (d / "sell_monitor").read_text().replace("listen 443 ssl;", "listen 127.0.0.1:18443;")
    (d / "sell_monitor").write_text(site.replace("listen 80;", "listen 127.0.0.1:18080;"))
    main = tmp_path / "nginx.conf"
    main.write_text(f"pid {tmp_path}/nginx.pid;\nerror_log {tmp_path}/error.log;\nevents {{}}\n"
                    f"http {{\n access_log off;\n include {d}/*;\n}}\n")
    r = subprocess.run(["nginx", "-t", "-c", str(main), "-p", str(tmp_path)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
