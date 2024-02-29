# -*- coding: utf-8 -*-
import os
import glob
from pathlib import Path
from ipywidgets import get_ipython
import pyscan as ps


class JupyterTools(object):
    '''
    Utility class for loading plotting data in jupyter notebooks

    Attributes
    ----------
    path_name : str
        Path to datasets, defaults to './'.
    default_z : str
        Default name of data, defaults to 'x'.
    default_vrange : list of length 2
        default z range of 3D plots, defaults to [-0.02, 0.02].
    plot_size :
        plot size. defaults to `None`.

    '''

    def __init__(self):
        self.path_name = './backup'
        self.default_z = 'x'
        self.default_vrange = [-0.02, 0.02]
        self.plot_size = None

    def get_last_scan_name(self):
        '''
        Finds most recent dataset in self.path_name
        '''
        if self.path_name[-1] == '/':
            self.path_name = self.path_name[0:-1]

        newest = max(glob.iglob('{}/{}'.format(
            self.path_name, '*.hdf5')), key=os.path.getctime)

        file_name = newest.replace(self.path_name + '\\', '')
        file_name = file_name.split('.')[0]

        return file_name

    def load_last_scan(self):
        '''
        Loads last dataset in self.path_name

        Returns
        -------
        ItemAttribute
        '''

        if self.path_name[-1] == '/':
            self.path_name = self.path_name[0:-1]
        newest = max(glob.iglob('{}/{}'.format(
            self.path_name, '*.hdf5')), key=os.path.getctime)

        file_name = newest.replace(self.path_name + '\\', '')
        file_name = file_name[0:-4]

        file_name = str(Path(self.path_name) / Path(file_name))

        self.last_scan = ps.load_experiment(file_name)

        return self.last_scan

    def load_next_cell(self, *arg, **kwarg):
        '''
        Generates a new jupyter cell with function and dataname in function

        Parameters
        ----------
        function_name :
            funciton to be applied to data

        Other Parameters
        ----------------
        *arg, **kwarg :
            arguments to be passed to function_name

        Returns
        -------
        None
        '''

        function_name = 'load_experiment'

        file_name = self.get_last_scan_name()
        file_name = self.path_name + "/" + file_name
        command_str = 'expt = ps.{}(\'{}\','.format(function_name, file_name)
        for key, value in kwarg.items():
            command_str += '{}={},'.format(key, value)

        command_str = command_str[:-1]
        command_str += ')'

        get_ipython().set_next_input(command_str)
