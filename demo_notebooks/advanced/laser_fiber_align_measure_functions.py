import matplotlib.pyplot as plt
from numbers import Real
import numpy as np
from time import sleep


# TODO: report pre and post raster voltages and power to Ax
# instead of pre voltages and post power?
# Configure optimize scan to report initial inputs and measurements?
# Configure measure function to report raster inputs and measurements?
def raster(devices,
           input_device_l, input_property_l,
           input_range_l,
           output_device, output_property,
           sweep_ct=1, set_delay=1., inc_delay=.01,
           vis=False, legend=False, xlabel='input', ylabel='output'):

    for _ in range(sweep_ct):
        for d, p, r in zip(input_device_l, input_property_l, input_range_l):
            devices[d][p] = r[0]
            sleep(set_delay)
            f_res = np.zeros_like(r)
            for i, v in enumerate(r):
                devices[d][p] = v
                sleep(inc_delay)
                f_res[i] = devices[output_device][output_property]
            devices[d][p] = r[np.argmax(f_res)]
            sleep(set_delay)
            if vis:
                plt.plot(r, f_res)
                plt.xlabel(xlabel)
                plt.ylabel(ylabel)
                if legend:
                    plt.legend(input_device_l,
                               loc='center left', bbox_to_anchor=(1, 0.5))
                print(np.max(f_res),
                      [devices[d][p] for d, p in zip(input_device_l, input_property_l)])


def grad_asc(devices,
             input_device_l, input_property_l,
             input_bounds_l, input_epsilon_l, learning_rate_l, update_epsilon_l,
             output_device, output_property,
             max_grad_step=100, set_delay=1., inc_delay=.1,):

    # input_l = ['x1', 'y1', 'x2', 'y2']
    input_ct = len(input_device_l)
    # bounds_l = [(-3., 3)] * input_ct
    # input_epsilon_l = [1e-3] * input_ct
    # learning_rate_l = [1e-1] * input_ct
    # update_epsilon_l = [1e-2] * input_ct

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

    sleep(set_delay)
    f_current = devices[output_device][output_property]
    keep_running = [True] * input_ct
    running = True
    for _ in range(max_grad_step):
        for d_idx, (d, p) in enumerate(zip(input_device_l, input_property_l)):
            input_current_dim = devices[d][p]
            f_in_dim_fd = input_current_dim + input_epsilon_l[d_idx]
            f_in_dim_fd, running = clamp_dev_prop(f_in_dim_fd,
                                                  input_bounds_l[d_idx])
            devices[d][p] = f_in_dim_fd
            sleep(inc_delay)
            if not running:
                break
            f_fd = devices[output_device][output_property]
            grad_dim, f_in_dim_next = gd_f(input_current_dim,
                                           f_fd, f_current,
                                           input_epsilon_l[d_idx],
                                           learning_rate_l[d_idx])
            f_in_dim_next, running = clamp_dev_prop(f_in_dim_next,
                                                    input_bounds_l[d_idx])
            devices[d][p] = f_in_dim_next
            sleep(inc_delay)
            f_current = devices[output_device][output_property]

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
            sleep(set_delay)
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


def append_measure_opt(x1m, y1m, x2m, y2m, lpm):

    opt_meas_idx = np.argmax(lpm)
    x1_opt_meas = x1m[opt_meas_idx]
    y1_opt_meas = y1m[opt_meas_idx]
    x2_opt_meas = x2m[opt_meas_idx]
    y2_opt_meas = y2m[opt_meas_idx]
    power_opt_meas = lpm[opt_meas_idx]

    x1_opt = np.append(x1m, x1_opt_meas)
    y1_opt = np.append(y1m, y1_opt_meas)
    x2_opt = np.append(x2m, x2_opt_meas)
    y2_opt = np.append(y2m, y2_opt_meas)
    power_opt = np.append(lpm, power_opt_meas)

    return x1_opt, y1_opt, x2_opt, y2_opt, power_opt
