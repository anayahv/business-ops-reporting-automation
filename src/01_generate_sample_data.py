import numpy as np
import pandas as pd

np.random.seed(42)

n = 5000
dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
date = np.random.choice(dates, size=n)

regions = ["GTA", "Ontario East", "Ontario West", "Ottawa", "Remote"]
channels = ["Web", "Phone", "Branch"]
teams = ["Team A", "Team B", "Team C", "Team D"]

df = pd.DataFrame({
    "date": pd.to_datetime(date),
    "region": np.random.choice(regions, size=n, p=[0.35, 0.2, 0.2, 0.15, 0.1]),
    "channel": np.random.choice(channels, size=n, p=[0.55, 0.35, 0.10]),
    "team": np.random.choice(teams, size=n),
    "claims_received": np.random.poisson(lam=40, size=n),
})

# simulate processing outcomes
df["avg_handle_time_min"] = np.clip(np.random.normal(loc=18, scale=6, size=n), 5, 60)
df["sla_target_min"] = 20
df["sla_met_rate"] = np.clip(np.random.normal(loc=0.78, scale=0.10, size=n), 0.30, 0.98)

# backlog & cost
df["backlog_end"] = np.clip(np.random.normal(loc=260, scale=90, size=n), 20, 900).round()
df["cost_per_claim"] = np.clip(np.random.normal(loc=12.5, scale=3.5, size=n), 4, 35).round(2)

outpath = "data/raw/claims_ops_sample.csv"
df.sort_values("date").to_csv(outpath, index=False)
print(f"✅ Wrote {outpath} with {len(df):,} rows")

