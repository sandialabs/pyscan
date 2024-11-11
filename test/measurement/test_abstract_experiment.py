'''
Pytest functions to test the meta sweep class
'''


import pyscan as ps
from pyscan.measurement.abstract_experiment import AbstractExperiment
from pathlib import Path
import random
import numpy as np
import pytest
from io import StringIO
import sys
import shutil
import re
import os


@pytest.fixture(scope='session')
def devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    devices.v3 = ps.TestVoltage()
    devices.v4 = ps.TestVoltage()
    return devices


def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = expt.runinfo.scan0.i
    d.x2 = [d.x1 for _ in range(2)]
    d.x3 = [[expt.runinfo.scan0.i, expt.runinfo.scan0.i] for _ in range(2)]

    return d


def test_abstract_experiment():
    """
    Testing abstract experiment

    Returns
    --------
    None
    """

    def test_ms_diff_inputs(data_dir=None, measure_function=measure_point, allocate='preallocate'):


        # ############### testing meta sweeps preallocate method here? Or will we be changing to dynamic allocation?
        data = ms.runinfo.measure_function(ms)
        if np.all(np.array(ms.runinfo.indicies) == 0):
            if allocate == 'preallocate':
                ms.preallocate(data)
            elif allocate == 'preallocate_line':
                ms.preallocate_line(data)
            else:
                assert False, "allocate input variable for test not acceptable"

        # testing meta sweep's check runinfo method with bad scan inputs
        bad_runinfo = ps.RunInfo()
        bad_runinfo.scan0 = ps.PropertyScan({'v8': ps.drange(0, 0.1, 0.1)}, 'voltage')
        bad_ms = AbstractExperiment(bad_runinfo, devices, data_dir)

        with pytest.raises(Exception):
            bad_ms.check_runinfo(), "Metasweep's check runinfo did not ensure validation of devices and properties"

        # testing meta sweep's check runinfo method with more than 1 repeat scan
        bad_runinfo2 = ps.RunInfo()
        bad_runinfo2.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
        bad_runinfo2.scan1 = ps.RepeatScan(3)
        bad_runinfo2.scan2 = ps.RepeatScan(3)
        bad_ms2 = AbstractExperiment(bad_runinfo, devices, data_dir)

        with pytest.raises(Exception):
            bad_ms2.check_runinfo(), "Metasweep's check runinfo did not flag runinfo with more than one repeat scan"

        # testing meta sweep's get time method *placeholder*
        assert callable(ms.get_time)

        # ############# The following saves don't seem to be saving any data to the file, not sure why...
        # testing meta sweep's save point method
        assert callable(ms.save_point)
        ms.save_point(data)

        # testing meta sweep's save meta data method
        assert callable(ms.save_metadata)
        ms.save_metadata()

        # now loading the experiment to check the information was saved properly
        temp = ps.load_experiment(file_name)
        os.remove(file_name + '.hdf5')
        # print("temp dict is: ", temp.__dict__.keys())

        # test that preallocate and saves functioned as expected based on loaded experiment
        if allocate == 'preallocate':
            if list(data.__dict__.keys()) == ['x']:
                assert temp.x.shape == (2, 5, 5)
                assert data.x in temp.x
            elif list(data.__dict__.keys()) == ['x1', 'x2', 'x3']:
                assert temp.x1.shape == (2, 5, 5)
                assert data.x1 in temp.x1

                assert temp.x2.shape == (2, 5, 5, 2)
                assert data.x2 in temp.x2

                assert temp.x3.shape == (2, 5, 5, 2, 2)
                assert data.x3 in temp.x3
        else:
            if list(data.__dict__.keys()) == ['x']:
                assert temp.x.shape == (2, 5, 5)
                assert data.x in temp.x
            elif list(data.__dict__.keys()) == ['x1', 'x2', 'x3']:
                assert temp.x1.shape == (2, 5, 5)
                assert data.x1 in temp.x1
                assert temp.x2.shape == (2, 5, 5)
                assert data.x2 in temp.x2
                assert temp.x3.shape == (2, 5, 5)
                assert data.x3 in temp.x3

        assert len(temp.__dict__.keys()) == 5 + len(ms.runinfo.measured)

        # check that the meta data was saved and loaded with expected attributes
        assert hasattr(temp, 'runinfo'), "runinfo was not saved/could not be loaded from meta data to temp"
        assert hasattr(temp, 'devices'), "devices was not saved/could not be loaded from meta data to temp"
        assert hasattr(temp, 'v1_voltage'), "v1_voltage was not saved/could not be loaded from meta data to temp"
        assert hasattr(temp, 'v2_voltage'), "v2_voltage was not saved/could not be loaded from meta data to temp"
        assert hasattr(temp, 'v3_voltage'), "v3_voltage was not saved/could not be loaded from meta data to temp"
        if list(data.__dict__.keys()) == ['x']:
            assert hasattr(temp, 'x'), "x was not saved/could not be loaded from meta data to temp"
        elif list(data.__dict__.keys()) == ['x1', 'x2', 'x3']:
            assert hasattr(temp, 'x1'), "x1 was not saved/could not be loaded from meta data to temp"
            assert hasattr(temp, 'x2'), "x2 was not saved/could not be loaded from meta data to temp"
            assert hasattr(temp, 'x3'), "x3 was not saved/could not be loaded from meta data to temp"

        # could maybe add to and clarify this
        assert hasattr(temp.runinfo, 'measured'), "save meta data didn't save runinfo.measured meta data"
        assert isinstance(temp.runinfo.measured, list), "save meta data didn't save runinfo.measured as a list"
        # order of list should not matter
        assert set(temp.runinfo.measured) == set(data.__dict__.keys()), "save meta data failed to save runinfo.measured"

        # check that scans meta data was saved/loaded correctly
        assert hasattr(temp.runinfo, 'scan0'), "save meta data didn't save scan0, or it couldn't be loaded"
        assert hasattr(temp.runinfo, 'scan1'), "save meta data didn't save scan1, or it couldn't be loaded"
        assert hasattr(temp.runinfo, 'scan2'), "save meta data didn't save scan2, or it couldn't be loaded"
        for scan in scans:
            assert temp.runinfo[scan].prop == 'voltage', "save meta data didn't save " + scan + ".prop correctly"
            assert hasattr(temp.runinfo[scan], 'scan_dict'), "save meta data didn't save " + scan + "scan_dict"
            assert hasattr(temp.runinfo[scan], 'input_dict'), "save meta data didn't save " + scan + "input_dict"
            assert temp.runinfo[scan].device_names == [scans[scan]], "save meta data didn't save " + scan + "devicename"
            assert temp.runinfo[scan].dt == 0, "save meta data didn't save " + scan + ".dt correctly"
            assert temp.runinfo[scan].i == 0, "save meta data didn't save " + scan + ".i correctly"

        assert temp.runinfo.scan0.n == 2, "save meta data didn't save scan0.n, or it couldn't be loaded"
        assert temp.runinfo.scan1.n == 5, "save meta data didn't save scan1.n, or it couldn't be loaded"
        assert temp.runinfo.scan2.n == 5, "save meta data didn't save scan2.n, or it couldn't be loaded"

        # check that devices were saved and loaded properly
        assert len(temp.devices.__dict__.keys()) == 3, "save meta data didn't save the right number of runinfo.devices"
        assert list(temp.devices.__dict__.keys()) == ['v1', 'v2', 'v3'], "save meta data issue saving runinfo.devices"

        # testing meta sweep's start thread method
        assert callable(ms.start_thread), "meta sweep's start thread method not callable"
        assert not hasattr(ms.runinfo, 'running'), "meta sweep runinfo has running attribute before expected"
        ms.start_thread()

        # try to affirm thread is running/ran here... threading only showed 1 thread running before and after
        assert hasattr(ms.runinfo, 'running'), "meta sweep runinfo does not have running attribute after start thread"
        assert ms.runinfo.running is True, "meta sweep's start thread method did not set runinfo running to true"

        # testing meta sweep's stop method
        assert callable(ms.stop), "meta sweep's stop method not callable"
        assert not hasattr(ms.runinfo, 'complete'), "meta sweep runinfo has complete attribute before expected"
        buffer = StringIO()
        sys.stdout = buffer
        ms.stop()
        assert hasattr(ms.runinfo, 'complete'), "meta sweep runinfo does not have complete attribute after stop()"
        assert ms.runinfo.running is False, "meta sweep's start thread method did not set runinfo running to false"
        assert ms.runinfo.complete == 'stopped', "meta sweep's stop method did not set runinfo complete to stopped"
        print_output = buffer.getvalue()
        sys.stdout = sys.__stdout__
        assert print_output.strip() == 'Stopping Experiment', "meta sweep's stop method does not print confirmation"

        # test meta sweep's run method *placeholder*
        assert callable(ms.run), "meta sweep's run method not callable"

        # test meta sweep's setup runinfo method *placeholder*
        assert callable(ms.setup_runinfo), "meta sweep's setup runinfo method not callable"

        # test meta sweep's setup instruments method *placeholder*
        assert callable(ms.setup_instruments), "meta sweep's setup instruments method not callable"

        # test meta sweep's default trigger method
        assert callable(ms.default_trigger_function), "meta sweep's default trigger method not callable"

        if data_dir is None:
            shutil.rmtree('./backup')
        else:
            shutil.rmtree(data_dir)

    test_ms_diff_inputs()
    test_ms_diff_inputs(data_dir='./backeep')

    test_ms_diff_inputs(data_dir=None, measure_function=measure_up_to_3D)
    test_ms_diff_inputs(data_dir='./backup', measure_function=measure_up_to_3D)
    with pytest.raises(Exception):
        # This should not work with preallocate_line as is,
        # because it doesn't factor data dimension into it's preallocation
        test_ms_diff_inputs(data_dir='./backup', measure_function=measure_up_to_3D, allocate='preallocate_line')
