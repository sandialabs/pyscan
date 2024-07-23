# -*- coding: utf-8 -*-
from time import sleep
import pyscan as ps
from pyscan.measurement.abstract_experiment import AbstractExperiment
from pyscan.general.is_list_type import is_list_type
import numpy as np
from datetime import datetime
import time


class Experiment(AbstractExperiment):
    '''
    Experiment class that takes data after each scan0 iteration. Inherits from
    `.AbstractExperiment`.

    Parameters
    ----------
    runinfo: :class:`pyscan.measurement.runinfo.Runinfo`
        Runinfo instance. The Runinfo scan containing the dependent variable
        that you want to average should be an instance of
        :class:`AverageScan<pyscan.measurement.scans.AverageScan>`.
        There should be only one dependent variable to be averaged.
        The scans representing independent variables can be instances of
        :class:`PropertyScan<pyscan.measurement.scans.PropertyScan>`.
    devices :
        ItemAttribute instance containing all experiment devices
    data_dir : str, optional
        The path to save the data, defaults to './backup'
    verbose: bool, optional
        Indicates whether to print status updates, defaults to `False`

    '''

    def __init__(self, runinfo, devices, data_dir=None, verbose=False, time=False):
        '''Constructor method
        '''
        super().__init__(runinfo, devices, data_dir)

        self.runinfo.time = time

    def generic_experiment(self):
        if self.runinfo.time:
            for i in range(6):
                self.runinfo['t{}'.format(i)] = np.zeros(self.runinfo.dims)

        # this var is used to track if the expt is continuous or not. Determines run behavior.
        run_count = 0

        t0 = (datetime.now()).timestamp()
        og_diff = 0
        time_diff = 0
        # Use for scan, but break if self.runinfo.running=False
        while run_count >= 0:
            if self.runinfo.continuous_expt is True:
                # st = time.time()
                print(f"Continuous experiment run {run_count} times with runtime diff {time_diff} (og diff {og_diff}).",
                      end='\r', flush=True)
                pass
            for m in range(self.runinfo.scan3.n):
                self.runinfo.scan3.i = m
                self.runinfo.scan3.iterate(m, self.devices)
                sleep(self.runinfo.scan3.dt)

                for k in range(self.runinfo.scan2.n):
                    self.runinfo.scan2.i = k
                    self.runinfo.scan2.iterate(k, self.devices)
                    sleep(self.runinfo.scan2.dt)

                    for j in range(self.runinfo.scan1.n):
                        self.runinfo.scan1.i = j
                        self.runinfo.scan1.iterate(j, self.devices)
                        sleep(self.runinfo.scan1.dt)

                        for i in range(self.runinfo.scan0.n):
                            self.runinfo.scan0.i = i
                            indicies = self.runinfo.indicies

                            if self.runinfo.time:
                                self.runinfo.t0[indicies] = (datetime.now()).timestamp()

                            self.runinfo.scan0.iterate(i, self.devices)

                            if self.runinfo.time:
                                self.runinfo.t1[indicies] = (datetime.now()).timestamp()

                            sleep(self.runinfo.scan0.dt)

                            if self.runinfo.time:
                                self.runinfo.t2[indicies] = (datetime.now()).timestamp()

                            data = self.runinfo.measure_function(self)

                            if self.runinfo.time:
                                self.runinfo.t3[indicies] = (datetime.now()).timestamp()

                            if np.all(np.array(self.runinfo.indicies) == 0) and (run_count == 0):
                                self.runinfo.measured = []
                                for key, value in data.items():
                                    self.runinfo.measured.append(key)
                                self.preallocate(data)

                            for key, value in data.items():
                                if is_list_type(self[key]):
                                    self[key][self.runinfo.indicies] = value
                                else:
                                    self[key] = value
                            if self.runinfo.time:
                                self.runinfo.t4[indicies] = (datetime.now()).timestamp()

                            if self.runinfo.continuous_expt is True:
                                self.continuous_save_point(run_count)
                            else:
                                self.save_point()

                            if self.runinfo.time:
                                self.runinfo.t5[indicies] = (datetime.now()).timestamp()

                            if self.runinfo.running is False:
                                self.runinfo.complete = 'stopped'
                                break

                        # Check if complete, stopped early
                        if self.runinfo.running is False:
                            self.runinfo.complete = 'stopped'
                            break

                    if self.runinfo.running is False:
                        self.runinfo.complete = 'stopped'
                        break

                if self.runinfo.verbose:
                    print('Scan {}/{} Complete'.format(m + 1, self.runinfo.scan3.n))
                if self.runinfo.running is False:
                    self.runinfo.complete = 'stopped'
                    break

            if self.runinfo.continuous_expt is True:
                run_count += 1
                self.runinfo.run_count = run_count
                st = time.time()
                self.reallocate()
                et = time.time()
                time_diff = et - st
                if run_count == 1:
                    og_diff = time_diff
                diff_limit = og_diff * 10
                if time_diff >= .1:
                    print(f"time diff: {diff_limit} exceeded {diff_limit} of 10x {og_diff} on run: {run_count}.")
                    run_count = -1
                    break
            else:
                run_count -= 1

        self.runinfo.complete = True
        self.runinfo.running = False

        if self.runinfo.time:
            try:
                self.runinfo.dt0 = [0] + [self.runinfo.t0[i]
                                          - self.runinfo.t0[i - 1]
                                          for i in range(1, len(self.runinfo.t0))]
            except Exception:
                pass
            self.runinfo.dt1 = self.runinfo.t1 - self.runinfo.t0
            self.runinfo.dt2 = self.runinfo.t2 - self.runinfo.t1
            self.runinfo.dt3 = self.runinfo.t3 - self.runinfo.t2
            self.runinfo.dt4 = self.runinfo.t4 - self.runinfo.t3
            self.runinfo.dt5 = self.runinfo.t5 - self.runinfo.t4
            self.runinfo.dttotal = self.runinfo.t5 - self.runinfo.t0
            self.runinfo.total_run_time = np.sum(self.runinfo.dttotal)
            self.runinfo.total_time = (datetime.now()).timestamp() - t0

        if 'end_function' in list(self.runinfo.keys()):
            self.runinfo.end_function(self)

    def average_experiment(self):
        for scan in self.runinfo.scans:
            if isinstance(scan, ps.AverageScan) and (scan.n == 1):
                print("n_average for average scan is 1. Running generic experiment instead of average experiment.")
                self.generic_experiment()
                return

        # Use for scan, but break if self.runinfo.running=False
        for m in range(self.runinfo.scan3.n):
            self.runinfo.scan3.i = m
            self.runinfo.scan3.iterate(m, self.devices)
            sleep(self.runinfo.scan3.dt)

            for k in range(self.runinfo.scan2.n):
                self.runinfo.scan2.i = k
                self.runinfo.scan2.iterate(k, self.devices)
                sleep(self.runinfo.scan2.dt)

                for j in range(self.runinfo.scan1.n):
                    self.runinfo.scan1.i = j
                    self.runinfo.scan1.iterate(j, self.devices)
                    sleep(self.runinfo.scan1.dt)

                    for i in range(self.runinfo.scan0.n):
                        self.runinfo.scan0.i = i
                        self.runinfo.scan0.iterate(i, self.devices)
                        sleep(self.runinfo.scan0.dt)

                        data = self.runinfo.measure_function(self)

                        # if on the first row of data, log the data names in self.runinfo.measured
                        if np.all(np.array(self.runinfo.indicies) == 0):
                            self.runinfo.measured = []
                            for key, value in data.items():
                                self.runinfo.measured.append(key)
                            self.preallocate(data)

                        self.rolling_average(data)

                        if self.runinfo.running is False:
                            self.runinfo.complete = 'stopped'
                            break

                        self.save_point()

                    # self.save_row()

                    # Check if complete, stopped early
                    if self.runinfo.running is False:
                        self.runinfo.complete = 'stopped'
                        break

                if self.runinfo.running is False:
                    self.runinfo.complete = 'stopped'
                    break

            print('Scan {}/{} Complete'.format(m + 1, self.runinfo.scan3.n))
            if self.runinfo.running is False:
                self.runinfo.complete = 'stopped'
                break

        self.runinfo.complete = True
        self.runinfo.running = False

        if 'end_function' in list(self.runinfo.keys()):
            self.runinfo.end_function(self)

    def rolling_average(self, data):
        '''Does a rolling average of newly measured data

        Parameters
        ----------
        data :
            ItemAttribute instance of newly measured data point
        '''
        for key, value in data.items():

            # two cases: 1. self[key] is a list 2. self[key] is not a list
            if is_list_type(self[key]):
                if is_list_type(value):
                    value = np.array(value).astype(float)

                if self.runinfo.average_index == 0:
                    self[key][self.runinfo.average_indicies] = value
                else:
                    self[key][self.runinfo.average_indicies] *= (
                        self.runinfo.average_index / (self.runinfo.average_index + 1))
                    self[key][self.runinfo.average_indicies] += (
                        value / (self.runinfo.average_index + 1))
            else:
                if self.runinfo.average_index == 0:
                    self[key] = value

                else:
                    self[key] *= (
                        self.runinfo.average_index / (self.runinfo.average_index + 1))
                    self[key] += (
                        value / (self.runinfo.average_index + 1))

    def run(self):
        '''Runs the experiment while locking the console
        '''

        self.check_runinfo()

        self.setup_instruments()
        # save instrument settings
        self.save_metadata()

        sleep(self.runinfo.initial_pause)

        self.get_time()

        self.runinfo.running = True

        if self.runinfo.average_d == -1:
            self.generic_experiment()

        elif 0 <= self.runinfo.average_d < 4:
            self.average_experiment()

        else:
            assert False, "self.average_d not setup correctly by check_runinfo method"


# legacy naming convention
class Sweep(Experiment):
    pass
