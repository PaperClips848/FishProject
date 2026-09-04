# program		beaty_sethData_v4p2.py
# purpose	    play with the visualization of fish data
# date			04/24/2024
# programmer    Michael M Beaty

### general notes
# 1)  v1     : made shapes off set from center based on size
# 2)  v2     : some clean up and clearer notes
# 3)  v3.0   : Removed "movement factor" and its dependencies. 
# 4)  v3.1   : Adjusted scaing mechanism
# 5)  v3.2   : Edited shapes to concentric rings and added more colors
# 6)  v3.3   : utilized "linestyle" to reduce color count
# 7)  v3.4   : color palette change. scaling tuning.
# 8)  v3.4.1 : replaced TSNE with UMAP. moved legend location
# 9)  v4     : implemented eco-region consideration into the scatter plots
#               added text labels for site numbers
# 10) v4.1   : added 3D scatter plots
# 11) v4.2   : added new UMAPs with genus considerations
###

### imports
import datetime          # used for getting the date
import os                # used for getting the basic file name (returns lower case)
import win32api          # used for getting fileName with correct case

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.impute import SimpleImputer
import umap

from matplotlib.markers import MarkerStyle


### Docstring Data
__all__ = ["dpi_var", "plot_threshold", "line_widths",
           "factor_power", "factor_multi", "factor_const",
           "x_offset", "y_offset", "rot", "x3_offset",
           "y3_offset", "z3_offset", "shape_list", 
           "color_list", "line_list", "s_point_shapes",
           "find_val",
           ]
__author__ = "Michael M Beaty"
__version__ = "4.2"


### init
print("start common initialization")
date_o = datetime.datetime.today()
date_c = date_o.strftime('%m/%d/%Y')
programname_c = os.path.basename(__file__)
programName_c = win32api.GetLongPathName(
                    win32api.GetShortPathName(programname_c))

ix = str.rfind(programName_c,'.')
# fileName_c = 'data.csv'
programMsg_c = programName_c + ' (' + date_c + ')'
authorName_c = 'Michael M Beaty'

figName_c = programName_c[:ix] + '_fig.png'

figure_count = 0
dpi_var = 200 # sets the effective dpi value for all figures. needs to be <270


g_to_plot = "Etheostoma"

# sets the minimum number of counts that a genus at a site needs 
# to have to be plotted
plot_threshold = 0.0


# sets the line widths of the circles
line_widths = 3


# area parameter for the dot marker for each site
site_dot_size = 128.0


# number for the power value for exponential scaling
factor_power = 0.8


# number being multiplied the data after the power
factor_multi = 280.0

# a constant value being summed with the data after power and multi
factor_const = -1000


### genus_data[site][genus] = ((genus_data[site][genus] ** factor_power) * factor_multi) + factor_const


# text offset for site numbers
x_offset = 0.04
y_offset = -0.04
rot = 15

x3_offset = 0.5
y3_offset = 0.5
z3_offset = 0

x3_offset_wf = 0.0
y3_offset_wf = 0.0
z3_offset_wf = 0.0



# list of colors, shapes, and line styles for plotting

shape_list = [MarkerStyle(marker = "o", 
                          fillstyle = "none"
                          )]

color_list = ["red", "green", "blue", "MediumTurquoise", "magenta", "goldenrod",
              "black", "DarkViolet", "Olive", "Brown",
              ]

line_list = ["solid", "dashed", "dashdot"]


s_point_shapes = [MarkerStyle(marker = "*", fillstyle = "full"),
                  MarkerStyle(marker = "s", fillstyle = "full"),
                  ]


eco_uniques_list = [[0, 3, 4, 24], [34, 36, 37, 38, 40, 42, 43, 44, 45]]

eco_reg_list = [[33, "a", "Northern Post Oak Savana", "TX"], # site 1
                [33, "a", "Northern Post Oak Savana", "TX"], # site 2
                [33, "a", "Northern Post Oak Savana", "TX"], # site 3
                [32, "a", "Northern Black Land Prairie", "TX"], # site 4
                [35, "c", "Pleistocene Fluvial Terraces", "TX"], # site 5
                [35, "c", "Pleistocene Fluvial Terraces", "TX"], # site 6
                [35, "c", "Pleistocene Fluvial Terraces", "TX"], # site 7
                [33, "a", "Northern Post Oak Savana", "TX"], # site 8
                [33, "a", "Northern Post Oak Savana", "TX"], # site 9
                [33, "a", "Northern Post Oak Savana", "TX"], # site 10
                [33, "a", "Northern Post Oak Savana", "TX"], # site 11
                [33, "a", "Northern Post Oak Savana", "TX"], # site 12
                [33, "a", "Northern Post Oak Savana", "TX"], # site 13
                [32, "a", "Northern Black Land Prairie", "TX"], # site 14
                [32, "a", "Northern Black Land Prairie", "TX"], # site 15
                [32, "a", "Northern Black Land Prairie", "TX"], # site 16
                [33, "a", "Northern Post Oak Savana", "TX"], # site 17
                [33, "a", "Northern Post Oak Savana", "TX"], # site 18
                [33, "a", "Northern Post Oak Savana", "TX"], # site 19
                [33, "a", "Northern Post Oak Savana", "TX"], # site 20
                [32, "a", "Northern Black Land Prairie", "TX"], # site 21
                [33, "a", "Northern Post Oak Savana", "TX"], # site 22
                [33, "a", "Northern Post Oak Savana", "TX"], # site 23
                [35, "c", "Pleistocene Fluvial Terraces", "TX"], # site 24
                [35, "g", "Red River Bottomlands", "TX"], # site 25
                [35, "c", "Pleistocene Fluvial Terraces", "TX"], # site 26
                [35, "c", "Pleistocene Fluvial Terraces", "TX"], # site 27
                [35, "g", "Red River Bottomlands", "TX"], # site 28
                [33, "a", "Northern Post Oak Savana", "TX"], # site 29
                [35, "g", "Red River Bottomlands", "TX"], # site 30
                [35, "g", "Red River Bottomlands", "TX"], # site 31
                [32, "a", "Northern Black Land Prairie", "TX"], # site 32
                [32, "a", "Northern Black Land Prairie", "TX"], # site 33
                [32, "a", "Northern Black Land Prairie", "TX"], # site 34
                [29, "g", "Arbuckle Uplift", "OK"], # site 35
                [29, "g", "Arbuckle Uplift", "OK"], # site 36
                [29, "b", "Eastern Cross Timbers", "OK"], # site 37
                [36, "a", "Athens Plateau", "OK"], # site 38
                [36, "b", "Central Mountain Ranges", "OK"], # site 39
                [36, "b", "Central Mountain Ranges", "OK"], # site 40
                [36, "f", "Western Ouachita Valleys", "OK"], # site 41
                [36, "f", "Western Ouachita Valleys", "OK"], # site 42
                [35, "h", "Blackland Prairie", "OK"], # site 43
                [37, "e", "Lower Canadian Hills", "OK"], # site 44
                [35, "d", "Fourche Mountains", "OK"], # site 45
                [36, "e", "Western Ouachitas", "OK"], # site 46
                ]


