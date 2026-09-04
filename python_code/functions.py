import matplotlib.pyplot as plt
from datetime import datetime

import os
import inspect
import ipynbname

# ============================================================
# function:     label_plot_edges
# purpose:      Add standardized edge labels (program name, author,
#               data sources, date, and optional message) to a matplotlib
#               figure. Automatically detects the calling script or notebook
#               when program_names is not provided.
#
# usage:        label_plot_edges(author_names="KLB",
#                                 data_filenames="dataset.csv",
#                                 fig_filename="plot.png",
#                                 save=True)
#
# inputs:
#     program_names : str, list, or None
#         Name(s) of the program/script generating the figure.
#         If None, the function automatically detects the caller's filename.
#
#     author_names : str or list of str
#         Name(s) of the author(s) or collaborators.
#
#     data_filenames : str or list of str
#         Dataset(s) used to generate the figure.
#
#     fig_filename : str or None
#         Output filename for the saved figure. Required when save=True.
#
#     message : str, optional
#         Additional text to display (e.g., notes, version tags).
#
#     save : bool, optional (default=False)
#         If True, the figure is saved to disk with metadata labels.
#
#     date_generated : str or None
#         If None, today's date is automatically inserted.
#
# outputs:
#     Saves a figure to disk (if save=True) and adds standardized
#     metadata labels to the edges of the current matplotlib figure.
#
# notes:
#     - Automatically detects the calling script using inspect.
#     - Falls back to "JupyterNotebook.ipynb" when run inside notebooks.
#     - Ensures consistent metadata formatting across all plots.
#
# date:         02/05/2026 (updated 06/26/2026)
# programmer:   Korbin Brashears
# ============================================================

def label_plot_edges(
        program_names=None,
        author_names=None,
        data_filenames=None,
        fig_filename=None,
        message="",
        save=False,
        date_generated=None,
        top_left=[0.050, 0.93, 0.20, 0.04],
        top_right=[0.750, 0.93, 0.20, 0.04],
        bottom_left=[0.050, 0.01, 0.20, 0.04],
        bottom_mid=[0.350, 0.01, 0.20, 0.04]
    ):
    """Add standardized edge labels and optionally save the figure."""

    
    # Auto-detect program name if not provided
    if program_names is None:
        try:
            caller_file = inspect.getfile(inspect.stack()[1][0])
            program_names = os.path.basename(caller_file)

            if (
                program_names.replace(".py", "").isdigit()
                or "interactiveshell" in program_names.lower()
            ):
                try:
                    program_names = f"{ipynbname.name()}.ipynb"
                except Exception:
                    program_names = "JupyterNotebook.ipynb"

        except Exception:
            program_names = "UnknownProgram"



    # If saving, a filename MUST be provided
    if save and fig_filename is None:
        raise ValueError("fig_filename is required when save=True")

    # Auto-generate today's date if not provided
    if date_generated is None:
        date_generated = datetime.now().strftime("%m/%d/%Y")

    # Normalize inputs to lists
    if isinstance(program_names, str):
        program_names = [program_names]
    if isinstance(author_names, str):
        author_names = [author_names]
    if isinstance(data_filenames, str):
        data_filenames = [data_filenames]

    # Convert lists to multi-line strings
    program_text = "\n".join(program_names)
    author_text = "\n".join(author_names) if author_names else ""
    data_text = "\n".join(data_filenames) if data_filenames else ""

    # Add date under author
    author_block = author_text + f"\n{date_generated}"

    plt.subplots_adjust(bottom=0.25)

    # Top-left: program names
    plt.subplot(position=top_left)
    plt.axis('off')
    plt.text(0, 0.5, program_text, fontsize=8, va='center')

    # Top-right: authors + date
    plt.subplot(position=top_right)
    plt.axis('off')
    plt.text(0, 0.5, author_block, fontsize=8, va='center')

    # Bottom-left: data files
    plt.subplot(position=bottom_left)
    plt.axis('off')
    plt.text(0, 0.5, data_text, fontsize=8, va='center')

    # Bottom-middle: optional message
    plt.subplot(position=bottom_mid)
    plt.axis('off')
    plt.text(0, 0.5, message, fontsize=8, va='center')

    # Save figure only if requested
    if save:
        plt.savefig(fig_filename, dpi=200)

    plt.show()



# ============================================================
# function:     scatter_trendLine_plotter
# purpose:      Generate a standardized scatter plot with an overlaid
#               regression trend line, optional point index labels, and
#               automated edge-label metadata via label_plot_edges().
#
# usage:        Call within any analysis or reporting script:
#               scatter_trendLine_plotter(x_series, y_series,
#                                         pointLabels=True,
#                                         save=False)
#
# inputs:
#     x : pandas Series
#         Independent variable to plot on the x-axis.
#
#     y : pandas Series
#         Dependent variable to plot on the y-axis.
#
#     pointLabels : bool, optional (default=True)
#         If True, each point is annotated with its index value.
#
#     save : bool, optional (default=False)
#         If True, the figure is saved using label_plot_edges() with the
#         appropriate filename and metadata. Requires global saveAll flag.
#
# outputs:
#     Displays a scatter plot with a regression trend line. Optionally
#     saves the figure to disk if save=True and saveAll=True.
#
# notes:
#     - Uses seaborn for both scatter and regression plotting.
#     - Automatically titles the figure using the x and y variable names.
#     - Integrates with label_plot_edges() for consistent metadata labeling.
#     - Designed for quick exploratory visualization of linear trends.
#
# date:         02/11/2026
# programmer:   Korbin Brashears
# ============================================================


