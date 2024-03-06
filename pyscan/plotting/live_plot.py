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
        try:
            while (expt.runinfo.running is True and len(expt.runinfo.measured) < 1):
                sleep(1)

            plt.axis()
            plt.ion()
        except KeyboardInterrupt:
            return 0

        try:
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
        except KeyboardInterrupt:
            return 0

    return live_plot_function