# https://umap-learn.readthedocs.io/en/latest/parameters.html
dim_red1 = umap.UMAP(n_neighbors = 2,
                     n_components = 2,
                     min_dist = 0.9,
                     metric = "correlation",
                     learning_rate = 0.01,
                     init = "pca",
                     low_memory = False,
                     random_state = 24,
                     # transform_seed = 42,
                     n_jobs = 1
                     )

dim_red2 = umap.UMAP(n_neighbors = 7,
                     n_components = 2,
                     min_dist = 0.1,
                     metric = "correlation",
                     learning_rate = 0.01,
                     init = "pca",
                     low_memory = False,
                     random_state = 24,
                     # transform_seed = 42,
                     n_jobs = 1
                     )

dim_red3 = umap.UMAP(n_neighbors = 7,
                     n_components = 2,
                     min_dist = 0.35,
                     metric = "correlation",
                     learning_rate = 0.01,
                     init = "pca",
                     low_memory = False,
                     random_state = 24,
                     # transform_seed = 42,
                     n_jobs = 1
                     )

dim_red4 = umap.UMAP(n_neighbors = 2,
                     n_components = 2,
                     min_dist = 0.1,
                     metric = "correlation",
                     learning_rate = 0.01,
                     init = "pca",
                     low_memory = False,
                     random_state = 24,
                     # transform_seed = 42,
                     n_jobs = 1
                     )

dim_red5 = umap.UMAP(n_neighbors = 7,
                     n_components = 3,
                     min_dist = 0.1,
                     metric = "correlation",
                     learning_rate = 0.01,
                     init = "pca",
                     low_memory = False,
                     random_state = 24,
                     # transform_seed = 42,
                     n_jobs = 1
                     )

dim_red6 = umap.UMAP(n_neighbors = 7,
                     n_components = 2,
                     min_dist = 0.1,
                     metric = "correlation",
                     learning_rate = 0.01,
                     init = "pca",
                     low_memory = False,
                     random_state = 24,
                     # transform_seed = 42,
                     n_jobs = 1
                     )

dim_red7 = umap.UMAP(n_neighbors = 7,
                     n_components = 3,
                     min_dist = 0.1,
                     metric = "correlation",
                     learning_rate = 0.01,
                     init = "pca",
                     low_memory = False,
                     random_state = 24,
                     # transform_seed = 42,
                     n_jobs = 1
                     )



imputer_site = SimpleImputer(missing_values = np.nan,
                             strategy = "mean",
                             copy = False
                             )

imputer_fish = SimpleImputer(missing_values = np.nan,
                             strategy = "median",
                             copy = False
                             )


print("end common initialization\n")


### custom functions definitions
print("start custom functions definitions")

### open_new_figure(dpi_val = dpi_var, 
###                 figure_size = (36,24), 
###                 figure_title_font_size = 36,
###                 default_font_size = 24)
# open_new_figure() is a function that initalizes a new figure. It is
# recomended to call close_current_figure() before calling 
# open_new_figure() in order to plot and save the previous figure. 
###
def open_new_figure(dpi_val = dpi_var, 
                    figure_size = (36,24), 
                    figure_title_font_size = 36,
                    default_font_size = 24
                    ):
    global figure_count
    figure_count += 1
    
    f = plt.figure(figure_count, # build the current figure
                   dpi = dpi_val, 
                   figsize = figure_size
                   )
    
    f.suptitle('Figure ' + str(figure_count), # add figure title
               fontsize = figure_title_font_size
               )
    
    plt.rcParams.update({'font.size': default_font_size})
    
    return f


### close_current_figure(corner_font_size = 24)
# close_current_figure() adds EE-497 common text blocks to the corneres 
# of the overall figure before plottting and saving the figure as a png.
###
def close_current_figure(corner_font_size = 24,
                         file_name = ""
                         ):
    plt.figure(figure_count)
    plt.subplot(position=[0.0500,    0.94,    0.02500,    0.02500]) # U-left
    plt.axis('off')
    plt.text(0,.5, programMsg_c, fontsize=corner_font_size)

    plt.subplot(position=[0.9,    0.94,    0.02500,    0.02500]) # U-right
    plt.axis('off')
    plt.text(0,.5, authorName_c, fontsize=corner_font_size)

    plt.subplot(position=[0.0500,    0.02,    0.02500,    0.02500]) # L-left
    plt.axis('off')
    plt.text(0,.5, file_name, fontsize=corner_font_size)
    
    
    plt.savefig(programName_c[:ix] + '_fig' + str(figure_count) + '.png')
    plt.show()


