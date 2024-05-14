import keyboard
from time import sleep
import matplotlib.pyplot as plt
from IPython import display


def stop(expt):
    expt.stop()
    print("stop function executed")


def engage_killswitch(expt, hotkey='c', plotting_function=None, dt=.1, *arg, **kwarg):
    if plotting_function is not None:
        plt.axis()
        plt.ion()

    keyboard.on_press_key(hotkey, lambda _: stop(expt))
    # keyboard.add_hotkey(hotkey, lambda _: stop(expt))

    while expt.runinfo.running is True:
        if keyboard.is_pressed(hotkey):
            print("killswitch engaged")
            break

        if dt > 1:
            expt.stop()
            assert False, "dt greater than 1 is not allowed because it may inhibit the killswitch from registering."

        if plotting_function is not None:
            while (expt.runinfo.running is True and len(expt.runinfo.measured) < 1):
                sleep(dt)

            sleep(dt)

            plt.gca().cla()

            plotting_function(expt, *arg, **kwarg)

            display.display(plt.gcf())
            display.clear_output(wait=True)

    keyboard.unhook_all()

    if plotting_function is not None:
        plt.gca().cla()

        plotting_function(expt, *arg, **kwarg)

        display.display(plt.gcf())
        display.clear_output(wait=True)

    return engage_killswitch
