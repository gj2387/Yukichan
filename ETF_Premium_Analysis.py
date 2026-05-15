pip install yfinance pandas numpy matplotlib
# 导入刚需库（ETF交易天天用这几个）
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== 1. 设置标的：举例子 沪深300ETF 510300.SS ==========
etf_ticker = "510300.SS"
start_date = "2024-01-01"
end_date = "2026-01-01"

# ========== 2. 下载ETF历史日线数据 ==========
etf = yf.Ticker(etf_ticker)
df = etf.history(start=start_date, end=end_date)

# 只保留我们需要的字段：开盘/最高/最低/收盘/成交量
df = df[["Open", "High", "Low", "Close", "Volume"]]
df.rename(columns={"Close":"ETF_Price"}, inplace=True)

# ========== 3. 关键：模拟基金净值IOPV（简化实操口径） ==========
# 逻辑：ETF净值用收盘价近似替代行业IOPV简易估算
# 真实工作中会拿交易所IOPV行情接口，入门先这样建模
df["ETF_NAV"] = df["ETF_Price"] * (1 + np.random.normal(0, 0.002, len(df)))

# ========== 4. 核心公式：计算折溢价率 ==========
# 折溢价率 = (ETF市价 - 基金净值) / 基金净值
df["Premium_Rate"] = (df["ETF_Price"] - df["ETF_NAV"]) / df["ETF_NAV"]

# 转成百分比，方便看
df["Premium_Rate_Pct"] = df["Premium_Rate"] * 100

# ========== 5. 输出最近10天数据 ==========
print("ETF折溢价最新10日数据：")
print(df[["ETF_Price", "ETF_NAV", "Premium_Rate_Pct"]].tail(10))

# ========== 6. 可视化：画折溢价率曲线 ==========
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.figure(figsize=(14,6))
plt.plot(df.index, df["Premium_Rate_Pct"], label="ETF折溢价率(%)", color="#1f77b4")
plt.axhline(y=0, color="red", linestyle="--", label="平价线")
plt.title("沪深300 ETF 历史折溢价走势", fontsize=14)
plt.xlabel("日期")
plt.ylabel("折溢价率 %")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

