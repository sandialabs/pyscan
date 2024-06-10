'''
Pytest functions to test the AverageSweep experiment class
'''


import pyscan as ps
import shutil
from pathlib import Path
from random import random
import numpy as np
import pytest
# import imp
# imp.reload(ps)


##################### FUNCTIONS USED BY TEST CASES #####################


# for setting runinfo measure_function to measure 1D data
def measure_point(expt):
    d = ps.ItemAttribute()

    d.x = random()

    return d


# for setting up prestring based on loaded to differentiate loaded experiment error strings
def loaded_modifier(loaded):
    if (loaded is True):
        return 'loaded '
    else:
        return ''


# for checking that the experiment has data measurement attribute
def check_has_single_data(expt, loaded=False):
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


# for setting up the experiments
def set_up_experiment(num_devices, measure_function, data_dir, verbose, n_average, bad):
    # set up core attributes
    devices = ps.ItemAttribute()
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_function

    # set up based on num devices
    if bad is False:
        if (num_devices < 0):
            assert False, "Num devices shouldn't be negative"
        if (num_devices == 0):
            runinfo.scan0 = ps.AverageScan(n_average, dt=0.01)
        elif (num_devices == 1):
            devices.v1 = ps.TestVoltage()
            runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
            runinfo.scan1 = ps.AverageScan(n_average, dt=0)
        elif (num_devices == 2):
            devices.v1 = ps.TestVoltage()
            devices.v2 = ps.TestVoltage()
            runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
            runinfo.scan1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')
            runinfo.scan2 = ps.AverageScan(n_average + 1, dt=0)
        elif (num_devices == 3):
            devices.v1 = ps.TestVoltage()
            devices.v2 = ps.TestVoltage()
            devices.v3 = ps.TestVoltage()
            runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
            runinfo.scan1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')
            runinfo.scan2 = ps.PropertyScan({'v3': ps.drange(0.3, 0.1, 0.2)}, 'voltage')
            runinfo.scan3 = ps.AverageScan(n_average + 2, dt=0.1)
        if (num_devices > 4):
            assert False, "num_devices > 4 not implemented in testing"
    # if bad runinfo it will have no average scan and thus should fail
    else:
        devices.v1 = ps.TestVoltage()
        runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')

    # instantiate expt based on additional parameters
    if data_dir is None:
        if verbose is False:
            expt = ps.Sweep(runinfo, devices)
        elif verbose is True:
            expt = ps.Sweep(runinfo, devices, verbose=verbose)
        else:
            assert False, "Invalid verbose entry. Must be boolean."
    elif isinstance(data_dir, str):
        if verbose is False:
            expt = ps.Sweep(runinfo, devices, data_dir)
        elif verbose is True:
            expt = ps.Sweep(runinfo, devices, data_dir, verbose)
        else:
            assert False, "Invalid verbose entry. Must be boolean."
    else:
        assert False, "Invalid data_dir entry. Must be a string"

    return expt


# for checking that the meta path is initialized properly
def check_meta_path(expt):
    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)
    assert meta_path.exists(), "meta_path not initialized"
    assert meta_path.is_file(), "meta_path is not a file"


# for checking that the voltage(s) as expected
def check_voltage_results(voltage, expected_value1, expected_value2, voltage_id=1, loaded=False, string_modifier=''):
    is_loaded = loaded_modifier(loaded)

    pre_string = is_loaded + "experiment v" + str(voltage_id) + string_modifier + "_voltage "
    assert (isinstance(voltage, np.ndarray) or isinstance(voltage, list)), pre_string + "is not a numpy array or a list"
    for i in voltage:
        try:
            assert i.dtype == 'float64'
        except (Exception):
            assert isinstance(i, float), pre_string + "data is not a float"
    assert len(voltage) == 2, pre_string + "array does not have 2 elements"
    assert voltage[0] == expected_value1, pre_string + "value[0] is not " + str(expected_value1)
    assert voltage[1] == expected_value2, pre_string + "value[1] is not " + str(expected_value2)


# for checking that the data results are as expected
def check_data_results(x, id='', dtype=np.ndarray, shape=[2], loaded=False, num_devices=0):
    is_loaded = loaded_modifier(loaded)
    pre_string = is_loaded + str(num_devices) + " devices experiment x" + str(id) + " measurement "

    if (dtype == float or shape == [1]):
        assert isinstance(x, dtype), pre_string + "is not a " + str(dtype)
    else:
        assert isinstance(x, dtype), pre_string + "is not a numpy array"
        assert x.dtype == 'float64', pre_string + "data is not a float"
        assert list(x.shape) == shape, pre_string + "array does not have " + str(shape) + " elements"

        if (shape == [2, 2] or shape == [2, 2, 2] or shape == [2, 2, 2, 2] or shape == [2, 2, 2, 2, 2]):
            for i in x:
                assert isinstance(i, np.ndarray), pre_string + "is not a numpy array of numpy arrays"


