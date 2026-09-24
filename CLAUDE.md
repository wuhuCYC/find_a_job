# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目简介

个人求职系统：在加州（优先 LA / Irvine）找「和钱打交道」的工作（量化开发、资管投资数据、金融科技、风控、交易市场）。
两部分：`docs/` 里的求职战略文档 + `jobhunt/` 抓取 → 打分 → 定制简历 → 半自动投递的工具。

### 关联文档（docs/ 目录）
- [STRATEGY.md](./docs/STRATEGY.md) — ★ 总战略（岗位匹配度、目标公司、时间线、待用户确认的信息）
- [TARGET_COMPANIES.md](./docs/TARGET_COMPANIES.md) — 公司地图（✅/❓ 验证状态）
- [SKILL_GAP_PLAN.md](./docs/SKILL_GAP_PLAN.md) — 技能差距与补强作品
- [PROJECT_PACKAGING.md](./docs/PROJECT_PACKAGING.md) — 项目讲法、不能上简历的说法、安全清单
- [VISA_NOTES.md](./docs/VISA_NOTES.md) — 签证现状（有时效，改动前先核实）
- [PIPELINE.md](./docs/PIPELINE.md) — 工具架构
- [PROJECT_STATUS.md](./docs/PROJECT_STATUS.md) — 里程碑与下一步

## 常用命令

```bash
pip install -r requirements.txt
python -m pytest                     # 全部测试
python -m jobhunt validate           # 校验经历素材库（改 experience_bank.yaml 后必跑）
python -m jobhunt base               # 生成各方向基础简历 → output/base/
python -m jobhunt run                # fetch + score + 导出 output/jobs.md
python -m jobhunt tailor <uid>       # 调用 Claude 定制简历（需 ANTHROPIC_API_KEY）
python -m jobhunt web                # 本地可视化网站；--export site.html 导出单文件快照；--server 服务器模式
```

## 铁律

1. **绝不编造经历。** `profile/experience_bank.yaml` 是简历内容的唯一事实来源。新增 bullet 必须引用 facts，
   facts 必须写出处；`validate` 和 `tests/test_bank_guard.py` 必须通过。数字、「N years / N% / Nx」、技术名词都受 guard 约束。
2. **LLM 只能挑选 / 重排 / 改写措辞。** `tailor.py` 的输出一律经过 `guard.py`，不合格的退回原文，不要绕过。
3. **不自动点提交。** `apply.py` 只预填和上传，签证/授权/EEO 问题由用户本人回答。
4. **隐私。** 真实联系方式、签证身份、原始简历只放 `private/`（gitignored）。仓库是 public 的。
   不要把私有仓库里的 token、策略阈值、私有参数写进本仓库。
5. **研究类结论要带出处和日期**（招聘信息、签证政策变化很快），未验证的标 ❓ / UNVERIFIED。
6. **不报时间预估，质量优先**（用户的工作风格：做精，不求快）。
7. 文档用中文，简历内容用英文；代码注释中文、简洁。

## 架构速览

- `config/companies.yaml` — 51 家公司，`ats.type` 决定抓取器（greenhouse / lever / ashby / workday / smartrecruiters / icims / jobvite / manual）
- `config/search.yaml` — 地区偏好、职级规则、分数权重、签证措辞、技能词表（canonical 名要和素材库 skills.name 一致）
- `config/archetypes.yaml` — 7 个岗位方向的关键词
- `jobhunt/scoring.py` — 总分 100 = 方向 40 + 技能 25 + 地区 15 + 职级 10 + 公司 10 − 经验年限惩罚 − 签证惩罚
- `jobhunt/resume.py` — RenderCV 2.3（engineeringresumes 主题）。**四边页边距必须相同**，否则 Typst 报
  "cannot multiply dictionary with integer"
- 渲染需要联网下载 Typst 的 fontawesome 包；离线环境会失败
- `jobhunt/web/` — 网站。数据来自 `docs/strategy.yaml`（STRATEGY.md 等文档的结构化版本，改一边要同步另一边）。
  strategy.yaml 的流式映射里：含英文逗号的值（如 `$103,265`）和 `yes` / `no` 必须加引号，`tests/test_web.py` 会检查
- 前端是原生 JS，所有外部文本用 textContent 写入；改完跑 `tests/test_web.py`（含 Playwright 冒烟测试）

## 环境注意

- 云端会话的网络策略会拦截招聘网站（greenhouse / lever / ashby / myworkdayjobs 等），抓取要在用户 Mac 上跑，
  或让用户在环境设置里放行这些域名。
- 用户的其他项目（私有）：`wuhuCYC/a-stock-signal-v2`、`csgo-agent`（活跃分支 `v6-phase2-3-stats-buypoints`）、
  `sell_csgo_monitor`、`csgo-monitor`；公开：`cs-monitor`、课程项目 `LilyLiu945/MR-Collaboration-Intervention`。
  素材库里的事实都来自这些仓库的文档，出处写在 facts.source。