# ====================================================== Defining Function =========================================================

def scatter_trendLine_plotter(x, y, pointLabels=True, save=False):

    import seaborn as sns
    
    # ===================================================== Plotting ===============================================================
    
    plt.figure(figsize=(10, 6))                                                                       # creating the figure for the scatter plot with matplotlib
    
    # Adding Trend Line
    sns.regplot(
        x=x,
        y=y,
        scatter=False,        # turn off regplot’s own dots
        line_kws={"linewidth": 2, "linestyle": "--", "zorder": 1, "color": "#000000"}
    )
    
    # Creating Scatter Plot
    sns.scatterplot(
        x=x,
        y=y,
        s=60,                 # dot size
        color="#ff0000",      # custom hex color (red)
        #zorder=2,
        edgecolor="black"     # optional: outline around dots
    )
    
    # Adding Point Index Labels (if enabled)
    if pointLabels:
        for i in range(len(x)):
            plt.text(x[i], y[i], str(i), fontsize=9, ha='right', va='bottom', color='#000099', zorder=3)       # adding index labels to each point
    
    # Labeling Axis and Title
    plt.xlabel(x.name)                                                                             # setting x-axis label as the specified attribute
    plt.ylabel(y.name)                                                                          # setting y-axis label
    
    plt.title(f'{y.name} vs {x.name}')                                                # setting the title of the plot with the specified attribute

    # ============================================= Adding Plot Edge Labels ======================================================
    
    # Adding Plot Edge Labels
    label_plot_edges(                                          # calling the function to label the edges of the plot
        author_names="Korbin Brashears", 
        data_filenames="seth_envData_2025.csv", 
        fig_filename=f"../figures/kbrashears_fishData_report_02042026/{x.name}_vs_{y.name}_trendLine.png",
        save = save                                
    )
    
    plt.show()                                                                             
    
    return None


# ============================================================
# function:     corr_decay_plotter
# purpose:      Compute and visualize the correlation decay pattern between a
#               target attribute (Series) and a set of environmental or biological
#               features (DataFrame). Produces a sorted correlation plot showing
#               both positive and negative relationships, with negative correlations
#               highlighted separately. Automatically applies standardized plot
#               metadata via label_plot_edges().
#
# usage:        corr_decay_plotter(attribute_series, feature_dataframe,
#                                   save=False)
#
# inputs:
#     attribute : pandas Series
#         The focal variable whose correlation with all features will be computed.
#         Example: a species abundance vector or an environmental attribute.
#
#     features : pandas DataFrame
#         A DataFrame containing multiple numeric feature columns to correlate
#         against the attribute. Must be numeric or convertible to numeric.
#
#     save : bool, optional (default=False)
#         If True, the figure is saved using label_plot_edges() with the
#         appropriate filename and metadata. Uses global saveAll override
#         if present.
#
# outputs:
#     Displays a correlation-decay plot showing:
#         - Sorted absolute correlation magnitudes
#         - Positive correlations (blue)
#         - Negative correlations (orange)
#     Optionally saves the figure to disk if save=True.
#
# notes:
#     - Uses pandas.corrwith() for efficient vectorized correlation computation.
#     - Negative correlations are tracked separately and plotted distinctly.
#     - Integrates with label_plot_edges() for consistent metadata labeling.
#     - Designed for exploratory analysis of feature importance and correlation
#       structure in ecological or environmental datasets.
#
# date:         02/11/2026
# programmer:   Korbin Brashears
# ============================================================


# ====================================================== Defining Function =========================================================

def corr_decay_plotter(attribute, features, save=False):

    import seaborn as sns
    
    # ===================================================== Data Analysis =========================================================
    
    # Calculating Correlations with Respect to the Specified Attribute
    cd_raw = features.corrwith(attribute, numeric_only=True)      # signed correlations
    neg_idx = cd_raw < 0                                          # mask for negative correlations
    cd = cd_raw.abs()                                             # absolute values for plotting
    
    # Sorting Correlation Values
    cd_sorted = cd.sort_values(ascending=False)                   # descending order
    neg_sorted = neg_idx.loc[cd_sorted.index]                     # reorder negative mask
    
    # ===================================================== Plotting =========================================================
    
    plt.figure(figsize=(12, 6))
    
    # Base line plot
    sns.lineplot(
        x=cd_sorted.index,
        y=cd_sorted.values,
        color='blue',
        zorder=1
    )
    
    # Positive correlations
    sns.scatterplot(
        x=cd_sorted.index[~neg_sorted],
        y=cd_sorted.values[~neg_sorted],
        color="blue",
        zorder=2,
        s=40
    )
    
    # Negative correlations
    sns.scatterplot(
        x=cd_sorted.index[neg_sorted],
        y=cd_sorted.values[neg_sorted],
        color="orange",
        zorder=2,
        s=40
    )
    
    # Labels and formatting
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('')
    plt.ylabel('Correlation Coefficient')
    plt.title(f'Correlation Decay of features with {attribute.name}')
    plt.grid(True)
       
    # ============================================= Adding Plot Edge Labels ======================================================
       
    label_plot_edges(
        author_names="Korbin Brashears",
        data_filenames="seth_envGenusCountData_2025.csv",
        fig_filename=f"../figures/kbrashears_fishData_report_02042026/{attribute.name}_correlation_decay_plot.png",
        save = save
    )
    
    plt.show()
    
    return None