# -*- coding: utf-8 -*-
import h5py
import pickle
import json
from pathlib import Path
from pyscan.general import ItemAttribute, recursive_to_itemattribute


def load_experiment(file_name):
    '''
    Function to load experimental data created by pyscan

    Parameters
    ----------
    file_name : str
        Path to file that is to be loaded

    '''
    if '.pkl' in file_name:
        data_version = 0.1
    elif '.hdf5' in file_name:
        data_version = 0.2
    else:
        file_path = Path(file_name)
        if file_path.with_suffix('.pkl').is_file():
            data_version = 0.1
        elif file_path.with_suffix('.hdf5').is_file():
            data_version = 0.2
            file_name += '.hdf5'
        else:
            assert 0, 'Cannot locate {}'.format(file_name)

    if data_version == 0.1:
        meta_data = pickle.load(
            open('{}.pkl'.format(file_name), "rb"))

        expt = ItemAttribute()
        expt.runinfo = ItemAttribute()
        expt.devices = ItemAttribute()

        for key, value in meta_data['runinfo'].items():
            expt.runinfo[key] = value

        for key, value in meta_data['devices'].items():
            expt.devices[key] = value

        data = h5py.File('{}.hdf5'.format(file_name), 'r')
        with h5py.File('{}.hdf5'.format(file_name), 'r') as f:
            for key, value in data.items():
                expt[key] = (f[key][:]).astype('float64')

        return expt

    elif data_version == 0.2:
        expt = ItemAttribute()
        expt.runinfo = ItemAttribute()
        expt.devices = ItemAttribute()

        f = h5py.File('{}'.format(file_name), 'r')
        runinfo = json.loads(f.attrs['runinfo'])
        expt.runinfo = recursive_to_itemattribute(runinfo)

        devices = json.loads(f.attrs['devices'])
        expt.devices = recursive_to_itemattribute(devices)

        for key, value in f.items():
            expt[key] = (f[key][:]).astype('float64')
        f.close()

        return expt
