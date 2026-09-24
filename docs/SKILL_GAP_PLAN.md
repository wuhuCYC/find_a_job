# 要掌握什么：按岗位要求倒推的补强计划

> 来源：2025–2026 年真实职位描述（PIMCO、Capital Group、Citadel、IMC、Acorns、Experian 等），
> 原文和链接见 [research/roles_and_calendar.md](./research/roles_and_calendar.md)。
> 按优先级排列，不按时间 —— 先把前面的做精，再往后走。

---

## 0. 所有方向都会考的基本功

| 项目 | 为什么 | 怎么练 |
|---|---|---|
| **LeetCode 中等题**（数组/哈希/双指针/堆/图/DP） | 几乎每家的第一轮 | NeetCode 150，用 Python 刷；Java 至少能写出来 |
| **SQL**（窗口函数、join、聚合、去重） | 资管数据、风控、金融科技都现场考 | LeetCode SQL 50 / DataLemur；拿你自己的 A 股库出题 |
| **系统设计** | 金融科技必考；量化开发常考「设计一个回测/行情服务」 | Alex Xu《System Design Interview》；Kleppmann《DDIA》；拿你的 SaaS 当案例练 |
| **概率与统计** | 量化岗必考；其他岗也会问 | 绿皮书（Zhou, *A Practical Guide to Quantitative Finance Interviews*）、*Heard on the Street*、Ross 概率 |
| **英文行为面试** | 资管（PIMCO、Capital Group）文化面权重很高 | 用 STAR 准备 6–8 个故事：从 0 做 SaaS、发现回测 bug、承认信号失效、和用户打交道 |
| **项目深挖** | 每家都会追问到细节 | [PROJECT_PACKAGING.md](./PROJECT_PACKAGING.md) 第 4 节的 7 个问题 |

---

## 1. 按方向：要求 vs 你已有 vs 缺口

### 量化开发 / 研究工程师（主攻）

- **必须**：生产级 Python（pandas/NumPy 向量化）、SQL、测试、Git/Linux、行情数据管道、回测基础设施、能和研究员聊统计
- **加分**：C++（或 pybind11）、kdb+/q、Parquet/Arrow、Dask/Spark、AWS、Airflow
- **金融知识**：回测陷阱（前视、幸存者偏差）、交易成本；PIMCO 要固收（久期/凸性/收益率曲线/利差），Capital Group 写明要现代组合理论和组合风险模型
- **你已有**：回测引擎、walk-forward、Optuna、数据管道、实时服务 —— PIMCO 岗位描述几乎一一对应
- **缺口**：C++；固收知识；「规模化」证据（Postgres/Parquet、CI、可复现）；很多岗写 3 年经验 → 优先投 new grad / junior / Technology Analyst

### 资管投资数据 / 组合分析工程（主攻，地点最匹配）

- **必须**：Python + SQL、ETL 与数据质量检查、API/服务、仪表盘、一个云数据平台（Snowflake / Databricks / AWS）
- **金融知识**：收益计算（TWR/MWR）、Brinson 归因、跟踪误差、VaR、因子暴露、固收分析（久期/凸性/OAS/关键利率）、证券主数据、公司行为、基准
- **你已有**：管道、仪表盘、React、测试
- **缺口**：领域词汇；企业数据栈（dbt / Airflow / Snowflake）

### 金融科技后端（主攻，雇主最多）

- **必须**：一门后端语言写到生产深度（Java/Kotlin、Go、Python 均可）、API 设计、Postgres（事务、隔离级别、迁移）、自动化测试、AWS、CI/CD
- **加分**：Kafka / 事件驱动、Docker/K8s、可观测性；支付（ACH、银行卡、清算）、KYC/AML
- **金融知识**：支付生命周期（授权/扣款/结算/退款/拒付）、**复式记账账本与对账**、**幂等性**；券商 T+1；贷款发放与催收
- **你已有**：真实上线的多用户 SaaS（JWT、付费分级、调度、推送容灾、375 测试）—— 这在后端面试里很有分量
- **缺口**：Java 作品、Postgres、金钱正确性模式（幂等 key、账本、对账）、AWS、系统设计面试

### 信贷风控 / 数据科学（南加州雇主密集）

- **必须**：大量 SQL、Python、逻辑回归 + GBM、评分卡（分箱、WoE/IV）、AUC/KS、PSI 监控、跨时间验证
- **加分**：可解释性（SHAP、拒贷理由码）、公平借贷检验、模型风险管理（SR 11-7）、PD/LGD/EAD、CECL
- **你已有**：XGBoost/HMM/LSTM 经验；信号收益回填本质就是模型监控
- **缺口**：信贷领域知识和一个信贷作品

