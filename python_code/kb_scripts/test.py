
import matplotlib.pyplot as plt

from functions import label_plot_edges as lpe

plt.figure(figsize=(12, 12))

lpe(                                      # Calling the lpe to label the edges of the plot.
    author_names="Korbin Brashears", 
    data_filenames='lllllll', 
    fig_filename="../figures/crop_runoff/CDL_catchmentMask_sites.png",
    save = False                                                        # Change False to True to save the figure.
    ) 

plt.show()