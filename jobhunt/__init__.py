"""jobhunt —— 找 LA / Irvine 金融相关工作的个人流水线。

流程：抓取（fetchers）→ 过滤打分（scoring）→ 入库追踪（store）
      → 定制简历（tailor + render）→ 半自动预填申请表（apply，人工点提交）。
"""

__version__ = "0.1.0"
