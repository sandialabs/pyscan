# -*- coding: utf-8 -*-
from time import sleep
from pyscan.measurement.abstract_experiment import AbstractExperiment
from pyscan.general.is_list_type import is_list_type
import numpy as np
from datetime import datetime


class RasterExperiment(AbstractExperiment):
    '''Experiment class that takes data after each loop0 iteration but reverses
    loop0's direction after each loop1 iteration.
    It inherits from :class:`pyscan.measurement.abstract_experiment.AbstractExperiment`.

    Parameters
    ----------
    runinfo: :class:`pyscan.measurement.runinfo.Runinfo`
        Runinfo instance. The Runinfo loop containing the dependent variable
        that you want to average should be an instance of
        :class:`AverageScan<pyscan.measurement.scans.AverageScan>`.
        There should be only one dependent variable to be averaged.
        The loops representing independent variables can be instances of
        :class:`PropertyScan<pyscan.measurement.scans.PropertyScan>`.
    devices :
        ItemAttribute instance containing all experiment devices
    data_dir : str, optional
        The path to save the data, defaults to './backup'
    verbose: bool, optional
        Indicates whether to print status updates, defaults to `False`

    '''

    def __init__(self, runinfo, devices, data_dir=None, verbose=False, time=False):
        super().__init__(runinfo, devices, data_dir)

        self.runinfo.time = time

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

        if self.runinfo.time:
            for i in range(6):
                self.runinfo['t{}'.format(i)] = np.zeros(self.runinfo.dims)

        t0 = (datetime.now()).timestamp()
        # Use for loop, but break if self.runinfo.running=False
        for m in range(self.runinfo.loop3.n):
            self.runinfo.loop3.i = m
            self.runinfo.loop3.iterate(m, self.devices)
            sleep(self.runinfo.loop3.dt)

            for k in range(self.runinfo.loop2.n):
                self.runinfo.loop2.i = k
                self.runinfo.loop2.iterate(k, self.devices)
                sleep(self.runinfo.loop2.dt)

                for j in range(self.runinfo.loop1.n):
                    self.runinfo.loop1.i = j
                    self.runinfo.loop1.iterate(j, self.devices)
                    sleep(self.runinfo.loop1.dt)

                    if j % 2 == 0:
                        range0D = range(self.runinfo.loop0.n)
                    else:
                        range0D = reversed(range(self.runinfo.loop0.n))
                    for i in range0D:
                        self.runinfo.loop0.i = i
                        indicies = self.runinfo.indicies

                        if self.runinfo.time:
                            self.runinfo.t0[indicies] = (datetime.now()).timestamp()

                        self.runinfo.loop0.iterate(i, self.devices)

                        if self.runinfo.time:
                            self.runinfo.t1[indicies] = (datetime.now()).timestamp()

                        sleep(self.runinfo.loop0.dt)

                        if self.runinfo.time:
                            self.runinfo.t2[indicies] = (datetime.now()).timestamp()

                        data = self.runinfo.measure_function(self)

                        if self.runinfo.time:
                            self.runinfo.t3[indicies] = (datetime.now()).timestamp()

                        if np.all(np.array(self.runinfo.indicies) == 0):
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
                print('Scan {}/{} Complete'.format(m + 1, self.runinfo.loop3.n))
            if self.runinfo.running is False:
                self.runinfo.complete = 'stopped'
                break

        self.runinfo.complete = True
        self.runinfo.running = False

        if self.runinfo.time:
            try:
                self.runinfo.dt0 = [0] + [self.runinfo.t0[i]
                                          - self.runinfo.t0[i - 1]
                                          for i in range(1, len(self.runinfo.t0))]
            except:
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


# legacy naming convention
class RasterSweep(RasterExperiment):
    pass
