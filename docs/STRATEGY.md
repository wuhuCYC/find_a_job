# 求职战略：LA / Irvine，和钱打交道的工作

> 调研日期：2026-09-24。公司、薪资、签证信息都有时效性，原始出处见 [research/](./research/)。
> 标 ⚠️ 的是还需要你确认的前提。

---

## 一句话结论

你最值钱的不是「会写 Python」，而是**把交易研究工程化**：数据管道 → 信号 → 带成本的回测 → 参数搜索 → 实时监控 → 上线给用户用。
在 LA / Irvine，这个能力最对口的是：

1. **资管公司的量化开发 / 投资数据工程**：PIMCO、Capital Group、Pacific Life、Research Affiliates（都在 Newport Beach / Irvine / LA）
2. **金融科技后端**：Acorns、Experian、Zest AI、Tala、PennyMac（Irvine / Costa Mesa / Burbank / Santa Monica / Westlake Village）
3. **冲刺目标**：Crabel（LA 唯一的系统化交易公司）、湾区的 Voleon / Headlands。纯量化研究和高频交易系统目前差在**统计严谨性的呈现**和 **C++**

---

## 1. 你的底牌（我从你的 5 个仓库里看到的）

| 项目 | 证明了什么 | 哪类岗位最在乎 |
|---|---|---|
| **CS2 饰品市场研究平台**（csgo-agent，约 48K 行 Python） | 3 年日线 + 在售/求购深度数据；**实时化（无前视）的事件信号 + 安慰剂对照 + 全天基线**（13,671 个事件：46.0% vs 33.3% vs 29.0%）；**带随机对照组的纸面交易**，并且在随机组跑赢全部 11 个信号源时，承认失败、转去做 regime 闸 | 量化研究、量化开发、预测市场、交易市场定价 |
| **A 股波段信号系统**（a-stock-signal-v2，约 16K 行，89 个测试） | 事件驱动回测（次日开盘成交、涨跌停、仓位上限、买卖分离费率、滑点）；Optuna + 滚动 walk-forward；每 6 秒的持仓风控监控 | 量化开发、资管投资数据、交易系统 |
| **卖点预警 SaaS**（sell_csgo_monitor，已上线） | Flask + React + JWT、付费分级、独立调度进程、多通道推送容灾、375 个测试、VPS 部署 | 金融科技后端、全栈 |
| **UCI EECS 215 课程项目** | HMM / LSTM / GRU / Transformer、按组切分防泄漏 | 风控数据科学（加分项） |

**真正稀缺的三点**（面试时要主动讲）：

1. **一个人从 0 做完整系统并上线收费** —— 大部分应届生只有课程项目。
2. **会自己证伪** —— 安慰剂对照、随机对照组、承认信号失效。这在量化面试里比任何「胜率」都值钱。
3. **对市场有真实热情和实盘经验** —— 金融公司很看重「你为什么想做这行」，你有具体的故事。

**短板**（下文逐条给补法）：

- ⚠️ 没看到正式工作/实习经历（如果有，务必告诉我，权重最高）
- 没有 C++；Java 你说熟练，但作品里全是 Python —— 需要一个 Java 作品来证明
- 研究叙事偏「庄家 / 技术分析」，需要翻译成美国量化的语言（见 [PROJECT_PACKAGING.md](./PROJECT_PACKAGING.md)）
- 技术栈是 SQLite / 单机 VPS，美国公司更常见 Postgres / AWS / Docker
- 项目全是私有仓库，招聘方看不到

---

## 2. 岗位方向匹配度（从高到低）

