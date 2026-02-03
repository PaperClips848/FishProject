# ============================================================
# program       brashearsKorbin_demo_dimReduce_seth_environmentalGenusCountData_nov2024.py
# purpose       Demonstrate dimensionality reduction (PCA, LDA, t-SNE, UMAP)
#               using environmental + eco region data for fish habitats
# usage         Run as a standalone script
# notes         This script produces four visualization methods:
#               (1) PCA – linear global structure
#               (2) LDA – supervised linear separation
#               (3) t-SNE – nonlinear local structure
#               (4) UMAP – nonlinear ecological niches
# date          02/01/2026
# programmer    Korbin Brashears
# ============================================================

import datetime
import os
import win32api
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
import umap

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')

programname_c = os.path.basename(__file__)
programName_c = win32api.GetLongPathName(win32api.GetShortPathName(programname_c))

ix = str.find(programName_c, '.')

fileNameData_c = 'seth_environmentalGenusCountData_nov2024.csv'
programMsg_c = programName_c + ' (' + date_c + ')'
authorName_c = 'K.L. Brashears'
figName_c = programName_c[:ix] + '_fig.png'

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
segc_d = pd.read_csv('data/seth_environmentalGenusCountData_nov2024.csv')
ser_d = pd.read_csv('data/seth_ecoRegionData.csv')

# Clean column names
datasets = [segc_d, ser_d]
for df in datasets:
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(' ', '_')
        .str.replace('\n', '', regex=False)
    )

num_df = segc_d.merge(ser_d, on="SiteN", how="left")

env_cols = [
    "DO", "pH",
    "avg_Depth", "avg_WW",
    "pflow_Run", "pflow_Riffle",
    "pbottom_Mud", "pbottom_SmGravel", "pbottom_Cobble",
    "pfloat_macrophytes", "pfloat_wood",
    "avgMonthFlow_cfs", "CV_flow"
]

# ------------------------------------------------------------
# Prepare features and labels
# ------------------------------------------------------------
labels = num_df["eco_Number"].astype(str)
X = num_df[env_cols].copy()

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(labels)
labelNames = le.inverse_transform(np.unique(y))
nLabels = len(labelNames)

# ------------------------------------------------------------
# Train/verify split
# ------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=24
)

# ------------------------------------------------------------
# Standardize
# ------------------------------------------------------------
scaler = StandardScaler()
scaler.fit(X_train)

Xtr = scaler.transform(X_train)
Xte = scaler.transform(X_test)

# ------------------------------------------------------------
# PCA
# ------------------------------------------------------------
pca = PCA(n_components=2)
Xtr_pca = pca.fit_transform(Xtr)
Xte_pca = pca.transform(Xte)

# ------------------------------------------------------------
# LDA
# ------------------------------------------------------------
if nLabels > 1:
    lda = LDA(solver="eigen", shrinkage="auto")
    Xtr_lda = lda.fit_transform(Xtr, y_train)
    Xte_lda = lda.transform(Xte)
else:
    Xtr_lda = np.zeros((len(Xtr), 2))
    Xte_lda = np.zeros((len(Xte), 2))

# ------------------------------------------------------------
# t-SNE
# ------------------------------------------------------------
tsne_tr = TSNE(
    n_components=2,
    perplexity=5,
    learning_rate=20,
    max_iter=3000,
    init="pca",
    random_state=30
).fit_transform(Xtr)

tsne_te = TSNE(
    n_components=2,
    perplexity=5,
    learning_rate=20,
    max_iter=3000,
    init="pca",
    random_state=30
).fit_transform(Xte)

# ------------------------------------------------------------
# UMAP
# ------------------------------------------------------------
um = umap.UMAP(
    n_components=2,
    n_neighbors=5,
    min_dist=0.05,
    metric="correlation",
    learning_rate=0.1,
    n_epochs=1000,
    random_state=30
)

Xtr_umap = um.fit_transform(Xtr)
Xte_umap = um.transform(Xte)

# ------------------------------------------------------------
# Plotting helper
# ------------------------------------------------------------
def plot_panel(idx, X, labels, title):
    plt.subplot(2, 4, idx)
    for kc in np.unique(labels):
        plt.scatter(X[labels == kc, 0], X[labels == kc, 1], s=18)
    plt.title(title, fontsize=9)
    plt.legend(labelNames, fontsize="x-small")

# ------------------------------------------------------------
# Plot all methods
# ------------------------------------------------------------
plt.figure(num=1, figsize=(15, 11), dpi=200)
plt.subplots_adjust(left=.05, right=0.95, top=0.9, bottom=0.10, wspace=0.3, hspace=0.3)
plt.rcParams.update({'font.size': 8})

# Train
plot_panel(1, Xtr_pca, y_train, "PCA – Train")
plot_panel(2, Xtr_lda, y_train, "LDA – Train")
plot_panel(3, tsne_tr, y_train, "t-SNE – Train")
plot_panel(4, Xtr_umap, y_train, "UMAP – Train")

# Verify
plot_panel(5, Xte_pca, y_test, "PCA – Verify")
plot_panel(6, Xte_lda, y_test, "LDA – Verify")
plot_panel(7, tsne_te, y_test, "t-SNE – Verify")
plot_panel(8, Xte_umap, y_test, "UMAP – Verify")

# ================= Label Plot Edges ==================
plt.subplot(position=[0.050, 0.93, 0.02500, 0.02500])
plt.axis('off')
plt.text(0, .5, programMsg_c, fontsize=8)

plt.subplot(position=[0.550, 0.93, 0.02500, 0.02500])
plt.axis('off')
plt.text(0, .5, authorName_c, fontsize=8)

plt.subplot(position=[0.050, 0.01, 0.02500, 0.02500])
plt.axis('off')
plt.text(0, .5, fileNameData_c, fontsize=8)

plt.subplot(position=[0.350, 0.01, 0.02500, 0.02500])
plt.axis('off')
plt.text(0, .5, "", fontsize=8)

plt.savefig(figName_c)