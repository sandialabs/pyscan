'''
Pytest functions to test the meta sweep class
'''


import pyscan as ps
from pyscan.measurement.abstract_experiment import MetaSweep
from pathlib import Path
import random
import numpy as np
import pytest
from io import StringIO
import sys
import shutil
import re


# for testing default trigger function with empty function
def empty_function():
    pass


# for setting runinfo measure_function to measure 1D data randomly
def measure_point(expt):
    d = ps.ItemAttribute()

    d.x = random.random()

    return d


# for setting runinfo measure_function to measure (up to) 3D data randomly
def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = random.random()  # could make predictable to ensure data is saved properly
    d.x2 = [random.random() for i in range(2)]
    d.x3 = [[random.random() for i in range(2)] for j in range(2)]

    return d


# for checking 3d shaped arrays filled with nans
def check_3D_array(array):
    for k in array:
        for j in k:
            for i in j:
                assert isinstance(i, np.float64)
                # again, is this supposed to always be nan after running above save functions?
                assert np.isnan(i)


def test_meta_sweep():
    """
    Testing meta sweep (legacy)

    Returns
    --------
    None
    """

    def test_ms_diff_inputs(data_dir=None, measure_function=measure_point, allocate='preallocate'):
        devices = ps.ItemAttribute()
        devices.v1 = ps.TestVoltage()
        devices.v2 = ps.TestVoltage()
        devices.v3 = ps.TestVoltage()

        runinfo = ps.RunInfo()

        # consider adding and testing for 4 loops since runinfo has 4 by default. Should 3 be allowed by Meta Sweep?
        runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
        runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0.5)}, 'voltage')
        runinfo.loop2 = ps.PropertyScan({'v3': ps.drange(0.5, 0.1, 0.8)}, 'voltage')

        # dictionary of scans to later verify they were saved according to scans created
        scans = {'scan0': 'v1', 'scan1': 'v2', 'scan2': 'v3'}

        runinfo.measure_function = measure_function

        ms = MetaSweep(runinfo, devices, data_dir)

        # testing meta sweep's init
        assert hasattr(ms, 'runinfo'), "Meta Sweep runinfo not set up"
        assert ms.runinfo == runinfo, "Meta Sweep runinfo not set up properly"

        assert hasattr(ms, 'devices'), "Meta Sweep devices not set up"
        assert ms.devices == devices, "Meta Sweep devices not set up properly"

        assert hasattr(ms.runinfo, 'data_path'), "Meta Sweep data path not set up"

        # testing meta sweep's setup data dir method
        assert callable(ms.setup_data_dir)
        ms.setup_data_dir(data_dir)
        if data_dir is None:
            assert ms.runinfo.data_path == Path('./backup'), "Meta Sweep data path not set up properly"
        else:
            # ################ This is what the program is doing... is this what we want? ###############
            assert ms.runinfo.data_path == Path(Path(data_dir)), "Meta Sweep data path not set up properly"
        assert ms.runinfo.data_path.is_dir()

        # testing meta sweep's check runinfo method
        assert callable(ms.check_runinfo)
        ms.check_runinfo()
        assert ms.check_runinfo() == 1

        assert hasattr(ms.runinfo, 'long_name'), "Meta Sweep runinfo long name is not initialized by check_runinfo()"
        assert isinstance(ms.runinfo.long_name, str), "Meta Sweep runinfo long name is not initialized as a string"
        # check that the long name is formatted with values for YYYYMMDDTHHMMSS, and optionally a - followed by digits.
        assert re.match(r'^\d{8}T\d{6}(-\d+)?$', ms.runinfo.long_name), "runinfo long_name is not properly formatted"

        assert hasattr(ms.runinfo, 'short_name'), "Meta Sweep runinfo long name is not initialized by check_runinfo()"
        assert isinstance(ms.runinfo.short_name, str), "Meta Sweep runinfo short name is not initialized as a string"
        assert len(ms.runinfo.short_name) == 7, "Meta Sweep runinfo short name is not 7 characters"
        assert ms.runinfo.short_name == ms.runinfo.long_name[8:], "Meta Sweep short name is not the correct value"

        # setting file name for loading later
        if data_dir is None:
            file_name = './backup/' + ms.runinfo.long_name
        else:
            file_name = data_dir + '/' + ms.runinfo.long_name

        # ############### testing meta sweeps preallocate method here? Or will we be changing to dynamic allocation?
        data = ms.runinfo.measure_function(ms)
        if np.all(np.array(ms.runinfo.indicies) == 0):
            for key, value in data.items():
                ms.runinfo.measured.append(key)
            if allocate == 'preallocate':
                ms.preallocate(data)
            elif allocate == 'preallocate_line':
                ms.preallocate_line(data)
            else:
                assert False, "allocate input variable for test not acceptable"

        # testing meta sweep's check runinfo method with bad loop inputs
        bad_runinfo = ps.RunInfo()
        bad_runinfo.loop0 = ps.PropertyScan({'v8': ps.drange(0, 0.1, 0.1)}, 'voltage')
        bad_ms = MetaSweep(bad_runinfo, devices, data_dir)

        with pytest.raises(Exception):
            bad_ms.check_runinfo(), "Metasweep's check runinfo did not ensure validation of devices and properties"

        # testing meta sweep's check runinfo method with more than 1 repeat loop
        bad_runinfo2 = ps.RunInfo()
        bad_runinfo2.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
        bad_runinfo2.loop1 = ps.RepeatScan(3)
        bad_runinfo2.loop2 = ps.RepeatScan(3)
        bad_ms2 = MetaSweep(bad_runinfo, devices, data_dir)

        with pytest.raises(Exception):
            bad_ms2.check_runinfo(), "Metasweep's check runinfo did not flag runinfo with more than one repeat scan"

        # testing meta sweep's get time method *placeholder*
        assert callable(ms.get_time)

        # ############# The following saves don't seem to be saving any data to the file, not sure why...
        # testing meta sweep's save point method
        assert callable(ms.save_point)
        ms.save_point()

        # testing meta sweep's save row method
        assert callable(ms.save_row)
        ms.save_row()

        # testing meta sweep's save meta data method
        assert callable(ms.save_metadata)
        ms.save_metadata()

        # now loading the experiment to check the information was saved properly
        temp = ps.load_experiment(file_name)
        # print("temp dict is: ", temp.__dict__.keys())

        # test that preallocate and saves functioned as expected based on loaded experiment
        if allocate == 'preallocate':
            if list(data.__dict__.keys()) == ['x']:
                assert temp.x.shape == (2, 5, 5)
                check_3D_array(temp.x)
            elif list(data.__dict__.keys()) == ['x1', 'x2', 'x3']:
                assert temp.x1.shape == (2, 5, 5)
                check_3D_array(temp.x1)

                assert temp.x2.shape == (2, 5, 5, 2)
                for f in temp.x2:
                    check_3D_array(f)

                assert temp.x3.shape == (2, 5, 5, 2, 2)
                for z in temp.x3:
                    for f in z:
                        check_3D_array(f)
        else:
            if list(data.__dict__.keys()) == ['x']:
                assert temp.x.shape == (2, 5, 5)
                check_3D_array(temp.x)
            elif list(data.__dict__.keys()) == ['x1', 'x2', 'x3']:
                assert temp.x1.shape == (2, 5, 5)
                check_3D_array(temp.x1)
                assert temp.x2.shape == (2, 5, 5)
                check_3D_array(temp.x2)
                assert temp.x3.shape == (2, 5, 5)
                check_3D_array(temp.x3)

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
        assert temp.runinfo.measured == list(data.__dict__.keys()), "save meta data didn't save true runinfo.measured"

        # check that loops meta data was saved/loaded correctly
        ''' legacy not working with loop nomenclature for loaded expt's... consider fixing this somehow...
        assert hasattr(temp.runinfo, 'scan0'), "save meta data didn't save loop0, or it couldn't be loaded"
        assert hasattr(temp.runinfo, 'loop1'), "save meta data didn't save loop1, or it couldn't be loaded"
        assert hasattr(temp.runinfo, 'loop2'), "save meta data didn't save loop2, or it couldn't be loaded"'''
        assert hasattr(temp.runinfo, 'scan0'), "save meta data didn't save loop0, or it couldn't be loaded"
        assert hasattr(temp.runinfo, 'scan1'), "save meta data didn't save loop1, or it couldn't be loaded"
        assert hasattr(temp.runinfo, 'scan2'), "save meta data didn't save loop2, or it couldn't be loaded"

        for scan in scans:
            assert temp.runinfo[scan].prop == 'voltage', "save meta data didn't save " + scan + ".prop correctly"
            assert hasattr(temp.runinfo[scan], 'scan_dict'), "save meta data didn't save " + scan + "scan_dict"
            assert hasattr(temp.runinfo[scan], 'input_dict'), "save meta data didn't save " + scan + "input_dict"
            assert temp.runinfo[scan].device_names == [scans[scan]], "save meta data didn't save " + scan + "devicename"
            assert temp.runinfo[scan].dt == 0, "save meta data didn't save " + scan + ".dt correctly"
            assert temp.runinfo[scan].i == 0, "save meta data didn't save " + scan + ".i correctly"

        assert temp.runinfo.scan0.n == 2, "save meta data didn't save loop0.n, or it couldn't be loaded"
        assert temp.runinfo.scan1.n == 5, "save meta data didn't save loop1.n, or it couldn't be loaded"
        assert temp.runinfo.scan2.n == 5, "save meta data didn't save loop2.n, or it couldn't be loaded"
        assert temp.runinfo.scan0.nrange == [0, 1], "save meta data didn't save loop0.nrange value"
        assert temp.runinfo.scan1.nrange == [0, 1, 2, 3, 4], "save meta data didn't save loop1.nrange value"
        assert temp.runinfo.scan2.nrange == [0, 1, 2, 3, 4], "save meta data didn't save loop2.nrange value"

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
        with pytest.raises(Exception):
            ms.default_trigger_function()

        ms.devices.trigger = ps.ItemAttribute()
        ms.devices.trigger.trigger = empty_function
        ms.default_trigger_function()

        if data_dir is None:
            shutil.rmtree('./backup')
        else:
            shutil.rmtree(data_dir)

    test_ms_diff_inputs()
    test_ms_diff_inputs(data_dir='./backeep')
    test_ms_diff_inputs(data_dir='./backup', allocate='preallocate_line')
    test_ms_diff_inputs(data_dir=None, measure_function=measure_up_to_3D)
    test_ms_diff_inputs(data_dir='./backup', measure_function=measure_up_to_3D)
    test_ms_diff_inputs(data_dir='./backup', measure_function=measure_up_to_3D, allocate='preallocate_line')
