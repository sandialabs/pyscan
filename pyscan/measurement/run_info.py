# -*- coding: utf-8 -*-
from pyscan.general.item_attribute import ItemAttribute
from pyscan.general.get_pyscan_version import get_pyscan_version
from .scans import PropertyScan, AverageScan
import pyscan as ps


class RunInfo(ItemAttribute):
    '''
    Object that contains information of how to run the experiment. Inherits from :class:`.ItemAttribute`.
    This is generally used as an input parameter to Experiment classes.

    You must set the desired number of scans to a type of Scan before setting RunInfo as a parameter
    in a Experiment class.
    Set the scans in order from `scan0` to `scan3` - for example, if you are experimenting over 2 variables,
    set `scan0` and `scan1`. Do not set `scan0` and `scan2`.

    Attributes
    ----------
    scan0, scan1, scan2, scan3 : :class:`.PropertyScan`, :class:`.AverageScan`, :class:`.RepeatScan`
     or :class:`.FunctionScan`
        Set each scan to a scan object representing one independent experimental variable. The scan property or
        function will be scanned during the experiment, with scan0 being the innermost scan.
        Defaults to :class:`PropertyScan({}, prop=None)<.PropertyScan>`,
        which indicates that the scan will not be used.
    measured :
        Array that contains the names of collected data, defined by the `measure_function` return object.
    measure_function : func
        User-defined function that controls how to measure data.
        It should accept a :class:`.Experiment` object as its only parameter,
        and returns an :class:`.ItemAttribute` object containing the measured data. The names of the measured data,
        each being an attribute of the return object, will appear as keys of the experiment after it is run.
    trigger_function : func
        User-defined function that controls triggering of instruments
    initial_pause : float
        Pause before first setting instruments in seconds, defaults to 0.1.
    average_d : int
        scan index used by an Experiment with one of its scans being :class:`.AverageScan`.
        It is used to track which scan to average over, defaults to -1.
        Automatically is set to the correct index by :meth:`.RunInfo.check` method, which is automatically
        called by Experiment objects `run()` methods.
    verbose : bool
        Flag to print status information, defaults to `False`.
    version : str
        Current version of pyscan to be saved as metadata.

    '''

    def __init__(self):
        """ Constructor method
        """
        self.scan0 = PropertyScan({}, prop=None)
        self.scan1 = PropertyScan({}, prop=None)
        self.scan2 = PropertyScan({}, prop=None)
        self.scan3 = PropertyScan({}, prop=None)

        self.static = {}
        self.measured = []

        self.measure_function = None
        self.trigger_function = None

        self.initial_pause = 0.1
        self.average_d = -1

        # Assumed not a continuous expt. If there is a continuous scan this will be set to true in self.check()
        self.continuous = False

        self.verbose = False
        self._pyscan_version = get_pyscan_version()

    def check(self):
        '''Checks to see if runinfo is properly formatted. Called by Experiment object's `run()` methods.

        Automatically sets `self.average_d` to the correct scan index (i.e., the scan which contains an
        instance of `.AverageScan`) to average over.
        '''
        # find the scan set to average scan (if any) and determine the index
        index = 0
        num_av_scans = 0
        for scan in self.scans:
            if isinstance(scan, AverageScan):
                self.average_d = index
                num_av_scans += 1
            index += 1

        # if no average scans found set average_d to -1
        if num_av_scans == 0:
            self.average_d = -1

        # throw an error if more than one average scan is found
        if num_av_scans > 1:
            assert False, "More than one average scan is not allowed"

        # make sure there are no empty scans inbetween used scans.
        used_scan_found = False
        scans = self.scans
        for i in range(len(scans)):
            count_down = len(scans) - i - 1
            if used_scan_found is False:
                if not (isinstance(scans[count_down], PropertyScan) and len(scans[count_down].input_dict) == 0):
                    used_scan_found = True
                    used_scan_index = count_down
            else:
                assert not (isinstance(scans[count_down], PropertyScan) and len(scans[count_down].input_dict) == 0), \
                    (f"Found empty PropertyScan (scan{count_down}) below used scan (scan{used_scan_index}).\n"
                     + "Scans must be populated in sequential order.")

        # find the scan set to continuous scan (if any) and determine the index
        for i, scan in enumerate(self.scans):
            if isinstance(scan, ps.ContinuousScan):
                self.continuous = True
                self.continuous_scan_index = i

        # If there is a ContinuousScan, ensure it is the highest level scan
        if self.continuous:
            for i in range(self.continuous_scan_index + 1, len(self.scans)):
                assert isinstance(self.scans[i], PropertyScan) and len(self.scans[i].input_dict) == 0, \
                    f"ContinuousScan found at scan{self.continuous_scan_index} but is not the highest level scan."

    def stop_continuous(self, plus_one=False):
        stop = False
        if self.continuous:
            continuous_scan = self.scans[self.continuous_scan_index]
            if hasattr(continuous_scan, 'n_max'):
                if plus_one is False:
                    if continuous_scan.n_max <= continuous_scan.i:
                        stop = True
                elif plus_one is True:
                    if continuous_scan.n_max <= continuous_scan.i + 1:
                        stop = True

        return stop

    @property
    def scans(self):
        ''' Returns array of all scans
        '''
        return [self.scan0, self.scan1, self.scan2, self.scan3]

    @property
    def dims(self):
        ''' Returns tuple containing the length of each scan, in order from scan0 to scan3, and excludes scans of size 1
        '''
        dims = (self.scan0.n,
                self.scan1.n,
                self.scan2.n,
                self.scan3.n)
        dims = [n for n in dims if n != 1]
        if self.continuous:
            if len(dims) - 1 == self.continuous_scan_index:
                dims = dims[:-1]
            dims.append(1)
        self._dims = tuple(dims)
        return self._dims

    @property
    def average_dims(self):
        ''' Returns tuple containing the length of each scan, excluding scans of size 1 and the averaged scan
        '''
        self._average_dims = tuple(drop(self.dims, self.average_d))

        return self._average_dims

    @property
    def ndim(self):
        ''' Returns number of non 1 sized scans
        '''
        self._ndim = len(self.dims)
        return self._ndim

    @property
    def n_average_dim(self):
        ''' Returns number of scans that are neither size-1 nor average scans
        '''
        self._n_average_dim = len(self.average_dims)
        return self._n_average_dim

    @property
    def indicies(self):
        '''
        Returns tuple of the current scan iteration indicies,
        '''
        self._indicies = (self.scan0.i,
                          self.scan1.i,
                          self.scan2.i,
                          self.scan3.i)
        self._indicies = self._indicies[:self.ndim]
        if self.continuous:
            self._indicies = self._indicies[:-1]
        return tuple(self._indicies)

    @property
    def line_indicies(self):
        self._line_indicies = (
            self.scan1.i,
            self.scan2.i,
            self.scan3.i)
        self._line_indicies = self._line_indicies[:self.ndim]
        return tuple(self._line_indicies)

    @property
    def average_indicies(self):
        ''' Returns tuple of the current scan iteration indicies,
        excluding scans of size 1 and averaged scan. These are the active
        scans not to be averaged. Used by `.AverageExperiment`.
        '''
        self._average_indicies = drop(self.indicies, self.average_d)
        return tuple(self._average_indicies)

    @property
    def average_index(self):
        ''' Returns the index of the scan to be averaged. Used by `pyscan.AverageExperiment`.
        '''
        self._average_index = self.indicies[self.average_d]
        return self._average_index

    @property
    def has_average_scan(self):
        ''' Returns a boolean of whether or not an average scan is present.
        '''
        num_av_scans = 0
        for scan in self.scans:
            if isinstance(scan, AverageScan):
                num_av_scans += 1

        if num_av_scans > 0:
            self._has_average_scan = True
        else:
            self._has_average_scan = False

        return self._has_average_scan

    ####################### LEGACY SECTION ########################
    # This section is set up to alert users who try to use legacy nomenclature
    # of the updated naming convention that they must use instead.
    @property
    def loop0(self):
        legacy_warning()
        return self.scan0

    @loop0.setter
    def loop0(self, value):
        legacy_warning()
        self.scan0 = value

    @property
    def loop1(self):
        legacy_warning()
        return self.scan1

    @loop1.setter
    def loop1(self, value):
        legacy_warning()
        self.scan1 = value

    @property
    def loop2(self):
        legacy_warning()
        return self.scan2

    @loop2.setter
    def loop2(self, value):
        legacy_warning()
        self.scan2 = value

    @property
    def loop3(self):
        legacy_warning()
        return self.scan3

    @loop3.setter
    def loop3(self, value):
        legacy_warning()
        self.scan3 = value

    @property
    def loops(self):
        '''
        Returns array of all scans
        '''
        legacy_warning()
        return [self.scan0, self.scan1, self.scan2, self.scan3]


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


def legacy_warning():
    warning_msg = ("Use of legacy nomenclature detected but no longer supported.\n"
                   + "You entered 'loop', use 'scan' instead.")
    raise DeprecationWarning(f"\033[93m*** WARNING! ***: {warning_msg} \033[0m")
    assert False, f"\033[93m*** WARNING! ***: {warning_msg} \033[0m"
