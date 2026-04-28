from dataclasses import dataclass
import numpy as np
from typing import Iterable
from pyscan.measurement.scans import AbstractOptimizeScan, OptimizeDeviceProperty, T


@dataclass
class GradientDescentOptimizeDeviceProperty(OptimizeDeviceProperty):
    """
    Data Class with the fields needed to describe a device property for gradient descent optimization.

    Parameters
    ----------
    device_name : str
        Device name.
    property_name : str
        Property of the device to be changed.
    optimizer_input : str
        Instrument input provided by the measure_function as ItemAttribute of the Experiment.
        Input for the optimizer to optimize over.
    initial_value : T
        Initial value at which to begin the optimization routine.
    input_epsilon : T
        Infinintesimal approximation used in finite-differencing to compute the gradient.
    learning_rate: T
        Scaler multiplier applied to computed gradients to control the update magnitude.
    update_epsilon: T
        Gradient update threshold.
        Optimization stops early if updates for all inputs are below thresholds.
    """
    input_epsilon: T
    learning_rate: T
    update_epsilon: T


class GradientDescentOptimizeScan(AbstractOptimizeScan):
    """
    Minimizes objective function using gradient descent.
    Gradients are approximated using forward finite differences.
    Gradient descent is performed over one dimension at a time.

    Parameters
    ----------
    optimize_device_property_list : iterable of GradientDescentOptimizeDeviceProperty
        List of device Data Classes containing device name, property, initial value, optimizer input,
        and any other fields needed by the optimizer
    sample_function_output : str
        Measurement output provided by the measure_function as ItemAttributes of the Experiment.
        Output for the optimizer to optimize.
    dt : float, optional
        Wait time in seconds after each iteration. Used by Experiment classes. Default is 0.
    n_max : int, optional
        Maximum number of iterations to run. Default is 100.
    """

    def __init__(self, optimize_device_property_list: Iterable[GradientDescentOptimizeDeviceProperty],
                 sample_function_output: str,
                 dt: float = 0, n_max: int = 100):

        super().__init__(optimize_device_property_list,
                         sample_function_output,
                         dt=dt, n_max=n_max)

        self.dim = 0
        self.fd_step = True
        self.dim_ct = len(optimize_device_property_list)
        self.keep_running = np.full(self.dim_ct, True)

    def step_optimizer(self, index, experiment):
        '''
        Performs gradient descent using finite differencing.
        Iterates over all input dimensions.
        Returns next measurement first based on finite difference approximation
        and then based on the resulting gradient update.

        Parameters
        ----------
        index : int
            The index of the data array.
        experiment : Experiment
            `Experiment` class specifying configuration of runinfo and devices.

        Returns
        -------
        ndarray
            Array with elements containing next input value for each device property.
            Same as last except for updating dimension,
            which is modified for finite difference or gradient update.
        '''

        def gd_f(f_in_prev, f_out, f_out_prev, input_epsilon, learning_rate):
            """
            Compute gradient update from forward finite difference
            """
            grad = (f_out - f_out_prev) / input_epsilon
            grad_update = learning_rate * grad
            f_in_dim_next = f_in_prev - grad_update
            return grad, f_in_dim_next

        if self.fd_step:
            f_in = [experiment.__dict__[p.optimizer_input][index - 1] for p in self.opt_dev_prop_l]
            f_in[self.dim] += self.opt_dev_prop_l[self.dim].input_epsilon
            self.fd_step = False
            return f_in
        else:
            f_in_prev = [experiment.__dict__[p.optimizer_input][index - 2] for p in self.opt_dev_prop_l]
            f_out = experiment.__dict__[self.sample_f_out][index - 1]
            f_out_prev = experiment.__dict__[self.sample_f_out][index - 2]
            grad_dim, f_in_next_dim = gd_f(f_in_prev[self.dim], f_out, f_out_prev,
                                           self.opt_dev_prop_l[self.dim].input_epsilon,
                                           self.opt_dev_prop_l[self.dim].learning_rate)
            f_in_next = f_in_prev.copy()
            f_in_next[self.dim] = f_in_next_dim
            self.keep_running[self.dim] = abs(grad_dim) > self.opt_dev_prop_l[self.dim].update_epsilon
            if not self.keep_running.any():
                self.running = False
            self.fd_step = True
            self.dim += 1
            self.dim %= self.dim_ct
            return f_in_next
