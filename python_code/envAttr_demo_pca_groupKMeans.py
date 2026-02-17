# program		envAttr_demo_pca_groupKMeans
# purpose	    Using PCA->Kmeans to find groupings and clusterings
# usage         script
# notes         (1) 
# date			02/10/2026
# programmer    Xavier Ramirez

import datetime
import os
#import win32api #NEW REMOVE
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from matplotlib.patches import Ellipse

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
#programname_c = os.path.basename(__file__) #NEW REMOVE
programName_c = os.path.dirname(os.path.abspath(__file__)) #NEW
#programName_c = win32api.GetLongPathName(win32api.GetShortPathName(programname_c))
script_name = os.path.splitext(os.path.basename(__file__))[0] #NEW

#ix = str.find(programName_c, '.') #NEW REMOVE

fileName_c = 'data/seth_gov_envData10dtsMetrics_genusCount2026.csv'
programMsg_c = script_name + ' (' + date_c + ')' #changed from programName_c to script_name
authorName_c = 'Xavier Ramirez'

#figName_c = programName_c[:ix] + '_fig.png'

fig_dir = os.path.abspath(os.path.join(programName_c, "..", "figures")) #NEW
os.makedirs(fig_dir, exist_ok=True) #NEW
figName_c = os.path.join(fig_dir, f"{script_name}_fig.png") #NEW

# ============== 0. Load and preprocess data ===============
df = pd.read_csv(fileName_c)                # load dataset
df.columns = df.columns.str.strip()         # clean column names
genus_col = "Gambusia"                      # target genus for script

# ============== 1. Select environmental columns ===========
env_cols = df.columns[4:25]                 # columns 1–24 are environmental
X_env = df[env_cols]

# ============== 2. Standardize the data ===================
scaler = StandardScaler()                   # standardize environmental attributes
X_env_scaled = scaler.fit_transform(X_env)  # ensures PCA is not dominated by large-scale variables

# ============== 3. Standardize the environmental variables =
pca_env = PCA()                             # initialize PCA model
pca_env.fit(X_env_scaled)                   # fit PCA to standardized data

# ============== 4. Fit PCA (all components) ===============
pc_scores = pca_env.transform(X_env_scaled)         # compute each site's pc scores
df["PC1"] = pc_scores[:, 0]                 # store PC1 scores
df["PC2"] = pc_scores[:, 1]                 # store PC2 scores

plt.figure(figsize=(12,6))                  # creates a nicely-sized figure
# ============== 5. PC1 vs PC2 scatter plot (121)===========
pc_scores = pca_env.transform(X_env_scaled)
plt.subplot(121)
plt.scatter(pc_scores[:, 0], pc_scores[:, 1], alpha=0.7)
plt.xlabel(f"PC1 ({pca_env.explained_variance_ratio_[0]*100:.1f}% var)")
plt.ylabel(f"PC2 ({pca_env.explained_variance_ratio_[1]*100:.1f}% var)")
plt.title("Environmental PCA (PC1 vs PC2)")
plt.tight_layout()

# Cluster sites based on PC1 and PC2
cluster_colors = {
    0: 'orange',
    1: 'green',
    2: 'red'}
kmeans = KMeans(n_clusters=3, random_state=42).fit(pc_scores[:, :2])
df["Cluster"] = kmeans.labels_
# Plot with cluster colors
plt.subplot(121)
for cluster_id in np.unique(df["Cluster"]):
    cluster_points = pc_scores[df["Cluster"] == cluster_id]
    color = cluster_colors[cluster_id]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                label=f"Cluster {cluster_id}", alpha=0.7, color=color)
    center = cluster_points.mean(axis=0)
    width = cluster_points[:, 0].ptp() * 1.2
    height = cluster_points[:, 1].ptp() * 1.2
    ellipse = Ellipse(center, width, height,
                      edgecolor=color, facecolor='none', linestyle='--', linewidth=1.5)
    plt.gca().add_patch(ellipse)
plt.legend()

print("/Cluster labels for Environmental PCA:")
for idx, label in enumerate(kmeans.labels_):
    print(f"Point {idx}: Cluster {label}")
    
# TIME SERIES METRICS SECTION
# ============== 6. Select metric columns ==================
timeMet = df.columns[59:202]                # columns 59-202 are time metrics
X_met = df[timeMet]

# ============== 7. Standardize the data ==================
scaler = StandardScaler()                   # standardize environmental attributes
X_met_scaled = scaler.fit_transform(X_met)  # ensures PCA is not dominated by large-scale variables

# ============== 8. Standardize the environmental variables 
pca_met = PCA()                             # initialize PCA model
pca_met.fit(X_met_scaled)                   # fit PCA to standardized data

# ============== 9. Fit PCA (all components) ==============
pc_met_scores = pca_met.transform(X_met_scaled) # compute each site's pc scores
df["PC1"] = pc_met_scores[:, 0]                 # store PC1 scores
df["PC2"] = pc_met_scores[:, 1]                 # store PC2 scores

# ============== 10. PC1 vs PC2 scatter plot (122)==========
pc_met_scores = pca_met.transform(X_met_scaled)
plt.subplot(122)
plt.scatter(pc_met_scores[:, 0], pc_met_scores[:, 1], alpha=0.7)
plt.xlabel(f"PC1 ({pca_met.explained_variance_ratio_[0]*100:.1f}% var)")
plt.ylabel(f"PC2 ({pca_met.explained_variance_ratio_[1]*100:.1f}% var)")
plt.title("Time Series Metrics PCA (PC1 vs PC2)")
plt.tight_layout()

# Cluster sites based on PC1 and PC2
cluster_colors = {
    0: 'orange',
    1: 'green',
    2: 'red'}
kmeans = KMeans(n_clusters=3, random_state=42).fit(pc_met_scores[:, :2])
df["Cluster"] = kmeans.labels_
# Plot with cluster colors
plt.subplot(122)
for cluster_id in np.unique(df["Cluster"]):
    cluster_points = pc_met_scores[df["Cluster"] == cluster_id]
    color = cluster_colors[cluster_id]
    plt.scatter(cluster_points[:, 0], cluster_points[:, 1],
                label=f"Cluster {cluster_id}", alpha=0.7, color=color)
    center = cluster_points.mean(axis=0)
    width = cluster_points[:, 0].ptp() * 1.2
    height = cluster_points[:, 1].ptp() * 1.2
    ellipse = Ellipse(center, width, height,
                      edgecolor=color, facecolor='none', linestyle='--', linewidth=1.5)
    plt.gca().add_patch(ellipse)
plt.legend()

print("Cluster labels for Time Series Metrics PCA:")
for idx, label in enumerate(kmeans.labels_):
    print(f"Point {idx}: Cluster {label}")

# ============= Make the subplots look a little nicer ================= 
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.13, wspace=0.3, hspace=0.3)

# ================= label plot edges ==================
plt.subplot(position=[0.0500,    0.93,    0.02500,    0.02500]) # U-left
plt.axis('off')
plt.text(0,.5, programMsg_c, fontsize=7)

plt.subplot(position=[0.550,    0.93,    0.02500,    0.02500]) # U-right
plt.axis('off')
plt.text(0,.5, authorName_c, fontsize=7)

plt.subplot(position=[0.0500,    0.02,    0.02500,    0.02500]) # L-left
plt.axis('off')
plt.text(0,.5, fileName_c, fontsize=7)

plt.subplot(position=[0.3500,    0.02,    0.02500,    0.02500]) # L-right
plt.axis('off')
#plt.text(0,.5, msg_plot_c, fontsize=8)

plt.savefig(figName_c)
plt.show()