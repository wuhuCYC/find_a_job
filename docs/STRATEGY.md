# 求职战略：LA / Irvine，和钱打交道的工作

> 调研日期：2026-09-24。公司、薪资、签证信息都有时效性，原始出处见 [research/](./research/)。
> 标 ⚠️ 的是还需要你确认的前提。可视化版本：`python -m jobhunt web`（结构化数据在 [strategy.yaml](./strategy.yaml)，两边同步改）。

---

## 一句话结论

你最值钱的不是「会写 Python」，而是**把交易研究工程化**：数据管道 → 信号 → 带成本的回测 → 参数搜索 → 实时监控 → 上线给用户用。
在 LA / Irvine，这个能力最对口的是：

1. **金融科技后端（主线）**：Acorns、Experian、Zest AI、Tala、PennyMac（Irvine / Costa Mesa / Burbank / Santa Monica / Westlake Village），加上远程岗
2. **资管公司的技术岗 / 投资数据工程**：PIMCO、Capital Group、Pacific Life、Research Affiliates（Newport Beach / Irvine / LA）—— 做工程，但离市场和量化最近
3. **量化开发（副线，精投）**：同一批资管公司的量化开发岗；**冲刺**：Crabel（LA 唯一的系统化交易公司）、湾区的 Voleon / Headlands。纯量化研究和高频交易系统目前差在**统计严谨性的呈现**和 **C++**

> **你的选择（2026-09-24）**：主线金融科技，副线量化开发。理由：岗位多、远程多、签证担保更常见，SaaS 的 100+ 付费用户是现在最硬的证据；
> 量化兴趣不放弃，用研究作品持续积累（见 1.6 节）。

---

## 1. 你的底牌（5 个仓库 + 你的简历）

**工作 / 研究经历**（来自你 2024-12 版简历，已进素材库；带数字和不确定说法的等你确认，见 `private/cv_review.md`）：

| 经历 | 证明了什么 | 哪类岗位最在乎 |
|---|---|---|
| **知合科技 ERP 开发工程师**（2023-10 起） | 航空结算（billing）ERP 系统、Elasticsearch 查询、系统测试与性能优化 | **金融科技后端**（结算、交易类系统正对口）、资管数据 |
| **广州数字安盟 软件开发工程师**（2023-06 – 2023-10） | 公司网站前端组件 + 和后端的 API 对接 | 金融科技全栈 |
| **Smart Medicine Laboratory 数据分析 / 研究助理**（2023-10 – 2024-09） | 可穿戴心率数据分睡眠阶段的机器学习、数据预处理与融合 | 风控 / 数据科学 |
| **AI 金融科技评估系统（队长）** | 保险资格评估；从金融报告和法律文书里抽取信息的 NLP；系里比赛前 5 | 金融科技、风控（核保）、资管数据 |
| **道路病害检测（暑期研究实习）** | 数据增强把平均 F1 从 55.14% 提到 56.98%；骨干网络 / 注意力模块对比 | 数据科学（加分项） |
| 学历 | 诺丁汉大学宁波校区计算机本科（GPA 3.7/4.0）；UCI EECS 硕士（简历写作 MEng） | —— |

**自己的项目**：

| 项目 | 证明了什么 | 哪类岗位最在乎 |
|---|---|---|
| **CS2 饰品市场研究平台**（csgo-agent，约 48K 行 Python） | 3 年日线 + 在售/求购深度数据；**实时化（无前视）的事件信号 + 安慰剂对照 + 全天基线**（13,671 个事件：46.0% vs 33.3% vs 29.0%）；**带随机对照组的纸面交易**，并且在随机组跑赢全部 11 个信号源时，承认失败、转去做 regime 闸 | 量化研究、量化开发、预测市场、交易市场定价 |
| **A 股波段信号系统**（a-stock-signal-v2，约 16K 行，89 个测试） | 事件驱动回测（次日开盘成交、涨跌停、仓位上限、买卖分离费率、滑点）；Optuna + 滚动 walk-forward；每 6 秒的持仓风控监控 | 量化开发、资管投资数据、交易系统 |
| **卖点预警 SaaS**（sell_csgo_monitor，已上线） | **100+ 付费用户（每月 ¥100）**；Flask + React + JWT、付费分级、独立调度进程、多通道推送容灾、375 个测试、VPS 部署 | 金融科技后端、全栈、交易市场 |
| **UCI EECS 215 课程项目** | HMM / LSTM / GRU / Transformer、按组切分防泄漏 | 风控数据科学（加分项） |

