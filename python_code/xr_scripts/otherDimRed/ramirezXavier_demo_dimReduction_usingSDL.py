# program		ramirezXavier_demo_dimReduction_usingSDL.py
# purpose	    Demonstrate dimensionality reduction techniques on the seth_gov_envData10dtsMetrics_genusCount2026.csv
# notes         (1) Techniques include: NMDS
#               (2) The plot includes the reduced dimensions for each technique.
#               (3) Standardized
#               (4) Genus and environmental attributes are reduced separately.
#               (5) The arrows show the correlation of the original features with the reduced dimensions.
# date			09/04/2026
# programmer    Xavier Ramirez

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
programName_c = os.path.dirname(os.path.abspath(__file__))
script_name = os.path.splitext(os.path.basename(__file__))[0]

fileName_c = 'data/seth_gov_envData10dtsMetrics_genusCount2026.csv'
programMsg_c = script_name + ' (' + date_c + ')'
authorName_c = 'Xavier Ramirez'

fig_dir = os.path.abspath(os.path.join(programName_c, "..", "..", "..", "figures"))
os.makedirs(fig_dir, exist_ok=True)
figName_c = os.path.join(fig_dir, f"{script_name}_fig.png")

# ================= GET ALL DATA ======================
fish_df = pd.read_csv(fileName_c)
print(fish_df.columns)

# fish_df already has SiteN
print("fish_df SiteN head:", fish_df["SiteN"].head())


print("fish_df SHAPE:", fish_df.shape)
print("fish_df columns:", fish_df.columns)

# ================= SDL DATA ======================
sdl = pd.read_csv("data/SDL_results.csv")

# Create SiteN in SDL
sdl["SiteN"] = (
    sdl["site"]
    .str.replace("site_", "", regex=False)
    .astype(int)
)
sdl = sdl.drop(columns=["site"])

print("SDL SHAPE:", sdl.shape)
print("SDL columns:", sdl.columns)

# Pivot SDL into wide format
sdl_wide = sdl.pivot_table(
    index="SiteN",
    columns="variable",
    values=["trend_mean", "trend_slope", "seasonal_amp", "resid_std"]
)

sdl_wide.columns = [f"{var}_{metric}" for metric, var in sdl_wide.columns]
sdl_wide = sdl_wide.reset_index()

print("SDL_WIDE SHAPE:", sdl_wide.shape)
print("SDL_WIDE columns:", sdl_wide.columns)

# ================= MERGE ======================
full = fish_df.merge(sdl_wide, on="SiteN", how="inner")

print("FULL SHAPE:", full.shape)
print("FULL columns:", full.columns)

# ================= SELECT ENV + GENUS FEATURES ======================
env_cols = full.filter(regex="trend|seasonal|resid|_mean|_slope").columns
genus_cols = full.columns[26:55]

print("ENV COLS:", env_cols)
print("GENUS COLS:", genus_cols)

# ================= PREPROCESS ======================
X_env = full[env_cols]
print("X_env RAW SHAPE:", X_env.shape)

X_genus = full[genus_cols]
print("X_genus RAW SHAPE:", X_genus.shape)

# Standardize
X_env_std = StandardScaler().fit_transform(X_env)
X_genus_std = StandardScaler().fit_transform(X_genus)

# State labels
cat = fish_df["State"].astype("category")
y_fish = cat.cat.codes.values
target_names_fish = cat.cat.categories.tolist()

print("y_fish shape:", y_fish.shape)
print("State categories:", target_names_fish)

# ================= NMDS ======================
nmds_env = MDS(metric=False, n_components=2, random_state=10, dissimilarity='euclidean')
X_env_nmds = nmds_env.fit_transform(X_env_std)

nmds_genus = MDS(metric=False, n_components=2, random_state=5, dissimilarity='euclidean')
X_genus_nmds = nmds_genus.fit_transform(X_genus_std)

