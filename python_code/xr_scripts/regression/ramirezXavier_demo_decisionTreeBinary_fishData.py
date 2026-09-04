# program		ramirezXavier_demo_decisionTreeBinary_fishData.py
# purpose	    Demonstrate classification algorithms from sklearn on the seth_gov_envData10dtsMetrics_genusCount2026.csv
# notes         (1) Algorithms include: Decision Tree Classifier
#               (2) Log Transformed the Gambusia abundance for better regression performance.
# date			4/28/2026 
# programmer    Xavier Ramirez

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, RocCurveDisplay
import datetime          # used for getting the date
import os                # used for getting the basic file name (returns lower case)
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns

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
data_df = pd.read_csv((fileName_c))

# Binary target in Y
Y = (data_df['Gambusia'] > 0).astype(int).to_numpy().ravel()
pc1_drivers = ['pbottom_Mud', 'pbottom_Cobble', 'maxMonthFlow_cfs', 'avgMonthFlow_cfs', 'upstreamCumDA_km2',
               'pbottom_SmGravel', 'slopePercent']
X_all = data_df[pc1_drivers]
X_all_std = StandardScaler().fit_transform(X_all)
print("X_all shape:", X_all.shape)

# =============== GET TRAIN, TEST DATA ==================
X_train, X_test, Y_train, Y_test = train_test_split(X_all_std, Y, test_size = 0.3, random_state = 42)
print("\nX_train:", X_train.shape)
print("Y_train:", Y_train.shape)

# =============== Algorithm ( Decision Tree Classifier ) ==================
dt_model = DecisionTreeClassifier(
    max_depth=7,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42
)

# Training (Decision Tree Classifier)
# Early stopping on validation set
dt_model.fit(X_train, Y_train)

# Predict (Decision Tree Classifier)
Y_prob = dt_model.predict_proba(X_test)[:, 1]
Y_pred = dt_model.predict(X_test)

# Evaluate (Decision Tree Classifier)
acc_dt = accuracy_score(Y_test, Y_pred)
f1_dt = f1_score(Y_test, Y_pred)
auc_dt = roc_auc_score(Y_test, Y_prob)

print('\nDecision Tree Metrics:')
print("Accuracy Score:", acc_dt)
print("F1 Score:", f1_dt)
print("AUC Score:", auc_dt)

# For correlation heatmap for visualization of feature relationships
# --- Compute correlation matrix ---
corr_matrix = X_all.corr(method='pearson')

# PLOTTING
fig, axs = plt.subplots(1, 3, figsize=(13, 6), dpi=400)
# 1. Correlation Heatmap
sns.heatmap(
    corr_matrix,
    cmap='coolwarm',
    annot=False,
    linewidths=0.5,
    square=True,
    cbar_kws={'shrink': 0.7},
    ax=axs[0]
)
axs[0].set_title("Environmental Correlation Heatmap", fontsize=10)

# 2. ROC Curve
RocCurveDisplay.from_estimator(dt_model, X_test, Y_test, ax=axs[1])
axs[1].set_title("Decision Tree ROC Curve for Gambusia", fontsize=10)

# 3. Feature Importance
importances = dt_model.feature_importances_
sorted_idx = np.argsort(importances)[::-1]
top_k = min(12, len(sorted_idx))
top_idx = sorted_idx[:top_k]
top_names = X_all.columns[top_idx]
top_vals = importances[top_idx]

axs[2].barh(range(top_k), top_vals[::-1])
axs[2].set_yticks(range(top_k))
axs[2].set_yticklabels(top_names[::-1], fontsize=7)
axs[2].set_title("Decision Tree Feature Importance", fontsize=10)

# ================= label plot edges ==================
plt.subplot(position=[0.0500, 0.955, 0.02500, 0.02500])  # U-left (moved up)
plt.axis('off')
plt.text(0, .5, programMsg_c, fontsize=8)

plt.subplot(position=[0.550, 0.955, 0.02500, 0.02500])   # U-right (moved up)
plt.axis('off')
plt.text(0, .5, authorName_c, fontsize=8)

plt.subplot(position=[0.0500, 0.015, 0.02500, 0.02500])  # L-left (moved down)
plt.axis('off')
plt.text(0, .5, fileName_c, fontsize=8)

plt.subplot(position=[0.950, 0.025, 0.02500, 0.02500])  # L-right (moved down)
plt.axis('off')
plt.text(0, .5, f"Accuracy: {acc_dt:.2f}\nF1: {f1_dt:.2f}\nAUC: {auc_dt:.2f}", fontsize=8, ha='right', va='center')

plt.tight_layout
plt.savefig(figName_c)
plt.close()