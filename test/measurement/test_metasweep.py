'''
Pytest functions to test the meta sweep class
'''


import pyscan as ps
from pyscan.measurement.metasweep import MetaSweep
from pathlib import Path
from random import random
import numpy as np


# for setting runinfo measure_function to measure 1D data
def measure_point(expt):
    d = ps.ItemAttribute()

    d.x = random()

    return d


# for setting runinfo measure_function to measure (up to) 3D data
def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = random()  # could make predictable to ensure data is saved properly
    d.x2 = [random() for i in range(2)]
    d.x3 = [[random() for i in range(2)] for j in range(2)]

    return d


def test_meta_sweep():

    def test_ms_diff_inputs(data_dir=None, measure_function=measure_point):
        devices = ps.ItemAttribute()
        devices.v1 = ps.TestVoltage()

        runinfo = ps.RunInfo()
        runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
        print(list(runinfo.loop0.scan_dict.values()))

        runinfo.measure_function = measure_function

        ms = MetaSweep(runinfo, devices, data_dir)

        # testing meta sweeps check runinfo function
        ms.check_runinfo()
        assert ms.check_runinfo() == 1
        assert hasattr(ms.runinfo, 'long_name'), "Meta Sweep runinfo long name is not initialized by check_runinfo()"
        # check long name format here
        assert hasattr(ms.runinfo, 'short_name'), "Meta Sweep runinfo long name is not initialized by check_runinfo()"
        assert ms.runinfo.short_name == ms.runinfo.long_name[8:], "Meta Sweep short name is not the correct value"

        assert ms.runinfo == runinfo, "Meta Sweep runinfo not set up properly"
        assert ms.devices == devices, "Meta Sweep devices not set up properly"
        assert ms.runinfo.data_path == Path('./backup')

        '''
        # testing meta sweeps preallocat function here
        data = ms.runinfo.measure_function(ms)
        if np.all(np.array(ms.runinfo.indicies) == 0):
            for key, value in data.items():
                ms.runinfo.measured.append(key)
            ms.preallocate(data)
        '''

    test_ms_diff_inputs()


test_meta_sweep()
