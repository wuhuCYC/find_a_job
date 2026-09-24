# find_a_job —— LA / Irvine 金融相关求职系统

目标：在加州（优先 LA / Irvine）找到**和钱打交道**的工作 —— 量化开发、资管投资数据、金融科技、风控、交易市场。

这个仓库有两部分：

1. **战略文档**：你能匹配哪些岗位、哪些公司、要补什么、项目怎么讲、签证怎么影响选择
2. **一套工具**：自动抓 51 家目标公司的职位 → 可解释打分 → 按 JD 定制一页简历（防编造）→ 浏览器预填申请表（你亲手提交）→ 追踪进度，全部可以在可视化网站里操作

## 可视化网站

```bash
python -m jobhunt web                        # 本地网站（自动打开浏览器）：职位排名、公司地图、简历版本、技能差距、签证时间线
python -m jobhunt web --export site.html     # 导出单文件快照（只读，可以直接发给别人 / 手机上看）
```

- 本地版可以直接在网页上改投递状态、定制简历、打开申请页预填、一键抓取最新职位。
- 部署到服务器（每天自动抓两次、手机随时看）：在 Mac 上运行 `bash deploy/deploy_vps.sh`，挂在 SaaS 那台 VPS 的 `/jobs/` 下，详见 [deploy/README.md](deploy/README.md)。

## 先读这些

| 文档 | 内容 |
|---|---|
| [docs/STRATEGY.md](docs/STRATEGY.md) | ★ 总战略：你的底牌、岗位匹配度排序、第一梯队公司、时间线、投递节奏、需要你补充的信息 |
| [docs/TARGET_COMPANIES.md](docs/TARGET_COMPANIES.md) | LA / OC / 加州公司地图（岗位、新人入口、H-1B 记录、验证状态） |
| [docs/SKILL_GAP_PLAN.md](docs/SKILL_GAP_PLAN.md) | 按岗位要求倒推：要掌握什么、5 个补强作品、书单 |
| [docs/PROJECT_PACKAGING.md](docs/PROJECT_PACKAGING.md) | 同一个项目给不同岗位怎么讲；哪些说法不能上简历；面试追问；公开作品集前的安全清单 |
| [docs/VISA_NOTES.md](docs/VISA_NOTES.md) | 2026 年 OPT / STEM OPT / H-1B 现状和对求职的影响 |
| [docs/PIPELINE.md](docs/PIPELINE.md) | 工具的设计：抓取、打分、防编造、半自动投递 |
| [docs/research/](docs/research/) | 调研原文（英文，带出处链接） |

## 快速开始（在你的 Mac 上）

```bash
git clone https://github.com/wuhuCYC/find_a_job && cd find_a_job
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium            # 半自动投递用；或 export JOBHUNT_BROWSER_CHANNEL=chrome 用本机 Chrome

# 1. 个人信息（private/ 不会进 git）
mkdir -p private && cp profile/profile.example.yaml private/profile.yaml
#    编辑 private/profile.yaml：联系方式、签证、毕业时间、方向偏好
#    编辑 profile/experience_bank.yaml：补全 TODO（教育、技能等级、实习经历）
python -m jobhunt validate             # 校验素材库：每个数字/技术都要有事实支撑

# 2. 各方向的基础简历（不调用 LLM）
python -m jobhunt base                 # → output/base/resume_<方向>.pdf

# 3. 找岗位
python -m jobhunt check                # 检查公司招聘接口配置（❓未验证的会在这里暴露）
python -m jobhunt run                  # 抓取 + 打分 + 导出 output/jobs.md
python -m jobhunt list --region OC,LA --hide-visa
python -m jobhunt show <uid>           # 看打分理由

# 4. 定制简历（需要 ANTHROPIC_API_KEY）
python -m jobhunt tailor <uid>         # → output/tailored/.../resume.pdf + report.md（关键词覆盖、差距、why us）
python -m jobhunt tailor --jd-file jd.txt --company "PIMCO" --title "Quantitative Developer"   # 手动粘贴的 JD

# 5. 投递与追踪
python -m jobhunt apply <uid>          # 打开申请页、预填、上传简历 —— 你检查后自己点 Submit
python -m jobhunt status <uid> interview --note "一面：回测系统深挖"
```

## 测试

```bash
python -m pytest        # 127 个测试：解析、地点、职级、打分、防编造守卫、简历渲染、浏览器预填、网站、部署脚本
```

## 隐私

- 真实联系方式、签证身份、原始简历只放 `private/`（已在 `.gitignore`）。
- ⚠️ 这个仓库目前是 **public**，建议改成 private（GitHub → Settings → Change visibility）。
