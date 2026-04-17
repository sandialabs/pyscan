from ax.api.client import Client
from ax.api.configs import RangeParameterConfig
from pyscan.measurement import AbstractOptimizeScan


class AXOptimizeScan(AbstractOptimizeScan):
    """
    AX Client API
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
        self.gi_t = global_improvement_threshold
        self.gi_i_w = global_improvement_index_window
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
                raise ValueError('Extremum must be max or min')
        self.client.configure_optimization(objective=self.objective)

        self.proposed_trial_index = None
        self.gi_latest_i = None

    def step_optimizer(self, index, experiment):

        def early_stop(f_out, f_out_best, index):
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