### find_val(arr = [], val = None, count = 1))
# Linearly finds the address of the Xth instance of the given value   
# in the given array, where X == count. 
# 
# If the value could not be found returns -1. 
###
def find_val(arr = [], val = None, count = 1) : 
    t_count = 1
    for index in range(len(arr)) : 
        if (arr[index] == val and t_count == count) : 
            del t_count
            return index
        elif arr[index] == val : 
            t_count += 1
    
    del t_count
    return -1



print("end custom functions definitions\n")

### main
print("start main")

site_data = pd.read_csv("seth_environmentalData_march2023.csv")
genus_data = pd.read_csv("seth_genusCountData_feb2024.csv")

for index in range(len(site_data.to_numpy())) : 
    if site_data.at[index, "State"] == "TX" : 
        site_data.at[index, "State"] = 0
    else :
        site_data.at[index, "State"] = 1

for index in range(len(genus_data.to_numpy())) : 
    if genus_data.at[index, "State"] == "TX" : 
        genus_data.at[index, "State"] = 0
    else :
        genus_data.at[index, "State"] = 1


genus_labels = genus_data.drop(["SiteN", "State"], axis = 1).columns
genus_data = np.transpose(genus_data.drop(["SiteN", "State"], axis = 1).to_numpy())



print("\tstart impute")
imputer_site.fit_transform(site_data)
imputer_fish.fit_transform(genus_data)
print("\tend impute\n")


csf_data = pd.DataFrame(site_data)

csf_data.insert(len(site_data.columns), 
                g_to_plot, 
                genus_data[find_val(genus_labels, g_to_plot)],
                )


print("\tstart UMAP")

print("\n\t\tUMAP 1")
site_2D = np.transpose(dim_red1.fit_transform(site_data))

print("\t\tUMAP 2")
site_2D_2 = np.transpose(dim_red2.fit_transform(site_data))

print("\t\tUMAP 3")
site_2D_3 = np.transpose(dim_red3.fit_transform(site_data))

print("\t\tUMAP 4")
site_2D_4 = np.transpose(dim_red4.fit_transform(site_data))

print("\t\tUMAP 5")
site_3D = np.transpose(dim_red5.fit_transform(site_data))

print("\t\tUMAP 6")
site_wf_2D = np.transpose(dim_red6.fit_transform(csf_data))

print("\t\tUMAP 7")
site_wf_3D = np.transpose(dim_red7.fit_transform(csf_data))

print("\n\tend UMAP\n")



print("\tstart data manipulation")
temp = []

print("\t\tconversion to float datatype for stability reasons\n")
for a in range(len(genus_data)) : 
    t = []
    for b in range(len(genus_data[a])) : 
        t.append(float(genus_data[a][b])*2)
    temp.append(t)

genus_data = temp
del temp
del t



sorted_genus = []
site_order_index = []

print("\t\tmake a list with the site where each genus has the highest counts\n")
for site in range(len(genus_data)) : 
    sorted_genus.append(sorted(genus_data[site], reverse = True))
    
    temp = []
    counts = 1
    for genus in range(len(sorted_genus[site])) :
        if sorted_genus[site][genus] > plot_threshold : 
            if (genus != 0 and
                sorted_genus[site][genus] == sorted_genus[site][genus - 1]
                ) : 
                counts += 1
                temp.append(find_val(genus_data[site], 
                                     sorted_genus[site][genus],
                                     count = counts
                                     ))
            else : 
                counts = 1
                temp.append(find_val(genus_data[site], 
                                 sorted_genus[site][genus],
                                 count = counts
                                 ))
        else : 
            temp.append(-1)
    
    site_order_index.append(temp)



genus_data = np.transpose(genus_data)
site_order_index = np.transpose(site_order_index)

sorted_genus = []
genus_order_index = []


print("\t\tmake a list with the genus that has the most counts at each site\n")
for site in range(len(genus_data)) : 
    sorted_genus.append(sorted(genus_data[site], reverse = True))
    
    temp = []
    counts = 1
    for genus in range(len(sorted_genus[site])) :
        if sorted_genus[site][genus] > plot_threshold : 
            if (genus != 0 and
                sorted_genus[site][genus] == sorted_genus[site][genus - 1]
                ) : 
                counts += 1
                temp.append(find_val(genus_data[site], 
                                     sorted_genus[site][genus],
                                     count = counts
                                     ))
            else : 
                counts = 1
                temp.append(find_val(genus_data[site], 
                                 sorted_genus[site][genus],
                                 count = counts
                                 ))
        else : 
            temp.append(-1)
    
    genus_order_index.append(temp)



print("\t\tfind the max value for potential later size scaling and scale all values\n")
max_count = -1
for site in range(len(genus_data)) : 
    for genus in range(len(genus_data[site])) : 
        if (genus_data[site][genus] > 0 and
            genus_data[site][genus] > plot_threshold
            ) : 
            genus_data[site][genus] = ((((genus_data[site][genus] 
                                          ** factor_power)
                                          * factor_multi)
                                          + factor_const)
                                        )
            
            if genus_data[site][genus] > max_count :
                max_count = genus_data[site][genus]


print("\tend data manipulation\n")


print("end main\n")

### plots
print("start plots")

#'''
open_new_figure()
# fig1