# ================= PLOT ======================
plt.figure(num=1, figsize=(12.0, 5.5), dpi=400)
plt.subplots_adjust(left=.05, right=0.95, top=0.9, bottom=0.10, wspace=0.15, hspace=0.4)
plt.rcParams.update({'font.size': 8})
colors = ['red','green','blue','magenta','cyan','yellow','orange','purple','brown','pink']

# ---------- ENV NMDS ----------
plt.subplot(121)
for label, color in zip(np.unique(y_fish), colors):
    plt.scatter(X_env_nmds[y_fish==label, 0],
                X_env_nmds[y_fish==label, 1],
                label=target_names_fish[label],
                alpha=0.7, s=60, color=color)

feature_names_env = X_env.columns
corrs_env = np.zeros((X_env_std.shape[1], 2))

for i in range(X_env_std.shape[1]):
    cor_x = np.corrcoef(X_env_std[:, i], X_env_nmds[:, 0])[0, 1]
    cor_y = np.corrcoef(X_env_std[:, i], X_env_nmds[:, 1])[0, 1]
    corrs_env[i] = [cor_x, cor_y]

arrow_threshold = 0.9
important_env = np.where(np.abs(corrs_env).max(axis=1) > arrow_threshold)[0]
# Compute importance score for each environmental variable
importance_scores_env = np.sqrt(corrs_env[:,0]**2 + corrs_env[:,1]**2)

# Print top 10 drivers
top_env_idx = np.argsort(importance_scores_env)[-10:]

print("\nTop 10 Environmental Drivers:")
for i in top_env_idx:
    print(f"{feature_names_env[i]}: {importance_scores_env[i]:.3f}")

arrow_scale_env = 0.8 * np.max(np.abs(X_env_nmds))

for i in important_env:
    cx, cy = corrs_env[i]
    plt.arrow(0, 0, cx * arrow_scale_env, cy * arrow_scale_env,
              color='black', width=0.003, head_width=0.05, alpha=0.8)
    plt.text(cx * arrow_scale_env * 1.1,
             cy * arrow_scale_env * 1.1,
             feature_names_env[i], fontsize=8)

plt.title("NMDS Projection (Environmental Attributes)")
plt.xlabel("NMDS1")
plt.ylabel("NMDS2")
plt.grid(True)
plt.legend()

# ---------- GENUS NMDS ----------
plt.subplot(122)
for label, color in zip(np.unique(y_fish), colors):
    plt.scatter(X_genus_nmds[y_fish==label, 0],
                X_genus_nmds[y_fish==label, 1],
                label=target_names_fish[label],
                alpha=0.7, s=60, color=color)

feature_names_genus = X_genus.columns
corrs_genus = np.zeros((X_genus_std.shape[1], 2))

for i in range(X_genus_std.shape[1]):
    cor_x = np.corrcoef(X_genus_std[:, i], X_genus_nmds[:, 0])[0, 1]
    cor_y = np.corrcoef(X_genus_std[:, i], X_genus_nmds[:, 1])[0, 1]
    corrs_genus[i] = [cor_x, cor_y]

arrow_scale_genus = 0.8 * np.max(np.abs(X_genus_nmds))

for i, (cx, cy) in enumerate(corrs_genus):
    plt.arrow(0, 0, cx * arrow_scale_genus, cy * arrow_scale_genus,
              color='black', width=0.003, head_width=0.05, alpha=0.8)
    plt.text(cx * arrow_scale_genus * 1.1,
             cy * arrow_scale_genus * 1.1,
             feature_names_genus[i], fontsize=8)

plt.title("NMDS Projection (Genus Attributes)")
plt.xlabel("NMDS1")
plt.ylabel("NMDS2")
plt.grid(True)
plt.legend()

# ---------- LABELS ----------
fig = plt.gcf()
fig.text(0.01, 0.99, programMsg_c, fontsize=8, ha='left', va='center')
fig.text(0.55, 0.96, authorName_c, fontsize=8, ha='right', va='center')
fig.text(0.02, 0.02, fileName_c, fontsize=8, ha='left', va='center')

plt.tight_layout()
plt.savefig(figName_c)
plt.close()