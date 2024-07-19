# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from .plot_generator import PlotGenerator
from .live_plot import live_plot


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

    c = plt.pcolormesh(pg.x, pg.y, pg.data.T,
                   vmin=pg.get_data_range()[0],
                   vmax=pg.get_data_range()[1])
    cax = plt.gcf().axes[-1]
    if cax.get_label() == '<colorbar>':
        cax.cla()
        plt.colorbar(c, cax=cax)
    else:
        plt.colorbar(c)

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
