from typing import Optional, Tuple, Set

import matplotlib.pyplot as plt
import numpy
import pandas


def show_selector(sy: pandas.DataFrame, figsize: Optional[Tuple[int, int]] = None, *args, **kwargs) -> Set[int]:
    """Plot the Depth in function of Sy and allow the selection of data.

    This function plot the Depth(Sy) relation and allows the selection of
    data points. It allows the user to easily retrieve aberrant points
    without too much hassle. The selected data points will appear in
    red when clicked.
    
    Examples
    --------
    >>> selected_indexes = show_selector(sy)
    >>> print(selected_indexes)
     {0, 100, 5, 101, 103, 46, 79, 47, 19, 24}

    Parameters
    ----------
    sy
        The Sy DataFrame (same format as the `calculate_sy` output).
    figsize
        Optional, a tuple (width, height).
    args
        Optional, arguments that will be given to the scatter plot.
    kwargs
        Optional, named arguments that will be given to the scatter plot.

    Returns
    -------
    Set[int]
        A set of indexes of the selected data points.
    """
    if figsize:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig, ax = plt.subplots()

    scatter_plot = ax.scatter(sy['sy'], sy['depth'], picker=True, color=['blue'] * len(sy['sy']), *args, **kwargs)
    ax.set_xlabel('Sy')
    ax.set_ylabel('Depth [m]')

    selected_indexes = set()

    def on_pick(event):
        indexes = event.ind
        for index in indexes:
            selected_indexes.add(index)
            scatter_plot._facecolors[index] = numpy.array([1, 0, 0, 1])  # Set to color Red
            scatter_plot._edgecolors[index] = numpy.array([1, 0, 0, 1])  # Set to color Red
            fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    plt.show()

    return selected_indexes


def plot_depth(sy: pandas.DataFrame, *args, **kwargs):
    plt.scatter(
        x=sy['sy'],
        y=sy['depth'],
        *args,
        **kwargs
    )
    plt.xlabel('Sy')
    plt.ylabel('Depth [m]')


def plot_water_level(sy: pandas.DataFrame, *args, **kwargs):

    plt.xlabel('time [h]')
    plt.ylabel('Water level [m]')