| 方向 | 匹配度 | 典型职位名 | LA/OC 代表雇主 | 加州新人 base（调研值） | 最大差距 |
|---|---|---|---|---|---|
| 量化开发 / 研究工程师 | ★★★★ | Quantitative Developer, Quant Engineer, Research Engineer | PIMCO, Capital Group, Research Affiliates, Crabel | 资管约 $120–195K；湾区基金 $160–190K | C++、固收知识、很多岗要 3 年经验 |
| 资管投资数据 / 组合分析工程 | ★★★★ | Investment Data Engineer, Portfolio Analytics, Technology Analyst | Capital Group, PIMCO, Pacific Life, TCW | 约 $110–150K | 业绩归因、风险模型、固收术语；云数据栈 |
| 金融科技后端 | ★★★★ | Software Engineer I, Backend Engineer, SDE | Acorns, Experian, PennyMac, Zest AI, Tala, Dave | 约 $90–160K | Java/Postgres、支付/账本正确性、系统设计面试 |
| 信贷风控 / 数据科学 | ★★★ | Credit Risk Analyst, Data Scientist, ML Engineer | Experian, Zest AI, Hyundai Capital, Tala, PennyMac | 约 $100–150K | 信贷领域知识（评分卡、WoE/IV、PSI）、SQL 作品 |
| 预测市场 / 加密 / 定价 | ★★★（故事最契合） | Quant Analyst (Prediction Markets), Trading Engineer | 基本不在 LA（NYC / 远程） | AQR 预测市场分析师 $200–230K（在 CT） | 概率校准、做市理论；地点不匹配 |
| 量化研究 | ★★～★★★ | Quantitative Researcher / Analyst | PIMCO QRA, Research Affiliates, Pacific Life | $95–215K（顶级基金 $225–300K 但不在加州） | 看得见的统计严谨性、研究报告、和 PhD 竞争 |
| 交易系统 / 低延迟 | ★～★★（C++ 岗）/ ★★★（Java 岗） | Trading Systems Engineer, Low-latency Developer | 南加州很少；Java 路线：PIMCO 交易技术 | 芝加哥/纽约 $200–300K | C++、网络/并发、FIX / 行情接入 |

> 我的建议：**主攻前三行**（量化开发、资管数据、金融科技后端），它们都在 Irvine / Newport Beach / LA，而且互相可以用同一套素材；**量化研究和预测市场作为冲刺**；交易系统等补了 Java/C++ 作品再考虑。

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

- **如果 2026 年 12 月毕业**：你算 2027 届应届生（IMC 明确写了 2026-09 到 2027-07 毕业都可以）。现在就投所有开放的 2027 new grad 岗位，同时投南加州资管的具体职位。
- **如果已经毕业（2026 年春/夏）**：部分「20XX 届」岗位可能不收你；重点投常年开放的 University Graduate 岗（如 Citadel）、滚动入职的轮岗项目（Experian 4/6 月、PennyMac 1/6 月、Capital Group CAMPUS）、以及写「0–2 年经验」的初级岗。**注意 OPT 的失业天数在累计**（见签证部分）。

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

> ⚠️ 前提：假设你是 F-1 学生、需要 OPT → STEM OPT → H-1B。**请确认**，不是的话这部分就不适用。

- **OPT / STEM OPT 目前照常**（STEM OPT 要求雇主加入 E-Verify）。有一个 OPT 收费的提案刚过白宫审查、还没公布金额。
- **H-1B 抽签已改为按工资级别加权**：给的工资越高，中签概率越高。→ **量化、资管这类高薪岗位在抽签上天然占优**，这对你的方向是利好。
- **最大的不确定性**：2026-08-25 提出的「每个 cap H-1B 申请加收 $103,265」的规则（尚未生效），如果落地，小公司会更不愿意担保新人。→ 优先投**有持续担保记录的大公司**（PIMCO、Capital Group、Pacific Life、Experian、Acorns 这类）。
- **兜底**：大学及附属非营利研究机构的 H-1B 不受名额限制（cap-exempt），包括 UC 系统的研究岗。
- 打分器会自动识别 JD 里「不担保」的措辞并降权（`list --hide-visa` 可以直接隐藏）。

---

## 7. 我还需要你告诉我的信息（按重要性）

1. **签证身份和毕业时间**（决定整个策略的时间线和公司筛选）
2. **你现在的简历**，以及有没有**实习 / 工作经历**、本科学校、GPA（有真实雇主的经历权重最高）
3. 卖点预警 SaaS **有没有真实用户 / 付费用户 / 收入**（有的话是很强的一条）
4. EECS 215 项目里**你具体负责哪部分**
5. Java、C++、SQL 的真实水平；用过 AWS / Docker 吗
6. 偏好：更想做量化还是金融科技？能接受湾区 / 圣地亚哥 / 远程吗？期望薪资？
7. 愿不愿意把部分项目**公开到 GitHub**（需要先清理 token，见 [PROJECT_PACKAGING.md](./PROJECT_PACKAGING.md) 最后一节）

拿到这些之后，我会：更新素材库和打分偏好、把你的真实简历合进来、针对第一梯队公司逐个定制。
