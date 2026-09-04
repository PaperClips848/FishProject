# program		ramirezXavier_demo_presence_fishData.py
# purpose	    Demonstrate regression algorithms from sklearn on the seth_gov_envData10dtsMetrics_genusCount2026.csv
# notes         (1) Algorithms include: Gradient Boosting, XGBoost Regressor, 
#               (2) Polynomial Regression, and Decision Tree Regression.
#               (3) The plot includes the actual vs predicted for the first 3 algorithms, and the polynomial regression fit for alcohol vs quality.
#               (4) Log Transformed the Gambusia abundance for better regression performance.
# date			3/16/2026 
# programmer    Xavier Ramirez

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures # use this for polynomial regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier 
import xgboost as xgb 
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import datetime          # used for getting the date
import os                # used for getting the basic file name (returns lower case)

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
programName_c = os.path.dirname(os.path.abspath(__file__)) #NEW
script_name = os.path.splitext(os.path.basename(__file__))[0] #NEW


fileName_c = 'data/seth_gov_envData10dtsMetrics_genusCount2026.csv'
programMsg_c = script_name + ' (' + date_c + ')'
authorName_c = 'Xavier Ramirez'

nX = 1 # will only work for nX = 1 at the moment

fig_dir = os.path.abspath(os.path.join(programName_c, "..", "..", "..", "figures")) #NEW
os.makedirs(fig_dir, exist_ok=True) #NEW
figName_c = os.path.join(fig_dir, f"{script_name}_fig.png") #NEW

# ================= GET ALL DATA ======================
data_df = pd.read_csv((fileName_c))

Y_features = (data_df['Gambusia'] > 0).astype(int).to_numpy().ravel()

pc1_drivers = ['pbottom_Mud', 'pbottom_Cobble', 'maxMonthFlow_cfs', 'avgMonthFlow_cfs', 'upstreamCumDA_km2',
               'pbottom_SmGravel', 'slopePercent']
X_features = data_df[pc1_drivers]

# =============== GET TRAIN, TEST DATA ==================
# For Gradient Boosting, XGBoost Regressor, and Decision Tree Regression,  will use the same train/test split
X_train, X_test, Y_train, Y_test = train_test_split(X_features, Y_features, test_size = 0.3, random_state = 42)
Y_train = Y_train.ravel()
Y_test = Y_test.ravel()

print("\nX_train:", X_train.shape) # Make sure these are the same size
print("Y_train:", Y_train.shape)

# =============== Algorithm 1 ( Gradient Boosting ) ==================
GrdBoost = GradientBoostingClassifier(n_estimators = 200,learning_rate = 0.1,max_depth = 3,random_state = 42)

# Training (Gradient Boosting)
GrdBoost.fit(X_train, Y_train)

# Predict (Gradient Boosting)
Y_predict_GrdBoost = GrdBoost.predict(X_test)

# Evaluate (Gradient Boosting)
acc_grb = accuracy_score(Y_test, Y_predict_GrdBoost)
f1_grb = f1_score(Y_test, Y_predict_GrdBoost)
auc_grb = roc_auc_score(Y_test, GrdBoost.predict_proba(X_test)[:,1])

print('Gradient Boosting Error Metrics:')
print("Accuracy Score:", acc_grb)
print("F1 Score:", f1_grb)
print("AUC Score:", auc_grb)

# =============== Algorithm 2 ( XGBoost Classifier ) ==================
xgb_model = xgb.XGBClassifier(
    n_estimators=1500,
    learning_rate=0.001,
    max_depth=7,
    min_child_weight=2,
    gamma=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    colsample_bylevel=0.8,
    colsample_bynode=0.8,
    reg_lambda=1.0,
    reg_alpha=0.5,
    tree_method="hist",
    grow_policy="lossguide",
    max_leaves=128,
    random_state=42)

# Training (XGB Regressor)
xgb_model.fit(X_train, Y_train)

# Predict (XGB Regressor)
Y_predict_XGB = xgb_model.predict(X_test)

