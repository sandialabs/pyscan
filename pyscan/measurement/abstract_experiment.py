# -*- coding: utf-8 -*-
import h5py
import json
from pathlib import Path
import numpy as np
from threading import Thread as thread
from time import strftime
from pyscan.general import (ItemAttribute,
                            is_list_type)
from pyscan.measurement.scans import PropertyScan, RepeatScan
from pyscan.general.pyscan_json_encoder import PyscanJSONEncoder


class AbstractExperiment(ItemAttribute):
    '''The base class for experiments.

    Parameters
    ----------
    runinfo : :class:`.RunInfo`
        RunInfo instance
    devices : :class:`.ItemAttribute`
        ItemAttribute instance containing all experiment devices
    data_dir : str, optional
        The path to save the data, defaults to './backup'

    Attributes
    ----------
    runinfo : :class:`.RunInfo`
        RunInfo instance passed into :class:`.AbstractExperiment`.
    devices : :class:`.ItemAttribute`
        ItemAttribute instance passed into :class:`.AbstractExperiment`.
    '''

    def __init__(self, runinfo, devices,
                 data_dir):
        '''Constructor method
        '''

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
        self.runinfo.data_path = Path(data_dir)  # seems redundant to use Path() again here

        if not self.runinfo.data_path.is_dir():
            self.runinfo.data_path.mkdir()

    def preallocate(self, data):
        '''Preallocate data based on the first value of the measurement function

        Parameters
        ----------
        data : `.ItemAttribute`
            ItemAttribute containing data
        '''

        if self.runinfo.continuous_expt is True:
            self.continuous_preallocate(data)
        else:
            save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
            save_name = str(save_path.absolute())

            # Create scan arrays
            with h5py.File(save_name, 'a') as f:
                for s in self.runinfo.scans:
                    for key, values in s.scan_dict.items():
                        self[key] = values
                        f[key] = values

            # Create arrays in self and make hdf5 version
            # Possibilies 1. data is a list, dims are list
            #             2. data is a float, dims are list,
            #             3. data is list , dims are 0
            #             4. datais a float, dims are 0
            if self.runinfo.average_d == -1:
                scan_dims = self.runinfo.dims
                ndim = self.runinfo.ndim
            else:
                scan_dims = self.runinfo.average_dims
                ndim = self.runinfo.n_average_dim

            with h5py.File(save_name, 'a') as f:
                for name in self.runinfo.measured:
                    if is_list_type(data[name]) and ndim > 0:
                        dims = (*scan_dims, * np.array(data[name]).shape)
                        self[name] = np.zeros(dims) * np.nan
                        f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')
                    elif (not is_list_type(data[name])) and (ndim > 0):
                        dims = scan_dims
                        self[name] = np.zeros(dims) * np.nan
                        f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')
                    elif is_list_type(data[name]) and (ndim == 0):
                        dims = np.array(data[name]).shape
                        self[name] = np.zeros(dims) * np.nan
                        f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')
                    else:
                        self[name] = np.nan
                        f.create_dataset(name, shape=[1, ], fillvalue=np.nan, dtype='float64')

    def continuous_preallocate(self, data, debug=False):
        ''' Functions similarly to preallocate; however,
        continuous_preallocate preallocates in a way that can be resized and expanded endlessly,
        essentially adding another dimension by default, which is only useful for expts where
        hdf5 memory cannot be preallocated because the measurement size is indeterminate.'''

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        with h5py.File(save_name, 'a') as f:
            for s in self.runinfo.scans:
                for key, values in s.scan_dict.items():
                    self[key] = values
                    f[key] = values

        if self.runinfo.average_d == -1:
            scan_dims = self.runinfo.dims
            ndim = self.runinfo.ndim
        else:
            scan_dims = self.runinfo.average_dims
            ndim = self.runinfo.n_average_dim

        with h5py.File(save_name, 'a') as hdf:
            for name in data.__dict__.keys():
                if is_list_type(data[name]) and ndim > 0:
                    if debug is True:
                        print("preallocate 1")
                    dims = (*scan_dims, * np.array(data[name]).shape)
                    d_shape = (1,) + dims
                    self[name] = np.zeros(dims) * np.nan
                    chunks = tuple(min(d, 64) for d in dims)
                    d_chunks = (1,) + chunks
                    max_shape = tuple(None for _ in dims)  # Adjusted maxshape
                    d_max_shape = (None,) + max_shape
                    hdf.create_dataset(name, shape=d_shape, maxshape=d_max_shape,
                                       fillvalue=np.nan, dtype='float64', chunks=d_chunks)
                elif (not is_list_type(data[name])) and (ndim > 0):
                    if debug is True:
                        print("preallocate 2")
                    dims = scan_dims
                    self[name] = np.zeros(dims) * np.nan
                    hdf.create_dataset(name, shape=(1, dims[0]), maxshape=(None, dims[0]),
                                       fillvalue=np.nan, dtype='float64', chunks=(1, dims[0]))
                elif is_list_type(data[name]) and (ndim == 0):
                    if debug is True:
                        print("preallocate 3")
                    dims = np.array(data[name]).shape
                    self[name] = np.zeros(dims) * np.nan
                    hdf.create_dataset(name, shape=dims, maxshape=(None,),
                                       fillvalue=np.nan, dtype='float64', chunks=(ndim,))
                else:
                    if debug is True:
                        print("preallocate 4")
                    self[name] = np.nan
                    hdf.create_dataset(name, shape=[1, ], maxshape=(None,),
                                       fillvalue=np.nan, dtype='float64', chunks=(ndim,))

    def reallocate(self, debug=False):
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        with h5py.File(save_name, 'a') as hdf:
            for name in self.runinfo.measured:
                if name in hdf:
                    dataset = hdf[name]
                    current_shape = dataset.shape
                    if len(current_shape) == 2:
                        if debug is True:
                            print("dataset shape is: ", dataset.shape, " dset shape[0] is: ", dataset.shape[0])
                        new_size = (dataset.shape[0] + 1, dataset.shape[1])
                        if debug is True:
                            print("new size is: ", new_size)
                        dataset.resize(new_size)
                        if debug is True:
                            print("resized dset is: ", dataset.shape, " and shape 0: ", dataset.shape[0])
                        # fill the new part with nans
                        dataset[current_shape[0]:] = np.nan
                    elif len(current_shape) > 2:
                        # Expand the first dimension, there might be a problem here...
                        # new_shape = (current_shape[0] + self[name].shape[0],) + current_shape[1:]
                        if debug is True:
                            print("old shape part 2 is: ", current_shape)
                        new_shape = (dataset.shape[0] + 1,) + current_shape[1:]
                        if debug is True:
                            print("new shape part 2 is: ", new_shape)

                        # Resize the dataset to the new shape
                        dataset.resize(new_shape)
                        # Optionally, fill the new elements with specific data
                        # Be careful with multi-dimensional slicing and filling, make sure this is done right.
                        if len(current_shape) > 2:
                            # Create a slice object for filling the new elements, not sure this is formatted correctly.
                            fill_slice = ((slice(current_shape[0], None),)
                                          + tuple(slice(0, dim) for dim in current_shape[1:]))
                            dataset[fill_slice] = np.nan

                else:
                    assert False, f"cannot reallocate dataset {name}, not found in file."

    # this function seems redundant/dead, since it is already accomplished by preallocate()
    # consider deleting this dead code if it truly smells.
    def preallocate_line(self, data):
        '''Preallocate line data based on the first value of the measurement function

        Parameters
        ----------
        data : :class:`~pyscan.general.itemattribute.ItemAttribute`
            ItemAttribute containing data
        '''

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        # Create scan arrays
        with h5py.File(save_name, 'a') as f:
            for s in self.runinfo.scans:
                for key, values in s.scan_dict.items():
                    self[key] = values
                    f[key] = values

        # Create arrays in self and make hdf5 version
        # Possibilies 1. data is a list, dims are list
        #             2. data is a float, dims are list,
        #             3. data is list , dims are 0
        #             4. datais a float, dims are 0
        scan_dims = self.runinfo.dims

        with h5py.File(save_name, 'a') as f:
            for name in self.runinfo.measured:
                dims = scan_dims
                self[name] = np.zeros(dims) * np.nan
                f.create_dataset(name, shape=dims, fillvalue=np.nan, dtype='float64')

    def check_runinfo(self):
        '''
        Function that is run at the beginning of experiment to ensure runinfo is
        property formatted.
        '''

        num_repeat_scans = 0
        for scan in self.runinfo.scans:
            scan.check_same_length()
            if isinstance(scan, PropertyScan):
                for dev in scan.device_names:
                    prop = scan.prop
                    assert hasattr(self.devices[dev], prop), 'Device {} does not have property {}'.format(dev, prop)
            if isinstance(scan, RepeatScan):
                num_repeat_scans += 1

        if num_repeat_scans > 1:
            assert False, "More than one repeat scan detected. This is not allowed."

        base_name = strftime("%Y%m%dT%H%M%S")
        save_path = self.runinfo.data_path / '{}.hdf5'.format(base_name)
        count = 0

        while save_path.exists():
            count += 1
            save_path = self.runinfo.data_path / f'{base_name}-{count}.hdf5'

        self.runinfo.long_name = save_path.stem

        self.runinfo.short_name = self.runinfo.long_name[8:]

        self.runinfo.check()

        assert hasattr(self.runinfo, 'average_d'), "runinfo did not have average d attribute after checking runinfo"
        if self.runinfo.average_d == -1:
            assert self.runinfo.has_average_scan is False
        elif 0 <= self.runinfo.average_d < 4:
            assert self.runinfo.has_average_scan is True
        else:
            assert False, "runinfo average d incorrect while has average scan is: " + str(self.runinfo.has_average_scan)

        return 1

    def get_time(self):
        '''Meta function intended to predict the entire time for experiment
        Not implemented.
        '''

        pass

    def save_point(self):
        '''
        Saves single point of data for current scan indicies. Does not return anything.
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

    def continuous_save_point(self, continuous_count, debug=False):
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        with h5py.File(save_name, 'a') as f:
            for key in self.runinfo.measured:
                if debug is True:
                    print(f"key is {key}")
                if continuous_count == 0:
                    if not is_list_type(self[key]):
                        if debug is True:
                            print("save after if 1-1.")
                        f[key][continuous_count * f[key].shape[0]:] = self[key]
                    # checks if the shapes of the files dataset and the measured dataset shape are the same.
                    elif f[key].shape == self[key].shape:
                        if debug is True:
                            print("save after if 1-2.")
                        f[key][continuous_count * f[key].shape[0]:] = self[key][:]
                    elif self.runinfo.average_d == -1:
                        if debug is True:
                            print("save after if 1-3.")
                        f[key][continuous_count] = self[key]
                    else:
                        if debug is True:
                            print("save after if 1-4.")
                        f[key][self.runinfo.indicies, ...] = self[key][self.runinfo.indicies, ...]
                elif continuous_count > 0:
                    if not is_list_type(self[key]):
                        if debug is True:
                            print("save after if 2-1.")
                        f[key][continuous_count * self[key].shape[0]:] = self[key]
                    if len(self[key].shape) == 1:
                        if debug is True:
                            print("save after if 2-2.")
                        if f[key][0].shape == self[key].shape:
                            if debug is True:
                                print("save after if 2-3.")
                            f[key][continuous_count] = self[key][:]
                    elif len(self[key].shape) > 1:
                        if debug is True:
                            print("save after if 2-4.")
                        if f[key][0].shape == self[key].shape:
                            if debug is True:
                                print("save after if 2-5.")
                            f[key][continuous_count] = self[key]

    def save_row(self):
        '''Saves full scan0 of data at once. Does not return anything.
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

        with h5py.File(save_name, 'a') as f:
            f.attrs['runinfo'] = json.dumps(self.runinfo, cls=PyscanJSONEncoder)
            f.attrs['devices'] = json.dumps(self.devices, cls=PyscanJSONEncoder)

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
        '''Meta function the runs the experiment. It is not implemented in AbstractExperiment,
        but must be implemented by its inheriting classes such as :class:`.Experiment`.
        '''

        pass

    def setup_runinfo(self):
        '''Meta function that setups runinfo based on experiment type.
        It is not implemented in AbstractExperiment, but must be implemented
        by its inheriting classes such as :class:`.Experiment`.
        '''

        pass

    def setup_instruments(self):
        '''Meta Function that sets up devices based on experiment type.
        It is not implemented in AbstractExperiment, but must be implemented
        by its inheriting classes such as :class:`.Experiment`.
        '''

        pass

    def default_trigger_function(self):
        '''Default trigger function that is called every scan0 iteration
        '''

        devices = self.devices

        devices.trigger.trigger()


# legacy naming convention
class MetaSweep(AbstractExperiment):
    ''' Present for backwards compatibility. Renamed to :class:`.AbstractExperiment`.
    '''
    pass
