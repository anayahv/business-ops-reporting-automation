import pandas as pd

inpath = "data/processed/claims_ops_clean.csv"
outpath = "reports/outputs/kpis_monthly.csv"

df = pd.read_csv(inpath, parse_dates=["date", "month"])

kpis = (df.groupby("month")
          .agg(
              total_claims=("claims_received", "sum"),
              avg_handle_time_min=("avg_handle_time_min", "mean"),
              sla_met_rate=("sla_met_rate", "mean"),
              avg_backlog=("backlog_end", "mean"),
              avg_cost_per_claim=("cost_per_claim", "mean"),
          )
          .reset_index())

# a simple "productivity" proxy
kpis["cost_total_est"] = (kpis["total_claims"] * kpis["avg_cost_per_claim"]).round(2)

kpis.to_csv(outpath, index=False)
print(f"✅ Wrote {outpath}")
