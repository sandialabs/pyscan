'''
Pytest functions to test the load experiment function
'''

import pyscan as ps
import pytest
import os
from pathlib import Path

# This will need to be changed to omit the \..\.. but is in place for my current testing system
ROOT_DIR = os.path.abspath(os.curdir) + r'\..\..'
#ROOT_DIR = os.path.abspath(os.curdir)


def check_has_attributes(obj, name, attributes):
    for a in attributes:
        assert hasattr(obj, a), "loaded experiment " + name + " does not have " + a + " attribute"


def test_load_experiment():
    """
    Testing load experiment function

    Returns
    --------
    None
    """

    # for testing different files to see if they load or not. Must use actual experiment files to pass.
    def test_different_files(file_name):
        file_path = Path(file_name)
        if ('.pk1' in file_name or '.hdf5' in file_name 
                or file_path.with_suffix('.pkl').is_file() or file_path.with_suffix('.hdf5').is_file()):
            expt = ps.load_experiment(file_name)
        else:
            with pytest.raises(Exception):
                ps.load_experiment(file_name)

        expt_attributes = ['runinfo', 'devices', 'v1_voltage', 'x1', 'x2', 'x3']
        check_has_attributes(expt, 'expt', expt_attributes)

        runinfo_attributes = ['loop0', 'loop1', 'loop2', 'loop3', 'static', 'measured', 'measure_function',
                              'trigger_function', 'initial_pause', 'average_d', 'verbose', 'time',
                              'long_name', 'short_name', 'running']
        check_has_attributes(expt.runinfo, 'runinfo', runinfo_attributes)

        loop_attributes = ['prop', 'scan_dict', 'input_dict', 'device_names', 'property', 'dt', 'n', 'nrange', 'i']
        check_has_attributes(expt.runinfo.loop0, 'loop0', loop_attributes)
        check_has_attributes(expt.runinfo.loop1, 'loop1', loop_attributes)
        check_has_attributes(expt.runinfo.loop2, 'loop2', loop_attributes)
        check_has_attributes(expt.runinfo.loop3, 'loop3', loop_attributes)

        devices_attributes = ['v1', 'v2', 'v3']
        check_has_attributes(expt.devices, 'devices', devices_attributes)

        v_attributes = ['debug', '_voltage', '_other_voltage']
        for device in expt.devices.__dict__.keys():
            check_has_attributes(expt.devices[device], device, v_attributes)

            assert type(expt.devices[device].debug) is bool, "devices " + device + " debug is not loaded as a boolean"
            assert type(expt.devices[device]._voltage) is int, "devices " + device + " voltage is not loaded as an int"
            err_string = "devices " + device + " other voltage is not loaded as an int"
            assert type(expt.devices[device]._other_voltage) is int, err_string

        assert isinstance(expt, ps.ItemAttribute), "expt is not loaded as an instance of item attribute"
        assert isinstance(expt.runinfo, ps.ItemAttribute), "expt runinfo is not loaded as an instance of item attribute"
        assert isinstance(expt.devices, ps.ItemAttribute), "expt devices is not loaded as an instance of item attribute"
        assert isinstance(expt.runinfo.static, ps.ItemAttribute), "runinfo static is not loaded as an item attribute"
        assert isinstance(expt.devices.v1, ps.ItemAttribute), "runinfo v1 is not loaded as an item attribute"
        assert isinstance(expt.devices.v2, ps.ItemAttribute), "runinfo v2 is not loaded as an item attribute"
        assert isinstance(expt.devices.v3, ps.ItemAttribute), "runinfo v3 is not loaded as an item attribute"

        assert type(expt.runinfo.measured) is list, "runinfo measured is not loaded as a list"
        assert type(expt.runinfo.measure_function) is str, "runinfo measure function is not loaded as a string"
        assert expt.runinfo.trigger_function is None, "runinfo trigger function is not loaded as None"
        assert type(expt.runinfo.initial_pause) is float, "runinfo initial pause is not loaded as a float"
        assert type(expt.runinfo.average_d) is int, "runinfo average_d is not loaded as a float"
        assert type(expt.runinfo.verbose) is bool, "runinfo verbose is not loaded as a boolean"
        assert type(expt.runinfo.time) is bool, "runinfo time is not loaded as a boolean"
        assert type(expt.runinfo.long_name) is str, "runinfo long_name is not loaded as a string"
        assert type(expt.runinfo.short_name) is str, "runinfo short_name is not loaded as a string"
        assert type(expt.runinfo.running) is bool, "runinfo running is not loaded as a boolean"

        #print(type(expt.devices.v1['_other_voltage']))
        print("Success!")

    # file name may need to be updated depending on what files are available, or to select generic files.
    file_name = ROOT_DIR + r'\demo_notebooks\backup\20231129T090758.hdf5'
    test_different_files(file_name)


test_load_experiment()
