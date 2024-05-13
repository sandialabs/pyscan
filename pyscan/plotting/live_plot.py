# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from IPython import display
from time import sleep
import keyboard


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

    def live_plot_function(expt=None, killswitch=None, *arg, **kwarg):
        # The killswitch should be something like 'q' if you want to press q on the keyboard and stop the experiment.

        while (expt.runinfo.running is True and len(expt.runinfo.measured) < 1):
            sleep(1)

        plt.axis()
        plt.ion()

        while expt.runinfo.running:
            if killswitch is not None:
                if keyboard.ispressed(killswitch):
                    expt.stop()

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
