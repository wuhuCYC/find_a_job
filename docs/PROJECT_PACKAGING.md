# 你的项目怎么讲：同一段经历，不同的讲法

「打造不同的经历」在这里的意思是：**同样真实的项目，按目标岗位换重点、换语言**。
不是编经历 —— 美国公司会做背景调查，面试会追问到每一行代码，编的东西一问就穿，而且会进黑名单。
你的真实素材已经足够强，缺的只是「翻译」。

所有简历 bullet 都在 [`profile/experience_bank.yaml`](../profile/experience_bank.yaml)，每条都标了出处和适用方向。

---

## 1. 三个项目 × 不同方向的一句话 pitch（面试开场用）

**CS2 饰品市场研究平台**

- 量化研究：*"I took a discretionary trading setup, made it look-ahead-free, and tested it against a placebo and an unconditional baseline on 13,671 events — then showed where it breaks."*
- 量化开发：*"I built the research stack end to end: three years of price and order-book data for 2,430 instruments, scanners, backtests, and a paper-trading harness with a random control group."*
- 交易市场 / 游戏经济：*"I modeled supply, demand and large-holder inventories in a real virtual-goods market, and tracked how price cycles form and break."*（如果想加市场规模，只用你能给出出处的数字）

**A 股波段信号系统**

- 量化开发：*"An event-driven backtester with realistic fills — next-open execution, limit-up/down, position caps, asymmetric fees and slippage — plus walk-forward parameter search."*
- 交易系统：*"A 'buy slow, sell fast' design: end-of-day batch scan over 5,000 stocks, and a real-time monitor that polls holdings every 6 seconds with severity levels and de-duplication."*
- 资管数据：*"A data layer over positioning and fund-flow datasets with incremental Parquet caching and sector aggregation."*

**卖点预警 SaaS**

- 金融科技后端：*"I shipped a multi-user product people pay for: JWT auth, encrypted third-party credentials, a separate scheduler service, multi-channel alerts with failover, 375 tests, deployed on Linux with nginx and TLS."*（「people pay for」只有在真有付费用户时才能说 ⚠️）

---

## 2. 翻译表：你的说法 → 美国量化面试的说法

你的市场直觉是对的，但「庄家 / 主力 / 洗盘 / 乾卦六爻」在美国面试里会被当成「技术分析玄学」。**同一个现象，换成可检验的语言**：

| 你现在的说法 | 面试里的说法 | 能拿出的证据 / 该补的检验 |
|---|---|---|
| 主力吸筹 | persistent informed order flow；supply absorption（在售持续减少而价格不动） | 在售量变化对未来收益的预测力（IC、t 值），控制价格档位 |
| 洗盘 / 震仓 | temporary price pressure、short-term reversal | 你已经做了：回落到成本区的事件研究 + 安慰剂对照 |
| 庄盘八段 / 六爻 | market-cycle / regime state machine | 状态只能用过去数据判定；报告检测滞后；分 regime 的表现 |
| 板块合力 | sector co-movement / industry momentum | 你用了 Pearson 相关中位数衡量板块凝聚度 |
| 在售 / 求购 | order-book depth、bid/ask imbalance | walk-forward 下的 imbalance 特征有效性，扣除平台手续费 |
| 胜率 70% | hit rate **加上** payoff ratio、expectancy、每笔收益的 t 值 | 永远和盈亏比、回撤、基线一起报 |
| 优化了 21 个信号 | model selection under multiple testing | 报试了多少组参数；nested walk-forward；deflated Sharpe |
| 卖点监控 | exit rule / risk overlay | 和固定持有期、跟踪止损对比「回吐」多少 |

**在真正的做市商面试里**（Optiver、IMC、SIG、Citadel Securities、Jane Street）：面试官自己就是做市商，不要说「做市商操纵价格 / 割韭菜」。换成 inventory management、adverse selection、liquidity provision。

---

## 3. 不能写进简历的东西（以及为什么）

