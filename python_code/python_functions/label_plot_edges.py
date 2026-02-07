# ============================================================
# function:     label_plot_edges
# purpose:      Add standardized edge labels (program names, authors,
#               data files, and optional message) to a matplotlib figure.
#               Supports single strings or lists for each field.
#
# usage:        Import into any plotting script and call:
#               label_plot_edges(program_names, author_names,
#                                 data_filenames, fig_filename=None,
#                                 message="", save=True,
#                                 date_generated=None)
#
# inputs:
#     program_names : str or list of str
#         Name(s) of the program/script generating the figure.
#
#     author_names : str or list of str
#         Name(s) of the author(s) or collaborators.
#
#     data_filenames : str or list of str
#         Dataset(s) used to generate the figure.
#
#     fig_filename : str or None
#         Output filename for the saved figure (e.g., "plot_fig.png").
#         Required only when save=True.
#
#     message : str, optional
#         Additional text to display (e.g., notes, version tags).
#
#     save : bool, optional (default=True)
#         If True, the figure is saved to disk. If False, labels are added
#         but the figure is not saved.
#
#     date_generated : str or None
#         If None, today's date is automatically inserted under the author.
#
# outputs:
#     Saves a figure to disk with standardized edge labels (if save=True, default False).
#
# notes:
#     - Automatically handles single strings or lists.
#     - Places labels in four fixed positions around the figure.
#     - Ensures consistent formatting across all scripts.
#
# date:         02/05/2026
# programmer:   Korbin Brashears
# ============================================================

import matplotlib.pyplot as plt
from datetime import datetime

def label_plot_edges(
        program_names,
        author_names,
        data_filenames,
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
    author_text = "\n".join(author_names)
    data_text = "\n".join(data_filenames)

    # Add date under author
    author_block = author_text + f"\n{date_generated}"
    
    plt.subplots_adjust(bottom=0.25)                                        # adjusting the bottom margin to prevent x-axis labels from being cut off

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
