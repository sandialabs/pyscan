import h5py
import json
from pathlib import Path
import numpy as np
import pyscan as ps
from threading import Thread as thread
from time import strftime
from pyscan.measurement.scans import PropertyScan
from ..general.pyscan_json_encoder import PyscanJSONEncoder
from ..general.item_attribute import ItemAttribute
from ..general.is_list_type import is_list_type


class AbstractExperiment(ItemAttribute):
    '''The base class for experiments.

    Parameters
    ----------
    runinfo : ps.RunInfo
        Contains all information about the experiment
    devices : ItemAttribute
        ItemAttribute instance containing all experiment devices
    data_dir : str, optional
        The path to save the data, defaults to './backup'

    Attributes
    ----------
    runinfo : ps.RunInfo
        Contains all information about the experiment
    devices : ItemAttribute
        ItemAttribute instance containing all experiment devices

    Methods
    -------
    setup_data_dir(data_dir)
    preallocate(data)
    reallocate()
    check_runinfo()
    save_continuous_scan_dict(save_name, debug=False)
    assign_values(data)
    assign_continuous_values(data, save_name, run_count, continuous_indicies, debug=False)
    save_point(data)
    save_row()
    save_metadata()
    start_thread()
    stop()
    run()
    setup_runinfo()
    setup_instruments()
    '''

    def __init__(self, runinfo, devices, data_dir):
        '''
        Constructor method
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
            self.runinfo.data_path = Path('./backup')
        else:
            self.runinfo.data_path = Path(data_dir)

        if not self.runinfo.data_path.is_dir():
            self.runinfo.data_path.mkdir()

    def preallocate(self, data):
        '''
        Preallocate data based on the first value of the measurement function

        Parameters
        ----------
        data : ItemAttribute
            ItemAttribute instance containing data from self.runinfo.measure_function
        '''

        if self.runinfo.continuous:
            continuous_scan = self.runinfo.scans[self.runinfo.continuous_scan_index]
            if continuous_scan.i > 0:
                return

        self.runinfo.measured = []
        for key, value in data.items():
            self.runinfo.measured.append(key)

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
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
        else:
            scan_dims = self.runinfo.average_dims
            ndim = self.runinfo.n_average_dim

        with h5py.File(save_name, 'a') as f:
            for name in self.runinfo.measured:
                if is_list_type(data[name]) and ndim > 0:
                    dims = (*scan_dims, * np.array(data[name]).shape)
                    self[name] = np.zeros(dims) * np.nan
                    maxshape = tuple(None for _ in dims)
                    f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                     fillvalue=np.nan, dtype='float64')
                elif (not is_list_type(data[name])) and (ndim > 0):
                    dims = scan_dims
                    self[name] = np.zeros(dims) * np.nan
                    maxshape = tuple(None for _ in dims)
                    f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                     fillvalue=np.nan, dtype='float64')
                elif is_list_type(data[name]) and (ndim == 0):
                    dims = np.array(data[name]).shape
                    self[name] = np.zeros(dims) * np.nan
                    maxshape = tuple(None for _ in dims)
                    f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                     fillvalue=np.nan, dtype='float64')
                else:
                    self[name] = np.nan
                    f.create_dataset(name, shape=[1, ], maxshape=(None,), chunks=(1,),
                                     fillvalue=np.nan, dtype='float64')

    def reallocate(self):
        '''
        Reallocates memory for continuous experiments save files and measurement attribute arrays.
        '''
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
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
                            new_shape[0] += 1
                            dataset.resize(tuple(new_shape))
                            # fill the new part with nans
                            dataset[current_shape[0]:] = np.nan
                        elif len(current_shape) > 1:
                            dim_index = len(self.runinfo.dims) - 1
                            new_shape[dim_index] += 1
                            dataset.resize(tuple(new_shape))
                            slices = tuple(slice(original_dim, new_dim) for original_dim,
                                           new_dim in zip(current_shape, new_shape))
                            mask = np.zeros(new_shape, dtype=bool)
                            mask[slices] = True
                            dataset[mask] = np.nan
                            self.runinfo.new_slices[name] = tuple(slice(current_dim, new_dim) for current_dim,
                                                                  new_dim in zip(current_shape, new_shape))

                    else:
                        assert False, f"cannot reallocate dataset {name}, not found in file."

                    # reallocate for the self[key] to accomodate additional data
                    self[name] = np.pad(self[name],
                                        [(0, new_dim - original_dim) for original_dim,
                                        new_dim in zip(current_shape, new_shape)],
                                        mode='constant', constant_values=np.nan)

            elif self.runinfo.stop_continuous:
                self.stop()

    def check_runinfo(self):
        '''
        Function that is run at the beginning of experiment to ensure runinfo is
        property formatted.
        '''

        scanned_properties = []
        for scan in self.runinfo.scans:
            scan.check_same_length()
            if isinstance(scan, PropertyScan):
                for dev in scan.device_names:
                    prop = scan.prop
                    assert hasattr(self.devices[dev], prop), 'Device {} does not have property {}'.format(dev, prop)
                    assert f'{dev}_{prop}' not in scanned_properties, 'Property {} is duplicated in the scans'.format(f'{dev}_{prop}')
                    scanned_properties.append(f'{dev}_{prop}')

        base_name = strftime("%Y%m%dT%H%M%S")
        save_path = self.runinfo.data_path / '{}.hdf5'.format(base_name)
        count = 0

        while save_path.exists():
            count += 1
            save_path = self.runinfo.data_path / f'{base_name}-{count}.hdf5'

        self.runinfo.file_name = save_path.stem
        self.runinfo.check()

        return 1

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

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
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

        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
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
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
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
        '''
        Abstract function that setups runinfo based on experiment type.
        '''

        pass

    def setup_instruments(self):
        '''
        Abstract function that sets up devices based on experiment type.
       '''

        pass
