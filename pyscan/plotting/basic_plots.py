# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from .plot_generator import PlotGenerator
from .live_plot import live_plot
from time import sleep


def plot1D(expt, **kwarg):
    """
    Function to generate a simple 2D plot

    Parameters
    ----------
    expt :
        The experiment object
    d :
        Dimensionality of the data to be plotted

    Other Parameters
    ----------------
    **kwargs
        Additional kwargs are `pyscan.plotting.plotgenerator.PlotGenerator` properties.

    """

    pg = PlotGenerator(expt, d=1, **kwarg)

    # this ensures that continuous expts are plotted correctly when an n_max parameter is implemented.
    if expt.runinfo.continuous is True and expt.runinfo.running is False:
        n_max = expt.runinfo.scans[expt.runinfo.continuous_scan_index].n_max
        if len(pg.x) - 1 == n_max:
            # give a time buffer to make sure the most recent state of the expt is registered.
            # otherwise the plot will break as it finishes. May need to extend for low performing processors.
            sleep(3)
            pg.x = pg.x[:-1]

    plt.plot(pg.x, pg.data)

    plt.title(pg.get_title())
    plt.xlabel(pg.get_xlabel())
    plt.ylabel(pg.get_ylabel())

    plt.xlim(pg.get_xrange())
    plt.ylim(pg.get_yrange())


def plot2D(expt, **kwarg):
    """
    Function to generate a simple 2D plot

    Parameters
    ----------
    expt :
        The experiment object
    d :
        Dimensionality of the data to be plotted

    Other Parameters
    ----------------
    **kwargs
        Additional kwargs are `pyscan.plotting.plotgenerator.PlotGenerator` properties.

    """

    pg = PlotGenerator(expt, d=2, **kwarg)

    # this ensures that continuous expts are plotted correctly when an n_max parameter is implemented.
    if expt.runinfo.continuous is True and expt.runinfo.running is False:
        n_max = expt.runinfo.scans[expt.runinfo.continuous_scan_index].n_max
        if len(pg.y) - 1 == n_max:
            # give a time buffer to make sure the most recent state of the expt is registered.
            # otherwise the plot will break as it finishes. May need to extend for low performing processors.
            sleep(3)
            pg.y = pg.y[:-1]

    plt.pcolormesh(pg.x, pg.y, pg.data.T,
                   vmin=pg.get_data_range()[0],
                   vmax=pg.get_data_range()[1])

    plt.title(pg.get_title())
    plt.xlabel(pg.get_xlabel())
    plt.ylabel(pg.get_ylabel())

    plt.xlim(pg.get_xrange())
    plt.ylim(pg.get_yrange())


live_plot1D = live_plot(plot1D)
live_plot2D = live_plot(plot2D)


def average_plot1D(expt, **kwarg):
    """
    Wrapper for 1D plot to plot the average over the second dimension

    Other Parameters
    ----------------
    **kwargs
        Additional kwargs are `pyscan.plotting.plotgenerator.PlotGenerator` properties.

    """

    plot1D(expt, analysis_function=mean1D)


def average_plot2D(expt, **kwarg):
    """
    Wrapper for 1D plot to plot the average over the second dimension

    Other Parameters
    ----------------
    **kwargs
        Additional kwargs are `pyscan.plotting.plotgenerator.PlotGenerator` properties.

    """

    plot1D(expt, analysis_function=mean2D)


live_average_plot1D = live_plot(average_plot1D)
live_average_plot2D = live_plot(average_plot2D)


def mean1D(data):
    '''
    Returns mean of data over dim 1

    '''

    return np.nanmean(data, axis=1)


def mean2D(data):
    '''
    Returns mean of data over dim 2

    '''

    return np.nanmean(data, axis=2)
