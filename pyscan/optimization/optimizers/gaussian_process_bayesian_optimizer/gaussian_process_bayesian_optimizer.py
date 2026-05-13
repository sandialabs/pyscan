from collections.abc import Sequence
from dataclasses import dataclass, field
from numbers import Real
import numpy as np
from typing import Literal
from ....general.itertools_recipes import all_equal
from ....measurement.experiment import Experiment
from ....measurement.scans import AbstractOptimizeScan, OptimizeDeviceProperty
from .gp_bayes_opt import bayes_opt_main


@dataclass
class GPBayesianOptimizeDeviceProperty(OptimizeDeviceProperty):
    """
    Data Class with the fields needed to describe a device property for Gaussian process Bayesian optimization.

    Parameters
    ----------
    device_name : str
        Device name.
    property_name : str
        Property of the device to be changed.
    initial_value : Real
        Initial value at which to begin the optimization routine.
    domain_range : 3-tuple of Real
        Lower bound, upper bound, and increment magnitude for the property.
    optimizer_input : str, optional
        Instrument input provided by the `measure_function` as `ItemAttribute` of the `Experiment`.
        Input for the optimizer to optimize over.
        Default is `None`.
    initialization_scans : Sequence of Real, optional
        Measurement inputs for additional pre-determined scans to be performed
        after the scan specified by `initial_value` and before the optimizer determines scan inputs.
        All provided instances of `GPBayesianOptimizeDeviceProperty` must provide an `initialization_scan` of the same length.
        The initialization scans are only performed if each `GPBayesianOptimizeDeviceProperty` has an `initialization_scan`
        that is not `None`.
        Default is `None`.
    """
    domain_range: tuple[Real, Real, Real]
    initialization_scans: Sequence[Real] | None = field(default=None, kw_only=True)


class GPBayesianOptimizeScan(AbstractOptimizeScan[GPBayesianOptimizeDeviceProperty]):
    """
    Optimizes objective function using Gaussian process for Bayesian optimization.
    Bayesian optimization method `bayes_opt_main` predicts optimal next measurement from observed data.

    Parameters
    ----------
    optimize_device_property_list : Sequence of GPBayesianOptimizeDeviceProperty
        Data Classes containing device name, property, initial value, optimizer input,
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
    extremum : `{'min', 'max'}`, optional
        Determines extremum to optimize for. Set to `'min'` or `'max'`. Default is `'max'`.

    Attributes
    ----------
    opt_dev_prop_l : Sequence of OptimizeDeviceProperty
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
    ei_threshold : float
        The expected improvement threshold below which optimization is stopped.
        Default is `1e-1`.
    extremum : `{'min', 'max'}`
        Determines extremum to optimize for. Set to `'min'` or `'max'`. Default is `'max'`.
    """

    def __init__(self, optimize_device_property_list: Sequence[GPBayesianOptimizeDeviceProperty],
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
        self.set_final_opt = False  # Set True when opt terminates, final step sets inputs to best discovered value

    def step_optimizer(self, index: int, experiment: Experiment) -> list[Real]:
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
        list of Real
            Next input value for each device property.
        """

        def postproc_extremum(y: Real, extremum: str) -> Real:
            match extremum:
                case 'max':
                    return y
                case 'min':
                    return -y
                case _:
                    raise ValueError('Extremum must be max or min')

        def get_arg_opt(y: np.ndarray[Real], extremum: str) -> int:
            match extremum:
                case 'max':
                    return np.argmax(y)
                case 'min':
                    return np.argmin(y)
                case _:
                    raise ValueError('Extremum must be max or min')

        if self.set_final_opt:  # set final output to best observed output
            arg_opt = get_arg_opt(experiment.__dict__[self.sample_f_out][:index], self.extremum)
            opt_in_opt = [experiment.__dict__[p.experiment_key][arg_opt] for p in self.opt_dev_prop_l]
            self.running = False
            return opt_in_opt

        else:

            if index == 1:  # first optim step after init
                self.y_train = np.empty(1)
                self.y_train[0] = postproc_extremum(experiment.__dict__[self.sample_f_out][0], self.extremum)
            else:  # update observed data with latest optimized measurement
                i_prev = index - 1
                self.X_train = np.append(self.X_train, [[experiment.__dict__[p.experiment_key][i_prev]
                                                         for p in self.opt_dev_prop_l]], axis=0)
                self.y_train = np.append(self.y_train,
                                         [postproc_extremum(experiment.__dict__[self.sample_f_out][i_prev],
                                                            self.extremum)], axis=0)

            if self.init_scan_ct is not None and index <= self.init_scan_ct:
                # non-optimized measurement points to intialize Gaussian process
                i_prev = index - 1  # init_scans are indexed 1 behind expt because 1st init from init_dict
                f_in_next = [p.initialization_scans[i_prev] for p in self.opt_dev_prop_l]
                return f_in_next  # initialization scan could be None, constructor checks for this
            else:  # optimize next measurement
                f_in_next, keep_running = bayes_opt_main([p.domain_range for p in self.opt_dev_prop_l],
                                                         self.X_train, self.y_train,
                                                         ei_threshold=self.ei_threshold)
                self.set_final_opt = not keep_running or not (index < self.last_optim_idx)
                return f_in_next.numpy().astype(np.float64).tolist()
