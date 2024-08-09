# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from IPython import display
from time import sleep


def live_plot(plotting_function, dt=1):
    '''
    Generates a function that executes plotting_function while data
    is still being taken in Jupyter notebooks. Used by the live plotting
    functions such as :func:`~pyscan.plotting.basicplots.live_plot2D`.

    Parameters
    ----------
    plotting_function : func
        Function to be refreshed
    dt : float
        Time in s between refreshes

    Returns
    -------
    func

    '''

    def live_plot_function(expt=None, *arg, **kwarg):
        while (expt.runinfo.running is True and len(expt.runinfo.measured) < 1):
            sleep(1)

        plt.axis()
        plt.ion()

        while expt.runinfo.running:
            sleep(dt)

            plt.gca().cla()

            plotting_function(expt, *arg, **kwarg)

            display.display(plt.gcf())
            display.clear_output(wait=True)

        plt.gca().cla()

        plotting_function(expt, *arg, **kwarg)

        display.display(plt.gcf())
        display.clear_output(wait=True)

    return live_plot_function


def multi_live_plot(plotting_functions, subplot_locators=None, projections=None, nrows=1, ncols=1,
                    subplot_kw={}, dt=1):
    '''
    Generates a function that executes all plotting_function provided while data
    is still being taken in Jupyter notebooks. Used by the live plotting
    functions such as :func:`~pyscan.plotting.basicplots.live_plot2D`.

    Parameters
    ----------
    plotting_functions : list
        list of plotting functions to be refreshed. Each function must take exactly
        two parameters: expt and ax. The function should take data from expt and plot
        to a matplotlib axis object.
    subplot_locators : list, optional
        list of subplot locators in accordance with matplotlib subplot formatted as
        A 3-digit integer or a tuple with three numbers (nrows, ncols, index).
        If omitted, then plotting functions will occupy the axes object according to
        their index position.
    projections: list, optional
        list of projections such as None, '3d', 'polar', according to each plotting function.
        If ommitted, all plots default to 2d.
    nrows : int, optional
        How many rows to add to the multiplot. Only used if subplot_locators are not provided.
    ncols : int, optional
        How many cols to add to the multiplot. Only used if subplot_locators are not provided.
    subplot_kw : dict
        Dict with keywords passed to matplotlib's `add_subplot` call used to create each subplot.
    dt : float
        Time in s between refreshes

    Returns
    -------
    func : function
        Its mandatory parameter is list of experiments in the same order as the plotting_functions as
        defined in the multi_live_plot function. Keyword arguments can be provided and accessed by the
        plotting_functions as well to further customize plots.

    '''

    # check if subplot_locators was specified
    if not subplot_locators:
        # check if n_cols and n_rows accomodates all of the plotting_functions
        total_axes = nrows * ncols
        if len(plotting_functions) > total_axes:
            raise ValueError(f"not enough plots based on {nrows} nrows and {ncols} ncols to accomodate "
                             + f"{len(plotting_functions)} plotting_functions.")
    else:
        # check plotting functions is same length as subplot locators
        if not len(plotting_functions) == len(subplot_locators):
            raise ValueError("subplot_locators must be the same length as plotting_functions")

    # check if projections was specified
    if projections:
        # check plotting functions is same length as proejctions
        if not len(plotting_functions) == len(projections):
            raise ValueError("projections must be the same length as plotting_functions")

    def live_plot_function(expt, *arg, **kwarg):
        while (expt.runinfo.running is True and len(expt.runinfo.measured) < 1):
            sleep(1)

        fig = plt.figure(layout="constrained")
        plt.ion()

        def plot():
            if subplot_locators:
                for i, func in enumerate(plotting_functions):
                    subplot_locator = subplot_locators[i]
                    if projections:
                        projection = projections[i]
                    else:
                        projection = None
                    # check if subplot locator is int or tuple
                    if isinstance(subplot_locator, int):
                        ax = fig.add_subplot(subplot_locator, projection=projection, **subplot_kw)
                    elif isinstance(subplot_locator, tuple):
                        ax = fig.add_subplot(*subplot_locator, projection=projection, **subplot_kw)
                    func(expt, ax, *arg, **kwarg)
            else:
                for i, func in enumerate(plotting_functions):
                    if projections:
                        projection = projections[i]
                    else:
                        projection = None
                    ax = fig.add_subplot(nrows, ncols, i + 1, projection=projection, **subplot_kw)
                    func(expt, ax, *arg, **kwarg)
            plt.tight_layout()

        while expt.runinfo.running:
            sleep(dt)

            plt.clf()

            plot()

            display.display(plt.gcf())
            display.clear_output(wait=True)

        plt.clf()

        plot()

        display.display(plt.gcf())
        display.clear_output(wait=True)

    return live_plot_function
