import numpy as np
from pyscan.measurement.scans import AbstractOptimizeScan


class GradientDescentOptimizeScan(AbstractOptimizeScan):
    """
    Minimizes objective function using gradient descent.
    Gradients are approximated using forward finite differences.
    Gradient descent is performed over one dimension at a time.

    Parameters
    ----------
    device_list : iterable of str
        List of device name strings.
    property_list : iterable of str
        List of strings that indicates the property of the device(s) to be changed.
    initialization_list : iterable of str
        List of initialization values at which to begin the optimization routine.
    optimizer_inputs : iterable of str
        Instrument inputs provided by the measure_function as ItemAttributes of the Experiment.
        Inputs for the optimizer to optimize over.
    sample_function_output : str
        Measurement output provided by the measure_function as ItemAttributes of the Experiment.
        Output for the optimizer to optimize.
    input_epsilon : iterable of float
        Infinintesimal approximation on each input used in finite-differencing to compute the gradient.
    learning_rate: iterable of float
        Scaler multiplier applied to computed gradients on each input to control the update magnitude.
    update_epsilon: iterable of float
        Gradient update threshold for each input.
        Optimization stops early if updates for all inputs are below thresholds.
    dt : float, optional
        Wait time in seconds after each iteration. Used by Experiment classes. Default is 0.
    n_max : int, optional
        Maximum number of iterations to run. Default is 100.
    """

    def __init__(self, device_list, property_list, initialization_list, optimizer_inputs,
                 sample_function_output,
                 input_epsilon, learning_rate, update_epsilon,
                 dt=0, n_max=100):

        super().__init__(device_list, property_list, initialization_list, optimizer_inputs,
                         sample_function_output,
                         dt=dt, n_max=n_max)

        self.dim = 0
        self.fd_step = True
        self.input_epsilon = input_epsilon
        self.learning_rate = learning_rate
        self.update_epsilon = update_epsilon
        self.dim_ct = len(optimizer_inputs)
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
        experiment : AbstractExperiment
            Experiment class specifying configuration of runinfo and devices.

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
            f_in = [experiment.__dict__[measurement][index - 1] for measurement in self.opt_in]
            f_in[self.dim] += self.input_epsilon[self.dim]
            self.fd_step = False
            return f_in
        else:
            f_in_prev = [experiment.__dict__[measurement][index - 2] for measurement in self.opt_in]
            f_out = experiment.__dict__[self.sample_f_out][index - 1]
            f_out_prev = experiment.__dict__[self.sample_f_out][index - 2]
            grad_dim, f_in_next_dim = gd_f(f_in_prev[self.dim], f_out, f_out_prev,
                                           self.input_epsilon[self.dim], self.learning_rate[self.dim])
            f_in_next = f_in_prev.copy()
            f_in_next[self.dim] = f_in_next_dim
            self.keep_running[self.dim] = abs(grad_dim) > self.update_epsilon[self.dim]
            if not self.keep_running.any():
                self.running = False
            self.fd_step = True
            self.dim += 1
            self.dim %= self.dim_ct
            return f_in_next
