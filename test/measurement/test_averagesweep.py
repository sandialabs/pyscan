'''
Pytest functions to test the AverageSweep experiment class
'''


import pyscan as ps
import shutil
from pathlib import Path
from random import random
import numpy as np


##################### FUNCTIONS USED BY TEST CASES #####################


# for setting runinfo measure_function to measure 1D data
def measure_point(expt):
    d = ps.ItemAttribute()

    d.x = random()

    return d


# for checking that the experiment has data measurement attribute
def check_has_data(expt, loaded=False):
    is_loaded = loaded_modifier(loaded)
    assert hasattr(expt, 'x'), is_loaded + "experiment missing x attribute after running"


# for setting runinfo measure_function to measure (up to) 3D data
def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = random()  # could make predictable to ensure data is saved properly
    d.x2 = [random() for i in range(2)]
    d.x3 = [[random() for i in range(2)] for j in range(2)]

    return d


# for checking that the experiment has multidata measurement attributes
def check_has_multi_data(expt, loaded=False):
    is_loaded = loaded_modifier(loaded)
    pre_string = is_loaded + "experiment missing x"
    post_string = " attribute after running"
    assert hasattr(expt, 'x1'), pre_string + "1" + post_string
    assert hasattr(expt, 'x2'), pre_string + "2" + post_string
    assert hasattr(expt, 'x3'), pre_string + "3" + post_string


# for setting up prestring based on loaded to differentiate loaded experiment error strings
def loaded_modifier(loaded):
    if (loaded is True):
        return 'loaded '
    else:
        return ''


# for setting up the experiments
def set_up_experiment(num_devices, measure_function, data_dir, verbose):
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_function
    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')

    if (num_devices > 1):
        devices.v2 = ps.TestVoltage()
        runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')

    if (num_devices > 2):
        devices.v3 = ps.TestVoltage()
        runinfo.loop2 = ps.PropertyScan({'v3': ps.drange(0.3, 0.1, 0.2)}, 'voltage')

    if (num_devices > 3):
        devices.v4 = ps.TestVoltage()
        runinfo.loop3 = ps.PropertyScan({'v4': ps.drange(-0.1, 0.1, 0)}, 'voltage')

    if (num_devices > 4):
        assert False, "num_devices > 4 not implemented in testing"

    if data_dir is None:
        if verbose is False:
            expt = ps.AverageSweep(runinfo, devices)
        elif verbose is True:
            expt = ps.AverageSweep(runinfo, devices, verbose=verbose)
        else:
            assert False, "Invalid verbose entry. Must be boolean."
    elif type(data_dir) is str:
        if verbose is False:
            expt = ps.AverageSweep(runinfo, devices, data_dir)
        elif verbose is True:
            expt = ps.AverageSweep(runinfo, devices, data_dir, verbose)
        else:
            assert False, "Invalid verbose entry. Must be boolean."
    else:
        assert False, "Invalid data_dir entry. Must be a string"

    return expt


# for checking that the voltage(s) as expected
def check_voltage_results(voltage, expected_value1, expected_value2, voltage_id=1, loaded=False, string_modifier=''):
    is_loaded = loaded_modifier(loaded)

    pre_string = is_loaded + "experiment v" + str(voltage_id) + string_modifier + "_voltage "
    assert (isinstance(voltage, np.ndarray) or isinstance(voltage, list)), pre_string + "is not a numpy array"
    for i in voltage:
        try:
            assert i.dtype == 'float64', pre_string + "data is not a float"
        except Exception:
            assert isinstance(i, float), pre_string + "data is not a float"
    assert len(voltage) == 2, pre_string + "array does not have 2 elements"
    assert voltage[0] == expected_value1, pre_string + "value[0] is not " + str(expected_value1)
    assert voltage[1] == expected_value2, pre_string + "value[1] is not " + str(expected_value2)


def test_averagesweep():
    """
    Testing AverageSweep

    Returns
    --------
    None
    """

    def test_variations(num_devices=1, measure_function=measure_point, data_dir=None, verbose=False):
        expt = set_up_experiment(num_devices, measure_function, data_dir, verbose)

        # check the experiment core attributes are initialized correctly
        assert hasattr(expt, 'runinfo'), "expt does not have runinfo attribute"
        assert hasattr(expt, 'devices'), "expt does not have devices attribute"
        assert expt.runinfo.data_path.exists(), "experiment data path does not exist"
        assert expt.runinfo.data_path.is_dir(), "experiment data path is not a directory"
        if data_dir is None:
            assert str(expt.runinfo.data_path) == 'backup', "experiment data path does not equal 'backup'"
        else:
            assert str(expt.runinfo.data_path) == str(Path(data_dir)), "bad"

        # check the experiment runinfo
        expt.check_runinfo()

        # run the experiment
        expt.run()

        # check that the experiment has the data measurement attribute(s)
        if measure_function == measure_point:
            check_has_data(expt)
        elif measure_function == measure_up_to_3D:
            check_has_multi_data(expt)

        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1)
        if num_devices > 1:
            check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2)
        if num_devices > 2:
            check_voltage_results(expt.v3_voltage, expected_value1=0.3, expected_value2=0.2, voltage_id=3)
        if num_devices > 3:
            check_voltage_results(expt.v4_voltage, expected_value1=-0.1, expected_value2=0, voltage_id=4)

        # add more testing here?

        # saves file name of the saved experiment data and deletes the experiment
        file_name = expt.runinfo.long_name
        del expt

        # load the experiment we just ran
        temp = ps.load_experiment('./backup/{}'.format(file_name))

        

        # close and delete directories created from running this test
        if data_dir is None:
            shutil.rmtree('./backup')
        else:
            try:
                shutil.rmtree(data_dir)
            except (Exception):
                pass

    test_variations()
    # test_variations(num_devices=4)  # this is not working... should it be?
    test_variations(measure_function=measure_up_to_3D)
    test_variations(data_dir='./bakeep')
    test_variations(verbose=True)


test_averagesweep()
