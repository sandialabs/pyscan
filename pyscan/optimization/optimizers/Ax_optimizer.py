from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
from pyscan.measurement import AbstractOptimizeScan


class AxOptimizeScan(AbstractOptimizeScan):
    """
    Global optimization routine using Ax Client API.
    Minimizes objective function using Bayesian optimization.

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
    bounds_list : iterable of 2-tuple of float
        List of lower and upper bound pairs for each dimension.
    initialization_scans : iterable of iterable of float, optional
        List of measurement inputs for additional pre-determined scans to be performed
        after the scan specified by `intialization_list` and before the optimizer determines scan inputs.
        Default is `None`.
    dt : float, optional
        Wait time in seconds after each iteration. Used by `Experiment` classes. Default is `0`.
    n_max : int, optional
        Maximum number of iterations to run. Default is `100`.
    global_imporvement_threshold : float, optional
        Positive threshold of improvement magnitude below which optimization is stopped. Default is `1e-2`.
    global_improvement_index_window: int, optional
        Nonnegative number of consecutive iterations that must have improvement below threshold before optimization is stopped.
        Default is `10`.
    global_improvement_start_index : int, optional
        Nonnegative number of iterations to guarantee are performed.
        If `global_index_window` consecutive iterations are below `global_improvement_threshold`,
        but the index is lower than `global_improvement_start_index`, then optimization will continue.
    extremum : {'min', 'max'}, optional
        Determines extremum to optimize for. Set to `'min'` or `'max'`. Default is `'max'`.
    """

    def __init__(self, device_list, property_list, initialization_list, optimizer_inputs,
                 sample_function_output,
                 bounds_list,
                 initialization_scans=None,
                 dt=0., n_max=100,
                 global_improvement_threshold=1e-2,
                 global_improvement_index_window=10,
                 global_improvement_start_index=10,
                 extremum='min'):

        super().__init__(device_list, property_list, initialization_list, optimizer_inputs,
                         sample_function_output,
                         dt=dt, n_max=n_max)

        self.init_scans = initialization_scans
        if self.init_scans is not None:  # additional non-optimized init pts after init_dict
            self.init_scan_ct = len(self.init_scans)  # idx to expt 1 after len for init_dict
            self.complete_last_init_idx = self.init_scan_ct + 1  # 2 after len to complete last
        else:
            self.init_scan_ct = None
            self.complete_last_init_idx = None
        self.last_optim_idx = n_max - 1
        if global_improvement_threshold <= 0.:
            raise ValueError("global_improvement_threshold must be positive.")
        self.gi_t = global_improvement_threshold
        if global_improvement_index_window < 0:
            raise ValueError("global_improvement_index_window must be nonnegative.")
        self.gi_i_w = global_improvement_index_window
        if global_improvement_start_index < 0:
            raise ValueError("global_improvement_start_index must be nonnegative.")
        self.gi_st_i = global_improvement_start_index
        self.extremum = extremum
        parameters = [
            RangeParameterConfig(name=self.opt_in[i], parameter_type="float", bounds=bounds_list[i])
            for i in range(len(self.opt_in))
        ]
        self.client = Client()
        self.client.configure_experiment(parameters=parameters)
        match extremum:
            case 'max':
                self.objective = f"{self.sample_f_out}"
            case 'min':
                self.objective = f"-{self.sample_f_out}"
            case _:
                raise ValueError('extremum must be \'max\' or \'min\'.')
        self.client.configure_optimization(objective=self.objective)

        self.proposed_trial_index = None
        self.gi_latest_i = None

    def step_optimizer(self, index, experiment):
        """
        Performs global optimization step using Ax Client API.
        Compares new objective function result with previous best and determines whether optimization should continue.
        Returns the best point so far if optimization stops.
        Loads a pre-initialized point or the results of the last proposed trial into the client.
        Requests and returns the next point to sample from the client.

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

        def early_stop(f_out, f_out_best, index):
            """
            Global early stopping routine.
            """
            es = False
            gi_d = f_out - f_out_best
            if self.extremum == 'min':
                gi_d *= -1
            delta_over_threshold = gi_d > self.gi_t
            if delta_over_threshold:
                self.gi_latest_i = index
            if self.gi_latest_i is not None:
                gi_i_d = index - self.gi_latest_i
                index_delta_out_window = gi_i_d >= self.gi_i_w
                stop_checking_started = index >= self.gi_st_i
                es = index_delta_out_window and stop_checking_started
            return es

        i_prev = index - 1

        if index == 1 \
            or (self.init_scan_ct is not None
                and index <= self.complete_last_init_idx):
            # load init pts into Client
            parameters = {
                measurement: experiment.__dict__[measurement][i_prev]
                for measurement in self.opt_in
            }
            prev_trial_index = self.client.attach_trial(parameters=parameters)
            f_out = experiment.__dict__[self.sample_f_out][i_prev]
            raw_data = {self.sample_f_out: f_out}
            self.client.complete_trial(trial_index=prev_trial_index, raw_data=raw_data)
        else:
            # load last proposed trial results into Client
            best_parameters, best_prediction, best_index, best_name \
                = self.client.get_best_parameterization(use_model_predictions=False)  # best before prev
            prev_trial_index = self.proposed_trial_index
            f_out = experiment.__dict__[self.sample_f_out][i_prev]
            raw_data = {self.sample_f_out: f_out}
            self.client.complete_trial(trial_index=prev_trial_index, raw_data=raw_data)
            f_out_best = best_prediction[self.sample_f_out][0]  # get mean from (mean, sem) of output
            if index >= self.last_optim_idx or early_stop(f_out, f_out_best, index):
                # if last optim: return best param and stop optim
                f_in_next = [
                    best_parameters[measurement]
                    for measurement in self.opt_in
                ]
                self.running = False
                # print(f"best param: {best_parameters}")
                return f_in_next

        if self.init_scan_ct is not None \
                and index <= self.init_scan_ct:
            # get next point from init_scans
            f_in_next = self.init_scans[i_prev]  # init_scans idx 1 behind expt for init_dict
            return f_in_next
        else:
            # get next point from Client
            trials = self.client.get_next_trials(max_trials=1)  # only 1 trial
            for trial_index, parameters in trials.items():  # only 1 item
                f_in_next = [
                    parameters[measurement]
                    for measurement in self.opt_in
                ]
                self.proposed_trial_index = trial_index
            return f_in_next
