
from time import sleep
from .abstract_experiment import AbstractExperiment
from ..general.delta_product import delta_product
import numpy as np


class Experiment(AbstractExperiment):
    '''
    Experiment class that takes data after each scan0 iteration.

    Parameters
    ----------
    runinfo : ps.RunInfo instance
        Contains all information about the experiment
    devices : ItemAttribute instance
        ItemAttribute instance containing all experiment devices
    data_dir : str, optional
        The path to save the data, defaults to './backup'
    verbose: bool, optional
        Indicates whether to print status updates, defaults to `False`

    Methods
    -------
    start_thread()
    run()
    stop()
    '''

    def __init__(self, runinfo, devices, data_dir=None, verbose=False, time=False):
        '''
        Constructor method
        '''
        super().__init__(runinfo, devices, data_dir)

    def run(self):

        self.check_runinfo()

        self.save_metadata('runinfo')
        self.save_metadata('devices')

        sleep(self.runinfo.initial_pause)

        self.runinfo.running = True

        for indicies, deltas in delta_product(self.runinfo.iterators, self.runinfo.has_continuous_scan):
            for scan, i, d in zip(self.runinfo.scans[::-1], indicies[::-1], deltas[::-1]):
                scan.iterate(self, i, d)

            data = self.runinfo.measure_function(self)

            if np.all(np.array(indicies) == 0):
                self.preallocate(data)
            elif (self.runinfo.has_continuous_scan) and (deltas[-1] == 1):
                self.reallocate(data)
            elif self.runinfo.has_average_scan:
                self.rolling_average(data)

            self.save_point(data)

            if self.runinfo.running is False:
                self.runinfo.complete = 'stopped'
                break

        self.runinfo.complete = True
        self.runinfo.running = False

        if 'end_function' in list(self.runinfo.keys()):
            self.runinfo.end_function(self)
