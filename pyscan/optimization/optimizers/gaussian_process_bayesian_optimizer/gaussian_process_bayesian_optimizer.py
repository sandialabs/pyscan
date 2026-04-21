import numpy as np
from pyscan.measurement import AbstractOptimizeScan
from pyscan.optimization.optimizers.gaussian_process_bayesian_optimizer.gp_bayes_opt import bayes_opt_main


class GPBayesianOptimizeScan(AbstractOptimizeScan):
    """
    Optimizes objective function using Gaussian process for Bayesian optimization.
    Bayesian optimization method `bayes_opt_main` predicts optimal next measurement from observed data.

    Parameters
    ----------
    device_list : iterable of str
        List of device name strings.
    property_list : iterable of str
        List of strings that indicates the property of the device(s) to be changed.
    initialization_list : iterable of str
        List of initialization values at which to begin the optimization routine.
    optimizer_inputs : iterable of str
        Instrument inputs provided by the measure_function as `ItemAttributes` of the `Experiment`.
        Inputs for the optimizer to optimize over.
    sample_function_output : str
        Measurement output provided by the measure_function as `ItemAttributes` of the `Experiment`.
        Output for the optimizer to optimize.
    domain_range_list : iterable of 3-tuple of float
        List of lower and upper bound pairs and increment magnitude for each dimension.
    initialization_scans : iterable of iterable of float, optional
        List of measurement inputs for additional pre-determined scans to be performed
        after the scan specified by `intialization_list` and before the optimizer determines scan inputs.
        Default is `None`.
    dt : float, optional
        Wait time in seconds after each iteration. Used by `Experiment` classes. Default is `0`.
    n_max : int, optional
        Maximum number of iterations to run. Default is `100`.
    ei_threshold : float, optional
        The expected improvement threshold below which optimization is stopped.
        Default is `1e-1`.
    extremum : {'min', 'max'}, optional
        Determines extremum to optimize for. Set to `'min'` or `'max'`. Default is `'max'`.
    """

    def __init__(self, device_list, property_list, initialization_list, optimizer_inputs,
                 sample_function_output,
                 domain_range_list,
                 initialization_scans=None,
                 dt=0., n_max=100,
                 ei_threshold=1e-1, extremum='min'):
        super().__init__(device_list, property_list, initialization_list, optimizer_inputs,
                         sample_function_output,
                         dt=dt, n_max=n_max)
        self.last_optim_idx = n_max - 2  # stop optimizing on second-to-last index so that last index is best discovered value
        self.domain = domain_range_list
        self.X_train = np.empty((1, len(initialization_list)))
        self.X_train[0] = np.array(initialization_list)
        self.y_train = None  # TODO: multidim output? np.empty((1, 1))
        self.init_scans = initialization_scans
        if self.init_scans is not None:
            self.init_scan_ct = len(self.init_scans)
        else:
            self.init_scan_ct = None
        self.extremum = extremum
        self.ei_threshold = ei_threshold
        self.set_final_opt = False

    def step_optimizer(self, index, experiment):
        """
        Performs global optimization step using `bayes_opt_main` from `gp_bayes_opt`.
        Calculates expected improvement and determines whether optimization should continue.
        Returns the best point so far if optimization stops.
        Loads the data of all previous samples into `bayes_opt_main`
        to compute the next sample point and expected improvement.
        Returns the next point to sample.

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
        """

        def postproc_extremum(y, extremum):
            match extremum:
                case 'max':
                    return y
                case 'min':
                    return -y
                case _:
                    raise ValueError('Extremum must be max or min')

        def get_arg_opt(y, extremum):
            match extremum:
                case 'max':
                    return np.argmax(y)
                case 'min':
                    return np.argmin(y)
                case _:
                    raise ValueError('Extremum must be max or min')

        if self.set_final_opt:  # set final output to best observed output
            arg_opt = get_arg_opt(experiment.__dict__[self.sample_f_out][:index], self.extremum)
            opt_in_opt = [experiment.__dict__[measurement][arg_opt] for measurement in self.opt_in]
            self.running = False
            return opt_in_opt

        else:

            if index == 1:  # first optim step after init
                self.y_train = np.empty(1)
                self.y_train[0] = postproc_extremum(experiment.__dict__[self.sample_f_out][0], self.extremum)
            else:  # update observed data with latest optimized measurement
                i_prev = index - 1
                self.X_train = np.append(self.X_train, [[experiment.__dict__[measurement][i_prev]
                                                         for measurement in self.opt_in]], axis=0)
                self.y_train = np.append(self.y_train,
                                         [postproc_extremum(experiment.__dict__[self.sample_f_out][i_prev],
                                                            self.extremum)], axis=0)

            if self.init_scan_ct is not None and index <= self.init_scan_ct:
                # non-optimized measurement points to intialize Gaussian process
                i_prev = index - 1  # init_scans are indexed 1 behind expt because 1st init from init_dict
                f_in_next = self.init_scans[i_prev]
                return f_in_next
            else:  # optimize next measurement
                f_in_next, keep_running = bayes_opt_main(self.domain, self.X_train, self.y_train,
                                                         ei_threshold=self.ei_threshold)
                self.set_final_opt = not keep_running or not (index < self.last_optim_idx)
                return f_in_next.numpy().astype(np.float64)
