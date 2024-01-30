# -*- coding: utf-8 -*-
import numpy as np
from time import sleep
from pyscan.general.islisttype import is_list_type
from pyscan.measurement.metasweep import MetaSweep


class AverageSweep(MetaSweep):
    '''Experiment class that takes data after each runinfo.loop0 iteration and averages over
    the loop containing an `.AverageScan` instance
    It inherits from `.MetaSweep`.

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

        super().__init__(runinfo, devices, data_dir)

    def run(self):
        '''Runs the experiment while locking the console
        '''

        self.check_runinfo()
        assert -1 < self.runinfo.average_d < 4, "Averagesweep didn't register an averagescan with its runinfo average_d"

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
                        self.runinfo.loop0.iterate(i, self.devices)
                        sleep(self.runinfo.loop0.dt)

                        data = self.runinfo.measure_function(self)

                        # if on the first row of data, log the data names in self.runinfo.measured
                        if np.all(np.array(self.runinfo.indicies) == 0):
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

            print('Scan {}/{} Complete'.format(m + 1, self.runinfo.loop3.n))
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
