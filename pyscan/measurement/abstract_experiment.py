# -*- coding: utf-8 -*-
import h5py
import json
from pathlib import Path
import numpy as np
import pyscan as ps
from threading import Thread as thread
from time import strftime
from pyscan.measurement.scans import PropertyScan, RepeatScan, ContinuousScan
from ..general.pyscan_json_encoder import PyscanJSONEncoder
from ..general.item_attribute import ItemAttribute
from ..general.is_list_type import is_list_type


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

    def preallocate(self, data, debug=False):
        '''Preallocate data based on the first value of the measurement function

        Parameters
        ----------
        data : `.ItemAttribute`
            ItemAttribute containing data
        '''

        skip = False
        if self.runinfo.continuous:
            continuous_scan = self.runinfo.scans[self.runinfo.continuous_scan_index]
            if continuous_scan.i > 0:
                skip = True

        if not skip:
            self.runinfo.measured = []
            for key, value in data.items():
                self.runinfo.measured.append(key)

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
                scan_dims = self.runinfo.dims  # was () for rp 1, (2,) for rp 2< (3,) for rp3
                ndim = self.runinfo.ndim

                if debug is True:
                    print("scan dims are: ", scan_dims, " and ndim is: ", ndim)

            else:
                scan_dims = self.runinfo.average_dims
                ndim = self.runinfo.n_average_dim

            with h5py.File(save_name, 'a') as f:
                for name in self.runinfo.measured:
                    if debug is True:
                        print(f"for {name} data is : {data[name]}, and ndim is: {ndim}")
                    if is_list_type(data[name]) and ndim > 0:
                        if debug is True:
                            print(f"with measured name {name} preallocate1")
                        dims = (*scan_dims, * np.array(data[name]).shape)
                        self[name] = np.zeros(dims) * np.nan
                        maxshape = tuple(None for _ in dims)
                        f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                         fillvalue=np.nan, dtype='float64')
                    elif (not is_list_type(data[name])) and (ndim > 0):
                        if debug is True:
                            print(f"with measured name {name} preallocate2")
                        dims = scan_dims
                        self[name] = np.zeros(dims) * np.nan
                        maxshape = tuple(None for _ in dims)
                        f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                         fillvalue=np.nan, dtype='float64')
                    elif is_list_type(data[name]) and (ndim == 0):
                        if debug is True:
                            print(f"with measured name {name} preallocate3")
                        dims = np.array(data[name]).shape
                        self[name] = np.zeros(dims) * np.nan
                        maxshape = tuple(None for _ in dims)
                        f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                         fillvalue=np.nan, dtype='float64')
                    else:
                        if debug is True:
                            print(f"with measured name {name} preallocate4")
                        self[name] = np.nan
                        f.create_dataset(name, shape=[1, ], maxshape=(None,), chunks=(1,),
                                         fillvalue=np.nan, dtype='float64')

    def reallocate(self, debug=False):
        '''
        Reallocates memory for continuous experiments save files and measurement attribute arrays.
        '''
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        self.runinfo.new_slices = {}

        with h5py.File(save_name, 'a') as hdf:
            if not self.runinfo.stop_continuous(plus_one=True):
                for name in self.runinfo.measured:
                    if name in hdf:
                        dataset = hdf[name]
                        current_shape = dataset.shape
                        new_shape = list(current_shape)

                        if len(current_shape) == 1:
                            if debug is True:
                                print("dataset shape is: ", dataset.shape, " dset shape[0] is: ", dataset.shape[0])
                            new_shape[0] += 1
                            if debug is True:
                                print("new size is: ", new_shape)
                            dataset.resize(tuple(new_shape))
                            if debug is True:
                                print("resized dset is: ", dataset.shape, " and shape 0: ", dataset.shape[0])
                            # fill the new part with nans
                            dataset[current_shape[0]:] = np.nan
                        elif len(current_shape) > 1:
                            # Expand the first dimension, there might be a problem here...
                            if debug is True:
                                print("old shape part 2 is: ", current_shape)

                            dim_index = len(self.runinfo.dims) - 1
                            new_shape[dim_index] += 1

                            if debug is True:
                                print("new shape part 2 is: ", new_shape)

                            # Resize the dataset to the new shape
                            dataset.resize(tuple(new_shape))

                            # Create a mask for the new part
                            slices = tuple(slice(original_dim, new_dim) for original_dim,
                                           new_dim in zip(current_shape, new_shape))
                            mask = np.zeros(new_shape, dtype=bool)
                            mask[slices] = True

                            # Fill the new part with NaN values
                            dataset[mask] = np.nan

                            self.runinfo.new_slices[name] = tuple(slice(current_dim, new_dim) for current_dim,
                                                                  new_dim in zip(current_shape, new_shape))

                            if debug is True:
                                print("Original shape:", current_shape)
                                print("New shape:", dataset.shape)

                    else:
                        assert False, f"cannot reallocate dataset {name}, not found in file."

                    # reallocate for the self[key] to accomodate additional data
                    if debug is True:
                        print(f"{name} original shape: {self[name].shape} with self[{name}] = {self[name]}")
                    self[name] = np.pad(self[name],
                                        [(0, new_dim - original_dim) for original_dim,
                                        new_dim in zip(current_shape, new_shape)],
                                        mode='constant', constant_values=np.nan)
                    if debug is True:
                        print(f"new {name} shape: {self[name].shape} with self[{name}] = {self[name]}")

            elif self.runinfo.stop_continuous:
                self.stop()

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
        num_continuous_scans = 0
        for scan in self.runinfo.scans:
            scan.check_same_length()
            if isinstance(scan, PropertyScan):
                for dev in scan.device_names:
                    prop = scan.prop
                    assert hasattr(self.devices[dev], prop), 'Device {} does not have property {}'.format(dev, prop)
            if isinstance(scan, RepeatScan):
                num_repeat_scans += 1
            if isinstance(scan, ContinuousScan):
                num_continuous_scans += 1

        if num_repeat_scans > 1:
            assert False, "More than one repeat scan detected. This is not allowed."
        if num_continuous_scans > 1:
            assert False, "More than one continuous scan detected. This is not allowed."

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

    def save_continuous_scan_dict(self, save_name, debug=False):
        '''
        Increments continuous scan_dict to match run count for continuous experiments. Saves this change to file.
        '''
        for scan in self.runinfo.scans:
            if isinstance(scan, ps.ContinuousScan):
                run_count = scan.n

        if run_count == 1:
            with h5py.File(save_name, 'a') as f:
                for s in self.runinfo.scans:
                    for key, values in s.scan_dict.items():
                        if key == 'continuous':
                            del f[key]
                            f.create_dataset(key, shape=[1, ], maxshape=(None,), chunks=(1,),
                                             fillvalue=np.nan, dtype='float64')
                            if debug is True:
                                print("new dataset created")
                            self[key] = values
                            f[key][...] = values
        with h5py.File(save_name, 'a') as f:
            for s in self.runinfo.scans:
                for key, values in s.scan_dict.items():
                    if key == 'continuous':
                        f[key].resize((len(s.scan_dict[key]),))
                        self[key] = values
                        f[key][values[-1]] = values[-1]

    def assign_values(self, data):
        if self.runinfo.average_d == -1:
            try:
                sample = self.runinfo.sparse_points[self.runinfo.indicies]
            except:
                sample = True
            if sample:
                for key, value in data.items():
                    if is_list_type(self[key]):
                        self[key][self.runinfo.indicies] = value
                    else:
                        self[key] = value

    def assign_continuous_values(self, data, save_name, run_count, continuous_indicies, debug=False):
        if all(index == 0 for index in self.runinfo.indicies):
            self.save_continuous_scan_dict(save_name, debug)

        for key, value in data.items():
            if is_list_type(self[key][0]):
                if run_count > 0:
                    if debug is True:
                        print(f"before saving point self[{key}] is: {self[key]}")
                    self[key][continuous_indicies] = value
                    if debug is True:
                        print(f"after saving point self[{key}] is: {self[key]}")
                else:
                    self[key][self.runinfo.indicies] = value
            else:
                self[key][run_count] = value

    def save_point(self, data):
        '''
        Saves single point of data for current scan indicies. Does not return anything.
        '''

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.long_name)
        save_name = str(save_path.absolute())

        if self.runinfo.continuous:
            continuous_scan = self.runinfo.scans[self.runinfo.continuous_scan_index]
            run_count = continuous_scan.i
            continuous_indicies = self.runinfo.indicies + (run_count,)
            if self.runinfo.average_d >= 0:
                continuous_indicies = self.runinfo.average_indicies + (run_count,)
        else:
            run_count = 0
        stop = self.runinfo.stop_continuous()

        if not self.runinfo.continuous and self.runinfo.average_d == -1:
            self.assign_values(data)

        elif self.runinfo.continuous and not stop and self.runinfo.average_d == -1:
            self.assign_continuous_values(data, save_name, run_count, continuous_indicies)

        with h5py.File(save_name, 'a') as f:
            if not stop:
                for key in self.runinfo.measured:
                    if not is_list_type(self[key]):
                        f[key][:] = self[key]
                    else:
                        try:
                            original_file_shape = self[key].shape
                            original_file_shape[0] = original_file_shape[0] - run_count
                        except:
                            pass
                        if np.array([original_file_shape == self[key].shape]).all():
                            if run_count > 0:
                                f[key][continuous_indicies] = self[key][continuous_indicies]
                            else:
                                f[key][:] = self[key][:]
                        elif self.runinfo.average_d == -1:
                            f[key][self.runinfo.average_indicies, ...] = self[key][self.runinfo.average_indicies, ...]
                        else:
                            f[key][self.runinfo.indicies, ...] = self[key][self.runinfo.indicies, ...]

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

        # account for redundant run in the case of a continuous expt
        if self.runinfo.continuous:
            self.runinfo.scans[self.runinfo.continuous_scan_index].i -= 1
            self.runinfo.scans[self.runinfo.continuous_scan_index].n -= 1

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
    '''
    Present for backwards compatibility. Renamed to :class:`.AbstractExperiment`.
    '''

    def __init__(self, runinfo, devices, data_dir):
        warning_msg = ("Use of legacy nomenclature detected but no longer supported.\n"
                       + "You entered MetaSweep, use AbstractExperiment instead.")
        raise DeprecationWarning(f"\033[93m*** WARNING! ***: {warning_msg} \033[0m")
        assert False, f"\033[93m*** WARNING! ***: {warning_msg} \033[0m"
