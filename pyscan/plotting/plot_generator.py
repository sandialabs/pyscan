# -*- coding: utf-8 -*-
from ..general.set_difference import set_difference
from ..general.first_string import first_string
import numpy as np


class PlotGenerator(object):
    """
    Helper class to generate standarized figures

    Parameters
    ----------
    expt :
        The experiment object
    d :
        Dimensionality of the data to be plotted
    x_name : optional
        User choice of x_data, otherwise defautls to first valid
    x_range : optional
        User choice of x_range, otherwise default
    y_name : optional
        User choice of y_data, otherwise defautls to first valid
    y_range : optional
        User choice of y_range, otherwise default
    data_name : optional
        User choice of data, otherwise defautls to first valid
    data_range : optional
        User choice of y range (2D) or vertical range (3D), otherwise default
    index3D : optional
        If data is 3D and plot is 2D, choose slice, otherwise 0
    analysis_function : optional
        Analysis to perform on data, otherwise, returns data
    analysis_args : tuple, optional
        If analysis dependes on multipled datasets, will apply
        analysis function to these datasets

    """

    def __init__(self, expt, d, **kwarg):

        self.expt = expt
        self.d = d

        inputs = ['x_name', 'x_range',
                  'y_name', 'y_range',
                  'data_name', 'data_range',
                  'index3D',
                  'analysis_function', 'analysis_args']

        for key in inputs:
            self.key_or_none(key, kwarg)

        self.get_data()
        self.get_x()
        self.get_y()

    def key_or_none(self, key, kwarg):
        '''
        Sets attribute on PlotGenerator object if key is in kwarg

        Parameters
        ----------
        key :
            possible input
        kwarg :
            kwargs from __init__

        Returns
        -------
        None

        '''
        if key in kwarg.keys():
            setattr(self, key, kwarg[key])
        else:
            setattr(self, key, None)

    def get_x(self):
        '''
        Finds the x data for plotting
        '''

        if self.x_name is None:
            self.x_name = first_string(list(self.expt.runinfo.scan0.scan_dict.keys()))

        self.other_x = set_difference(list(self.expt.runinfo.scan0.scan_dict.keys()), self.x_name)
        self.x = self.expt[self.x_name]

    def get_xlabel(self):
        '''
        Generates label for x-axis of plot
        '''
        if len(self.other_x) == 0:
            return '{}'.format(self.x_name)
        else:
            return '{} ({})'.format(self.x_name, ', '.join(self.other_x))

    def get_y(self):
        '''
        Gets data for y axis fo plot
        '''
        if self.d == 1:
            return
        if self.expt.runinfo.ndim == 1:
            self.y_name = 'y_indicies'
            self.y = np.array(range(self.data.shape[1]))
            self.other_y = ''
        else:
            if self.y_name is None:
                self.y_name = first_string(list(self.expt.runinfo.scan1.scan_dict.keys()))
            self.other_y = set_difference(list(self.expt.runinfo.scan1.scan_dict.keys()), self.y_name)
            self.y = self.expt[self.y_name]

    def get_ylabel(self):
        '''
        Generates label for y-axis of plot
        '''
        if self.d == 1:
            return '{}'.format(self.data_name)
        else:
            if len(self.other_y) == 0:
                return '{}'.format(self.y_name)
            else:
                return '{} ({})'.format(self.y_name, ', '.join(self.other_y))

    def get_data(self):
        '''
        Gets the data to be plotted
        '''
        if self.data_name is None:
            self.data_name = first_string(self.expt.runinfo.measured)

        self.data = self.expt[self.data_name]

        if self.analysis_function is not None:
            if self.analysis_args is None:
                self.data = self.analysis_function(self.data)
            else:
                self.data = self.analysis_function(*self.analysis_args)

        self.data = np.ma.masked_where(np.isnan(self.data), self.data)

        if (self.d == 2) and (self.data.ndim > 2):
            if self.index3D is None:
                self.index3D = 0
            self.data_name = self.data_name + '[{}/{}]'.format(self.index3D, self.data.shape[2])
            self.data = self.data[:, :, self.index3D]

    def get_title(self):
        '''
        Generates the title of the plot
        '''

        if not self.expt.runinfo.running:
            return '{}, {}'.format(self.data_name, self.expt.runinfo.long_name)
        elif self.expt.runinfo.ndim == 4:
            return '{}/{}, {}, {}'.format(self.expt.runinfo.scan4.i,
                                          self.expt.runinfo.scan4.n,
                                          self.data_name,
                                          self.expt.runinfo.long_name)
        elif self.expt.runinfo.ndim == 3:
            return '{}/{}, {}, {}'.format(self.expt.runinfo.scan3.i,
                                          self.expt.runinfo.scan3.n,
                                          self.data_name,
                                          self.expt.runinfo.long_name)
        elif self.expt.runinfo.ndim == 2:
            return '{}/{}, {}, {}'.format(self.expt.runinfo.scan2.i,
                                          self.expt.runinfo.scan2.n,
                                          self.data_name,
                                          self.expt.runinfo.long_name)
        elif self.expt.runinfo.ndim == 1:
            return '{}/{}, {}, {}'.format(self.expt.runinfo.scan1.i,
                                          self.expt.runinfo.scan1.n,
                                          self.data_name,
                                          self.expt.runinfo.long_name)

    def get_xrange(self):
        '''
        Finds the min, max range of the x-values for the plot
        '''
        if self.x_range is None:
            return np.min(self.x), np.max(self.x)
        else:
            return self.x_range

    def get_yrange(self):
        '''
        Finds the min, max range of the  y-values for the plot
        '''

        if self.y_range is None:
            if self.d == 1:
                return np.min(self.data), np.max(self.data)
            else:
                return np.min(self.y), np.max(self.y)
        else:
            if self.d == 1:
                return self.y_range
            else:
                return self.data_range

    def get_data_range(self):
        '''
        Finds the min, max range of the  data values for the plot
        '''

        if self.data_range is None:
            return [np.min(self.data), np.max(self.data)]
        else:
            return self.data_range
