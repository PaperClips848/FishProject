# program		demo_umapPlot_sethEnvData_v1.py
# purpose	    Demonstrate UMAP plot with Seth environmental data
# usage         script
# notes         (1) This version uses StandardScaler
# date			4/17/2025
# programmer    GLF

import datetime          # used for getting the date
import os                # used for getting the basic file name (returns lower case)
import win32api          # used for getting fileName with correct case
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import umap
from sklearn import preprocessing    # Import label encoder  
import matplotlib.patheffects as PathEffects    # use for fancy plot text for example

# ============== COMMON INITIALIZATION =====================
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
programname_c = os.path.basename(__file__)                                          # case insensitive file name
programName_c = win32api.GetLongPathName(win32api.GetShortPathName(programname_c)) # case sensitive name

ix = str.find(programName_c,'.')

fileName_c = 'seth_environmentalData_march2023.csv'
programMsg_c = programName_c + ' (' + date_c + ')'
authorName_c = 'G.L. Fudge'

figName_c = programName_c[:ix]+'_fig.png'


# ================= get data ==================
sethEnvData_df = pd.read_csv((fileName_c))                 # load the sethEnv data into a pandas data frame
sethEnvData_num_df = sethEnvData_df.drop(['SiteN','State'], axis = 1)    # numerical data only
sethEnvData_labels = sethEnvData_df['State']
label_encoder = preprocessing.LabelEncoder()  
sethEnvData_labels_v = label_encoder.fit_transform(sethEnvData_labels) 
nLabels = len(np.unique(sethEnvData_labels_v))

sethEnvDataLabelsNames_cv = label_encoder.inverse_transform(range(0,nLabels))

# ==================== scale data ===================
sc_z = StandardScaler()

# Standardize features for training and testing sets
sethEnvData_num_df = sc_z.fit_transform(sethEnvData_num_df)

# ================ do UMAP ======================
# correlation metric -> more defined clusters than euclidean (default), hamming, chebyshev
# n_neighbors=15 (default) seems to yield more distinct clusters than range 5-20, although 5 OK also
# 5 OK with a larger number of epochs (1000-1500); 15 good with smaller # (500)
# also, 2, 3 generate handfull of tight clusters (maybe this is better?); 7 not bad either
# learn_rate = 0.5 seems to do better than 1.0 default
# default init seems better than pca
# min_dist default of 0.1 looks best
umapModel = umap.UMAP(n_components=2,metric='correlation',random_state=1,n_neighbors=7,n_epochs=500,learning_rate=0.5,min_dist=0.1,n_jobs = 1)
sethEnvData_umap = umapModel.fit_transform(sethEnvData_num_df)


print('type(isethEnvData_umap) = ',type(sethEnvData_umap))
print('sethEnvData_umap.shape = ',sethEnvData_umap.shape)


# ===================== PLOT RESULTS ===================
msg_parm_c = 'umapModel = umap(n_components=2'

plt.figure(num=1, figsize=(11.2, 5.2),dpi=200)        # control figure size and DPI of image
plt.rcParams.update({'font.size': 8})           # change default font size
plt.rcParams.update({'lines.markersize': 5})           # change default size of markers

# ============= Make the subplots look a little nicer ================= 
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.10, wspace=0.2, hspace=0.3)


for kc in range(nLabels):
    plt.scatter(sethEnvData_umap[sethEnvData_labels_v == kc, 0],sethEnvData_umap[sethEnvData_labels_v == kc,1])
    xtext, ytext = np.median(sethEnvData_umap[sethEnvData_labels_v == kc,:], axis=0)
    txt = plt.annotate(sethEnvDataLabelsNames_cv[kc],(xtext,ytext),fontsize=9)
    txt.set_path_effects([PathEffects.Stroke(linewidth=5, foreground='w'),PathEffects.Normal()])
plt.title('UMAP plot of sethEnv data')

# ================= label plot edges ==================
plt.subplot(position=[0.0500,    0.94,    0.02500,    0.02500]) # U-left
plt.axis('off')
plt.text(0,.5, programMsg_c, fontsize=8)

plt.subplot(position=[0.550,    0.94,    0.02500,    0.02500]) # U-right
plt.axis('off')
plt.text(0,.5, authorName_c, fontsize=8)

plt.subplot(position=[0.0500,    0.02,    0.02500,    0.02500]) # L-left
plt.axis('off')
plt.text(0,.5, fileName_c, fontsize=8)


plt.subplot(position=[0.3500,    0.02,    0.02500,    0.02500]) # L-right
plt.axis('off')
plt.text(0,.5, msg_parm_c, fontsize=8)


plt.savefig(figName_c)

