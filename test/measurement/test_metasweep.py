'''
Pytest functions to test the meta sweep class
'''


import pyscan as ps
from pyscan.measurement.metasweep import MetaSweep
from pathlib import Path
import random
import numpy as np
import pytest
from io import StringIO
import sys
# import string
import shutil


# for testing default trigger function with empty function
def empty_function():
    pass


# for setting runinfo measure_function to measure 1D data
def measure_point(expt):
    d = ps.ItemAttribute()

    d.x = random.random()

    return d


# for setting runinfo measure_function to measure (up to) 3D data
def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = random.random()  # could make predictable to ensure data is saved properly
    d.x2 = [random.random() for i in range(2)]
    d.x3 = [[random.random() for i in range(2)] for j in range(2)]

    return d


def test_meta_sweep():
    """
    Testing meta sweep

    Returns
    --------
    None
    """

    def test_ms_diff_inputs(data_dir=None, measure_function=measure_point):
        devices = ps.ItemAttribute()
        devices.v1 = ps.TestVoltage()
        devices.v2 = ps.TestVoltage()
        devices.v3 = ps.TestVoltage()

        runinfo = ps.RunInfo()
        runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
        runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0.5)}, 'voltage')
        runinfo.loop2 = ps.PropertyScan({'v3': ps.drange(0.5, 0.1, 0.8)}, 'voltage')

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
        assert type(ms.runinfo.long_name) is str, "Meta Sweep runinfo long name is not initialized as a string"
        assert len(ms.runinfo.long_name) == 15, "Meta Sweep runinfo long name is not 15 characters"

        assert hasattr(ms.runinfo, 'short_name'), "Meta Sweep runinfo long name is not initialized by check_runinfo()"
        assert type(ms.runinfo.short_name) is str, "Meta Sweep runinfo short name is not initialized as a string"
        assert len(ms.runinfo.short_name) == 7, "Meta Sweep runinfo short name is not 7 characters"
        assert ms.runinfo.short_name == ms.runinfo.long_name[8:], "Meta Sweep short name is not the correct value"

        # setting file name for loading later
        file_name = './backup/{}'.format(ms.runinfo.long_name)

        # ############### testing meta sweeps preallocat method here? Or will we be changing to dynamic allocation?
        data = ms.runinfo.measure_function(ms)
        if np.all(np.array(ms.runinfo.indicies) == 0):
            for key, value in data.items():
                ms.runinfo.measured.append(key)
            ms.preallocate(data)

        # testing meta sweep's check runinfo method with bad inputs
        bad_runinfo = ps.RunInfo()
        bad_runinfo.loop0 = ps.PropertyScan({'v8': ps.drange(0, 0.1, 0.1)}, 'voltage')
        bad_ms = MetaSweep(bad_runinfo, devices, data_dir)

        with pytest.raises(Exception):
            bad_ms.check_runinfo()

        # testing meta sweep's get time method *placeholder*
        assert callable(ms.get_time)

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
        print("temp.__dict__ is: ", temp.__dict__)

        assert len(temp.__dict__.keys()) == 5 + len(ms.runinfo.measured)

        assert hasattr(temp.runinfo, 'measured'), "save meta data didn't save runinfo.measured meta data"
        assert type(temp.runinfo.measured) is list, "save meta data didn't save runinfo.measured as a list"
        assert temp.runinfo.measured == list(data.__dict__.keys()), "save meta data didn't save true runinfo.measured"

        assert hasattr(temp.devices, 'v1'), "save meta data didn't save runinfo.devices meta data"
        assert len(temp.devices.__dict__.keys()) == 3, "save meta data didn't save the right number of runinfo.devices"
        assert list(temp.devices.__dict__.keys()) == ['v1', 'v2', 'v3'], "save meta data issue saving runinfo.devices"

        # testing meta sweep's start thread method
        assert callable(ms.start_thread), "meta sweep's start thread method not callable"
        assert not hasattr(ms.runinfo, 'running'), "meta sweep runinfo has running attribute before expected"
        ms.start_thread()
        # try to affirm thread is running here... threading only showed 1 thread running before and after
        assert hasattr(ms.runinfo, 'running'), "meta sweep runinfo does not have running attribute after start thread"
        assert ms.runinfo.running is True, "meta sweep's start thread method did not set runinfo to running"

        # testing meta sweep's stop method
        assert callable(ms.stop), "meta sweep's stop method not callable"
        assert not hasattr(ms.runinfo, 'complete'), "meta sweep runinfo has complete attribute before expected"
        buffer = StringIO()
        sys.stdout = buffer
        ms.stop()
        assert hasattr(ms.runinfo, 'complete'), "meta sweep runinfo does not have complete attribute after stop()"
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

        ms.runinfo.complete = True
        ms.runinfo.running = False

        shutil.rmtree('./backup')

        print("Success!")

    test_ms_diff_inputs()
    test_ms_diff_inputs(data_dir=None, measure_function=measure_up_to_3D)
    test_ms_diff_inputs(data_dir='./backup', measure_function=measure_up_to_3D)


test_meta_sweep()
