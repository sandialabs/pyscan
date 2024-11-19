import h5py
import json
from pathlib import Path
import numpy as np
import pyscan as ps
from threading import Thread as thread
from time import strftime
from pyscan.measurement.scans import PropertyScan
from .pyscan_json_encoder import PyscanJSONEncoder
from itemattribute import ItemAttribute
from ..general.is_list_type import is_list_type


class AbstractExperiment(ItemAttribute):
    '''
    The abstract class for experiments.

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
    # Setup methods
    setup_data_dir(data_dir)
    check_runinfo()
    save_metadata(metadata_name)

    # Data methods
    preallocate(data)
    reallocate(data)
    save_point(data)

    # Running experiment methods
    start_thread()
    stop()
    run()
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

    # Data methods
    def preallocate(self, data):
        '''
        Preallocate save data based on the first value of the measurement function

        Parameters
        ----------
        data : ItemAttribute
            ItemAttribute instance containing data from self.runinfo.measure_function
        '''

        # fill in what was measured
        self.runinfo.measured = []
        for key, value in data.items():
            self.runinfo.measured.append(key)

        # get the file save path name
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
        save_name = str(save_path.absolute())

        # Create and save scan arrays
        with h5py.File(save_name, 'a') as f:
            for s in self.runinfo.scans:
                for key, values in s.scan_dict.items():
                    self[key] = values
                    f[key] = values

        # Get dimensions based off of averaging or not
        if self.runinfo.average_index == -1:
            scan_dims = self.runinfo.dims
            ndim = self.runinfo.ndim
        else:
            scan_dims = self.runinfo.average_dims
            ndim = self.runinfo.n_average_dim

        # Initialize the data arrays
        with h5py.File(save_name, 'a') as f:
            for name in self.runinfo.measured:
                # array of data, at least one non average scan
                if is_list_type(data[name]) and ndim > 0:
                    dims = (*scan_dims, * np.array(data[name]).shape)
                    self[name] = np.zeros(dims) * np.nan
                    maxshape = tuple(None for _ in dims)
                    f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                     fillvalue=np.nan, dtype='float64')
                # single data point, at least on non average scan
                elif (not is_list_type(data[name])) and (ndim > 0):
                    dims = scan_dims
                    self[name] = np.zeros(dims) * np.nan
                    maxshape = tuple(None for _ in dims)
                    f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                     fillvalue=np.nan, dtype='float64')
                # data is an array, but there are no scan dimension other than average
                elif is_list_type(data[name]) and (ndim == 0):
                    dims = np.array(data[name]).shape
                    self[name] = np.zeros(dims) * np.nan
                    maxshape = tuple(None for _ in dims)
                    f.create_dataset(name, shape=dims, maxshape=maxshape, chunks=dims,
                                     fillvalue=np.nan, dtype='float64')
                # data is a single point, but there are no scan dimensions other than average
                else:
                    self[name] = np.nan
                    f.create_dataset(name, shape=[1, ], maxshape=(None,), chunks=(1,),
                                     fillvalue=np.nan, dtype='float64')

    def reallocate(self, data):
        '''
        Reallocates memory for continuous experiments save files and measurement attribute arrays.

        Parameters
        ----------
        data : ItemAttribute
            ItemAttribute instance containing data from self.runinfo.measure_function
        '''
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
        save_name = str(save_path.absolute())

        new_slices = {}

        with h5py.File(save_name, 'a') as f:
            for name in self.runinfo.measured:
                dataset = f[name]
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
                    slices = tuple(slice(
                        original_dim, new_dim) for original_dim,
                        new_dim in zip(current_shape, new_shape))
                    mask = np.zeros(new_shape, dtype=bool)
                    mask[slices] = True
                    dataset[mask] = np.nan

                    new_slices[name] = tuple(slice(
                        current_dim, new_dim) for current_dim,
                        new_dim in zip(current_shape, new_shape))

                self[name] = np.pad(self[name],
                                    [(0, new_dim - original_dim) for original_dim,
                                    new_dim in zip(current_shape, new_shape)],
                                    mode='constant', constant_values=np.nan)

    def save_continuous_scan_dict(self, save_name, debug=False):
        '''
        Increments continuous scan_dict to match run count for continuous experiments.
        Saves this change to file.
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

    def assign_continuous_values(self, data, save_name, run_count, continuous_indicies, debug=False):
        if all(index == 0 for index in self.runinfo.indicies):
            self.save_continuous_scan_dict(save_name, debug)

        for key, value in data.items():
            if is_list_type(self[key][0]):
                if run_count > 0:
                    self[key][continuous_indicies] = value
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

        if self.runinfo.has_average_scan:
            indicies = self.runinfo.average_indicies
        else:
            indicies = self.runinfo.indicies

        for key, value in data.items():
            if is_list_type(self[key]):
                self[key][indicies] = value
            else:
                self[key] = value

        with h5py.File(save_name, 'a') as f:
            for key in self.runinfo.measured:
                if is_list_type(self[key]):
                    f[key][*indicies, ...] = self[key][*indicies, ...]
                else:
                    f[key][:] = self[key]

    def save_metadata(self, metadata_name):
        '''
        Formats and saves metadata to the hdf5 file

        Parameters
        ----------
        metadata_name : str
            Name of the metadata to be saved, ex. "runinfo", "devices"

        '''
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
        save_name = str(save_path.absolute())

        with h5py.File(save_name, 'a') as f:
            f.attrs[metadata_name] = json.dumps(self[metadata_name], cls=PyscanJSONEncoder)

    def start_thread(self):
        '''
        Starts experiment as a background thread, this works in conjunction with live plot
        '''

        self.expt_thread = thread(target=self.run, daemon=True)
        self.expt_thread.start()
        self.runinfo.running = True

    def stop(self):
        '''
        Stops the experiment after the next data point is take ensuring that the data
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
        '''
        Meta function the runs the experiment. It is not implemented in AbstractExperiment,
        but must be implemented by its inheriting classes such as :class:`.Experiment`.
        '''

        pass