plt.subplot(111).set_title("UMAP Scatter Plot\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


enum_style = []
current_style = 0

print("\tenumerate combinations of colors and line styles\n")
for genus in range(len(genus_labels)) : 
    if genus % len(color_list) == 0: 
        current_style += 100
    
    enum_style.append((genus % len(color_list)) + current_style)
    

print("\tplot a point for each genus with its colored marker and label, " + 
      "\n\tand hide the points in the plot. used for legend()\n"
      )
for index in range(len(site_order_index[0])) : 
    current_genus = index
    current_site = site_order_index[0][current_genus]
    
    plt.scatter(x = site_2D[0][current_site],
                y = site_2D[1][current_site],
                s = 420,
                c = color_list[enum_style[current_genus] % 100],
                marker = shape_list[0],
                label = genus_labels[current_genus],
                # edgecolors = "black",
                linewidths = 2,
                linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                )
    
    plt.scatter(x = site_2D[0][current_site],
                y = site_2D[1][current_site],
                s = 420*2,
                c = "white",
                marker = "o",
                )




print("\tplot the center of each site location under the genus circles\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_2D[0][eco_uniques_list[state][u]],
                    y = site_2D[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_2D[0][eco_uniques_list[state][u]],
                    y = site_2D[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_2D[0][site],
                            y = site_2D[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                break


del state
del u

print("\tplot all genus counts at each site and scale and offset each count value\n")
for current_site in range(len(genus_data)) : 
    for genus_index in range(len(genus_order_index[current_site])) : 
        current_genus = genus_order_index[current_site][genus_index]
        if current_genus > -1 : 
            plt.scatter(x = site_2D[0][current_site],
                        y = site_2D[1][current_site],
                        s = (genus_data[current_site][current_genus]),
                        c = color_list[enum_style[current_genus] % 100],
                        marker = shape_list[0],
                        # label = genus_labels[current_genus],
                        # edgecolors = "black",
                        linewidths = line_widths,
                        linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                        )
            
    plt.text(x = site_2D[0][current_site] + x_offset,
             y = site_2D[1][current_site] + y_offset,
             s = "#" + str(current_site + 1),# + "\n" + 
                 # "{:.2f}".format(site_data["Lat"][current_site]) + ", " + 
                 # "{:.2f}".format(site_data["Long"][current_site]),
             backgroundcolor = "white",
             fontsize = 12,
             rotation = rot
             )
                


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "upper right", 
           bbox_to_anchor = (1.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 3,
           fontsize = 20
           )

print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )



open_new_figure()
# fig2

plt.subplot(111).set_title("UMAP Scatter Plot\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


print("\tRedo the site points with differnt UMAP values. no genera for cleaner plot\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_2D_2[0][eco_uniques_list[state][u]],
                    y = site_2D_2[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_2D_2[0][eco_uniques_list[state][u]],
                    y = site_2D_2[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_2D_2[0][site],
                            y = site_2D_2[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                
                plt.text(x = site_2D_2[0][site] + x_offset,
                         y = site_2D_2[1][site] + y_offset,
                         s = "#" + str(site + 1),# + "\n" + 
                             # "{:.2f}".format(site_data["Lat"][site]) + ", " + 
                             # "{:.2f}".format(site_data["Long"][site]),
                         backgroundcolor = "white",
                         fontsize = 12,
                         rotation = rot
                         )
                
                break


del state
del u


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "upper right", 
           bbox_to_anchor = (1.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 2,
           fontsize = 20
           )


print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )




open_new_figure()
# fig3

print("\tRedo the site points with differnt UMAP values with genera\n")


plt.subplot(111).set_title("UMAP Scatter Plot\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


enum_style = []
current_style = 0

print("\tenumerate combinations of colors and line styles\n")
for genus in range(len(genus_labels)) : 
    if genus % len(color_list) == 0: 
        current_style += 100
    
    enum_style.append((genus % len(color_list)) + current_style)
    

print("\tplot a point for each genus with its colored marker and label, " + 
      "\n\tand hide the points in the plot. used for legend()\n"
      )
for index in range(len(site_order_index[0])) : 
    current_genus = index
    current_site = site_order_index[0][current_genus]
    
    plt.scatter(x = site_2D_2[0][current_site],
                y = site_2D_2[1][current_site],
                s = 420,
                c = color_list[enum_style[current_genus] % 100],
                marker = shape_list[0],
                label = genus_labels[current_genus],
                # edgecolors = "black",
                linewidths = 2,
                linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                )
    
    plt.scatter(x = site_2D_2[0][current_site],
                y = site_2D_2[1][current_site],
                s = 420*2,
                c = "white",
                marker = "o",
                )




print("\tplot the center of each site location under the genus circles\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_2D_2[0][eco_uniques_list[state][u]],
                    y = site_2D_2[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_2D_2[0][eco_uniques_list[state][u]],
                    y = site_2D_2[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D_2[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_2D_2[0][site],
                            y = site_2D_2[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                break


del state
del u

print("\tplot all genus counts at each site and scale and offset each count value\n")
for current_site in range(len(genus_data)) : 
    for genus_index in range(len(genus_order_index[current_site])) : 
        current_genus = genus_order_index[current_site][genus_index]
        if current_genus > -1 : 
            plt.scatter(x = site_2D_2[0][current_site],
                        y = site_2D_2[1][current_site],
                        s = (genus_data[current_site][current_genus]),
                        c = color_list[enum_style[current_genus] % 100],
                        marker = shape_list[0],
                        # label = genus_labels[current_genus],
                        # edgecolors = "black",
                        linewidths = line_widths,
                        linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                        )
            
    plt.text(x = site_2D_2[0][current_site] + x_offset,
             y = site_2D_2[1][current_site] + y_offset,
             s = "#" + str(current_site + 1),# + "\n" + 
                 # "{:.2f}".format(site_data["Lat"][current_site]) + ", " + 
                 # "{:.2f}".format(site_data["Long"][current_site]),
             backgroundcolor = "white",
             fontsize = 12,
             rotation = rot
             )
                


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "upper right", 
           bbox_to_anchor = (1.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 3,
           fontsize = 20
           )

print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )




open_new_figure()
# fig4

plt.subplot(111).set_title("UMAP Scatter Plot\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


enum_style = []
current_style = 0

print("\tenumerate combinations of colors and line styles\n")
for genus in range(len(genus_labels)) : 
    if genus % len(color_list) == 0: 
        current_style += 100
    
    enum_style.append((genus % len(color_list)) + current_style)
    

print("\tplot a point for each genus with its colored marker and label, " + 
      "\n\tand hide the points in the plot. used for legend()\n"
      )
for index in range(len(site_order_index[0])) : 
    current_genus = index
    current_site = site_order_index[0][current_genus]
    
    plt.scatter(x = site_2D_3[0][current_site],
                y = site_2D_3[1][current_site],
                s = 420,
                c = color_list[enum_style[current_genus] % 100],
                marker = shape_list[0],
                label = genus_labels[current_genus],
                # edgecolors = "black",
                linewidths = 2,
                linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                )
    
    plt.scatter(x = site_2D_3[0][current_site],
                y = site_2D_3[1][current_site],
                s = 420*2,
                c = "white",
                marker = "o",
                )




print("\tplot the center of each site location under the genus circles\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_2D_3[0][eco_uniques_list[state][u]],
                    y = site_2D_3[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_2D_3[0][eco_uniques_list[state][u]],
                    y = site_2D_3[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D_3[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_2D_3[0][site],
                            y = site_2D_3[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                break


del state
del u

print("\tplot all genus counts at each site and scale and offset each count value\n")
for current_site in range(len(genus_data)) : 
    for genus_index in range(len(genus_order_index[current_site])) : 
        current_genus = genus_order_index[current_site][genus_index]
        if current_genus > -1 : 
            plt.scatter(x = site_2D_3[0][current_site],
                        y = site_2D_3[1][current_site],
                        s = (genus_data[current_site][current_genus]),
                        c = color_list[enum_style[current_genus] % 100],
                        marker = shape_list[0],
                        # label = genus_labels[current_genus],
                        # edgecolors = "black",
                        linewidths = line_widths,
                        linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                        )
            
    plt.text(x = site_2D_3[0][current_site] + x_offset,
             y = site_2D_3[1][current_site] + y_offset,
             s = "#" + str(current_site + 1),# + "\n" + 
                 # "{:.2f}".format(site_data["Lat"][current_site]) + ", " + 
                 # "{:.2f}".format(site_data["Long"][current_site]),
             backgroundcolor = "white",
             fontsize = 12,
             rotation = rot
             )
                


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "upper right", 
           bbox_to_anchor = (1.05, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 3,
           fontsize = 20
           )

print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )






open_new_figure()
# fig5

plt.subplot(111).set_title("UMAP Scatter Plot\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


print("\tRedo the site points with differnt UMAP values. no genera for cleaner plot\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_2D_4[0][eco_uniques_list[state][u]],
                    y = site_2D_4[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_2D_4[0][eco_uniques_list[state][u]],
                    y = site_2D_4[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_2D_4[0][site],
                            y = site_2D_4[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                
                plt.text(x = site_2D_4[0][site] + x_offset,
                         y = site_2D_4[1][site] + y_offset,
                         s = "#" + str(site + 1),# + "\n" + 
                             # "{:.2f}".format(site_data["Lat"][site]) + ", " + 
                             # "{:.2f}".format(site_data["Long"][site]),
                         backgroundcolor = "white",
                         fontsize = 12,
                         rotation = rot
                         )
                
                break


del state
del u


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "upper right", 
           bbox_to_anchor = (1.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 2,
           fontsize = 20
           )


print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )




open_new_figure()
# fig6

plt.subplot(111).set_title("UMAP Scatter Plot\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


enum_style = []
current_style = 0

print("\tenumerate combinations of colors and line styles\n")
for genus in range(len(genus_labels)) : 
    if genus % len(color_list) == 0: 
        current_style += 100
    
    enum_style.append((genus % len(color_list)) + current_style)
    

print("\tplot a point for each genus with its colored marker and label, " + 
      "\n\tand hide the points in the plot. used for legend()\n"
      )
for index in range(len(site_order_index[0])) : 
    current_genus = index
    current_site = site_order_index[0][current_genus]
    
    plt.scatter(x = site_2D_4[0][current_site],
                y = site_2D_4[1][current_site],
                s = 420,
                c = color_list[enum_style[current_genus] % 100],
                marker = shape_list[0],
                label = genus_labels[current_genus],
                # edgecolors = "black",
                linewidths = 2,
                linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                )
    
    plt.scatter(x = site_2D_4[0][current_site],
                y = site_2D_4[1][current_site],
                s = 420*2,
                c = "white",
                marker = "o",
                )




print("\tplot the center of each site location under the genus circles\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_2D_4[0][eco_uniques_list[state][u]],
                    y = site_2D_4[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_2D_4[0][eco_uniques_list[state][u]],
                    y = site_2D_4[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D_4[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_2D_4[0][site],
                            y = site_2D_4[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                break


del state
del u

print("\tplot all genus counts at each site and scale and offset each count value\n")
for current_site in range(len(genus_data)) : 
    for genus_index in range(len(genus_order_index[current_site])) : 
        current_genus = genus_order_index[current_site][genus_index]
        if current_genus > -1 : 
            plt.scatter(x = site_2D_4[0][current_site],
                        y = site_2D_4[1][current_site],
                        s = (genus_data[current_site][current_genus]),
                        c = color_list[enum_style[current_genus] % 100],
                        marker = shape_list[0],
                        # label = genus_labels[current_genus],
                        # edgecolors = "black",
                        linewidths = line_widths,
                        linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                        )
            
    plt.text(x = site_2D_4[0][current_site] + x_offset,
             y = site_2D_4[1][current_site] + y_offset,
             s = "#" + str(current_site + 1),# + "\n" + 
                 # "{:.2f}".format(site_data["Lat"][current_site]) + ", " + 
                 # "{:.2f}".format(site_data["Long"][current_site]),
             backgroundcolor = "white",
             fontsize = 12,
             rotation = rot
             )
                


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "upper right", 
           bbox_to_anchor = (1.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 3,
           fontsize = 20
           )

print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )
#'''


fig = open_new_figure()
# fig7

focal_len = 0.15

axs = fig.add_subplot(projection='3d')

axs.set_proj_type('persp', focal_length = focal_len)

axs.set_title("UMAP Scatter Plot\n" + 
              "Threshold = " + str(plot_threshold)
              )

print("\t3D UMAP Plot\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        axs.scatter(xs = site_3D[0][eco_uniques_list[state][u]],
                    ys = site_3D[1][eco_uniques_list[state][u]],
                    zs = site_3D[2][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        axs.scatter(xs = site_3D[0][eco_uniques_list[state][u]],
                    ys = site_3D[1][eco_uniques_list[state][u]],
                    zs = site_3D[2][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                axs.scatter(xs = site_3D[0][site],
                            ys = site_3D[1][site],
                            zs = site_3D[2][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                '''
                axs.text(x = site_3D[0][site] + x3_offset,
                         y = site_3D[1][site] + y3_offset,
                         z = site_3D[2][site] + z3_offset,
                         s = "#" + str(site + 1) + "\n" + 
                             "{:.2f}".format(site_data["Lat"][site]) + ",\n" + 
                             "{:.2f}".format(site_data["Long"][site]),
                         backgroundcolor = "white",
                         fontsize = 12,
                         # rotation = rot3
                         )
                '''
                break


del state
del u


axs.set_xlabel(xlabel = "UMAP Dimension 0", labelpad = 8.0)
axs.set_ylabel(ylabel = "UMAP Dimension 1", labelpad = 8.0)
axs.set_zlabel(zlabel = "UMAP Dimension 2", labelpad = 8.0)

plt.legend(loc = "best", 
           # bbox_to_anchor = (2.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 2,
           fontsize = 20
           )


print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )




fig = open_new_figure()
# fig8

# axs = fig.add_subplot(projection='3d')

plt.gcf().add_subplot(projection='3d').set_proj_type('persp', focal_length = focal_len)

plt.gca().set_title("UMAP Scatter Plot\n" + 
              "Threshold = " + str(plot_threshold)
              )

print("\t3D UMAP Plot\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.gca().scatter(xs = site_3D[0][eco_uniques_list[state][u]],
                          ys = site_3D[1][eco_uniques_list[state][u]],
                          zs = site_3D[2][eco_uniques_list[state][u]],
                          s = 420,
                          c = color_list[u],
                          marker = s_point_shapes[state],
                          label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                          eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                          eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                          eco_reg_list[eco_uniques_list[state][u]][3]
                                          ),
                          edgecolors = "face",
                          )
        
        plt.gca().scatter(xs = site_3D[0][eco_uniques_list[state][u]],
                          ys = site_3D[1][eco_uniques_list[state][u]],
                          zs = site_3D[2][eco_uniques_list[state][u]],
                          s = 420*2,
                          c = "white",
                          marker = "o",
                          )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.gca().scatter(xs = site_3D[0][site],
                                  ys = site_3D[1][site],
                                  zs = site_3D[2][site],
                                  s = 180,
                                  c = color_list[u],
                                  marker = s_point_shapes[state],
                                  edgecolors = "face",
                                  )
                
                plt.gca().text(x = site_3D[0][site] + x3_offset,
                               y = site_3D[1][site] + y3_offset,
                               z = site_3D[2][site] + z3_offset,
                               s = "#" + str(site + 1),# + "\n" + 
                                   # "{:.2f}".format(site_data["Lat"][site]) + ",\n" + 
                                   # "{:.2f}".format(site_data["Long"][site]),
                               backgroundcolor = "white",
                               fontsize = 12,
                               )
                
                break


del state
del u


plt.gca().set_xlabel(xlabel = "UMAP Dimension 0", labelpad = 8.0)
plt.gca().set_ylabel(ylabel = "UMAP Dimension 1", labelpad = 8.0)
plt.gca().set_zlabel(zlabel = "UMAP Dimension 2", labelpad = 8.0)

plt.legend(loc = "best", 
           # bbox_to_anchor = (2.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 2,
           fontsize = 20
           )


print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )


fig = open_new_figure()
# fig9

focal_len = 0.15

axs = fig.add_subplot(projection='3d')

axs.set_proj_type('persp', focal_length = focal_len)

axs.set_title("UMAP Scatter Plot with Fish\n" + 
              "Threshold = " + str(plot_threshold)
              )

print("\t3D UMAP Plot\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        axs.scatter(xs = site_wf_3D[0][eco_uniques_list[state][u]],
                    ys = site_wf_3D[1][eco_uniques_list[state][u]],
                    zs = site_wf_3D[2][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        axs.scatter(xs = site_wf_3D[0][eco_uniques_list[state][u]],
                    ys = site_wf_3D[1][eco_uniques_list[state][u]],
                    zs = site_wf_3D[2][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                axs.scatter(xs = site_wf_3D[0][site],
                            ys = site_wf_3D[1][site],
                            zs = site_wf_3D[2][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                #'''
                axs.text(x = site_wf_3D[0][site] + x3_offset_wf,
                         y = site_wf_3D[1][site] + y3_offset_wf,
                         z = site_wf_3D[2][site] + z3_offset_wf,
                         s = "#" + str(site + 1),# + "\n" + 
                             # "{:.2f}".format(site_data["Lat"][site]) + ",\n" + 
                             # "{:.2f}".format(site_data["Long"][site]),
                         backgroundcolor = "white",
                         fontsize = 12,
                         # rotation = rot3
                         )
                #'''
                break


del state
del u


axs.set_xlabel(xlabel = "UMAP Dimension 0", labelpad = 8.0)
axs.set_ylabel(ylabel = "UMAP Dimension 1", labelpad = 8.0)
axs.set_zlabel(zlabel = "UMAP Dimension 2", labelpad = 8.0)

plt.legend(loc = "upper left", 
           bbox_to_anchor = (-0.4, 0.9),
           borderpad = 0.5,
           title = "Legend",
           ncols = 2,
           fontsize = 20
           )


print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )



fig = open_new_figure()
# fig10

focal_len = 0.15

axs = fig.add_subplot(projection='3d')

axs.set_proj_type('persp', focal_length = focal_len)

axs.set_title("UMAP Scatter Plot with Fish\n" + 
              "Threshold = " + str(plot_threshold)
              )

print("\t3D UMAP Plot\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        axs.scatter(xs = site_wf_3D[0][eco_uniques_list[state][u]],
                    ys = site_wf_3D[1][eco_uniques_list[state][u]],
                    zs = site_wf_3D[2][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        axs.scatter(xs = site_wf_3D[0][eco_uniques_list[state][u]],
                    ys = site_wf_3D[1][eco_uniques_list[state][u]],
                    zs = site_wf_3D[2][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                axs.scatter(xs = site_wf_3D[0][site],
                            ys = site_wf_3D[1][site],
                            zs = site_wf_3D[2][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                '''
                axs.text(x = site_wf_3D[0][site] + x3_offset,
                         y = site_wf_3D[1][site] + y3_offset,
                         z = site_wf_3D[2][site] + z3_offset,
                         s = "#" + str(site + 1) + "\n" + 
                             "{:.2f}".format(site_data["Lat"][site]) + ",\n" + 
                             "{:.2f}".format(site_data["Long"][site]),
                         backgroundcolor = "white",
                         fontsize = 12,
                         # rotation = rot3
                         )
                '''
                break


del state
del u


axs.set_xlabel(xlabel = "UMAP Dimension 0", labelpad = 8.0)
axs.set_ylabel(ylabel = "UMAP Dimension 1", labelpad = 8.0)
axs.set_zlabel(zlabel = "UMAP Dimension 2", labelpad = 8.0)

plt.legend(loc = "upper left", 
           bbox_to_anchor = (-0.4, 0.9),
           borderpad = 0.5,
           title = "Legend",
           ncols = 2,
           fontsize = 20
           )


print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )



open_new_figure()
# fig11

plt.subplot(111).set_title("UMAP Scatter Plot with Fish\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


print("\tRedo the site points with differnt UMAP values. no genera for cleaner plot\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_wf_2D[0][eco_uniques_list[state][u]],
                    y = site_wf_2D[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_wf_2D[0][eco_uniques_list[state][u]],
                    y = site_wf_2D[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_wf_2D[0][site],
                            y = site_wf_2D[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                
                plt.text(x = site_wf_2D[0][site] + x_offset,
                         y = site_wf_2D[1][site] + y_offset,
                         s = "#" + str(site + 1),# + "\n" + 
                             # "{:.2f}".format(site_data["Lat"][site]) + ", " + 
                             # "{:.2f}".format(site_data["Long"][site]),
                         backgroundcolor = "white",
                         fontsize = 12,
                         rotation = rot
                         )
                
                break


del state
del u


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "upper right", 
           bbox_to_anchor = (1.0, 1.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 2,
           fontsize = 20
           )


print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )




open_new_figure()
# fig12

print("\tRedo the site points with differnt UMAP values with genera\n")


plt.subplot(111).set_title("UMAP Scatter Plot with Fish\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


enum_style = []
current_style = 0

print("\tenumerate combinations of colors and line styles\n")
for genus in range(len(genus_labels)) : 
    if genus % len(color_list) == 0: 
        current_style += 100
    
    enum_style.append((genus % len(color_list)) + current_style)
    

print("\tplot a point for each genus with its colored marker and label, " + 
      "\n\tand hide the points in the plot. used for legend()\n"
      )
for index in range(len(site_order_index[0])) : 
    current_genus = index
    current_site = site_order_index[0][current_genus]
    
    plt.scatter(x = site_wf_2D[0][current_site],
                y = site_wf_2D[1][current_site],
                s = 420,
                c = color_list[enum_style[current_genus] % 100],
                marker = shape_list[0],
                label = genus_labels[current_genus],
                # edgecolors = "black",
                linewidths = 2,
                linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                )
    
    plt.scatter(x = site_wf_2D[0][current_site],
                y = site_wf_2D[1][current_site],
                s = 420*2,
                c = "white",
                marker = "o",
                )




print("\tplot the center of each site location under the genus circles\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_wf_2D[0][eco_uniques_list[state][u]],
                    y = site_wf_2D[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_wf_2D[0][eco_uniques_list[state][u]],
                    y = site_wf_2D[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D_2[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_wf_2D[0][site],
                            y = site_wf_2D[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                break


del state
del u

print("\tplot all genus counts at each site and scale and offset each count value\n")
for current_site in range(len(genus_data)) : 
    for genus_index in range(len(genus_order_index[current_site])) : 
        current_genus = genus_order_index[current_site][genus_index]
        if current_genus > -1 : 
            plt.scatter(x = site_wf_2D[0][current_site],
                        y = site_wf_2D[1][current_site],
                        s = (genus_data[current_site][current_genus]),
                        c = color_list[enum_style[current_genus] % 100],
                        marker = shape_list[0],
                        # label = genus_labels[current_genus],
                        # edgecolors = "black",
                        linewidths = line_widths,
                        linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                        )
            
    plt.text(x = site_wf_2D[0][current_site] + x_offset,
             y = site_wf_2D[1][current_site] + y_offset,
             s = "#" + str(current_site + 1), # + "\n" + 
                 # "{:.2f}".format(site_data["Lat"][current_site]) + ", " + 
                 # "{:.2f}".format(site_data["Long"][current_site]),
             backgroundcolor = "white",
             fontsize = 12,
             rotation = rot
             )
                


plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "lower right", 
           bbox_to_anchor = (1.0, 0.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 3,
           fontsize = 20
           )

print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )



open_new_figure()
# fig13

print("\tRedo the site points with differnt UMAP values with genera\n")


plt.subplot(111).set_title("UMAP Scatter Plot with Fish\n" + 
                           "Threshold = " + str(plot_threshold)
                           )


enum_style = []
current_style = 0

print("\tenumerate combinations of colors and line styles\n")
for genus in range(len(genus_labels)) : 
    if genus % len(color_list) == 0: 
        current_style += 100
    
    enum_style.append((genus % len(color_list)) + current_style)
    

print("\tplot a point for each genus with its colored marker and label, " + 
      "\n\tand hide the points in the plot. used for legend()\n"
      )
for index in range(len(site_order_index[0])) : 
    current_genus = index
    current_site = site_order_index[0][current_genus]
    
    plt.scatter(x = site_wf_2D[0][current_site],
                y = site_wf_2D[1][current_site],
                s = 420,
                c = color_list[enum_style[current_genus] % 100],
                marker = shape_list[0],
                label = genus_labels[current_genus],
                # edgecolors = "black",
                linewidths = 2,
                linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                )
    
    plt.scatter(x = site_wf_2D[0][current_site],
                y = site_wf_2D[1][current_site],
                s = 420*2,
                c = "white",
                marker = "o",
                )




print("\tplot the center of each site location under the genus circles\n")
for state in range(len(eco_uniques_list)) : 
    for u in range(len(eco_uniques_list[state])) : 
        plt.scatter(x = site_wf_2D[0][eco_uniques_list[state][u]],
                    y = site_wf_2D[1][eco_uniques_list[state][u]],
                    s = 420,
                    c = color_list[u],
                    marker = s_point_shapes[state],
                    label = str(str(eco_reg_list[eco_uniques_list[state][u]][0]) + 
                                eco_reg_list[eco_uniques_list[state][u]][1] + ": " +  
                                eco_reg_list[eco_uniques_list[state][u]][2] + " - " + 
                                eco_reg_list[eco_uniques_list[state][u]][3]
                                ),
                    edgecolors = "face",
                    )
        
        plt.scatter(x = site_wf_2D[0][eco_uniques_list[state][u]],
                    y = site_wf_2D[1][eco_uniques_list[state][u]],
                    s = 420*2,
                    c = "white",
                    marker = "o",
                    )
        



for site in range(len(site_2D_2[0])) : 
    for state in range(len(eco_uniques_list)) : 
        for u in range(len(eco_uniques_list[state])) : 
            if eco_reg_list[site][2] == eco_reg_list[eco_uniques_list[state][u]][2] : 
                plt.scatter(x = site_wf_2D[0][site],
                            y = site_wf_2D[1][site],
                            s = 180,
                            c = color_list[u],
                            marker = s_point_shapes[state],
                            edgecolors = "face",
                            )
                break


del state
del u

giq = find_val(genus_labels, g_to_plot)
print("\tplot all genus counts at each site and scale and offset each count value\n")
for current_site in range(len(genus_data)) : 
    for genus_index in range(len(genus_order_index[current_site])) : 
        current_genus = genus_order_index[current_site][genus_index]
        if current_genus > -1 and current_genus == giq : 
            plt.scatter(x = site_wf_2D[0][current_site],
                        y = site_wf_2D[1][current_site],
                        s = (genus_data[current_site][current_genus]),
                        c = color_list[enum_style[current_genus] % 100],
                        marker = shape_list[0],
                        # label = genus_labels[current_genus],
                        # edgecolors = "black",
                        linewidths = line_widths,
                        linestyle = line_list[int(enum_style[current_genus] / 100) - 1]
                        )
            
    plt.text(x = site_wf_2D[0][current_site] + x_offset,
             y = site_wf_2D[1][current_site] + y_offset,
             s = "#" + str(current_site + 1), # + "\n" + 
                 # "{:.2f}".format(site_data["Lat"][current_site]) + ", " + 
                 # "{:.2f}".format(site_data["Long"][current_site]),
             backgroundcolor = "white",
             fontsize = 12,
             rotation = rot
             )


del giq

plt.xlabel("UMAP Dimension 0")
plt.ylabel("UMAP Dimension 1")

plt.legend(loc = "lower right", 
           bbox_to_anchor = (1.0, 0.0),
           borderpad = 0.5,
           title = "Legend",
           ncols = 3,
           fontsize = 20
           )

print("\tsaving figure " + str(figure_count) + "...\n")
close_current_figure(file_name = 
                     str("\"seth_environmentalData_march2023.csv\", " + 
                         "\"seth_genusCountData_feb2024.csv\""
                         )
                     )

print("end plots\n")



print("start clean up")
#'''
del a
del b
# del i
del genus
del index
# del row
# del t
del temp
del site
# del val
del counts
del sorted_genus
del current_genus
del current_site
# del current_size
del current_style
del genus_index
# del movement_factor
del axs
del fig
#'''
print("end clean up\n")

print("\n\n\n === eof === ")