**真正稀缺的三点**（面试时要主动讲）：

1. **一个人从 0 做完整产品并有 100+ 付费用户** —— 大部分应届生只有课程项目，这是你最硬的一条。
   再加上**航空结算 ERP 的工作经历**，金融科技面试里「做过和钱有关的生产系统」这一点两边都能讲。
2. **会自己证伪** —— 安慰剂对照、随机对照组、承认信号失效。这在量化面试里比任何「胜率」都值钱。
3. **对市场有真实热情和实盘经验** —— 金融公司很看重「你为什么想做这行」，你有具体的故事。

**短板**（下文逐条给补法）：

- 简历里有几处要先核实再用：分布式数据库（「TiDB 或 CockroachDB」）、前端框架（「React 或 Vue」）、各项百分比和日交易量、
  CRDDC2022 排名的说法 —— 美国公司会做背景调查，面试也会追问怎么测的（清单在 `private/cv_review.md`）
- **手写代码的手感退化了**（你自己的判断：能看懂代码，但主要靠 AI 写）。面试大多要现场手写，这是现在最该补的一项
- 没有 C++；作品里全是 Python —— 需要一个 Java 作品
- 用过 Docker，没用过 AWS
- 研究叙事偏「庄家 / 技术分析」，需要翻译成美国量化的语言（见 [PROJECT_PACKAGING.md](./PROJECT_PACKAGING.md)）
- 技术栈是 SQLite / 单机 VPS，美国公司更常见 Postgres / AWS / Docker
- 项目全是私有仓库，招聘方看不到

---

## 1.5 量化 vs 金融科技：区别是什么

两者都和钱打交道：**量化是拿钱去市场里博弈赚钱，金融科技是做让别人用钱的产品。**

| | 量化（Quant） | 金融科技（Fintech） |
|---|---|---|
| 做什么 | 用数据、统计和代码直接在市场里赚钱：找信号、做策略、搭研究和交易系统 | 用软件做金融产品：投资 App、支付、借贷、征信、银行系统 |
| 典型雇主 | 对冲基金、做市商、资管的量化团队（PIMCO、Capital Group 量化岗、Crabel） | Acorns、Experian、Zest AI、Tala、PennyMac、Robinhood、Coinbase |
| 怎么衡量你 | 研究和策略能不能赚钱（P&L） | 产品和系统做得好不好 |
| 面试 | 概率统计、脑筋急转弯、手写 Python / C++ | LeetCode、系统设计、行为面 |
| 薪资 | 上限最高；资管量化开发约 $120–195K，顶级基金 $200–300K | 南加州应届约 $90–160K |
| 机会 | 名额少、门槛高、远程少 | 岗位多、远程多、担保更常见 |
| 对你 | 最贴近你的兴趣（投机、博弈） | 你已经有 100+ 付费用户的产品 |

**中间地带**：资管公司的技术岗（PIMCO / Capital Group 的 SDE、投资数据工程）、交易平台、信贷风控建模 —— 做工程，但天天和市场、交易打交道。

**建议**：OPT 的失业计时从 EAD 开始日算起，所以两条线并行 —— 金融科技和资管技术岗先拿到工作、赶上下一次 H-1B 抽签；量化方向靠研究报告等作品持续积累。从资管技术岗内部转量化开发是很常见的路径。


---

## 1.6 量化团队是怎么「跑」的？你能不能做

一条完整的量化流水线（各家叫法不同，环节差不多）：

