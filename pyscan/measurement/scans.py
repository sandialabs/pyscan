# -*- coding: utf-8 -*-
import numpy as np
from ..general.same_length import same_length
from ..general.item_attribute import ItemAttribute


class AbstractScan(ItemAttribute):
    '''
    Meta class for different scan types. Inherits from `.ItemAttribute`.
    '''

    def iterate(self, index, devices):
        '''
        A function to be implemented by inheriting Scan classes.
        '''
        pass

    def check_same_length(self):
        '''
        A function to be implemented by inheriting Scan classes.
        '''
        pass

    # This must be a method and not an attribute as iterators can only be used once
    def iterator(self):
        '''
        Returns an iterator for the scan over its n range.
        '''
        return iter(range(self.n))


class PropertyScan(AbstractScan):
    '''
    Class for iterating a property of an intruments inside an
    experimental loop. Inherits from `pyscan.measurement.scans.AbstractScan`.

    Parameters
    ----------
    input_dict : dict{string:array}
        key:value pairs of device name strings and arrays of values representing the new `prop`
        values you want to set for each device.
    prop : str
        String that indicates the property of the device(s) to be changed
    dt : float
        Wait time in seconds after changing a single property value, and before the measure_function
        is called. Used by experiment classes, defaults to 0.
    '''

    def __init__(self, input_dict, prop, dt=0):
        '''
        Constructor method
        '''
        self.prop = prop
        self.scan_dict = {}
        self.input_dict = input_dict
        for device, array in input_dict.items():
            self.scan_dict['{}_{}'.format(device, prop)] = array

        self.device_names = list(input_dict.keys())

        self.dt = dt
        self.check_same_length()
        self.i = 0

    def iterate(self, index, devices):
        '''
        Changes `prop` of the listed `devices` to the value of `PropertyScan`'s input_dict at the given `index`.

        :param index: The index of the data array
        :param devices: ItemAttribute instance of experimental devices
        :type devices: ItemAttribute
        '''
        for dev in self.device_names:
            try:
                devices[dev][self.prop] = self.scan_dict[dev + '_' + self.prop][index]
            except Exception:
                continue

    def check_same_length(self):
        '''
        Check that the input_dict has values that are arrays of the same length.
        '''

        if len(list(self.scan_dict.keys())) > 0:
            if same_length(list(self.scan_dict.values())):
                self.n = len(list(self.scan_dict.values())[0])  # self.n is the length of the input_dict arrays.
            else:
                assert 0, 'Values are not of the same length'
        else:
            self.n = 1  # n=1 is required to allow the run() function to proceed atleast once.


class FunctionScan(AbstractScan):
    '''
    Class for iterating a function with input values inside an
    experimental loop. Inherits from `pyscan.measurement.scans.AbstractScan`.

    Parameters
    ----------
    function : func
        Function to be applied during each iteration. Must take a single argument representing one
        item in the `values` array. The function's return value is not used.
    values : list
        An array of values to run the function on.
    dt: float
        Wait time in seconds after running `function` once, and before the ``runinfo.measure_function``
        is called. Used by experiment classes, defaults to 0.
    '''

    def __init__(self, function, values, dt=0):

        self.scan_dict = {}

        self.scan_dict[function.__name__] = values

        self.function = function
        self.dt = dt
        self.i = 0
        self.n = len(values)

    def iterate(self, index, devices):
        '''
        Executes function(self.values[index]). Used by a Experiment class's run() function.

        Parameters
        ----------
        index :
            The index of the `values` array to run the function on. The `FunctionScan`'s `values` at
            the given `index` will be the function input.
        devices:
            Not used
        '''
        self.function(self.scan_dict[self.function.__name__][index])

    def check_same_length(self):
        pass


class RepeatScan(AbstractScan):
    '''Class for repeating inner loops.

    Parameters
    ----------
    n_repeat : int
        Number of times to repeat inner loops.
    dt : float
        Wait time in seconds after repeat. Used by experiment classes, defaults to 0.
    '''

    def __init__(self, nrepeat, dt=0):
        '''
        Constructor method.
        '''
        assert nrepeat > 0, "nrepeat must be > 0"
        assert nrepeat != np.inf, "nrepeat is np.inf, make a continuous scan instead."
        self.scan_dict = {}
        self.scan_dict['repeat'] = list(range(nrepeat))

        self.device_names = ['repeat']
        self.dt = dt

        self.n = nrepeat

        self.i = 0

    def iterate(self, index, devices):
        '''
        Iterates repeat loop.
        '''

        # Need a method here to iterate infinitely/continuously.

        pass

    def check_same_length(self):
        '''
        Not used
        '''
        return 1


class ContinuousScan(AbstractScan):
    '''
    Class for performing a continuous scan, which runs indefinitely or until a specified maximum number of iterations.
    Inherits from `pyscan.measurement.scans.AbstractScan`.

    Parameters
    ----------
    dt : float, optional
        Wait time in seconds after each iteration. Used by experiment classes, defaults to 0.
    n_max : int, optional
        Maximum number of iterations to run. If not specified, the scan will run indefinitely.
    '''

    def __init__(self, dt=0, n_max=None):
        self.scan_dict = {}
        self.scan_dict['continuous'] = []

        self.device_names = ['continuous']
        self.dt = dt

        self.run_count = 0
        # essentially run_count
        self.n = 1
        # current experiment number index
        self.i = 0
        if n_max is not None:
            self.n_max = n_max

    def iterate(self, index, devices):
        self.run_count += 1

        if hasattr(self, "stop_at"):
            if not self.n_max <= self.i:
                self.scan_dict['continuous'].append(self.i)
        else:
            self.scan_dict['continuous'].append(self.i)

    def iterator(self):
        '''
        The following iterator increments continuous scan i and n by one each time continuously.
        '''
        def incrementing_n():
            while True:
                yield self.i
                self.i += 1
                self.n += 1

        iterator = iter(incrementing_n())

        # returns an infinite iterator, overwriting Abstract scans default iterator
        return iterator


class AverageScan(AbstractScan):
    '''
    Class for averaging inner loops.

    Parameters
    ----------
    n_average : int
        Number of times to average data from inner loops
    dt : float
        Wait time in seconds before each measurement. Used by Experiment classes, defaults to 0.
    '''

    def __init__(self, n_average, dt=0):
        assert isinstance(n_average, int), "n_average input for average scan must be an int"
        assert n_average >= 1, "average scan's n_average must be 1 or more"
        assert n_average != np.inf, "average scan's n_average must not be np.inf"

        self.scan_dict = {}
        self.n = n_average
        self.scan_dict['average'] = list(self.iterator())
        self.device_names = ['average']
        self.i = 0
        self.dt = dt

    def iterate(self, index, devices):
        '''
        Place holder, does nothing
        '''
        pass

    def check_same_length(self):
        '''
        Not used
        '''
        return 1
