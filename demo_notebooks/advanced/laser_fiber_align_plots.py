import matplotlib.pyplot as plt
import numpy as np
from typing import Sequence


xl = "optimizer step"  # x label
lpyl = "laser power"  # laser poser y label
avcyt = np.arange(-3., 4., 1.)  # axis voltage combined y ticks
lpyt = np.arange(0., 3.5e-3, 5e-4)  # laser power y ticks


def input_combined_output_init():
    fig, axs = plt.subplots(2, layout='constrained')
    return fig, axs


def input_separate_output_init():
    fig, axs = plt.subplots(5, layout='constrained')
    fig.set_size_inches(8, 7)
    return fig, axs


# @ps.live_plot
# def plot_optim_live(expt):
#     global fig, axs


def input_combined_output_plot(axs: Sequence[plt.Axes], x1, y1, x2, y2, lp):
    axs[0].clear()
    axs[0].set_yticks(avcyt)
    axs[0].plot(list(zip(x1, y1, x2, y2)))
    axs[0].legend(['x1', 'y1', 'x2', 'y2'], loc='center left', bbox_to_anchor=(1, 0.5))
    axs[0].set_xlabel(xl)
    axs[0].set_ylabel("axis voltage")
    # axs[0].set_title("Device Inputs as a Function of Optimizer Step")
    axs[1].clear()
    axs[1].set_yticks(lpyt)
    axs[1].plot(lp)
    axs[1].set_xlabel(xl)
    axs[1].set_ylabel(lpyl)
    # axs[1].set_title("Laser Power as a Function of Optimizer Step")


def input_separate_output_plot(axs: Sequence[plt.Axes], x1, y1, x2, y2, lp):
    axs[0].clear()
    axs[0].plot(x1)
    axs[0].set_xlabel(xl)
    axs[0].set_ylabel("x1 voltage")
    axs[1].clear()
    axs[1].plot(y1)
    axs[1].set_xlabel(xl)
    axs[1].set_ylabel("y1 voltage")
    axs[2].clear()
    axs[2].plot(x2)
    axs[2].set_xlabel(xl)
    axs[2].set_ylabel("x2 voltage")
    axs[3].clear()
    axs[3].plot(y2)
    axs[3].set_xlabel(xl)
    axs[3].set_ylabel("y2 voltage")
    axs[4].clear()
    axs[4].set_yticks(lpyt)
    axs[4].plot(lp)
    axs[4].set_xlabel(xl)
    axs[4].set_ylabel(lpyl)
