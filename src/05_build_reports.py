import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("reports/charts").mkdir(parents=True, exist_ok=True)
Path("reports/outputs").mkdir(parents=True, exist_ok=True)

kpis = pd.read_csv("reports/outputs/kpis_monthly.csv", parse_dates=["month"])
forecast = pd.read_csv("reports/outputs/forecast.csv", parse_dates=["month"])

# Charts
plt.figure()
plt.plot(kpis["month"], kpis["total_claims"])
plt.title("Total Claims (Monthly)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/charts/total_claims.png")
plt.close()

plt.figure()
plt.plot(kpis["month"], kpis["sla_met_rate"])
plt.title("SLA Met Rate (Monthly)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/charts/sla_met_rate.png")
plt.close()

# Excel report
xlsx_path = "reports/kpi_report.xlsx"
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
    kpis.to_excel(writer, sheet_name="KPIs_Monthly", index=False)
    forecast.to_excel(writer, sheet_name="Forecast", index=False)

# Executive summary (simple, powerful)
latest = kpis.sort_values("month").iloc[-1]
summary = f"""# Executive Summary

**Period:** {latest['month'].date()}

## Key Metrics (Latest Month)
- Total Claims: **{int(latest['total_claims']):,}**
- Avg Handle Time: **{latest['avg_handle_time_min']:.1f} min**
- SLA Met Rate: **{latest['sla_met_rate']:.1%}**
- Avg Backlog: **{latest['avg_backlog']:.0f}**
- Est. Total Cost: **${latest['cost_total_est']:,.2f}**

## Observations
- Monitor SLA and handle time together: rising handle time often correlates with lower SLA performance.
- Backlog stability is a leading indicator for operational risk and downstream service delays.

## Next Steps / Recommendations
- Investigate top drivers by region/channel/team for months with low SLA.
- Prioritize automation in monthly reporting to reduce manual effort and speed decision cycles.
"""

with open("reports/executive_summary.md", "w", encoding="utf-8") as f:
    f.write(summary)

print("✅ Built reports: Excel + charts + executive_summary.md")
