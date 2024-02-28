# -*- coding: utf-8 -*-
import numpy as np
from time import sleep
from pyscan.general.stackorappend import stack_or_append
from pyscan.measurement.abstract_experiment import AbstractExperiment


class ChartRecorder(AbstractExperiment):
    '''Class to run single loop repeatedly.
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

    def __init__(self, runinfo, devices, data_dir=None, verbose=False):
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

        i = 0

        if self.runinfo.loop0.n == 0:
            niter = np.inf
        else:
            niter = self.runinfo.loop0.n

        while i < niter:
            self.runinfo.loop0.i = i
            self.runinfo.loop0.iterate(i, self.devices)
            sleep(self.runinfo.loop0.dt)

            data = self.runinfo.measure_function(self)

            if np.all(np.array(self.runinfo.indicies) == 0):

                for key, value in data.items():
                    self.runinfo.measured.append(key)
                    self[key] = []

                if self.runinfo.save is True:
                    self.preallocate(data)

            for key, value in data.items():
                self[key] = stack_or_append(self[key], value)

            if self.runinfo.running is False:
                self.runinfo.complete = 'stopped'
                break
            i += 1

        self.runinfo.running = False

        if 'end_function' in list(self.runinfo.keys()):
            self.runinfo.end_function(self)
