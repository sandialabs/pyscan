# -*- coding: utf-8 -*-
from time import sleep
from pyscan.measurement.abstract_experiment import AbstractExperiment
from pyscan.general.is_list_type import is_list_type
import numpy as np


class SparseExperiment(AbstractExperiment):
    '''Experiment class that takes data after each loop0 iteration if
    runinfo.sparse_points[self.runinfo.indicies] = 1, allowing the experiment
    to skip taking data points. Inherits from :class:`pyscan.measurement.abstract_experiment.AbstractExperiment`.

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

    def __init__(self, runinfo, devices, data_dir=None, verbose=False):
        '''Constructor method
        '''
        super().__init__(runinfo, devices, data_dir)

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

                    for i in range(self.runinfo.loop0.n):
                        self.runinfo.loop0.i = i
                        sample = self.runinfo.sparse_points[self.runinfo.indicies]

                        if (sample) or (np.all(np.array(self.runinfo.indicies) == 0)):
                            self.runinfo.loop0.iterate(i, self.devices)
                            sleep(self.runinfo.loop0.dt)

                            data = self.runinfo.measure_function(self)
                            if np.all(np.array(self.runinfo.indicies) == 0):
                                for key in data.keys():
                                    self.runinfo.measured.append(key)
                                self.preallocate(data)

                            if sample:
                                for key, value in data.items():
                                    if is_list_type(self[key]):
                                        self[key][self.runinfo.indicies] = value
                                    else:
                                        self[key] = value

                                self.save_point()

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

        if 'end_function' in list(self.runinfo.keys()):
            self.runinfo.end_function(self)


# legacy naming convention
class SparseSweep(SparseExperiment):
    pass