# for checking that the multi data results are as expected
def check_multi_data_results(expt, num_devices, shape1=[2], shape2=[2, 2], shape3=[2, 2, 2], shape4=[2, 2, 2, 2]):
    if num_devices == 0:
        check_data_results(expt.x1, id=1, dtype=float, shape=shape1)
        check_data_results(expt.x2, id=2, shape=shape1)
        for i in expt.x3:
            assert isinstance(i, np.ndarray), "experiment x3 measurement is not a numpy array of numpy arrays"
        check_data_results(expt.x3, id=3, shape=shape2)
    if num_devices == 1:
        check_data_results(expt.x1, id=1, shape=shape1, num_devices=1)
        check_data_results(expt.x2, id=2, shape=shape2, num_devices=1)
        for i in expt.x3:
            assert isinstance(i, np.ndarray), "experiment x3 measurement is not a numpy array of numpy arrays"
        check_data_results(expt.x3, id=3, shape=shape3, num_devices=1)
    if num_devices == 2:
        check_data_results(expt.x1, id=1, shape=shape2, num_devices=2)
        check_data_results(expt.x2, id=2, shape=shape3, num_devices=2)
        for i in expt.x3:
            assert isinstance(i, np.ndarray), "experiment x3 measurement is not a numpy array of numpy arrays"
        check_data_results(expt.x3, id=3, shape=shape4, num_devices=2)


##################### TEST CASES BEGIN HERE #####################

def test_averagesweep():
    """
    Testing AverageSweep

    Returns
    --------
    None
    """

    def test_variations(num_devices=0, measure_function=measure_point, data_dir=None, verbose=False, n_average=2,
                        bad=False):
        expt = set_up_experiment(num_devices, measure_function, data_dir, verbose, n_average, bad)

        # check the experiment core attributes are initialized correctly
        assert hasattr(expt, 'runinfo'), "expt does not have runinfo attribute"
        assert hasattr(expt, 'devices'), "expt does not have devices attribute"
        assert expt.runinfo.data_path.exists(), "experiment data path does not exist"
        assert expt.runinfo.data_path.is_dir(), "experiment data path is not a directory"
        if data_dir is None:
            assert str(expt.runinfo.data_path) == 'backup', "experiment data path does not equal 'backup'"
        else:
            assert str(expt.runinfo.data_path) == str(Path(data_dir)), "data path not setup to equal input data dir"

        # check the experiment runinfo
        expt.check_runinfo()

        # if no average scan was input, make sure runinfo_averaged is set correctly
        if bad is True:
            assert expt.runinfo.average_d == -1, "average_d not -1 even without average scan"

        # check the meta path was set successfully
        check_meta_path(expt)

        # run the experiment
        expt.run()

        # check that the experiment has the data measurement attribute(s)
        if measure_function == measure_point:
            check_has_single_data(expt)
        elif measure_function == measure_up_to_3D:
            check_has_multi_data(expt)

        # check voltage is as expected
        if num_devices >= 1:
            check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1)
        if num_devices >= 2:
            check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2)
        if num_devices >= 3:
            check_voltage_results(expt.v3_voltage, expected_value1=0.3, expected_value2=0.2, voltage_id=3)

        # ######### check that average scan is as expected ###### may add more test cases here?

        # check the data results are as expected
        if measure_function == measure_point:
            if num_devices == 1:
                check_data_results(expt.x)
            if num_devices == 2:
                check_data_results(expt.x, shape=[2, 2])
        elif measure_function == measure_up_to_3D:
            check_multi_data_results(expt, num_devices)

        # saves file name of the saved experiment data and deletes the experiment
        file_name = expt.runinfo.long_name
        del expt

        # basic check to load the experiment we just ran
        if data_dir is None:
            ps.load_experiment('./backup/{}'.format(file_name))
        else:
            ps.load_experiment('./' + str(Path(data_dir)) + '/{}'.format(file_name))

        # close and delete directories created from running this test
        if data_dir is None:
            shutil.rmtree('./backup')
        else:
            shutil.rmtree(data_dir)

    test_variations()
    test_variations(num_devices=1)
    test_variations(num_devices=2)
    test_variations(num_devices=3)
    test_variations(measure_function=measure_up_to_3D)
    test_variations(num_devices=1, measure_function=measure_up_to_3D)
    test_variations(num_devices=2, measure_function=measure_up_to_3D)
    test_variations(num_devices=3, measure_function=measure_up_to_3D)
    test_variations(data_dir='./bakeep')
    test_variations(verbose=True)
    test_variations(n_average=1)
    test_variations(n_average=10)
    test_variations(bad=True)

    with pytest.raises(Exception):
        test_variations(n_average=-1), "Averagesweep's n_average must be 1 or more"
    with pytest.raises(Exception):
        test_variations(n_average=0), "Averagesweep's n_average must be 1 or more"
