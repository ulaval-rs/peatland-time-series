from typing import Optional, Set, Tuple, Union
from warnings import warn

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy
import numpy as np
import pandas
from scipy.optimize import curve_fit
from matplotlib.ticker import FixedLocator

from .util import power_law, inverse_power_law

TWIN_COLOR = 'royalblue'


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
    warn('This function is deprecated, use "show_depth(..., select=True)" instead.', DeprecationWarning, stacklevel=2)

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


def show_depth(sy: pandas.DataFrame,
               height_of_line: Optional[float] = None,
               select: bool = False,
               show_plot: bool = True,
               power_law_x_axis: bool = False,
               show_legend: bool = False,
               show_indexes: bool = False,
               x_limits: Optional[Tuple[float, float]] = None,
               y_limits: Optional[Tuple[float, float]] = None) -> Optional[Union[Set[int], plt.Figure]]:
    """Plot the depth in function of Sy.

    Examples
    --------
    ```python
    time_series = read_time_series('./tests/data/kmr_area_c.csv')
    sy = calculate_sy(time_series=time_series)

    sy = filter_sy(sy, sy_min=0, delta_h_min=.01, precipitation_sum_min=10, precipitation_sum_max=100)

    visualization.show_depth(sy, height_of_line=2)
    # For selecting indexes (for removing data points for exemple)
    selected_indexes = visualization.show_depth(sy, select=True)
    ```

    Parameters
    ----------
    sy
        DataFrame of Sy, obtained by the `calculate_sy` function.
    height_of_line
        Optional, draw an asymptote line at specified height.
    select
        If True, the data points can be selected on the plot.
        When the plot is closed, the index of the selected data points
        are returned.
    show_plot
        If True, "plt.show()" is called, if False, the figure is return.
    power_law_x_axis
        If True, the Sy axis takes a power low graduation. If False, linear graduation.
    show_legend
        If True, show legend.
    show_indexes
        If true, a label with the index will point to its corresponding data point.
    x_limits
        Tuple of the limits for the x axis.
    y_limits
        Tuple of the limits for the y axis.

    Returns
    -------
    Optional[Union[Set[int], matplotlib.figure.Figure]]
        None if "select" is False (default). Set of selected indexes if "select" is True.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    sy['depth'] = sy['depth'] * 100  # To have the values in cm rather than m
    sy['min_wtd'] = sy['min_wtd'] * 100  # To have the values in cm rather than m
    sy['max_wtd'] = sy['max_wtd'] * 100  # To have the values in cm rather than m
    precepitation_sum = sy['precipitation_sum'].values

    # For the error bars
    ax.errorbar(
        x=sy['sy'],
        y=sy['depth'],
        yerr=(sy['min_wtd'] - sy['max_wtd']) / 2,
        c='gray',
        fmt=',',  # Marker is a pixel
        alpha=.5,
        zorder=-1  # Visualy set the plot behind others
    )

    # For the scatter plot
    scatter_plot = ax.scatter(x=sy['sy'], y=sy['min_wtd'],
                              c=precepitation_sum, s=precepitation_sum,
                              vmin=min(precepitation_sum), vmax=max(precepitation_sum),
                              picker=select)
    fig.colorbar(scatter_plot, label='Precipitation sum [mm]')

    # Annotation of the data points
    if show_indexes:
        for index, row in sy[['sy', 'min_wtd']].iterrows():
            ax.annotate(index, (row['sy'] + 0.01, row['min_wtd'] - 2))

    # Plotting the "asymptote" line
    sorted_sy = np.sort(sy['sy'])

    if height_of_line is not None:
        ax.plot(sorted_sy, [height_of_line for _ in sorted_sy], '--', color='gray', alpha=.5)

    # Curve fit
    pars, cov = curve_fit(f=power_law, xdata=sy['sy'], ydata=sy['min_wtd'])
    standard_deviation = numpy.sqrt(numpy.diag(cov))
    a, b = pars[0], pars[1]
    standard_deviation_a, standard_deviation_b = standard_deviation[0], standard_deviation[1]
    ax.plot(
        sorted_sy,
        power_law(sorted_sy, a, b),
        label=f'$Depth = a \cdot (Sy)^b$\n'
              f'$\quad a = {a:.4f}\ cm, \sigma_a = {standard_deviation_a:.4f}\ cm$\n'
              f'$\quad b = {b:.4f}\qquad, \sigma_b = {standard_deviation_b:.4f}$',
        color='gray', alpha=.5
    )

    if power_law_x_axis:
        # Transforming Sy axis show an linear expression in plot
        ax.set_xscale('function', functions=(lambda x: power_law(x, a, b), lambda x: inverse_power_law(x, a, b)))
        ax.xaxis.set_major_locator(FixedLocator(numpy.arange(0, 2.1, 0.5)))

        ax.set_ylim((-100, 0))
        ax.set_xlim((sorted_sy.min()-0.001, sorted_sy.max()+0.001))

    else:  # If note, plot with the default limits
        ax.set_ylim((-100, 0))
        ax.set_xlim((0, 1))

    # Overwriting default limits if specified
    if x_limits is not None:
        ax.set_xlim(x_limits)
    if y_limits is not None:
        ax.set_ylim(y_limits)

    ax.xaxis.set_ticks_position('top')  # Putting x-axis on top
    ax.xaxis.set_label_position('top')
    ax.set_xlabel('Sy')
    ax.set_ylabel('Depth [cm]')

    if show_legend:
        plt.legend()

    plt.tight_layout()

    if select:
        selected_indexes = set()

        def on_pick(event):
            indexes = event.ind
            for index in indexes:
                selected_indexes.add(index)
                scatter_plot._sizes[index] = 0
                fig.canvas.draw()

        fig.canvas.mpl_connect('pick_event', on_pick)
        plt.show()

        return selected_indexes
    
    if not show_plot:
        return fig

    plt.show()


def plot_depth(sy: pandas.DataFrame, *args, **kwargs) -> None:
    """Plot the depth in function of Sy.
    
    Examples
    --------
    ```python
    time_series = read_time_series('./tests/data/kmr_area_c.csv')
    sy1 = calculate_sy(time_series=time_series)

    time_series2 = read_time_series('./tests/data/kmr_area_c.csv')
    sy2 = calculate_sy(time_series=time_series2)

    sy1 = filter_sy(sy1, sy_min=0, delta_h_min=.01, precipitation_sum_min=10, precipitation_sum_max=100)
    sy2 = filter_sy(sy2, sy_min=0, delta_h_min=.01, precipitation_sum_min=10, precipitation_sum_max=100)

    visualization.plot_depth(sy1, label='Sy 1', color='blue')
    visualization.plot_depth(sy2, label='Sy 2', color='red')
    plt.legend()

    plt.show()
    ```

    Parameters
    ----------
    sy
        DataFrame of Sy, obtained by the `calculate_sy` function.
    args
        Any args that will be give to to the plt.scatter plot.
    kwargs
        Any named args that will be give to to the plt.scatter plot.

    Returns
    -------
    None
    """
    plt.scatter(
        x=sy['sy'],
        y=sy['depth'],
        *args,
        **kwargs
    )
    plt.xlabel('Sy')
    plt.ylabel('Depth [m]')


def show_water_level(
        time_series: pandas.DataFrame,
        sy: pandas.DataFrame,
        event_index: int,
        time_before: pandas.Timedelta,
        time_after: pandas.Timedelta,
        fig_size: Optional[Tuple[int, int]] = None,
        date_format: Optional[str] = '%H',
        xlabel_rotation: Optional[int] = 0,
        show_plot: bool = True) -> Optional[plt.Figure]:
    """Plot the water level in function of the time.

    Examples
    --------
    ```python
    time_series = read_time_series('./tests/data/kmr_area_c.csv')
    sy = calculate_sy(time_series)

    show_water_level(
        time_series,
        sy,
        event_index=30,
        time_before=pandas.Timedelta(hours=10),
        time_after=pandas.Timedelta(hours=20)
    )
    ```

    Parameters
    ----------
    time_series
        Time series as a DataFrame (from `read_time_series`).
    sy
        Sy as a DataFrame (from `calculate_sy`).
    event_index
        Index of the event in Sy.
    time_before
        pandas.Timedelta before the chosen event.
    time_after
        pandas.Timedelta after the chosen event.
    date_format
        Date format (see https://strftime.org/).
    fig_size
        (width, height), fig size given to plt.subplots.
    xlabel_rotation
        Rotation of the x axis label. This may be useful when using complete dates on the x axis.
    show_plot
        If True, "plt.show()" is called, if False, the figure is return.

    Returns
    -------
    Optional[matplotlib.figure.Figure]
        If "show_plot" is True, returns the plt.Figure. If False, returns None.
    """
    beginning = sy['date_beginning'].iloc[event_index] - time_before
    ending = sy['date_ending'].iloc[event_index] + time_after

    sub_time_series = time_series.loc[beginning:ending]

    fig, ax = plt.subplots(figsize=fig_size if fig_size else (10, 6))

    # Water table Depth plot
    ax.plot(sub_time_series.index, sub_time_series['data_wtd'], color='black')
    ax.set_xlabel('Time [h]')
    ax.set_ylabel('Water level [m]')

    # Twin plot for the precipitation
    # ------------------------------------------
    ax_precipitation = ax.twinx()
    ax_precipitation.bar(
        sub_time_series.index,
        sub_time_series['data_prec'],
        color=TWIN_COLOR,
        alpha=0.5,
        width=0.02
    )
    # Setting the color to all elements of the twin plot
    ax_precipitation.set_ylabel('Prec. [mm]', color=TWIN_COLOR)
    ax_precipitation.spines['right'].set_color(TWIN_COLOR)
    ax_precipitation.tick_params(axis='y', colors=TWIN_COLOR)

    ax.scatter(
        x=sy['idx_max'].iloc[[event_index]],
        y=sy['max_wtd'].iloc[[event_index]],
        s=100
    )
    ax.scatter(
        x=sy['idx_min'].iloc[[event_index]],
        y=sy['min_wtd'].iloc[[event_index]],
        s=100
    )
    
    date_formater = mdates.DateFormatter(date_format)
    ax.xaxis.set_major_formatter(date_formater)

    plt.tight_layout()
    
    if not show_plot:
        return fig
    
    plt.show()
