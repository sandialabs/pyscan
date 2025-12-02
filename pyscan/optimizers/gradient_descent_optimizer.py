import numpy as np
from pyscan.measurement.scans import AbstractOptimizeScan


class GradientDescentOptimizeScan(AbstractOptimizeScan):
    """
    Minimizes objective function using gradient descent.
    Gradients are approximated using forward finite differences.
    Gradient descent is performed over one dimension at a time.
    """

    def __init__(self, initialization_dict, prop, optimizer_inputs, sample_function_output,
                 input_epsilon, learning_rate, update_epsilon,
                 dt=0, n_max=100):
        super().__init__(initialization_dict, prop, optimizer_inputs, sample_function_output,
                         dt=dt, n_max=n_max)
        self.dim = 0
        self.fd_step = True
        self.input_epsilon = input_epsilon
        self.learning_rate = learning_rate
        self.update_epsilon = update_epsilon
        self.dim_ct = len(optimizer_inputs)
        self.keep_running = np.full(self.dim_ct, True)

    def step_optimizer(self, index, experiment):

        def gd_f(f_in_prev, f_out, f_out_prev, input_epsilon, learning_rate):
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
