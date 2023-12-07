# -*- coding: utf-8 -*-
"""
Meta Sweep
==========
"""


import h5py
import json
from pathlib import Path
import numpy as np
from threading import Thread as thread
from time import strftime
from pyscan.general import (ItemAttribute,
                            recursive_to_dict,
                            is_list_type)
from pyscan.measurement.scans import PropertyScan


class MetaSweep(ItemAttribute):
    '''The base class for sweep experiments.

    Parameters
    ----------
    runinfo : :class:`~pyscan.measurement.runinfo.RunInfo`
        RunInfo instance
    devices : :class:`~pyscan.general.itemattribute.ItemAttribute`
        ItemAttribute instance containing all experiment devices
    data_dir : str, optional
        The path to save the data, defaults to './backup'

    Attributes
    ----------
    runinfo : :class:`~pyscan.measurement.runinfo.RunInfo`
        RunInfo instance passed into :class:`MetaSweep`.
    devices : :class:`~pyscan.general.itemattribute.ItemAttribute`
        ItemAttribute instance passed into :class:`MetaSweep`.

    '''

    def __init__(self, runinfo, devices,
                 data_dir):
        """Constructor method
        """

        self.runinfo = runinfo
        self.devices = devices
        self.setup_data_dir(data_dir)

    def setup_data_dir(self, data_dir):
        '''Creates save directory if it does not exist

        Parameters
        ----------
        data_dir : str, optional
            Path to save the data, defaults to './backup'

        '''
        if data_dir is None:
            data_dir = Path('./backup')
        else:
            data_dir = Path(data_dir)
        self.runinfo.data_path = Path(data_dir)

        if not self.runinfo.data_path.is_dir():
            self.runinfo.data_path.mkdir()

    def preallocate(self, data):
        '''Preallocate data based on the first value of the measurement function

        Parameters
        ----------
        data : `.ItemAttribute`
            ItemAttribute containing data
        '''

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        # Create loop arrays
        with h5py.File(save_name, 'a') as f:
            for s in self.runinfo.loops:
                for key, values in s.scan_dict.items():
                    self[key] = values
                    f[key] = values

        # Create arrays in self and make hdf5 version
        # Possibilies 1. data is a list, dims are list
        #             2. data is a float, dims are list,
        #             3. data is list , dims are 0
        #             4. datais a float, dims are 0
        if self.runinfo.average_d == -1:
            loop_dims = self.runinfo.dims
            ndim = self.runinfo.ndim
        else:
            loop_dims = self.runinfo.average_dims
            ndim = self.runinfo.n_average_dim

        with h5py.File(save_name, 'a') as f:
            for name in self.runinfo.measured:
                if is_list_type(data[name]) and ndim > 0:
                    dims = (*loop_dims, * np.array(data[name]).shape)
                    self[name] = np.zeros(dims) * np.nan
                    f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')
                elif (not is_list_type(data[name])) and (ndim > 0):
                    dims = loop_dims
                    self[name] = np.zeros(dims) * np.nan
                    f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')
                elif is_list_type(data[name]) and (ndim == 0):
                    dims = np.array(data[name]).shape
                    self[name] = np.zeros(dims) * np.nan
                    f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')
                else:
                    self[name] = np.nan
                    f.create_dataset(name, shape=[1, ], fillvalue=np.nan, dtype='float64')

    def preallocate_line(self, data):
        '''Preallocate line data based on the first value of the measurement function

        Parameters
        ----------
        data : :class:`~pyscan.general.itemattribute.ItemAttribute`
            ItemAttribute containing data
        '''

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        # Create loop arrays
        with h5py.File(save_name, 'a') as f:
            for s in self.runinfo.loops:
                for key, values in s.scan_dict.items():
                    self[key] = values
                    f[key] = values

        # Create arrays in self and make hdf5 version
        # Possibilies 1. data is a list, dims are list
        #             2. data is a float, dims are list,
        #             3. data is list , dims are 0
        #             4. datais a float, dims are 0
        loop_dims = self.runinfo.dims

        with h5py.File(save_name, 'a') as f:
            for name in self.runinfo.measured:
                dims = loop_dims
                self[name] = np.zeros(dims) * np.nan
                f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')

    def check_runinfo(self):
        '''
        Function that is run at the beginning of experiment to ensure runinfo is
        property formatted.
        '''

        for loop in self.runinfo.loops:
            loop.check_same_length()
            if isinstance(loop, PropertyScan):
                for dev in loop.device_names:
                    prop = loop.prop
                    assert hasattr(self.devices[dev], prop), 'Device {} does not have property {}'.format(dev, prop)

        self.runinfo.long_name = strftime("%Y%m%dT%H%M%S")
        self.runinfo.short_name = self.runinfo.long_name[8:]

        self.runinfo.check()

        return 1

    def get_time(self):
        '''Meta function intended to predict the entire time for experiment
        Not implemented.
        '''

        pass

    def save_point(self):
        '''
        Saves single point of data for current loop indicies. Does not return anything.
        '''

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        with h5py.File(save_name, 'a') as f:
            for key in self.runinfo.measured:
                if not is_list_type(self[key]):
                    f[key][:] = self[key]
                elif np.array([f[key].shape == self[key].shape]).all():
                    f[key][:] = self[key][:]
                elif self.runinfo.average_d == -1:
                    f[key][self.runinfo.average_indicies, ...] = self[key][self.runinfo.average_indicies, ...]
                else:
                    f[key][self.runinfo.indicies, ...] = self[key][self.runinfo.indicies, ...]

    def save_row(self):
        '''Saves full loop0 of data at once. Does not return anything.
        '''

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        with h5py.File(save_name, 'a') as f:
            for key in self.runinfo.measured:
                if not is_list_type(self[key]):
                    f[key][:] = self[key]
                elif np.array([f[key].shape == self[key].shape]).all():
                    f[key][:] = self[key][:]
                elif self.runinfo.average_d == -1:
                    f[key][:, self.runinfo.line_indicies, ...] = self[key][self.runinfo.line_indicies, ...]
                else:
                    f[key][:, self.runinfo.line_indicies, ...] = self[key][self.runinfo.line_indicies, ...]

    def save_metadata(self):
        '''Formats and saves metadata from self.runinfo and self.devices. Does not return anything.

        '''
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        data = recursive_to_dict(self.__dict__)

        with h5py.File(save_name, 'a') as f:
            f.attrs['runinfo'] = json.dumps(data['runinfo'])
            f.attrs['devices'] = json.dumps(data['devices'])

    def start_thread(self):
        '''Starts experiment as a background thread, this works in conjunction with live plot
        '''

        self.expt_thread = thread(target=self.run, daemon=True)
        self.expt_thread.start()
        self.runinfo.running = True

    def stop(self):
        '''Stops the experiment after the next data point is take ensuring that the data
        is saved properly. Sets the associated runinfo.complete setting to 'stopped' and runinfo.running to `False`.
        '''

        self.runinfo.running = False
        self.runinfo.complete = 'stopped'
        print('Stopping Experiment')

    def run(self):
        '''Meta function the runs the experiment. It is not implemented in MetaSweep,
        but must be implemented by its inheriting classes such as AverageSweep.
        '''

        pass

    def setup_runinfo(self):
        '''Meta function that setups runinfo based on experiment type.
        It is not implemented in MetaSweep, but must be implemented
        by its inheriting classes such as AverageSweep.
        '''

        pass

    def setup_instruments(self):
        '''Meta Function that sets up devices based on experiment type.
        It is not implemented in MetaSweep, but must be implemented
        by its inheriting classes such as AverageSweep.
        '''

        pass

    def default_trigger_function(self):
        '''Default trigger function that is called every loop0 iteration
        '''

        devices = self.devices

        devices.trigger.trigger()
