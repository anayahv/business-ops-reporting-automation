import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

kpi_path = "reports/outputs/kpis_monthly.csv"
outpath = "reports/outputs/forecast.csv"

df = pd.read_csv(kpi_path, parse_dates=["month"])
df = df.sort_values("month").reset_index(drop=True)

# Forecast total_claims next 6 months via simple linear trend
df["t"] = np.arange(len(df))
X = df[["t"]]
y = df["total_claims"]

model = LinearRegression().fit(X, y)

future = pd.date_range(df["month"].max() + pd.offsets.MonthBegin(1), periods=6, freq="MS")
future_t = np.arange(len(df), len(df) + 6)
pred = model.predict(future_t.reshape(-1, 1))

forecast = pd.DataFrame({
    "month": future,
    "forecast_total_claims": np.round(pred).astype(int)
})

forecast.to_csv(outpath, index=False)
print(f"✅ Wrote {outpath}")
