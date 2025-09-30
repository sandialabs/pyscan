import numpy as np
from time import sleep
from itemattribute import ItemAttribute
from ..general.same_length import same_length


class AbstractScan(ItemAttribute):
    '''
    Abstract class for different scan types. Inherits from `.ItemAttribute`.
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
        for device, array in input_dict.items():
            self.scan_dict['{}_{}'.format(device, prop)] = array

        self.device_names = list(input_dict.keys())

        self.dt = dt
        self.i = 0

        self.check_same_length()

    def iterate(self, expt, i, d):
        '''
        Changes `prop` of the listed `devices` to the value of `PropertyScan`'s input_dict at the given `index`.

        :param index: The index of the data array
        :param devices: ItemAttribute instance of experimental devices
        :type devices: ItemAttribute
        '''

        self.i = i

        if d == 0:
            return 0

        for dev in self.device_names:
            expt.devices[dev][self.prop] = self.scan_dict[dev + '_' + self.prop][i]

        sleep(self.dt)

    def check_same_length(self):
        '''
        Check that the input_dict has values that are arrays of the same length.
        '''

        if len(list(self.scan_dict.keys())) > 0:
            if same_length(list(self.scan_dict.values())):
                self.n = len(list(self.scan_dict.values())[0])  # self.n is the length of the input_dict arrays.
            else:
                raise Exception('PropertyScan Values are not of the same length')
        else:
            self.n = 1  # n=1 is required to allow the run() function to proceed atleast once.

    def iterator(self):
        '''
        The following iterates over n
        '''
        return range(self.n)


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

        self.scan_dict[function.__name__] = np.array(values)

        self.function = function
        self.dt = dt
        self.i = 0
        self.n = len(values)

    def iterate(self, expt, i, d):
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

        self.i = i

        if d == 0:
            return 0

        self.function(self.scan_dict[self.function.__name__][i])
        sleep(self.dt)

    def check_same_length(self):
        pass

    def iterator(self):
        '''
        The following iterates over n
        '''
        return range(self.n)


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
        self.scan_dict['repeat'] = np.array(range(nrepeat))

        self.device_names = ['repeat']
        self.dt = dt

        self.n = nrepeat

        self.i = 0

    def iterate(self, expt, i, d):
        '''
        Iterates repeat loop.
        '''

        self.i = i

        if d == 0:
            return 0

        sleep(self.dt)

    def check_same_length(self):
        '''
        Not used
        '''
        return 1

    def iterator(self):
        '''
        The following iterates over n
        '''
        return range(self.n)


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

    def __init__(self, n_max=None, dt=0):

        assert n_max is None or isinstance(n_max, int), "n_max must be an int or None"
        assert n_max > 0, "n_max must be > 0 or None"

        self.scan_dict = {}
        self.scan_dict['iteration'] = np.ndarray((0))

        self.device_names = ['iteration']
        self.dt = dt

        self.i = 0
        self.n = 1

        self.n_max = n_max

    def iterate(self, expt, i, d):

        self.i = i
        self.n = i + 1

        if d == 0:
            return 0

        self.scan_dict['iteration'] = np.append(self.scan_dict['iteration'], i)
        expt.iteration = self.scan_dict['iteration']

        sleep(self.dt)

        if self.n == self.n_max:
            expt.stop()

    def iterator(self):
        '''
        The following iterates over n_max if n_max is specified, otherwise it iterates indefinitely.
        '''
        if self.n_max is None:
            return range(1)
        else:
            return range(self.n_max)


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
        self.scan_dict['average'] = np.array(list(range(n_average)))
        self.device_names = ['average']
        self.i = 0
        self.dt = dt

    def iterate(self, expt, i, d):
        '''
        Place holder, does nothing
        '''

        self.i = i

        if d == 0:
            return 0

        sleep(self.dt)

    def check_same_length(self):
        '''
        Not used
        '''
        return 1

    def iterator(self):
        '''
        The following iterates over n
        '''
        return range(self.n)
