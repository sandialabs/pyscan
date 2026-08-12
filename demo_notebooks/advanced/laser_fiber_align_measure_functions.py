import matplotlib.pyplot as plt
from numbers import Real
import numpy as np
from time import sleep

import pyscan as ps


# TODO: report pre and post raster voltages and power to Ax
# instead of pre voltages and post power?
# Configure optimize scan to report initial inputs and measurements?
# Configure measure function to report raster inputs and measurements?
def raster(devices):

    input_range = ps.drange(-3, 0.01, 3)
    sweep_ct = 1
    input_l = ['x1', 'y1', 'x2', 'y2']

    for _ in range(sweep_ct):
        for d in input_l:
            devices[d].voltage = input_range[0]
            sleep(1)
            f_res = np.zeros_like(input_range)
            for i, v in enumerate(input_range):
                devices[d].voltage = v
                sleep(0.01)
                f_res[i] = devices.pm16_120.power
            devices[d].voltage = input_range[np.argmax(f_res)]
            sleep(1)
            # plt.plot(voltage_range, power_res)
            # print(np.max(power_res),
            #       devices.x1.voltage,
            #       devices.y1.voltage,
            #       devices.x2.voltage,
            #       devices.y2.voltage)


def grad_desc(devices):

    max_grad_step = 100
    input_l = ['x1', 'y1', 'x2', 'y2']
    input_ct = len(input_l)
    input_epsilon_l = [1e-2] * input_ct
    learning_rate_l = [1e-2] * input_ct
    update_epsilon_l = [1e-5] * input_ct

    i_p_l = [[devices[d].voltage] for d in input_l]
    f_p = [devices.pm16_120.power]

    def gd_f(f_in_prev: Real, f_out: Real, f_out_prev: Real,
             input_epsilon: Real, learning_rate: Real) -> tuple[Real, Real]:
        grad = (f_out - f_out_prev) / input_epsilon
        grad_update = learning_rate * grad
        f_in_dim_next = f_in_prev - grad_update
        return grad, f_in_dim_next

    f_current = devices.pm16_120.power
    keep_running = [True] * input_ct
    running = True
    for _ in range(max_grad_step):
        for d_idx, d in enumerate(input_l):
            input_current_dim = devices[d].voltage
            devices[d].voltage = input_current_dim + input_epsilon_l[d_idx]
            sleep(.1)
            f_fd = devices.pm16_120.power
            grad_dim, f_in_dim_next = gd_f(input_current_dim,
                                           f_current, f_fd,
                                           input_epsilon_l[d_idx],
                                           learning_rate_l[d_idx])
            devices[d].voltage = f_in_dim_next
            sleep(.1)
            f_current = devices.pm16_120.power
            keep_running[d_idx] = abs(grad_dim) > update_epsilon_l[d_idx]

            for p_idx, p in enumerate(i_p_l):
                p.append(devices[input_l[p_idx]].voltage)
            f_p.append(f_current)

            if not any(keep_running):
                running = False
                break
        if not running:
            break

    plt.figure()
    for p in i_p_l:
        plt.plot(p)
    plt.figure()
    plt.plot(f_p)
