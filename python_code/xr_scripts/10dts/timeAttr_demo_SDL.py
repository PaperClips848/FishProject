# program		timeAttr_demo_SDL.py
# purpose	    RUN SDL ON TIME METRICS
# usage         script
# notes         (1) 
# date			09/4/2026
# programmer    Xavier Ramirez

import datetime
import os
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
programname_c = os.path.basename(__file__)
programName_c = os.path.dirname(os.path.abspath(__file__))

fileName_c = r"./data/gov_envData10dts_2025.csv"
print("WORKING DIRECTORY =", os.getcwd())

# ========== Load and preprocess data ==============
df = pd.read_csv(fileName_c)
df.columns = df.columns.str.strip()

# If  CSV has no date column, create one:
if "date" not in df.columns:
    df["date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="10D")

df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")

# Identify sites
sites = sorted(
    {col.split('.')[0] for col in df.columns if col.startswith("site_")},
    key=lambda s: int(s.split('_')[1])
)

# Storage for SDL results
rows = []

for site in sites:
    site_cols = [col for col in df.columns if col.startswith(site + ".")]

    for col in site_cols:
        ts = df[col].asfreq("10D")  # 10-day frequency

        # SDL requires at least 2 full periods; assume yearly seasonality (36 intervals)
        try:
            result = seasonal_decompose(ts, model='additive', period=36)
        except Exception as e:
            print(f"Skipping {col}: {e}")
            continue

        base = col.split('.', 1)[1]

        rows.append({
            "site": site,
            "variable": base,
            "trend_mean": result.trend.mean(),
            "trend_slope": (result.trend.dropna().iloc[-1] - result.trend.dropna().iloc[0]) / len(result.trend.dropna()),
            "seasonal_amp": result.seasonal.max() - result.seasonal.min(),
            "resid_std": result.resid.std()
        })

# Save results
out_df = pd.DataFrame(rows)
# Shift site numbers from site_0 → site_1, so on and so forth
out_df["site"] = out_df["site"].str.replace(
    r"site_(\d+)",
    lambda m: f"site_{int(m.group(1)) + 1}",
    regex=True
)
out_df.to_csv(r"./data/SDL_results.csv", index=False)

print("SDL complete. Output saved to SDL_results.csv")
