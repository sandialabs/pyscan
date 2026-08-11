# import matplotlib.pyplot as plt
import numpy as np
from time import sleep

import pyscan as ps


# TODO: report pre and post raster voltages and power to Ax
# instead of pre voltages and post power?
# Configure optimize scan to report initial inputs and measurements?
# Configure measure function to report raster inputs and measurements?
def raster(devices):
    voltage_range = ps.drange(-3, 0.01, 3)
    sweep_ct = 1
    for _ in range(sweep_ct):
        for axis in ['x1', 'y1', 'x2', 'y2']:
            devices[axis].voltage = voltage_range[0]
            sleep(1)
            power_res = np.zeros_like(voltage_range)
            for i, v in enumerate(voltage_range):
                devices[axis].voltage = v
                sleep(0.01)
                power_res[i] = devices.pm16_120.power
            devices[axis].voltage = voltage_range[np.argmax(power_res)]
            sleep(1)
            # plt.plot(voltage_range, power_res)
            # print(np.max(power_res),
            #       devices.x1.voltage,
            #       devices.y1.voltage,
            #       devices.x2.voltage,
            #       devices.y2.voltage)