# Evaluate (XGB Regressor)
acc_xgb = accuracy_score(Y_test, Y_predict_XGB)
f1_xgb = f1_score(Y_test, Y_predict_XGB)
auc_xgb = roc_auc_score(Y_test, xgb_model.predict_proba(X_test)[:,1])

print('\nXGB Regressor Error Metrics:')
print("Accuracy Score:", acc_xgb)
print("F1 Score:", f1_xgb)
print("AUC Score:", auc_xgb)

# ================= Algorithm 3 ( POLYNOMIAL REGRESSION ) ==================
Ytrain_v = Y_train
Ytest_v = Y_test

if nX == 1:
    XdataT_df = X_train[['pbottom_Mud']]
    XdataV_df = X_test[['pbottom_Mud']]

elif nX == 2:
    XdataT_df = X_train[['pbottom_Mud', 'pbottom_Cobble']]
    XdataV_df = X_test[['pbottom_Mud', 'pbottom_Cobble']]

else:
    XdataT_df = X_train[pc1_drivers]
    XdataV_df = X_test[pc1_drivers]

# Linear (Degree 1)
pipe1 = make_pipeline(
    PolynomialFeatures(1),
    LogisticRegression(max_iter=2000))

pipe1.fit(XdataT_df, Ytrain_v)
Y_pred_p1 = pipe1.predict(XdataV_df)
Y_prob_p1 = pipe1.predict_proba(XdataV_df)[:,1]

acc_p1 = accuracy_score(Ytest_v, Y_pred_p1)
f1_p1 = f1_score(Ytest_v, Y_pred_p1)
auc_p1 = roc_auc_score(Ytest_v, Y_prob_p1)

print('\nPolynomial Regression Error Metrics:')
print("Accuracy Score (Linear):", acc_p1)
print("F1 Score (Linear):", f1_p1)
print("AUC Score (Linear):", auc_p1)

# Quadratic (Degree 2)
pipe2 = make_pipeline(
    PolynomialFeatures(2),
    LogisticRegression(max_iter=2000))

pipe2.fit(XdataT_df, Ytrain_v)
Y_pred_p2 = pipe2.predict(XdataV_df)
Y_prob_p2 = pipe2.predict_proba(XdataV_df)[:,1]

acc_p2 = accuracy_score(Ytest_v, Y_pred_p2)
f1_p2 = f1_score(Ytest_v, Y_pred_p2)
auc_p2 = roc_auc_score(Ytest_v, Y_prob_p2)

print("Accuracy Score (Quadratic):")
print("Accuracy Score (Quadratic):", acc_p2)
print("F1 Score (Quadratic):", f1_p2)
print("AUC Score (Quadratic):", auc_p2)

# ================= Algorithm 4 ( Decision Tree Classifier ) ==================
Tree = DecisionTreeClassifier(max_depth=5, random_state=42)

#Training (Decision Tree)
Tree.fit(X_train, Y_train)

#Predicting (Decision Tree)
Y_predict_Tree = Tree.predict(X_test)

# Evaluate
acc_tree = accuracy_score(Y_test, Y_predict_Tree)
f1_tree = f1_score(Y_test, Y_predict_Tree)
auc_tree = roc_auc_score(Y_test, Tree.predict_proba(X_test)[:,1])

print('\nDecision Tree Error Metrics:')
print("Accuracy Score:", acc_tree)
print("F1 Score:", f1_tree)
print("AUC Score:", auc_tree)

# Plot ROC Curves for all models
fig, axs = plt.subplots(2, 2, figsize=(11, 5.5), dpi=200)

RocCurveDisplay.from_estimator(GrdBoost, X_test, Y_test, ax=axs[0,0])
axs[0,0].set_title("Gradient Boosting ROC")

RocCurveDisplay.from_estimator(xgb_model, X_test, Y_test, ax=axs[0,1])
axs[0,1].set_title("XGBoost ROC")

RocCurveDisplay.from_estimator(pipe1, XdataV_df, Y_test, ax=axs[1,0])
axs[1,0].set_title("Logistic Regression ROC")

RocCurveDisplay.from_estimator(Tree, X_test, Y_test, ax=axs[1,1])
axs[1,1].set_title("Decision Tree ROC")

fig.tight_layout()
fig.savefig(figName_c)
plt.close()