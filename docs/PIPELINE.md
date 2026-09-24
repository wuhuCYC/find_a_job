# 系统设计：从「找岗位」到「点提交」

## 总流程

```
config/companies.yaml ──► fetch ──► data/jobs.db ──► score ──► list / jobs.md
   (51 家公司,                (SQLite:           (过滤+打分,      (排名 + 理由)
    7 种招聘系统)              职位/分数/状态)     可解释)              │
                                                                     ▼ 你挑选
profile/experience_bank.yaml ─────────────────────────────────► tailor（Claude）
   (所有简历内容的唯一事实来源)                                       │
                                                                     ▼
                                                              guard（防编造）
                                                                     │
                                                                     ▼
                                                       RenderCV → 一页 PDF + 差距报告
                                                                     │
                                                                     ▼
                                                    apply（浏览器预填，你亲手点提交）
                                                                     │
                                                                     ▼
                                                           status（投递追踪）
```

## 模块

| 模块 | 作用 |
|---|---|
| `jobhunt/fetchers/` | Greenhouse / Lever / Ashby / Workday / SmartRecruiters 用公开 JSON 接口；iCIMS / Jobvite 解析 HTML（实验性）。列表页先粗筛，不相关的不请求详情页 |
| `jobhunt/location.py` | 把各种地点写法归到 OC / LA / SD / BAY / REMOTE_US；排除 Glendale, AZ 这类同名城市 |
| `jobhunt/seniority.py` | 从职位名判断 entry / mid / senior / intern；从 JD 抽「N+ years」 |
| `jobhunt/scoring.py` | 总分 100 = 方向 40 + 技能 25 + 地区 15 + 职级 10 + 公司 10，减去经验年限和签证惩罚。每个分数都附中文理由 |
| `jobhunt/store.py` | SQLite：职位（自动标记下架）、打分、投递状态、抓取日志 |
| `jobhunt/bank.py` | 素材库加载 + 校验 |
| `jobhunt/guard.py` | **防编造守卫**：改写后的内容里，数字、「N years / N% / Nx」这类说法、技术名词，都必须能在原始事实里找到 |
| `jobhunt/resume.py` | 按方向挑 bullet（不用 LLM）→ RenderCV YAML → PDF；超过一页自动删最弱的 bullet |
| `jobhunt/tailor.py` | 调用 Claude（默认 `claude-opus-5`）按 JD 挑选 + 改写 + 找差距；结构化输出；素材库做 prompt 缓存 |
| `jobhunt/apply.py` | Playwright 打开申请页，按标签识别姓名/邮箱/电话/LinkedIn/GitHub 等并填写、上传简历；**不点提交** |

## 防编造是怎么做的

1. 素材库里每条 bullet 都引用了具体的 facts（带出处）。`python -m jobhunt validate` 会检查每条 bullet 的数字、数量说法和技术栈是否都有事实支撑 —— 我写素材库时它就拦下过一条（「~10K-line JS」在事实里没写）。
2. Claude 改写时必须引用原 bullet 的 id；改写结果再过一遍同样的检查，不合格的**退回原文**并写进报告。
3. 技能栏只能从素材库 `skills` 里选、且等级 ≥ working（C++ 目前是 coursework，就不会出现在简历上）。
4. 签证、工作授权、EEO 这类问题**永远由你本人回答**。

## 为什么是半自动投递

- 签证 / 授权问题答错有法律后果；
- 很多 ATS 有 reCAPTCHA；LinkedIn 等平台用户协议禁止自动化，封号得不偿失；
- 金融公司看得到你的全部申请记录，海投减分。

所以流程是：程序把能自动的都做了（找、排、定制、预填、上传），最后一步由你确认。

## 在哪里运行

- **你的 Mac 上**（推荐）：网络不受限，所有招聘接口都能访问。
- **Claude Code 云端会话**：当前环境的网络策略**拦截了**招聘网站（`boards-api.greenhouse.io`、`api.lever.co`、`api.ashbyhq.com`、`*.myworkdayjobs.com` 等）。如果想在云端跑抓取，需要在环境设置里把这些域名加入允许列表（会话标题栏的环境菜单 → Edit → Network access）。

## 调参

- 地区偏好、职级规则、分数权重、签证措辞：`config/search.yaml`
- 岗位方向关键词：`config/archetypes.yaml`
- 方向偏好顺序、要不要实习：`private/profile.yaml` 的 `preferences`
- 公司优先级、招聘系统配置：`config/companies.yaml`

改完直接 `python -m jobhunt score` 重新打分，不需要重新抓取。
