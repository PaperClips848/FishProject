# program		ramirezXavier_demo_regression_fishData.py
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
from sklearn.ensemble import GradientBoostingRegressor 
import xgboost as xgb 
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
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

Y_features = np.log1p(data_df['Gambusia'])

pc1_drivers = ['pbottom_Mud', 'pbottom_Cobble', 'maxMonthFlow_cfs', 'avgMonthFlow_cfs', 'upstreamCumDA_km2',
               'pbottom_SmGravel', 'slopePercent']
X_features = data_df[pc1_drivers]

# =============== GET TRAIN, TEST DATA ==================
# For Gradient Boosting, XGBoost Regressor, and Decision Tree Regression,  will use the same train/test split
X_train, X_test, Y_train, Y_test = train_test_split(X_features, Y_features, test_size = 0.3, random_state = 42)

print("\nX_train:", X_train.shape) # Make sure these are the same size
print("Y_train:", Y_train.shape)

# =============== Regression Algorithm 1 ( Gradient Boosting ) ==================
GrdBoost = GradientBoostingRegressor(n_estimators = 200,learning_rate = 0.1,max_depth = 3,random_state = 42)

# Training (Gradient Boosting)
GrdBoost.fit(X_train, Y_train)

# Predict (Gradient Boosting)
Y_predict_GrdBoost = GrdBoost.predict(X_test)

# Evaluate (Gradient Boosting)
rmse = np.sqrt(mean_squared_error(Y_test, Y_predict_GrdBoost))
mae = mean_absolute_error(Y_test, Y_predict_GrdBoost)
r2 = r2_score(Y_test, Y_predict_GrdBoost)

print('Gradient Boosting Error Metrics:')
print("Root Mean Squared Error:", rmse)
print("Mean Abosolute Error:", mae)
print("R2 Score :", r2)

# =============== Regression Algorithm 2 ( XGBoost Regressor ) ==================
xgb_model = xgb.XGBRegressor(
    n_estimators=1500,
    learning_rate=0.01,
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
    random_state=42
)

# Training (XGB Regressor)
xgb_model.fit(X_train, Y_train)

# Predict (XGB Regressor)
Y_predict_XGB = xgb_model.predict(X_test)

# Evaluate (XGB Regressor)
rmse_XGB = np.sqrt(mean_squared_error(Y_test, Y_predict_XGB))
mae_XGB = mean_absolute_error(Y_test, Y_predict_XGB)
r2_XGB = r2_score(Y_test, Y_predict_XGB)

print('\nXGB Regressor Error Metrics:')
print("Root Mean Squared Error:", rmse_XGB)
print("Mean Abosolute Error:", mae_XGB)
print("R2 Score :", r2_XGB)

# ================= Regression Algorithm 3 ( POLYNOMIAL REGRESSION ) ==================
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
pipe1 = make_pipeline(PolynomialFeatures(1), linear_model.LinearRegression())

pipe1.fit(XdataT_df, Ytrain_v)

r2_p1 = pipe1.score(XdataV_df, Ytest_v)

# Quadratic (Degree 2)
pipe2 = make_pipeline(PolynomialFeatures(2), linear_model.LinearRegression())

pipe2.fit(XdataT_df, Ytrain_v)

r2_p2 = pipe2.score(XdataV_df, Ytest_v)

print('\nPolynomial Regression Scores:')
print("Linear R2:", r2_p1)
print("Quadratic R2:", r2_p2)

# ================= Regression Algorithm 4 ( Decision Tree Regression ) ==================
Tree = DecisionTreeRegressor(max_depth=5, random_state=42)

#Training (Decision Tree)
Tree.fit(X_train, Y_train)

#Predicting (Decision Tree)
Y_predict_Tree = Tree.predict(X_test)

# Evaluate
rmse_Tree = np.sqrt(mean_squared_error(Y_test, Y_predict_Tree))
mae_Tree = mean_absolute_error(Y_test, Y_predict_Tree)
r2_Tree = r2_score(Y_test, Y_predict_Tree)

