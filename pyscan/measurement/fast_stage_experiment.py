# -*- coding: utf-8 -*-
from time import sleep
from pyscan.measurement.abstract_experiment import AbstractExperiment
from ..general.item_attribute import ItemAttribute
import numpy as np
# import nidaqmx


class FastStageExperiment(AbstractExperiment):
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

        chan = self.runinfo.loop0.prop

        if chan == 'x':
            chan = 1
        elif chan == 'y':
            chan = 2
        elif chan == 'z':
            chan = 3

        xrange = list(self.runinfo.loop0.scan_dict.values())[0]
        runinfo.fast_values = xrange

        runinfo.start = xrange[0]
        runinfo.stop = xrange[-1]
        delta = xrange[1] - xrange[0]
        d = runinfo.stop - runinfo.start

        runinfo.vel0, runinfo.acc = devices.stage.get_channel_velocity_parameters(1)  # in mm/s

        n_points = int(np.abs((runinfo.start - runinfo.stop) / delta))

        t = n_points / runinfo.srate
        runinfo.vel = round(np.abs(d / t), 5)

        runinfo.scan_time = t
        runinfo.fast_chan = chan

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

        if runinfo.fast_chan == 1:
            chan = 'x'
            chan_fast = 'xfast'
        elif runinfo.fast_chan == 2:
            chan = 'y'
            chan_fast = 'yfast'
        elif runinfo.fast_chan == 3:
            chan = 'z'
            chan_fast = 'zfast'

        d = ItemAttribute()

        devices.stage.reset_speed()

        devices.stage[chan] = runinfo.start

        sleep(2)

        devices.stage.set_channel_velocity_parameters(
            runinfo.fast_chan,
            runinfo.vel,
            runinfo.acc)

        devices.stage[chan_fast] = runinfo.stop

        if runinfo.counter == 'picoharp':
            d.counts0 = []
            # d.counts1 = []
            # d.counts_sum = []
            for i in range(runinfo.loop0.n):
                counts0 = devices.ph.get_count_rate_0()
                # counts1 = devices.ph.get_count_rate_1()
                # counts_sum = counts0 + counts1
                d.counts0.append(counts0)
                # d.counts1.append(counts1)
                # d.counts_sum.append(counts_sum)
                sleep(1 / runinfo.srate)
        else:
            d.counts = devices.counter.get_n_binary_points(runinfo.loop0.n)

        devices.stage.reset_speed()

        return d


# legacy naming convention
class FastStageSweep(FastStageExperiment):
    pass
