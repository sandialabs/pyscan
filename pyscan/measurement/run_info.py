from itemattribute import ItemAttribute
from .get_pyscan_version import get_pyscan_version
from .scans import PropertyScan, AverageScan, ContinuousScan, AbstractOptimizeScan
import pyscan as ps
import re
import numpy as np


class RunInfo(ItemAttribute):
    '''
    Object that contains information of how to run the experiment.

    Attributes
    ----------
    scan<#>: ps.PropertyScan, ps.RepeatScan, ps.FunctionScan, ps.FunctionScan
        Instance of ps.AbstractScan to a scan object representing one independent experimental variable.
        The scan property or function will be scanned during the experiment, with scan0 being the innermost scan loop.
    measured : list
        List that contains the names of collected data, defined by the `measure_function` return.
    measure_function : func
        User-defined function that controls how to measure data.
        It should accept a ps.Experiment object as its only parameter,
        and returns an ItemAttribute object containing the measured data. The names of the measured data,
        each being an attribute of the return object, will appear as keys of the experiment after it is run.
    initial_pause : float
        Pause before first setting instruments in seconds, defaults to 0.1.
    _pyscan_version : str
        Current version of pyscan to be saved as metadata.

    (Properties)
    scans : list
        Returns list of all scans in sequential order.
    dims : tuple
        Returns tuple containing the length of each scan, by increasing scan number
    average_dims : tuple
        Returns a tuple containing the lenght of each scan, excluding the average scan
    ndim : int
        Returns number of scans
    has_average_scan : bool
        True if an average scan is present, False otherwise
    indicies : tuple
        Returns tuple of the current scan iteration indicies
    average_indicies : tuple
        Returns tuple of the current scan iteration indicies, excludingb averaged scan
    average_index : int
        Returns the index of the scan to be averaged, -1 if no average scan is present

    Methods
    -------
    check()
    check_sequential_scans()
    check_property_scan()
    check_repeat_scan()
    check_average_scan()
    check_continuous_scan()
    check_optimize_scan()
    '''

    def __init__(self):
        """
        Constructor method
        """

        self.measured = []
        self.measure_function = None

        self.initial_pause = 0.1

        self._pyscan_version = get_pyscan_version()

    def check(self):
        '''
        Checks to see if runinfo is properly formatted. Called by Experiment object's `run()` methods.

        Automatically sets `self.average_index` to the correct scan index (i.e., the scan which contains an
        instance of `.AverageScan`) to average over.
        '''

        self.check_sequential_scans()

        self.check_property_scans()

        self.check_repeat_scan()

        self.check_average_scan()

        self.check_continuous_scan()

        self.check_optimize_scan()

    def check_sequential_scans(self):

        scan_indicies = []
        for key in self.__dict__.keys():
            if 'scan' in key:
                if len(re.findall(r'\d+', key)) > 0:
                    scan_indicies.append(int(re.findall(r'\d+', key)[0]))

        scan_indicies.sort()
        delta_indices = [scan_indicies[i] - scan_indicies[i - 1] for i in range(1, len(scan_indicies))]
        assert np.all(np.array(delta_indices) == 1), 'Scan indicies are not sequential'

    def check_property_scans(self):
        '''
        Checks to see if there are any errors with PropertyScans
        '''

        scanned_properties = []
        for scan in self.scans:
            if isinstance(scan, PropertyScan):
                for dev in scan.device_names:
                    assert f'{dev}_{scan.prop}' not in scanned_properties, \
                        'Property {} is duplicated in the scans'.format(f'{dev}_{scan.prop}')
                    scanned_properties.append(f'{dev}_{scan.prop}')

    def check_average_scan(self):
        '''
        Checks to see if there is an average scan present and sets `self.average_index` to the correct index.
        '''

        # find the scan set to average scan (if any) and determine the index
        index = 0
        num_av_scans = 0
        for scan in self.scans:
            if isinstance(scan, AverageScan):
                num_av_scans += 1
            index += 1

        # throw an error if more than one average scan is found
        if num_av_scans > 1:
            assert False, "More than one average scan is not allowed"

    def check_repeat_scan(self):
        '''
        Checks to see if there a repeat scan present and if there are more the one repeat scans
        '''

        repeat_count = 0
        for scan in self.scans:
            if isinstance(scan, ps.RepeatScan):
                repeat_count += 1

        assert repeat_count <= 1, "More than one repeat scan is not allowed"

    def check_continuous_scan(self):
        # find the scan set to continuous scan (if any) and determine the index
        n_continuous_scans = 0
        for i, scan in enumerate(self.scans):
            if isinstance(scan, ps.ContinuousScan):
                n_continuous_scans += 1

        assert n_continuous_scans <= 1, "More than one continuous scan detected. Only one continuous scan is allowed."

        # If there is a ContinuousScan, ensure it is the highest level scan
        if self.has_continuous_scan:
            assert self.continuous_index == (self.ndim - 1), 'Error, continuous scan must be the last scan'

    def stop_continuous(self, plus_one=False):
        stop = False
        if self.has_continuous_scan:
            continuous_scan = self.scans[self.continuous_scan_index]
            if hasattr(continuous_scan, 'n_max'):
                if plus_one is False:
                    if continuous_scan.n_max <= continuous_scan.i:
                        stop = True
                elif plus_one is True:
                    if continuous_scan.n_max <= continuous_scan.i + 1:
                        stop = True

        return stop

    def check_optimize_scan(self):
        # find the scans set to optimize scan (if any) and determine the index
        n_optimize_scans = 0
        for scan in self.scans:
            if isinstance(scan, AbstractOptimizeScan):
                n_optimize_scans += 1

        # throw an error if more than one optimize scan is found
        assert n_optimize_scans <= 1, "More than one optimize scan detected. Only one optimize scan is allowed."

        # if there is a optimize scan, ensure it is the highest level scan
        if self.has_optimize_scan:
            assert self.optimize_index == (self.ndim - 1), 'Error, optimize scan must be the last scan'

    # Regular properties
    @property
    def scans(self):
        '''
        Returns array of all scans
        '''
        i = 0
        scans = []
        while hasattr(self, f'scan{i}'):
            scans.append(getattr(self, f'scan{i}'))
            i += 1
        return scans

    @property
    def dims(self):
        '''
        Returns tuple containing the length of each scan, in order from scan0 to scan3, and excludes scans of size 1
        '''
        dims = [scan.n for scan in self.scans]
        self._dims = tuple(dims)
        return self._dims

    @property
    def indicies(self):
        '''
        Returns tuple of the current scan iteration indicies,
        '''
        self._indicies = [scan.i for scan in self.scans]
        return tuple(self._indicies)

    @property
    def ndim(self):
        '''
        Returns number of scans
        '''
        self._ndim = len(self.dims)
        return self._ndim

    # Properties modified due to the presence of an average scan
    @property
    def has_average_scan(self):
        '''
        Returns a boolean of whether or not an average scan is present.
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

    @property
    def average_index(self):
        '''
        Returns the index of the scan to be averaged. Used by `pyscan.AverageExperiment`.
        '''
        if self.has_average_scan:
            i = 0
            for scan in self.scans:
                if isinstance(scan, AverageScan):
                    return i
                i += 1
            self._average_index = self.indicies[self.average_dims]
            return self._average_index
        else:
            return -1

    @property
    def average_dims(self):
        '''
        Returns tuple containing the length of each scan, excluding scans of size 1 and the averaged scan
        '''
        if self.average_index != -1:
            self._average_dims = list(self.dims)
            self._average_dims.pop(self.average_index)
            return tuple(self._average_dims)
        else:
            return ()

    @property
    def average_indicies(self):
        '''
        Returns tuple of the current scan iteration indicies, excluding scans of size 1 and averaged scan.
        Used by `.AverageExperiment`.
        '''
        if self.has_average_scan:
            self._average_indicies = list(self.indicies)
            self._average_indicies.pop(self.average_index)
            return tuple(self._average_indicies)
        else:
            return ()

    @property
    def n_average_dim(self):
        '''
        Returns number of scans that are neither size-1 nor average scans
        '''
        self._n_average_dim = len(self.average_dims)
        return self._n_average_dim

    # Properties based on the presence of a continuous scan
    @property
    def has_continuous_scan(self):
        '''
        Returns a boolean of whether or not an continuous scan is present.
        '''
        num_av_scans = 0
        for scan in self.scans:
            if isinstance(scan, ContinuousScan):
                num_av_scans += 1

        if num_av_scans > 0:
            self._has_continuous_scan = True
        else:
            self._has_continuous_scan = False

        return self._has_continuous_scan

    @property
    def continuous_index(self):
        '''
        Returns the index of the scan to be averaged. Used by `pyscan.AverageExperiment`.
        '''
        if self.has_continuous_scan:
            i = 0
            for i in range(self.ndim):
                if isinstance(self.scans[i], ContinuousScan):
                    return i
                self._continuous_index = i
        else:
            self._continuous_index = -1
        return self._continuous_index

    # Properties based on the presence of an optimize scan
    @property
    def has_optimize_scan(self):
        '''
        Returns a boolean of whether or not an optimize scan is present.
        '''
        num_op_scans = 0
        for scan in self.scans:
            if isinstance(scan, AbstractOptimizeScan):
                num_op_scans += 1

        if num_op_scans > 0:
            self._has_optimize_scan = True
        else:
            self._has_optimize_scan = False

        return self._has_optimize_scan

    @property
    def optimize_index(self):
        '''
        Returns the index of the optimize scan.
        '''
        if self.has_optimize_scan:
            i = 0
            for i in range(self.ndim):
                if isinstance(self.scans[i], AbstractOptimizeScan):
                    return i
                self._optimize_index = i
        else:
            self._optimize_index = -1
        return self._optimize_index

    # for reallocate in Experiment.run()
    @property
    def has_resizing_data(self):
        return self.has_continuous_scan or self.has_optimize_scan

    # collect scan iterators for Experiment.run()
    @property
    def iterators(self):
        return [scan.iterator() for scan in self.scans]
