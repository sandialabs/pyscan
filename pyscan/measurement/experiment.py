
from time import sleep
from .abstract_experiment import AbstractExperiment
from ..general.is_list_type import is_list_type
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
    generic_experiment()
    average_experiment()
    rolling_average(data)
    run()
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

        for indicies, deltas in delta_product(self.runinfo.dims):
            for scan, i, d in zip(self.runinfo.scans[::-1], indicies[::-1], deltas[::-1]):
                scan.iterate(self, i, d)

            data = self.runinfo.measure_function(self)

            if np.all(np.array(indicies) == 0):
                self.preallocate(data)
            elif self.runinfo.continuous:
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

    # def average_experiment(self):

    #     for indicies, deltas in delta_product(self.runinfo.dims):
    #         for scan, i, d in zip(self.runinfo.scans[::-1], indicies[::-1], deltas[::-1]):
    #             scan.iterate(self, i, d)

    #             data = self.runinfo.measure_function(self)

    #             if np.all(indicies == 0):
    #                 self.preallocate(data)

    #             self.rolling_average(data)

    #             self.save_point(data)

    #             if self.runinfo.running is False:
    #                 self.runinfo.complete = 'stopped'
    #                 break

    #     self.runinfo.complete = True
    #     self.runinfo.running = False

    #     if 'end_function' in list(self.runinfo.keys()):
    #         self.runinfo.end_function(self)

    def rolling_average(self, data):
        '''
        Does a rolling average of newly measured data

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