| 环节 | 做什么 | 主要谁做 | 你做过的对应部分 |
|---|---|---|---|
| 1. 数据 | 采集、清洗、对齐行情 / 基本面 / 另类数据；按「当时能看到什么」存（point-in-time），防前视 | 量化开发、数据工程 | CS2 三年价格和盘口数据；A 股增量 Parquet 缓存 |
| 2. 研究 | 提出假设 → 做成信号 → 统计检验（IC、t 值、分组收益） | 量化研究员 | 事件研究 + 安慰剂对照 |
| 3. 回测 | 带手续费、滑点、成交规则的历史模拟；样本外验证 | 研究员用，开发搭框架 | 事件驱动回测、walk-forward |
| 4. 组合与风控 | 把多个信号合成仓位；控制风险暴露、杠杆、换手 | 研究员、风控 | A 股回测里的仓位上限 |
| 5. 执行 | 下单算法，降低冲击成本 | 交易 / 执行团队 | —— |
| 6. 监控 | 实盘和回测对比、信号衰减、系统告警 | 开发 + 研究 | 实时监控、多渠道推送、信号收益回填 |

新人进去通常做什么：

- **量化开发**：维护数据管道和回测框架，把研究员的原型代码变成每天稳定运行的生产系统，写测试、查数据问题。工程为主，和金融科技后端的技能重叠最多。
- **量化研究**：在现成框架上负责一个小方向的信号研究，写研究报告，由资深研究员审。统计为主，顶级公司多招 PhD。

**你能做吗？** 量化开发能做：上面第 1、3、6 步你已经完整做过一遍，这正是量化开发的日常。
差距是部分岗位要的 C++、PIMCO 要的固收知识，以及面试里的概率统计题。量化研究现在比较难：要拿出看得见的统计严谨性（一份研究报告），还要和 PhD 竞争。

**副线怎么走**：

1. 每周固定一段业余时间做研究报告（[SKILL_GAP_PLAN.md](./SKILL_GAP_PLAN.md) 项目 3），用美股或加密的公开数据
2. 刷概率题（绿皮书）—— 量化面试的第一关
3. 只精投资管公司的量化开发 / 量化工程岗，不海投
4. 先进金融科技或资管技术岗，再内部转量化开发，是很常见的路径
5. 进了金融公司通常有个人交易规定（预先审批、最短持有期），研究可以继续做，实盘要按公司规定来

---

## 2. 岗位方向匹配度（从高到低）

| 方向 | 匹配度 | 典型职位名 | LA/OC 代表雇主 | 加州新人 base（调研值） | 最大差距 |
|---|---|---|---|---|---|
| 金融科技后端 | ★★★★ | Software Engineer I, Backend Engineer, SDE | Acorns, Experian, PennyMac, Zest AI, Tala, Dave | 约 $90–160K | Java/Postgres、支付/账本正确性、系统设计面试 |
| 量化开发 / 研究工程师 | ★★★★ | Quantitative Developer, Quant Engineer, Research Engineer | PIMCO, Capital Group, Research Affiliates, Crabel | 资管约 $120–195K；湾区基金 $160–190K | C++、固收知识、很多岗要 3 年经验 |
| 资管投资数据 / 组合分析工程 | ★★★★ | Investment Data Engineer, Portfolio Analytics, Technology Analyst | Capital Group, PIMCO, Pacific Life, TCW | 约 $110–150K | 业绩归因、风险模型、固收术语；云数据栈 |
| 信贷风控 / 数据科学 | ★★★ | Credit Risk Analyst, Data Scientist, ML Engineer | Experian, Zest AI, Hyundai Capital, Tala, PennyMac | 约 $100–150K | 信贷领域知识（评分卡、WoE/IV、PSI）、SQL 作品 |
| 预测市场 / 加密 / 定价 | ★★★（故事最契合） | Quant Analyst (Prediction Markets), Trading Engineer | 基本不在 LA（NYC / 远程） | AQR 预测市场分析师 $200–230K（在 CT） | 概率校准、做市理论；地点不匹配 |
| 量化研究 | ★★～★★★ | Quantitative Researcher / Analyst | PIMCO QRA, Research Affiliates, Pacific Life | $95–215K（顶级基金 $225–300K 但不在加州） | 看得见的统计严谨性、研究报告、和 PhD 竞争 |
| 交易系统 / 低延迟 | ★～★★（C++ 岗）/ ★★★（Java 岗） | Trading Systems Engineer, Low-latency Developer | 南加州很少；Java 路线：PIMCO 交易技术 | 芝加哥/纽约 $200–300K | C++、网络/并发、FIX / 行情接入 |

