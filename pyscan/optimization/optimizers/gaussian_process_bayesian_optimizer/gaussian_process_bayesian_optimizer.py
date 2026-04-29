from collections.abc import Collection
from dataclasses import dataclass
import numpy as np
from typing import Iterable, Literal
from pyscan.general.itertools_recipes import all_equal
from pyscan.measurement.scans import AbstractOptimizeScan, OptimizeDeviceProperty, T
from pyscan.optimization.optimizers.gaussian_process_bayesian_optimizer.gp_bayes_opt import bayes_opt_main


@dataclass
class GPBayesianOptimizeDeviceProperty(OptimizeDeviceProperty):
    """
    device_name : str
        Device name.
    property_name : str
        Property of the device to be changed.
    optimizer_input : str
        Instrument input provided by the measure_function as ItemAttribute of the Experiment.
        Input for the optimizer to optimize over.
    initial_value : T
        Initial value at which to begin the optimization routine.
    domain_range : 3-Collection of T
        List of lower and upper bound pairs and increment magnitude for the property.
    initialization_scans : iterable of T, optional
        List of measurement inputs for additional pre-determined scans to be performed
        after the scan specified by `initial_value` and before the optimizer determines scan inputs.
        All provided instances of `GPBayesianOptimizeDeviceProperty` must provide an `initialization_scan` of the same length.
        Default is `None`.
    """
    domain_range: Collection[T, T, T]
    initialization_scans: Iterable[T] | None = None


class GPBayesianOptimizeScan(AbstractOptimizeScan):
    """
    Optimizes objective function using Gaussian process for Bayesian optimization.
    Bayesian optimization method `bayes_opt_main` predicts optimal next measurement from observed data.

    Parameters
    ----------
    optimize_device_property_list : iterable of GradientDescentOptimizeDeviceProperty
        List of device Data Classes containing device name, property, initial value, optimizer input,
        and any other fields needed by the optimizer
    sample_function_output : str
        Measurement output provided by the measure_function as `ItemAttributes` of the `Experiment`.
        Output for the optimizer to optimize.
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

    def __init__(self, optimize_device_property_list: Iterable[GPBayesianOptimizeDeviceProperty],
                 sample_function_output: str,
                 dt: float = 0., n_max: int = 100,
                 ei_threshold: float = 1e-1, extremum: Literal['min', 'max'] = 'min'):
        super().__init__(optimize_device_property_list,
                         sample_function_output,
                         dt=dt, n_max=n_max)
        self.last_optim_idx = n_max - 2  # stop optimizing on second-to-last index so that last index is best discovered value
        self.X_train = np.empty((1, len(optimize_device_property_list)))
        self.X_train[0] = np.array([p.initial_value for p in optimize_device_property_list])
        self.y_train = None  # TODO: multidim output? np.empty((1, 1))
        if not any([p.initialization_scans is None for p in optimize_device_property_list]):
            init_scan_lens = [len(p.initialization_scans) for p in optimize_device_property_list]
            if not all_equal(init_scan_lens):
                raise ValueError("All device properties must have initialization scans of the same length.")
            self.init_scan_ct = init_scan_lens[0]
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
            opt_in_opt = [experiment.__dict__[p.optimizer_input][arg_opt] for p in self.opt_dev_prop_l]
            self.running = False
            return opt_in_opt

        else:

            if index == 1:  # first optim step after init
                self.y_train = np.empty(1)
                self.y_train[0] = postproc_extremum(experiment.__dict__[self.sample_f_out][0], self.extremum)
            else:  # update observed data with latest optimized measurement
                i_prev = index - 1
                self.X_train = np.append(self.X_train, [[experiment.__dict__[p.optimizer_input][i_prev]
                                                         for p in self.opt_dev_prop_l]], axis=0)
                self.y_train = np.append(self.y_train,
                                         [postproc_extremum(experiment.__dict__[self.sample_f_out][i_prev],
                                                            self.extremum)], axis=0)

            if self.init_scan_ct is not None and index <= self.init_scan_ct:
                # non-optimized measurement points to intialize Gaussian process
                i_prev = index - 1  # init_scans are indexed 1 behind expt because 1st init from init_dict
                f_in_next = np.asarray([p.initialization_scans[i_prev] for p in self.opt_dev_prop_l], dtype=np.float64)
                return f_in_next
            else:  # optimize next measurement
                f_in_next, keep_running = bayes_opt_main([p.domain_range for p in self.opt_dev_prop_l],
                                                         self.X_train, self.y_train,
                                                         ei_threshold=self.ei_threshold)
                self.set_final_opt = not keep_running or not (index < self.last_optim_idx)
                return f_in_next.numpy().astype(np.float64)