### 量化研究 / 预测市场（冲刺）

- **必须**：统计深度（估计、检验、回归、时间序列）、正确的 ML 验证、研究写作
- **要补**：多重检验校正（deflated Sharpe、White's Reality Check）、Newey-West 标准误、平稳性、IC/t 值报告；预测市场要概率校准（Brier / log loss）、做市理论（库存风险、逆向选择）
- **你已有**：安慰剂对照、随机对照组 —— 这是研究员思维，已经比大多数应届生强

### 交易系统 / 低延迟（暂缓）

- 高频公司核心是 C++（内存模型、无锁、缓存、网络）；Java 路线（IMC 收 Java、银行电子交易、PIMCO 交易技术）也存在
- 你的实时监控是「秒级」，不是「微秒级」—— 需要专门的作品才能进这个方向

---

## 2. 补强作品（按优先级）

每个都做成**公开仓库 + 英文 README + 结果**，做完后把事实加进 `experience_bank.yaml`。

### 项目 1：一份严谨的研究报告（最高优先级 —— 所有量化方向都受益）

用公开数据（美股日线，或加密货币交易所的公开 K 线 / 盘口）重跑你的信号框架，写成一份 PDF 研究报告：

- 数据：点时（point-in-time）、含退市股的股票池，或加密货币的完整币种列表
- 方法：nested walk-forward（参数搜索只在训练窗口内）、最终留一段完全不碰的 holdout
- 成本：手续费、价差、按波动/成交额缩放的滑点
- 报告：年化收益/波动、Sharpe 及其置信区间、最大回撤及持续时间、命中率 + 盈亏比、换手、**试了多少组参数**、deflated Sharpe、对市场/规模/动量因子回归后的 alpha
- 对照：随机入场安慰剂（相同持有期分布）；逐个去掉信号看贡献（ablation）
- **写清楚失败的信号** —— 负结果最能建立可信度

> 为什么是美股/加密：美国面试官能直接理解和验证；也不暴露你在 A 股 / CS2 的私有阈值。

### 项目 2：Java 限价订单簿 + 撮合引擎

- 价格-时间优先撮合、限价/市价/撤单、部分成交；ITCH 风格的行情回放
- JMH 基准测试 + 延迟分位数（p50/p99/p99.9）直方图；单元测试覆盖撮合正确性
- 进阶：LMAX Disruptor 风格的单线程事件循环

> 同时证明「我 Java 熟练」和「我懂市场微观结构」，量化开发、交易系统、金融科技都用得上。想走高频的话，再用 C++17 做一版。

### 项目 3：信贷评分卡（打开南加州信贷雇主）

- 公开数据：Home Credit Default Risk、Lending Club 或 Freddie Mac 贷款级数据
- 评分卡（分箱 + WoE + 逻辑回归）对比 GBM 挑战模型；跨时间验证；PSI 稳定性监控；SHAP 拒贷理由码；简单的公平性检验
- 写一页「模型文档」（仿 SR 11-7 风格）

### 项目 4：把 SaaS 升级到「金融级正确性」

- SQLite → Postgres（迁移脚本）；Docker 化；GitHub Actions 跑测试
- 加一个**复式记账 + 幂等 API** 的模块（比如订阅付费：幂等 key、账本分录、日终对账）
- 部署到 AWS（或写清楚部署架构）

### 项目 5（投 PIMCO / Capital Group 前）：固收小工具库

- 收益率曲线 bootstrap、久期/凸性、关键利率久期、简单的 OAS 概念演示
- 面试时能自然聊固收，是 PIMCO 的强加分

---

## 3. 书单（按用途）

- **量化面试**：Zhou《绿皮书》、Crack《Heard on the Street》、Joshi《Quant Job Interview Q&A》、Mosteller《Fifty Challenging Problems in Probability》
- **研究方法（最推荐先读）**：Aronson《Evidence-Based Technical Analysis》—— 专门讲怎么用统计检验技术分析，是你从「庄家理论」过渡到量化语言的最佳桥梁；López de Prado《Advances in Financial Machine Learning》
- **微观结构**：Harris《Trading and Exchanges》
- **固收**：Donald Smith《Bond Math》；Tuckman《Fixed Income Securities》
- **信贷**：Siddiqi《Intelligent Credit Scoring》
- **后端**：Kleppmann《Designing Data-Intensive Applications》；Alex Xu《System Design Interview》

## 4. 证书

- **CFA Level I**：现在不考。PIMCO 等公司入职后报销，而且对工程岗帮助有限；先读固收和组合管理的章节即可
- **SIE**：不需要（工程岗用不到）
- **AWS Associate**：金融科技 / 资管数据方向的小加分，可选