> 按你的选择（2026-09-24）：**主线是金融科技后端 + 资管数据 / 技术岗**（都在 Irvine / Newport Beach / LA，也有很多远程），**量化开发作为副线精投**，用同一套素材换讲法；**量化研究和预测市场作为冲刺**；交易系统等补了 Java/C++ 作品再考虑。

---

## 3. LA / Irvine 目标公司（完整版见 [TARGET_COMPANIES.md](./TARGET_COMPANIES.md)）

**第一梯队**（地点对 + 和钱直接相关 + 有新人入口或担保记录）：

| 公司 | 地点 | 为什么是你 |
|---|---|---|
| **PIMCO** | Newport Beach | Quantitative Developer 的职责原文就是「research infrastructure (market data, backtest, compute)」—— 和你的回测系统一一对应。H-1B 记录强 |
| **Capital Group** | Irvine 技术园区 / LA | OC 新人技术岗最多（CAMPUS 轮岗、New Grad SDE I）+ Quant Engineer |
| **Pacific Life** | Newport Beach | Quantitative Analyst（组合优化/监控）是可达的入口；担保记录稳定 |
| **Research Affiliates** | Newport Beach | 因子/信号研究，内容上最对口（注意 2026 年指数业务被 TMX 收购） |
| **Crabel** | LA | 系统化期货/外汇交易，方向最贴；门槛高、名额少 —— 冲刺 |
| **Acorns** | Irvine | 投资 App，出过 "Software Engineer I, Recent Graduate"；担保记录强 |
| **Experian** | Costa Mesa | Xcelerator 12 个月轮岗（SWE / 数据分析） |
| **Zest AI** | Burbank | 机器学习信贷审批 —— 你的建模 + 工程能力都用得上 |
| **Tala** | Santa Monica | 小额信贷，见过 Engineer I 岗 |
| **PennyMac** | Westlake Village | 技术轮岗项目（2027 年 1 月 / 6 月批次） |
| **TCW** | LA 市中心 | 资管工程团队 + 实习转全职 analyst |

**和你 CS2 经验最对口的非传统金融**：Riot Games（LA）、Blizzard（Irvine）的经济系统/商业化岗；Whatnot（LA，收藏品拍卖市场）。这些是「交易市场定价」方向，可以拿 CS2 项目直接讲。

**已确认在 LA/OC 没有办公室**：HRT、Jane Street、Citadel、Two Sigma、Jump、Optiver、IMC、DRW、Akuna、Tower 等高频/做市公司。最近的在旧金山。

---

## 4. 时间线：现在（2026 年 9 月底）意味着什么

| 雇主类型 | 2027 年入职的招聘窗口 | 现在的状态 |
|---|---|---|
| 量化基金 / 做市（Citadel、IMC、HRT、Voleon…） | 6–8 月开放，滚动审，9–12 月发 offer | **还没关，但已过第一波 —— 要立刻投** |
| 资管（PIMCO、Capital Group、Pacific Life、TCW） | 新人主要靠提前一年的实习转正；具体职位全年开放 | 具体 requisition 不算晚；2027 暑期实习 9–10 月陆续开 |
| 金融科技 / 科技公司 | 滚动；8–11 月、1–3 月两波 | 正常 |
| 银行科技 analyst 项目 | 多数名额由暑期实习转正 | 偏晚，但仍有 |

**取决于你的毕业时间** ⚠️：

你 2026 年夏天毕业，属于「已毕业」的情况：

- 部分「2027 届」岗位只收还没毕业的人，投之前看清要求；
- 重点投：常年开放的 University Graduate 岗（如 Citadel）、写「0–2 年经验」的初级岗、资管的具体职位、远程的金融科技岗；
- 滚动入职的轮岗项目（Experian 4 / 6 月、PennyMac 1 / 6 月、Capital Group CAMPUS）也可以投，但入职时间要和 OPT 失业计时对得上；
- **OPT 的失业天数从 EAD 开始日起累计**，投递节奏要比在读学生更紧（个人时间线在网站「签证」页）。

