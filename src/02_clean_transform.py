import pandas as pd

inpath = "data/raw/claims_ops_sample.csv"
outpath = "data/processed/claims_ops_clean.csv"

df = pd.read_csv(inpath, parse_dates=["date"])

# basic cleaning
df = df.dropna()
df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()

# sanity caps
df["claims_received"] = df["claims_received"].clip(lower=0)
df["sla_met_rate"] = df["sla_met_rate"].clip(0, 1)

df.to_csv(outpath, index=False)
print(f"✅ Wrote {outpath} with {len(df):,} rows")
