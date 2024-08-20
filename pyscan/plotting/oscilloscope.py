# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from time import sleep, time
from IPython import display
from pyscan.general import is_list_type, is_numeric_type


def oscilloscope(measure_function, histo_range=100, dt=0.001, numy=1):
    '''
    Takes a function that returns a value and plots live until function is killed

    Parameters
    ----------
    measure_function : func
        Function that generates a data point or set
    histo_range : int
        Total number of data points before overwriting
    dt : float
        Time in s between datapoints being taken
    normalize_max :
        normalize maximum of data to 1
    numy : int
        Number of datasets to plot

    Returns
    -------
    None

    '''

    fig, ax = plt.subplots()
    if numy==2:
        ax2 = ax.twinx()
    plt.axis()
    plt.ion()

    x_data = []
    y_data = []
    data = []
    y = None

    t0 = time()

    i = 0
    try:
        while True:
            sleep(dt)

            d = measure_function()

            # print(is_list_type(d), is_numeric_type(d))

            if is_numeric_type(d):
                dims = 0
                new_data = d
                x = time() - t0
                y_name = 'Data'
                x_name = 'time (s)'

            elif is_list_type(d):
                if len(d) == 2:
                    dims = 1
                    x, new_data = d
                    y_name = None
                    x_name = None
                elif len(d) == 3:
                    dims = 2
                    x, y, new_data = d
                    x_name = None
                    y_name = None
                else:
                    if len(d[0]) == 1:
                        dims = 1
                        new_data = d
                        x = list(range(len(new_data)))
                    else:
                        print("Bad measure function return type")
                        return 0
            else:
                print("Bad measure function return type")
                return 0

            if histo_range == 1:
                data = new_data
                x_data = x
                if np.any(np.array(y)):
                    y_data = y
            elif i < histo_range:
                data = np.array(list(data)+[new_data])
                x_data = np.append(x_data, [x])
                if y:
                    y_data = np.append(y_data, [y])
            else:
                data = np.array(list(data[1:])+[new_data])
                x_data = np.append(x_data[1:], [x])
                if y:
                    y_data = np.append(y_data[1:], [y])

            plt.gca().cla()
            if numy==2:
                ax2.cla()

            plt.title("Oscilloscope {}".format(i))

            if dims == 0:
                plt.plot(x_data, data)
                plt.xlabel("Time (s)")
                ypad = (np.max(data) - np.min(data)) / 20
                plt.ylim(np.min(data) - ypad, np.max(data) + ypad)
                plt.xlim(x_data[0], x_data[-1])

            if dims == 1:
                if numy==1:
                    plt.plot(x_data.T, data.T, 'o-')
                    ypad=(np.max(data)-np.min(data))/20
                    plt.ylim(np.min(data)-ypad,np.max(data)+ypad)
                elif numy==2:
                    ax.plot(x_data.T, data.T[0], 'o-')
                    ypad=(np.max(data.T[0])-np.min(data.T[0]))/20
                    ax.set_ylim(np.min(data.T[0])-ypad,np.max(data.T[0])+ypad)
                    ax2.plot(x_data.T, data.T[1], 'o-r')
                    y2pad=(np.max(data.T[1])-np.min(data.T[1]))/20
                    ax2.set_ylim(np.min(data.T[1])-y2pad,np.max(data.T[1])+y2pad)
                else:
                    [plt.plot(x_data.T, dat, 'o-') for dat in data.T]
                    ypad=(np.max(data)-np.min(data))/20
                    plt.ylim(np.min(data)-ypad,np.max(data)+ypad)
                plt.xlabel(x_name)

            if dims == 2:
                plt.pcolormesh(x_data, y_data, data.T)
                plt.xlabel(x_name)
                plt.xlim(x_data[0], x_data[-1])
                plt.ylim(y_data[0], y_data[-1])

            plt.ylabel(y_name)
            display.display(plt.gcf())
            display.clear_output(wait=True)

            i += 1
    except KeyboardInterrupt:
        return None
