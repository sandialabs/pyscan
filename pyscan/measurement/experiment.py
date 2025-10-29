import h5py
import json
import numpy as np

from time import sleep
from pathlib import Path
from threading import Thread as thread
from time import strftime

from .scans import PropertyScan
from .pyscan_json_encoder import PyscanJSONEncoder
from itemattribute import ItemAttribute

from ..general.is_list_type import is_list_type
from ..general.append_stack_or_contact import append_stack_or_contact
from ..general.delta_product import delta_product


class Experiment(ItemAttribute):
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
    rolling_average(data)
    save_point(data)

    # Running experiment methods
    start_thread()
    stop()
    run()
    '''

    def __init__(self, runinfo, devices, data_dir=None):
        '''
        Constructor method, instantiates Experiment object, sets runinfo and devices to attributes,
        then sets up data directory as needed
        '''

        self.runinfo = runinfo
        self.devices = devices
        self.setup_data_dir(data_dir)

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
            elif (self.runinfo.has_resizing_data) and (deltas[-1] == 1):
                self.reallocate(data)
                # early terminate here
                if not self.runinfo.running:
                    break
                continue  # saving is handled here
            elif self.runinfo.has_average_scan:
                self.rolling_average(data)

            self.save_point(data)

            # early terminate here
            if not self.runinfo.running:
                break

        self.runinfo.complete = True
        self.runinfo.running = False

        if 'end_function' in list(self.runinfo.keys()):
            self.runinfo.end_function(self)

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
                    assert f'{dev}_{prop}' not in scanned_properties, \
                        'Property {} is duplicated in the scans'.format(f'{dev}_{prop}')
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
                    values = np.array(values)  # TODO: values.shape requires np.array
                    self[key] = values
                    if key == 'iteration':
                        f.create_dataset(key, shape=values.shape, maxshape=(None,), chunks=(100, ),)
                    else:
                        f.create_dataset(key, shape=values.shape, maxshape=values.shape, chunks=values.shape,)
                    f[key][:] = values

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
                    # changed from scalar to len 1 arr for start len 1 compat with len/shape in optimizer
                    self[name] = np.array([np.nan], dtype='float64')
                    f.create_dataset(name, shape=[1, ], maxshape=(None,), chunks=(1,),
                                     fillvalue=np.nan, dtype='float64')

    def reallocate(self, data):
        '''
        Reallocates memory for resizing (continuous or optimize) experiments
        save files and measurement attribute arrays.

        Parameters
        ----------
        data : ItemAttribute
            ItemAttribute instance containing data from self.runinfo.measure_function
        '''
        save_path = self.runinfo.data_path / '{}.hdf5'.format(self.runinfo.file_name)
        save_name = str(save_path.absolute())

        with h5py.File(save_name, 'a') as f:
            continuous_n = self.runinfo.scans[-1].n
            f['iteration'].resize((continuous_n,))
            self['iteration'] = self.runinfo.scans[-1].scan_dict['iteration']
            f['iteration'][-1] = self.runinfo.scans[-1].scan_dict['iteration'][-1]

            for name in self.runinfo.measured:
                if is_list_type(data[name]):
                    f[name].resize(tuple((*self.runinfo.dims, *np.array(data[name]).shape)))
                    f[name][-1] = data[name]
                    self[name] = append_stack_or_contact(self[name], data[name])
                else:
                    f[name].resize(self.runinfo.dims)
                    f[name][-1] = data[name]
                    self[name] = append_stack_or_contact(self[name], data[name])

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

        print('Stopping Experiment')
