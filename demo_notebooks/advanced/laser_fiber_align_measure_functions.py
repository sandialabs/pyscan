import matplotlib.pyplot as plt
from numbers import Real
import numpy as np
from time import sleep

import pyscan as ps


# TODO: report pre and post raster voltages and power to Ax
# instead of pre voltages and post power?
# Configure optimize scan to report initial inputs and measurements?
# Configure measure function to report raster inputs and measurements?
def raster(devices, sweep_ct=1, vis=False):

    input_range = ps.drange(-3, 0.01, 3)
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
            if vis:
                plt.plot(input_range, f_res)
                plt.xlabel("axis voltage")
                plt.ylabel("laser power")
                print(np.max(f_res),
                      devices.x1.voltage,
                      devices.y1.voltage,
                      devices.x2.voltage,
                      devices.y2.voltage)


def grad_asc(devices):

    max_grad_step = 100
    input_l = ['x1', 'y1', 'x2', 'y2']
    input_ct = len(input_l)
    bounds_l = [(-3., 3)] * input_ct
    input_epsilon_l = [1e-3] * input_ct
    learning_rate_l = [1e-1] * input_ct
    update_epsilon_l = [1e-2] * input_ct

    def gd_f(f_in_prev: Real, f_out: Real, f_out_prev: Real,
             input_epsilon: Real, learning_rate: Real) -> tuple[Real, Real]:
        grad = (f_out - f_out_prev) / input_epsilon
        grad_update = learning_rate * grad
        f_in_dim_next = f_in_prev + grad_update
        return grad, f_in_dim_next

    def clamp_dev_prop(f_in: Real, bounds: tuple[Real, Real]):
        running = True
        # if bounds is not None:
        lb, ub = bounds
        el = f_in < lb  # exceeds lower bound
        eu = f_in > ub  # exceeds upper bound
        if el or eu:
            running = False
            if el:
                f_in = lb
            elif eu:
                f_in = ub
        return f_in, running

    # i_p_l = [[devices[d].voltage] for d in input_l]
    # f_p = [devices.pm16_120.power]

    sleep(1)
    f_current = devices.pm16_120.power
    keep_running = [True] * input_ct
    running = True
    for i in range(max_grad_step):
        for d_idx, d in enumerate(input_l):
            input_current_dim = devices[d].voltage
            f_in_dim_fd = input_current_dim + input_epsilon_l[d_idx]
            f_in_dim_fd, running = clamp_dev_prop(f_in_dim_fd,
                                                  bounds_l[d_idx])
            devices[d].voltage = f_in_dim_fd
            sleep(.1)
            if not running:
                break
            f_fd = devices.pm16_120.power
            grad_dim, f_in_dim_next = gd_f(input_current_dim,
                                           f_fd, f_current,
                                           input_epsilon_l[d_idx],
                                           learning_rate_l[d_idx])
            f_in_dim_next, running = clamp_dev_prop(f_in_dim_next,
                                                    bounds_l[d_idx])
            devices[d].voltage = f_in_dim_next
            sleep(.1)
            f_current = devices.pm16_120.power

            # for p_idx, p in enumerate(i_p_l):
            #     p.append(devices[input_l[p_idx]].voltage)
            # f_p.append(f_current)

            if not running:
                break

            # print(i)
            # print(d_idx)
            # print(abs(grad_dim))
            # print(update_epsilon_l[d_idx])

            keep_running[d_idx] = abs(grad_dim) > update_epsilon_l[d_idx]
            if not any(keep_running):
                running = False
                break
        if not running:
            sleep(1)
            break

    # plt.figure()
    # for p in i_p_l:
    #     plt.plot(p)
    # plt.figure()
    # plt.plot(f_p)


def get_measure_opt(devices, x1m, y1m, x2m, y2m, lpm):

    opt_meas_idx = np.argmax(lpm)
    x1_opt_meas = x1m[opt_meas_idx]
    y1_opt_meas = y1m[opt_meas_idx]
    x2_opt_meas = x2m[opt_meas_idx]
    y2_opt_meas = y2m[opt_meas_idx]

    devices.x1.voltage = x1_opt_meas
    devices.y1.voltage = y1_opt_meas
    devices.x2.voltage = x2_opt_meas
    devices.y2.voltage = y2_opt_meas
    sleep(1)
    power_opt_meas = devices.pm16_120.power

    x1_opt = np.append(x1m, x1_opt_meas)
    y1_opt = np.append(y1m, y1_opt_meas)
    x2_opt = np.append(x2m, x2_opt_meas)
    y2_opt = np.append(y2m, y2_opt_meas)
    power_opt = np.append(lpm, power_opt_meas)

    return x1_opt, y1_opt, x2_opt, y2_opt, power_opt
