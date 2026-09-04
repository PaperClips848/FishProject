# program		timeAttr_demo_sumMetrics.py
# purpose	    Gets summary metrics from 10-day time series csv, make NEW csvs
# usage         script
# notes         (1) envData10-DayTimeSeries_18f.csv -> env_summary_metrics.csv
# date			02/1/2026
# programmer    Xavier Ramirez

import datetime
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
programname_c = os.path.basename(__file__)
programName_c = os.path.dirname(os.path.abspath(__file__))

ix = programname_c.find('.')
figName_c = programname_c[:ix] + '_fig.png'

fileName_c = r"./data/gov_envData10dts_2025.csv"
programMsg_c = programName_c + ' (' + date_c + ')'
authorName_c = 'Xavier Ramirez'


# ========== Load and preprocess data ==============
print("WORKING DIRECTORY =", os.getcwd())
df = pd.read_csv(fileName_c)
df.columns = df.columns.str.strip()
sites = sorted({col.split('.')[0] for col in df.columns if col.startswith("site_")})

# ---- 1. Compute trend ----
def compute_trend(y):
    x = np.arange(len(y)).reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    return model.coef_[0]

summary_rows = []

for site in sites:
    # all columns for this site
    site_cols = [col for col in df.columns if col.startswith(site + ".")]
    site_df = df[site_cols]

    site_summary = {"site": site}

    for col in site_cols:
        y = site_df[col].values
        base = col.split('.', 1)[1]  # variable name only

        site_summary[f"{base}_mean"] = np.mean(y)
        site_summary[f"{base}_median"] = np.median(y)
        site_summary[f"{base}_sd"] = np.std(y)
        site_summary[f"{base}_min"] = np.min(y)
        site_summary[f"{base}_max"] = np.max(y)
        site_summary[f"{base}_range"] = np.max(y) - np.min(y)
        site_summary[f"{base}_cv"] = np.std(y) / np.mean(y)
        site_summary[f"{base}_trend"] = compute_trend(y)

    summary_rows.append(site_summary)

summary_df = pd.DataFrame(summary_rows)
summary_df = summary_df.sort_values(
    by="site",
    key=lambda s: s.str.extract(r'(\d+)')[0].astype(int)
)
summary_df["site"] = summary_df["site"].str.replace(
    r"site_(\d+)",
    lambda m: f"site_{int(m.group(1)) + 1}",
    regex=True
)
summary_df.to_csv(r"./data/new_CSV.csv", index=False)

# # ---- 2. Combine both csvs into one
# env_static = pd.read_csv(r"../../../data/seth_environmentalGenusCountData_nov2024.csv")
# env_metrics = pd.read_csv(r"../../../data/env_summary_metrics.csv")

# env_metrics["site"] = (                 # turns site_# to # integers only
#     env_metrics["site"]
#     .str.replace("site_", "", regex=False)
#     .astype(int)
# )
# env_metrics = env_metrics.rename(columns={"site": "SiteN"})

# env_static["SiteN"] = env_static["SiteN"].astype(int)

# merged = env_static.merge(env_metrics, on="SiteN", how="inner")
# merged.to_csv(r"../../../data/envAttrGenusCountSumMetrics_feb2026.csv", index=False)