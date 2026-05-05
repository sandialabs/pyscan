from dataclasses import dataclass
from numbers import Real
import numpy as np
from ...measurement.experiment import Experiment
from ...measurement.scans import AbstractOptimizeScan, OptimizeDeviceProperty


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
        Instrument input provided by the `measure_function` as `ItemAttribute` of the `Experiment`.
        Input for the optimizer to optimize over.
    initial_value : Real
        Initial value at which to begin the optimization routine.
    input_epsilon : Real
        Infinintesimal approximation used in finite-differencing to compute the gradient.
    learning_rate: Real
        Scaler multiplier applied to computed gradients to control the update magnitude.
    update_epsilon: Real
        Gradient update threshold.
        Optimization stops early if updates for all inputs are below thresholds.
    """
    input_epsilon: Real
    learning_rate: Real
    update_epsilon: Real


class GradientDescentOptimizeScan(AbstractOptimizeScan[GradientDescentOptimizeDeviceProperty]):
    """
    Minimizes objective function using gradient descent.
    Gradients are approximated using forward finite differences.
    Gradient descent is performed over one dimension at a time.

    Parameters
    ----------
    optimize_device_property_list : list or tuple of GradientDescentOptimizeDeviceProperty
        Data Classes containing device name, property, initial value, optimizer input,
        and any other fields needed by the optimizer
    sample_function_output : str
        Measurement output provided by the measure_function as ItemAttributes of the Experiment.
        Output for the optimizer to optimize.
    dt : float, optional
        Wait time in seconds after each iteration. Used by Experiment classes. Default is 0.
    n_max : int, optional
        Maximum number of iterations to run. Default is 100.

    Attributes
    ----------
    opt_dev_prop_l : list or tuple of OptimizeDeviceProperty
        Data Classes containing device name, property, initial value, optimizer input,
        and any other fields needed by the optimizer.
    sample_f_out : str
        Measurement output provided by the measure_function as ItemAttributes of the Experiment.
        Output for the optimizer to optimize.
    dt : float
        Wait time in seconds after each iteration. Used by Experiment classes. Default is 0.
    n_max : int or None
        Maximum number of iterations to run. Default is 100.
    scan_dict : dict of string: ndarray
        Describes and records scan sequence. For optimization scans, this records the iteration.
    i : int
        Index of current iteration.
    n : int
        Number of measurements performed, including this iteration. `i + 1`.
    n_max : int
        Maximum number of measurements that can be performed.
    running : bool
        Boolean to indicate if optimization should run the next step.
        Set to `False` in `step_optimizer` when optimization has ended.
    """

    def __init__(self, optimize_device_property_list: list[GradientDescentOptimizeDeviceProperty]
                 | tuple[GradientDescentOptimizeDeviceProperty],
                 sample_function_output: str,
                 dt: float = 0, n_max: int = 100):

        super().__init__(optimize_device_property_list,
                         sample_function_output,
                         dt=dt, n_max=n_max)

        self.dim = 0  # dim to be optimized on this pair of finite diff and grad steps
        self.fd_step = True  # for each dimension, first a finite diff and then a grad step are performed
        self.dim_ct = len(optimize_device_property_list)
        self.keep_running = np.full(self.dim_ct, True)  # stop when all gradient updates are less than epsilons

    def step_optimizer(self, index: int, experiment: Experiment) -> list[Real]:
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
        list of Real
            Next input value for each device property.
            Same as last except for updating dimension,
            which is modified for finite difference or gradient update.
        '''

        def gd_f(f_in_prev: Real, f_out: Real, f_out_prev: Real,
                 input_epsilon: Real, learning_rate: Real) -> tuple[Real, Real]:
            """
            Compute gradient update from forward finite difference.

            Parameters
            ----------
            f_in_prev : Real
                Previous value of this input to the `measure_function`.
            f_out : Real
                Output of the `measure_function`.
            f_out_prev : Real
                Previous output of the `measure_function`.
            input_epsilon : Real
                Infinintesimal approximation used in finite-differencing to compute the gradient.
            learning_rate : Real
                Scaler multiplier applied to computed gradients to control the update magnitude.

            Returns
            -------
            2-tuple of Real
                The gradient and next input for the `measure_function` at the dimension of this step.
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