print('\nDecision Tree Error Metrics:')
print("Root Mean Squared Error:", rmse_Tree)
print("Mean Absolute Error:", mae_Tree)
print("R2 Score:", r2_Tree)

# ================= CLEAN DATA FOR PLOT ==================
# Combine driver + Gambusia
plot_df = pd.DataFrame({
    "driver": data_df['pbottom_Mud'],
    "Gambusia": data_df['Gambusia']
})
# Sort by driver for plotting
plot_df = plot_df.sort_values("driver")

X_plot = plot_df[['driver']]
Y_plot = plot_df[['Gambusia']]

# Fit clean models
pipe1.fit(X_plot, Y_plot)
pipe2.fit(X_plot, Y_plot)

Y_plot_p1 = pipe1.predict(X_plot)
Y_plot_p2 = pipe2.predict(X_plot)
# ======================== PLOT RESULTS ======================
plt.figure(num=1, figsize=(11.0, 5.5),dpi=200) # standard size for power point
plt.subplots_adjust(left=.05,right=0.95,top=0.9, bottom=0.10, wspace=0.15, hspace=0.4) 
plt.rcParams.update({'font.size': 8})
fontSizeTitle = 9               # the update doesn't impact title font size

# ===================== Algorithm 1 Plot (Gradient Boosting) ===================
plt.subplot(221)
plt.scatter(Y_test, Y_predict_GrdBoost, alpha=0.5, color = 'green')
plt.plot([Y_test.min(), Y_test.max()],
         [Y_test.min(), Y_test.max()],
         linestyle='--', color='red')
plt.xlabel("Actual Gambusia Abundance")
plt.ylabel("Predicted Gambusia Abundance")
plt.title("Gradient Boosting Regressor: Actual vs Predicted")

# ===================== Algorithm 2 Plot (XGBoost Regressor) ===================
plt.subplot(222)
plt.scatter(Y_test, Y_predict_XGB, alpha=0.5, color = 'purple')
plt.plot([Y_test.min(), Y_test.max()],
         [Y_test.min(), Y_test.max()],
         linestyle='--', color='red')
plt.xlabel("Actual Gambusia Abundance")
plt.ylabel("Predicted Gambusia Abundance")
plt.title("XGBoost Regressor: Actual vs Predicted")

# ===================== Algorithm 3 Plot (Polynomial Regression) ===================
plt.subplot(223)
plt.scatter(X_plot,Y_plot,color='magenta',alpha=0.7)
plt.plot(X_plot,Y_plot_p1,color='black',linewidth=3)
plt.plot(X_plot,Y_plot_p2,color='blue',linewidth=3)
plt.xlabel("Driver")
plt.ylabel("Gambusia Abundance")
plt.title("Polynomial Regression")
plt.legend(["Averaged Data","Linear Fit","Quadratic Fit"])

# ===================== Algorithm 4 Plot (Decision Tree Regression) ===================
plt.subplot(224)
plt.scatter(Y_test, Y_predict_Tree, alpha=0.5, color = 'orange')
plt.plot([Y_test.min(), Y_test.max()],
         [Y_test.min(), Y_test.max()],
         linestyle='--', color='red')
plt.xlabel("Actual Gambusia Abundance")
plt.ylabel("Predicted Gambusia Abundance")
plt.title("Decision Tree Regressor: Actual vs Predicted")

# ================= label plot edges ==================
plt.subplot(position=[0.0500,    0.94,    0.02500,    0.02500]) # U-left
plt.axis('off')
plt.text(0,.5, programMsg_c, fontsize=8)

plt.subplot(position=[0.550,    0.94,    0.02500,    0.02500]) # U-right
plt.axis('off')
plt.text(0,.5, authorName_c, fontsize=8)

plt.subplot(position=[0.0500,    0.0325,    0.02500,    0.02500]) # L-left
plt.axis('off')
plt.text(0,.5, fileName_c, fontsize=8)


plt.savefig(figName_c)

plt.close()