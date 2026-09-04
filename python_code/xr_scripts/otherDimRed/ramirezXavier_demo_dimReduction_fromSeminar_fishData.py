# program		ramirezXavier_demo_dimReduction_fromSeminar_fishData.py
# purpose	    Demonstrate dimensionality reduction techniques on the seth_gov_envData10dtsMetrics_genusCount2026.csv
# notes         (1) Techniques include: NMDS
#               (2) The plot includes the reduced dimensions for each technique.
#               (3) Standardized
#               (4) Genus and environmental attributes are reduced separately.
#               (5) The arrows show the correlation of the original features with the reduced dimensions.
# date			4/27/2026 
# programmer    Xavier Ramirez

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime          # used for getting the date
import os                # used for getting the basic file name (returns lower case)
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import MDS

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
programName_c = os.path.dirname(os.path.abspath(__file__)) #NEW
script_name = os.path.splitext(os.path.basename(__file__))[0] #NEW

fileName_c = 'data/seth_gov_envData10dtsMetrics_genusCount2026.csv'
programMsg_c = script_name + ' (' + date_c + ')'
authorName_c = 'Xavier Ramirez'

fig_dir = os.path.abspath(os.path.join(programName_c, "..", "..", "..", "figures")) #NEW
os.makedirs(fig_dir, exist_ok=True) #NEW
figName_c = os.path.join(fig_dir, f"{script_name}_fig.png") #NEW

# ================= GET ALL DATA ======================
fish_df = pd.read_csv(fileName_c)

# Preprocessing for attributes and labels
state_ohe = pd.get_dummies(fish_df["State"], prefix="State")
X_fish = pd.concat([fish_df.iloc[:, 4:25]], axis=1) # 26 to 55 for genus
X_fish_std = StandardScaler().fit_transform(X_fish)
cat = fish_df["State"].astype("category")
y_fish = cat.cat.codes.values
target_names_fish = cat.cat.categories.tolist()

print("X_fish shape:", X_fish_std.shape)
print("y_fish shape:", y_fish.shape)
print("State categories:", target_names_fish)

# Genus as attributes below
X_genus = fish_df.iloc[:, 26:55]          # genus columns
X_genus_std = StandardScaler().fit_transform(X_genus)

# ======================== APPLY DIMENSIONALITY REDUCTION TECHNIQUES ======================
nmds_env = MDS(metric=False, n_components=2, random_state=10, dissimilarity='euclidean')
X_fish_nmds = nmds_env.fit_transform(X_fish_std)

nmds_genus = MDS(metric=False, n_components=2, random_state=5, dissimilarity='euclidean')
X_genus_nmds = nmds_genus.fit_transform(X_genus_std)

# ======================== PLOT RESULTS ======================
plt.figure(num=1, figsize=(12.0, 5.5),dpi=400)
plt.subplots_adjust(left=.05,right=0.95,top=0.9, bottom=0.10, wspace=0.15, hspace=0.4) 
plt.rcParams.update({'font.size': 8})
fontSizeTitle = 9               # the update doesn't impact title font size
colors = ['red','green','blue', 'magenta', 'cyan', 'yellow', 'orange', 'purple', 'brown', 'pink']

plt.subplot(121)
# Scatter by state
for label, color in zip(np.unique(y_fish), colors):
    plt.scatter(X_fish_nmds[y_fish==label, 0],
                X_fish_nmds[y_fish==label, 1],
                label=target_names_fish[label],
                alpha=0.7, s=60, color=color)

# Compute correlations
feature_names_env = X_fish.columns
corrs_env = np.zeros((X_fish_std.shape[1], 2))

for i in range(X_fish_std.shape[1]):
    cor_x = np.corrcoef(X_fish_std[:, i], X_fish_nmds[:, 0])[0, 1]
    cor_y = np.corrcoef(X_fish_std[:, i], X_fish_nmds[:, 1])[0, 1]
    corrs_env[i] = [cor_x, cor_y]

# Scale arrows
arrow_scale_env = 0.8 * np.max(np.abs(X_fish_nmds))

# Plot arrows
for i, (cx, cy) in enumerate(corrs_env):
    plt.arrow(0, 0,
              cx * arrow_scale_env,
              cy * arrow_scale_env,
              color='black',
              width=0.003,
              head_width=0.05,
              alpha=0.8)
    plt.text(cx * arrow_scale_env * 1.1,
             cy * arrow_scale_env * 1.1,
             feature_names_env[i],
             fontsize=8)

plt.title("Fish NMDS Projection (Environmental Attributes)")
plt.xlabel("NMDS1")
plt.ylabel("NMDS2")
plt.grid(True)
plt.legend()

plt.subplot(122)
# Scatter by state
for label, color in zip(np.unique(y_fish), colors):
    plt.scatter(X_genus_nmds[y_fish==label, 0],
                X_genus_nmds[y_fish==label, 1],
                label=target_names_fish[label],
                alpha=0.7, s=60, color=color)

# Compute correlations
feature_names_genus = X_genus.columns
corrs_genus = np.zeros((X_genus_std.shape[1], 2))

for i in range(X_genus_std.shape[1]):
    cor_x = np.corrcoef(X_genus_std[:, i], X_genus_nmds[:, 0])[0, 1]
    cor_y = np.corrcoef(X_genus_std[:, i], X_genus_nmds[:, 1])[0, 1]
    corrs_genus[i] = [cor_x, cor_y]

# Scale arrows
arrow_scale_genus = 0.8 * np.max(np.abs(X_genus_nmds))

# Plot arrows
for i, (cx, cy) in enumerate(corrs_genus):
    plt.arrow(0, 0,
              cx * arrow_scale_genus,
              cy * arrow_scale_genus,
              color='black',
              width=0.003,
              head_width=0.05,
              alpha=0.8)
    plt.text(cx * arrow_scale_genus * 1.1,
             cy * arrow_scale_genus * 1.1,
             feature_names_genus[i],
             fontsize=8)

plt.title("Fish NMDS Projection (Genus Attributes)")
plt.xlabel("NMDS1")
plt.ylabel("NMDS2")
plt.grid(True)
plt.legend()

# ================= label plot edges ==================
fig = plt.gcf()  # get current figure
# Upper-left
fig.text(0.01, 0.99, programMsg_c, fontsize=8, ha='left', va='center')

# Upper-right
fig.text(0.55, 0.96, authorName_c, fontsize=8, ha='right', va='center')

# Lower-left
fig.text(0.02, 0.02, fileName_c, fontsize=8, ha='left', va='center')

plt.tight_layout()
plt.savefig(figName_c)
plt.close()