| 不要写 | 原因 | 用什么代替 |
|---|---|---|
| **「¥500+ 排手套左侧买 85% 胜率 / 中位 24%」**（UNIVERSAL_DEALER_THEORY） | 这是先用完整价格路径把「cycle」切出来、再回头算 phase 1 买入的收益 —— 买点是事后才知道的，有**后视偏差**。量化面试官第一个问题就是「你当时怎么知道自己在 phase 1？」 | 用你 6 月做的 **v0.3 事件研究**：信号日 = 回落确认日（实时可知），13,671 个事件，对比安慰剂和基线。这正是你自己已经做出来的更严谨版本 |
| 乾卦、六爻、庄家、主力、波特老师/方圆老师 | 听起来像玄学或跟单，削弱可信度 | 第 2 节的翻译表 |
| Optuna 最优 trial 的成绩 | 那是样本内结果 | 只报样本外 / walk-forward 的结果 |
| 课程项目的 0.82 accuracy / F1 | 测试集里 164/185 是负类，全猜负类就有 0.89 —— 这个数字比基线还低 | 只讲方法（HMM、按组切分防泄漏、类别不平衡处理） |
| 代码行数当卖点 | 2026 年大家都用 AI 写代码，行数说明不了能力，反而引来「你自己写的吗」 | 讲设计取舍、踩过的坑、怎么验证正确性。坦然说用了 Claude Code，重点讲你做了哪些判断 |
| 个人实盘收益截图 | 不可验证，还有合规味道；金融公司有 personal trading policy（预审批、持有期、禁止某些品种） | 讲纪律、风控、复盘；别说「入职后我还要继续跑自己的策略」 |
| 「CS:GO skins」开门见山 | 美国有 skin gambling 丑闻的负面联想 | 说 "the Steam CS2 item market — a virtual-goods marketplace with order-book data"，重点在数据和方法 |

---

## 4. 面试高频追问 & 你的回答素材

1. **"How do you know it's not overfit?"**
   → walk-forward 70/30；样本外命中率从 24.5% 到 29.5%（3,274 个测试信号）；方法论审计里去掉了相关特征重复加分（最高叠加分 83 → 25）、把冷却期从 7 天拉到 14 天减少重叠样本；安慰剂对照；随机对照组。**要补**：试过多少组参数（trial count）、deflated Sharpe。
2. **"What's the base rate?"**
   → 事件研究里全天基线 29.0%、安慰剂 33.3%、信号 46.0%。**A 股和 walk-forward 那组也要补基线**。
3. **"Why would this edge exist and persist?"**
   → 薄市场、散户主导、信息不对称、7 天交易冷却期造成的流动性摩擦；同时说清楚它在市场结构冲击时失效（43.5% vs 44.9%）。
4. **"What's the capacity / what about costs?"**
   → A 股回测里有买卖分离费率和三档滑点；CS2 要补平台手续费、交易冷却期对退出的影响、盘口深度对容量的限制。
5. **"Worst bug you found in your backtester?"**
   → 准备一个真实的：比如相关特征重复加分导致分数虚高，或者前视偏差的修复（`.shift(1)`、次日开盘成交）。
6. **"How did you avoid look-ahead in the regime and sector filters?"**
   → 只用截至当日的数据；HMM 要用 filtered 概率而不是 smoothed（smoothed 用了未来信息）—— 这一点可以主动讲，很加分。
7. **"Which single signal would you keep?"**
   → 准备一个，并说明理由和证据。

---

## 5. 把项目公开成作品集之前（安全清单）

招聘方看不到私有仓库。建议**新建干净的公开仓库**（不是把现有私有仓库直接改成公开），原因：

- ⚠️ `csgo-agent` 的 `CLAUDE.md` 里写着 CSQAQ 企业 API token 和 Telegram bot token；`csgo-monitor` 仓库提交了 `.env`。**不管公不公开，都建议现在就去轮换（rotate）这些 token**。git 历史里删不干净，所以公开版要从零新建。
- 私有仓库里有你的策略阈值（净买压档位、参数等），这是你的 alpha，不需要给别人看。
- `find_a_job` 这个仓库目前是 **public**，里面有你的简历素材和求职策略。建议在 GitHub 设置里改成 private（Settings → General → Danger Zone → Change visibility）。

公开版作品集建议：

1. **一个研究报告仓库**：英文 README + 架构图 + 方法（walk-forward、成本、安慰剂、随机对照）+ 结果表 + 失败的信号。数据用公开数据重跑（见 [SKILL_GAP_PLAN.md](./SKILL_GAP_PLAN.md) 项目 1）。
2. **一个工程仓库**：回测引擎核心（去掉私有信号），带单元测试和 CI。
3. SaaS 放演示视频 / 截图 + 架构说明，代码不必公开。
