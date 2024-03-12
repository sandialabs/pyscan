# -*- coding: utf-8 -*-
from time import sleep
from pyscan.measurement.abstract_experiment import AbstractExperiment
from pyscan.general.item_attribute import ItemAttribute
import numpy as np
# import nidaqmx


class FastGalvoExperiment(AbstractExperiment):
    '''Setup a point by point measurement.
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
        '''Constructor method
        '''
        super().__init__(runinfo, devices, data_dir)

        self.runinfo.measure_function = self.line_counts

    def setup_instruments(self):
        '''TODO
        '''
        runinfo = self.runinfo
        devices = self.devices

        dev = devices[self.runinfo.loop0['device_names'][0]]
        xrange = list(self.runinfo.loop0.scan_dict.values())[0]

        # ######### should this be sweep or experiment?
        dev.legacy_sweep_mode(xrange, runinfo.srate, 5)
        devices.pb.setup_single_ttl(
            ['counter', 'awg'],
            ['aom'],
            total_time=runinfo.loop0.n / runinfo.srate * 1.05)
        devices.counter.setup_timed_buffer(
            1 / runinfo.srate, runinfo.loop0.n, runinfo.loop1.n)

        sleep(0.2)

    def end_function(self):
        '''TODO
        '''
        devices = self.devices

        devices.x.dc_mode(0)
        devices.y.dc_mode(0)

        devices.counter.get_counts(1e-6)

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

                    data = self.runinfo.measure_function(self)

                    if np.all(np.array(self.runinfo.indicies) == 0):
                        for key, value in data.items():
                            self.runinfo.measured.append(key)
                        self.preallocate_line(data)

                    for key, value in data.items():
                        if self.runinfo.ndim == 1:
                            self[key] = np.array(value)
                        else:
                            self[key][:, self.runinfo.indicies[1::]] = np.reshape(np.array(value), (-1, 1))

                    self.save_row()

                    if self.runinfo.running is False:
                        self.runinfo.complete = 'stopped'
                        break

                    # Check if complete, stopped early
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

    def line_counts(self, expt):
        '''TODO
        '''
        runinfo = expt.runinfo
        devices = expt.devices

        d = ItemAttribute()

        devices.pb.start()

        sleep(runinfo.loop0.n / runinfo.srate * 1.01)

        for i in range(5):
            if int(devices.counter.query('DATA:POIN?')) == runinfo.loop0.n:
                d.data = devices.counter.read_data_points()
                break
            else:
                sleep(0.05)
        devices.pb.reset()

        return d


# legacy naming convention
class FastGalvoSweep(FastGalvoExperiment):
    pass
