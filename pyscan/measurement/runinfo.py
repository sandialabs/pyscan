# -*- coding: utf-8 -*-
from pyscan.general.itemattribute import ItemAttribute
from .scans import PropertyScan, AverageScan, RepeatScan


class RunInfo(ItemAttribute):
    '''
    Object that contains information of how to run the experiment. Inherits from `.ItemAttribute`.
    This is generally used as an input parameter to Sweep classes.

    You must set the desired number of loops to a type of Scan before using RunInfo in a Sweep class.
    Set the loops in order from `loop0` to `loop3` - for example, if you are sweeping over 2 variables,
    set `loop0` and `loop1`. Do not set `loop0` and `loop2`.
    Attributes
    ----------
    loop0, loop1, loop2, loop3 : `PropertyScan`, `AverageScan`, `RepeatScan` or `FunctionScan`
        Set each loop to a scan object representing one experimental variable. The scan property or
        function will be looped during the experiment, with loop0 being the innermost loop.
        Defaults to `PropertyScan({}, prop=None)<pyscan.measurement.scans.PropertyScan>`,
        which indicates that the loop will not be used.
    measured :
        Array that contains the names of measured dataset, assigned by a Sweep object's `.MetaSweep.run` method.
    measure_function : func
        User-defined function that controls how to measure data. It should accept a Sweep object as its only parameter,
        and returns an `.ItemAttribute` object containing the measured data.
    trigger_function : func
        User-defined function that controls triggering of instruments
    initial_pause : float
        Pause before first setting instruments in seconds, defaults to 0.1.
    average_d : int
        Loop index used by AverageSweep to track which loop to average over, defaults to -1.
        Automatically is set to the correct index by `RunInfo.check()` method, which is automatically
        called by Sweep `.MetaSweep.run` methods.
    verbose : bool
        Flag to print status information, defaults to `False`.

    '''

    def __init__(self):
        """ Constructor method
        """
        self.loop0 = PropertyScan({}, prop=None)
        self.loop1 = PropertyScan({}, prop=None)
        self.loop2 = PropertyScan({}, prop=None)
        self.loop3 = PropertyScan({}, prop=None)

        self.static = {}
        self.measured = []

        self.measure_function = None
        self.trigger_function = None

        self.initial_pause = 0.1
        self.average_d = -1

        self.verbose = False

    def check(self):
        '''Checks to see if runinfo is properly formatted. Called by Sweep object's `run` methods.

        Automatically sets self.average_d to the correct loop index (i.e., the loop which contains an
        instance of `.AverageScan`) to average over. Relevant for `.AverageSweep`.
        '''
        # find the loop set to average scan (if any) and determine the index
        index = 0
        num_av_scans = 0
        for loop in self.loops:
            if isinstance(loop, AverageScan):
                self.average_d = index
                num_av_scans += 1
            index += 1

        # if no average scans found set average_d to -1
        if num_av_scans == 0:
            self.average_d = -1

        # throw an error if more than one average scan is found
        if num_av_scans > 1:
            assert False, "More than one average scan is not allowed"

    @property
    def version(self):
        '''version of pyscan/runinfo
        '''
        return 0.2

    @property
    def loops(self):
        ''' Returns array of all loops
        '''
        return [self.loop0, self.loop1, self.loop2, self.loop3]

    @property
    def dims(self):
        ''' Returns tuple containing the length of each loop, in order from loop0 to loop3, and excludes loops of size 1
        '''
        dims = (self.loop0.n,
                self.loop1.n,
                self.loop2.n,
                self.loop3.n)
        dims = [n for n in dims if n != 1]
        self._dims = tuple(dims)
        return self._dims

    @property
    def average_dims(self):
        ''' Returns tuple containing the length of each loop, excluding loops of size 1 and the averaged loop
        '''
        self._average_dims = tuple(drop(self.dims, self.average_d))

        return self._average_dims

    @property
    def ndim(self):
        ''' Returns number of non 1 sized loops
        '''
        self._ndim = len(self.dims)  # why is this stored as a property? It is never used
        return self._ndim

    @property
    def n_average_dim(self):
        ''' Returns number of loops that are neither size-1 nor average loops
        '''
        self._n_average_dim = len(self.average_dims)
        return self._n_average_dim

    @property
    def indicies(self):
        '''
        Returns tuple of the current loop iteration indicies,
        '''
        self._indicies = (self.loop0.i,
                          self.loop1.i,
                          self.loop2.i,
                          self.loop3.i)
        self._indicies = self._indicies[:self.ndim]
        return tuple(self._indicies)

    @property
    def line_indicies(self):
        self._line_indicies = (
            self.loop1.i,
            self.loop2.i,
            self.loop3.i)
        self._line_indicies = self._line_indicies[:self.ndim]
        return tuple(self._line_indicies)

    @property
    def average_indicies(self):
        ''' Returns tuple of the current loop iteration indicies,
        excluding loops of size 1 and averaged loop. These are the active
        loops not to be averaged. Used by `.AverageSweep`.
        '''
        self._average_indicies = drop(self.indicies, self.average_d)
        return tuple(self._average_indicies)

    @property
    def average_index(self):
        ''' Returns the index of the loop to be averaged. Used by `pyscan.AverageSweep`.
        '''
        self._average_index = self.indicies[self.average_d]
        return self._average_index


def new_runinfo(*arg, **kwarg):
    ''' Creates a new instance of Runinfo
    '''
    return RunInfo(*arg, **kwarg)


def drop(array, index):
    '''
    Drops an object at `index` in `array`

    Parameters
    ----------
    array : list or numpy.array
        Array for object to be dropped
    index : int
        Index of object to be dropped

    Returns
    list
        The array minus the dropped value
    '''

    return list(array[0:index]) + list(array[index + 1:])