---

## 5. 投递策略：质量 > 数量

**为什么不海投**：

- 金融公司 HR 系统能看到你投了多少岗、每份简历写了什么；同一家投十几个岗反而减分。
- 量化 / 资管的筛选看的是「这个人为什么适合这个岗」，通用简历基本过不了。
- 本仓库的定位是：**自动找、自动排序、自动定制，人工把关后提交**。

**每周节奏**（建议）：

1. `python -m jobhunt run` —— 抓取 + 打分 + 导出 `output/jobs.md`
2. 从排名里挑出真正想投的，`status UID shortlisted`
3. 对每个 shortlisted：`tailor UID` 生成定制简历 + 差距报告 → 自己读一遍、改到满意
4. `apply UID` 打开申请页预填 → 自己检查、回答签证等问题 → 自己点提交
5. 同时找内推（见下）
6. 有回音就 `status UID oa / interview / offer / rejected`，记下面经

**内推是最高杠杆**：

- UCI 在 Irvine 本地，PIMCO、Capital Group、Experian、Pacific Life 都有大量 UCI 校友。LinkedIn 搜「公司名 + UC Irvine」，发简短、具体的消息（提你做的回测系统，问一个具体问题），而不是直接要内推。
- UCI 的 Career Center / Handshake / 招聘会：资管和保险公司会来 Irvine 招人。
- 中文是真优势的地方：East West Bank、Cathay Bank（华人背景银行），以及跨境业务团队。

---

## 6. 签证对策略的影响（摘要；详见 [VISA_NOTES.md](./VISA_NOTES.md)）

> 按 F-1 → OPT → STEM OPT → H-1B 的路径规划。你自己的日期只写在 `private/profile.yaml`。

- **OPT / STEM OPT 目前照常**（STEM OPT 要求雇主加入 E-Verify）。有一个 OPT 收费的提案刚过白宫审查、还没公布金额。
- **H-1B 抽签已改为按工资级别加权**：给的工资越高，中签概率越高。→ **量化、资管这类高薪岗位在抽签上天然占优**，这对你的方向是利好。
- **最大的不确定性**：2026-08-25 提出的「每个 cap H-1B 申请加收 $103,265」的规则（尚未生效），如果落地，小公司会更不愿意担保新人。→ 优先投**有持续担保记录的大公司**（PIMCO、Capital Group、Pacific Life、Experian、Acorns 这类）。
- **兜底**：大学及附属非营利研究机构的 H-1B 不受名额限制（cap-exempt），包括 UC 系统的研究岗。
- 打分器会自动识别 JD 里「不担保」的措辞并降权（`list --hide-visa` 可以直接隐藏）。

---

## 7. 我还需要你告诉我的信息（按重要性）

已确认（2026-09-24）：可以接受远程；卖点 SaaS 有 100+ 付费用户（每月 ¥100）；用过 Docker、没用过 AWS；
方向选定为**主线金融科技、副线量化开发**；签证进展和日期记在本地 `private/profile.yaml`（不进 git）；
收到 2024-12 版简历，确定的内容已进素材库（学历、3 段工作经历、2 个项目）。

还需要：

1. 简历核实清单（`private/cv_review.md`）：分布式数据库和前端框架到底用的哪个、各项数字怎么测的、
   CRDDC 排名是比赛期间还是事后对照、知合科技和道路病害项目的结束月份、知合科技是全职还是兼职
2. 美国简历用的邮箱（学校邮箱毕业后可能停用）和美国手机号、LinkedIn
3. I-20 上 OPT 推荐写的**开始日期**；拿到 EAD 卡后告诉我卡上的开始日
4. EECS 215 项目里**你具体负责哪部分**：流水线是 数据准备 → HMM 隐状态 → 特征选择 → LSTM / GRU / Transformer 训练 → 评估报告 → 干预效果验证
5. 部署到服务器后 `bash deploy/deploy_vps.sh check` 的结果
6. 愿不愿意把部分项目**公开到 GitHub**（需要先清理 token，见 [PROJECT_PACKAGING.md](./PROJECT_PACKAGING.md) 最后一节）
