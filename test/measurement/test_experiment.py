'''
Pytest functions to test the Experiment experiment class and the load experiment function from loadexperiment.py
'''


import pyscan as ps
from random import random
import shutil
import numpy as np
import pytest


##################### FUNCTIONS USED BY TEST CASES #####################


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


# for setting up prestring based on loaded to differentiate loaded experiment error strings
def loaded_modifier(loaded):
    if (loaded is True):
        return 'loaded '
    else:
        return ''


# for setting up the experiments
def set_up_experiment(num_devices, measure_function, repeat=False, repeat_num=1):
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    if (repeat is True):
        runinfo.scan0 = ps.RepeatScan(repeat_num)
    else:
        runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')

        if (num_devices > 1):
            devices.v2 = ps.TestVoltage()
            runinfo.scan1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')

        if (num_devices > 2):
            devices.v3 = ps.TestVoltage()
            runinfo.scan2 = ps.PropertyScan({'v3': ps.drange(0.3, 0.1, 0.2)}, 'voltage')

        if (num_devices > 3):
            devices.v4 = ps.TestVoltage()
            runinfo.scan3 = ps.PropertyScan({'v4': ps.drange(-0.1, 0.1, 0)}, 'voltage')

        if (num_devices > 4):
            assert False, "num_devices > 4 not implemented in testing"

    runinfo.measure_function = measure_function

    expt = ps.Experiment(runinfo, devices)
    return expt


# for checking keys, runinfo, and devices attributes
def check_has_attributes(expt, intended_keys_length, additional=None, loaded=False):
    is_loaded = loaded_modifier(loaded)
    assert hasattr(expt, 'keys'), is_loaded + "experiment missing attribute 'keys'"
    ks = str(len(expt.keys()))
    iks = str(intended_keys_length)
    error_string = is_loaded + "experiment has " + ks + " keys instead of " + iks + " keys"
    assert len(expt.keys()) == intended_keys_length, error_string

    assert hasattr(expt, 'runinfo'), is_loaded + "experiment missing runinfo attribute"
    assert hasattr(expt.runinfo, 'time'), is_loaded + "experiment missing runinfo time attribute"
    assert hasattr(expt, 'devices'), is_loaded + "experiment missing devices attribute"

    if (additional is not None):
        assert hasattr(expt, additional), is_loaded + "experiment missing " + additional + " attribute"


# for checking the experiment (expt) upon initialization
def check_expt_init(expt):
    check_has_attributes(expt, intended_keys_length=2)

    assert expt.runinfo.data_path.exists(), "experiment data path does not exist"
    assert expt.runinfo.data_path.is_dir(), "experiment data path is not a directory"
    assert str(expt.runinfo.data_path) == 'backup', "experiment data path does not equal 'backup'"

    assert len(expt.runinfo.measured) == 0
    assert expt.runinfo.measured == []


# for checking whether the check experimental run info succeeded
def check_expt_runinfo(expt):
    assert expt.check_runinfo(), "check_runinfo() failed"

    assert hasattr(expt.runinfo, 'long_name'), "experiment runinfo long name not initialized by check_runinfo"
    assert hasattr(expt.runinfo, 'short_name'), "experiment runinfo long name not initialized by check_runinfo"


# for checking that the meta path is initialized properly
def check_meta_path(expt):
    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)
    assert meta_path.exists(), "meta_path not initialized"
    assert meta_path.is_file(), "meta_path is not a file"


# for checking that the experiment has data measurement attribute
def check_has_data(expt, loaded=False):
    is_loaded = loaded_modifier(loaded)
    assert hasattr(expt, 'x'), is_loaded + "experiment missing x attribute after running"


# for checking that the data results are as expected
def check_data_results(x, id=None, dtype=np.ndarray, shape=[2], loaded=False):
    is_loaded = loaded_modifier(loaded)
    pre_string = is_loaded + "experiment x" + str(id) + " measurement "

    if (dtype == float or shape == [1]):
        assert isinstance(x, dtype), pre_string + "is not a float"
    else:
        assert isinstance(x, dtype), pre_string + "is not a numpy array"
        assert x.dtype == 'float64', pre_string + "data is not a float"
        assert list(x.shape) == shape, pre_string + "array does not have " + str(shape) + " elements"

        if (shape == [2, 2] or shape == [2, 2, 2] or shape == [2, 2, 2, 2] or shape == [2, 2, 2, 2, 2]):
            for i in x:
                assert isinstance(i, np.ndarray), pre_string + "is not a numpy array of numpy arrays"


# for checking that the experiment has multidata measurement attributes
def check_has_multi_data(expt, loaded=False):
    is_loaded = loaded_modifier(loaded)
    pre_string = is_loaded + "experiment missing x"
    post_string = " attribute after running"
    assert hasattr(expt, 'x1'), pre_string + "1" + post_string
    assert hasattr(expt, 'x2'), pre_string + "2" + post_string
    assert hasattr(expt, 'x3'), pre_string + "3" + post_string


# for checking that the multi data results are as expected
def check_multi_data_results(expt, shape1=[2], shape2=[2], shape3=[2]):
    assert isinstance(expt.x1, float)
    check_data_results(expt.x2, id=2, shape=shape2)
    for i in expt.x3:
        assert isinstance(i, np.ndarray), "experiment x3 measurement is not a numpy array of numpy arrays"
    check_data_results(expt.x3, id=2, shape=shape3)


# for checking the experiment has voltages
def check_has_voltages(expt, num_voltages, loaded=False):
    is_loaded = loaded_modifier(loaded)

    assert hasattr(expt, 'v1_voltage'), is_loaded + "experiment missing v1_voltage attribute after running"
    if (num_voltages > 1):
        assert hasattr(expt, 'v2_voltage'), is_loaded + "experiment missing v2_voltage attribute after running"
    else:
        assert not hasattr(expt, 'v2_voltage'), is_loaded + "experiment missing v2_voltage attribute after running"
    if (num_voltages > 2):
        assert hasattr(expt, 'v3_voltage'), is_loaded + "experiment missing v3_voltage attribute after running"
    else:
        assert not hasattr(expt, 'v3_voltage'), is_loaded + "experiment missing v3_voltage attribute after running"
    if (num_voltages > 3):
        assert hasattr(expt, 'v4_voltage'), is_loaded + "experiment missing v4_voltage attribute after running"
    else:
        assert not hasattr(expt, 'v4_voltage'), is_loaded + "experiment missing v4_voltage attribute after running"
    if (num_voltages > 4):
        assert hasattr(expt, 'v5_voltage'), is_loaded + "experiment missing v5_voltage attribute after running"
    else:
        assert not hasattr(expt, 'v5_voltage'), is_loaded + "experiment missing v5_voltage attribute after running"


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


# for checking that the load experiment function is working as expected
def check_loaded_expt_further(expt):
    # for checking variable devices formatting
    def check_loaded_dev_attributes(dev, name, attributes):
        for a in attributes:
            assert hasattr(dev, a), "loaded experiment device " + name + " does not have " + a + " attribute"
        assert isinstance(dev, ps.ItemAttribute), "loaded device " + name + " is not an instance of item attribute"

    # confirm these are instances of item attribute
    assert isinstance(expt, ps.ItemAttribute), "loaded expt is not loaded as an instance of item attribute"
    assert isinstance(expt.runinfo, ps.ItemAttribute), "expt runinfo is not loaded as an instance of item attribute"
    assert isinstance(expt.devices, ps.ItemAttribute), "expt devices is not loaded as an instance of item attribute"
    assert isinstance(expt.runinfo.static, ps.ItemAttribute), "runinfo static is not loaded as an item attribute"

    # check that the devices are as expected
    v_attributes = ['debug', '_voltage']
    for device_name in expt.devices.__dict__.keys():
        device = expt.devices[device_name]
        check_loaded_dev_attributes(device, device, v_attributes)

        assert isinstance(device.debug, bool), "devices " + device_name + " debug is not loaded as a boolean"
        assert isinstance(device._voltage, float) or isinstance(
            device._voltage, int), device_name + " voltage type error"

    # check the runinfo scans
    assert hasattr(expt.runinfo, 'scan0'), "loaded expt does not have scan0"
    assert hasattr(expt.runinfo, 'scan1'), "loaded expt does not have scan1"
    assert hasattr(expt.runinfo, 'scan2'), "loaded expt does not have scan2"
    assert hasattr(expt.runinfo, 'scan3'), "loaded expt does not have scan3"

    for key in expt.runinfo.__dict__.keys():
        if key.startswith('scan'):
            scan = key
            assert isinstance(expt.runinfo[scan], ps.ItemAttribute), "loaded runinfo " + scan + " not item attribute"

    # check other attributes for proper type when loaded
    assert isinstance(expt.runinfo.measured, list), "runinfo measured is not loaded as a list"
    assert isinstance(expt.runinfo.measure_function, str), "runinfo measure function is not loaded as a string"
    assert expt.runinfo.trigger_function is None, "runinfo trigger function is not loaded as None"
    assert isinstance(expt.runinfo.initial_pause, float), "runinfo initial pause is not loaded as a float"
    assert isinstance(expt.runinfo.average_d, int), "runinfo average_d is not loaded as a float"
    assert isinstance(expt.runinfo.verbose, bool), "runinfo verbose is not loaded as a boolean"
    assert isinstance(expt.runinfo.time, bool), "runinfo time is not loaded as a boolean"
    assert isinstance(expt.runinfo.long_name, str), "runinfo long_name is not loaded as a string"
    assert isinstance(expt.runinfo.short_name, str), "runinfo short_name is not loaded as a string"
    # ### sometimes loaded expt doesn't have runinfo.running... why? Is this supposed to be allowed? ###
    if hasattr(expt.runinfo, 'running'):
        assert isinstance(expt.runinfo.running, bool), "runinfo running is not loaded as a boolean"
    # runinfo.complete does not seem to be saved... do we want it to be
        # to know if the expt crashed before it could finish?


####################### TEST CASES BEGIN HERE #######################


def test_0D_multi_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=1, measure_function=measure_up_to_3D, repeat=True, repeat_num=1)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=6, additional='repeat', loaded=loaded)

        # check the experiment has multidata measurement attributes
        check_has_multi_data(expt, loaded=loaded)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        assert len(expt.repeat) == 1, "experiment repeat length is not 1"
        assert expt.repeat == [0], "expt.repeat is not [0]"
        assert expt.repeat[0] == 0.0, "experiment repeat[0] is not 0.0"

        # check the data results are as expected
        check_data_results(expt.x1, id=1, dtype=float, shape=[1], loaded=loaded)

        check_data_results(expt.x2, id=2, shape=[2], loaded=loaded)

        check_data_results(expt.x3, id=3, shape=[2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # test that load experiment rejects other file types
    with pytest.raises(Exception):
        temp = ps.load_experiment('./test/measurement/test_scans.py')

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded data results are as expected
        assert len(temp.repeat) == 1, "experiment repeat length is not 1"
        assert temp.repeat == [0], "expt.repeat is not [0]"
        assert temp.repeat[0] == 0.0, "experiment repeat[0] is not 0.0"

        check_data_results(temp.x1, id=1, shape=[1], loaded=True)

        check_data_results(temp.x2, id=2, shape=[2], loaded=True)

        check_data_results(temp.x3, id=3, shape=[2, 2], loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_1D_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=1, measure_function=measure_point)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment has intended keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=4, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=1, loaded=loaded)

        # check the experiment has data measurement attribute
        check_has_data(expt)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x, loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_1D_multi_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=1, measure_function=measure_up_to_3D)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    # check the experiment run info was initialized successfully
    expt.check_runinfo()

    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment keys, runinfo, and devices attributes
        check_has_attributes(expt, 6, loaded=loaded)

        # check the experiment has multidata measurement attributes
        check_has_multi_data(expt, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=1, loaded=loaded)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x1, id=1, loaded=loaded)

        check_data_results(expt.x2, id=2, shape=[2, 2], loaded=loaded)

        check_data_results(expt.x3, id=3, shape=[2, 2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_2D_data():
    """
    Testing 2D scan, measurement and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=2, measure_function=measure_point)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment has intended keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=5, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=2, loaded=loaded)

        # check the experiment has data measurement attribute
        check_has_data(expt)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1, loaded=loaded)

        check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x, shape=[2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_2D_multi_data():
    """
    Testing 2D scan, measurement and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=2, measure_function=measure_up_to_3D)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=7, loaded=loaded)

        # check the experiment has multidata measurement attributes
        check_has_multi_data(expt, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=2, loaded=loaded)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1, loaded=loaded)

        check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x1, id=1, shape=[2, 2], loaded=loaded)

        check_data_results(expt.x2, id=2, shape=[2, 2, 2], loaded=loaded)

        check_data_results(expt.x3, id=3, shape=[2, 2, 2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_3D_data():
    """
    Testing 3D scan, measurement and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=3, measure_function=measure_point)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment has intended keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=6, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=3, loaded=loaded)

        # check the experiment has data measurement attribute
        check_has_data(expt)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1, loaded=loaded)

        check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2, loaded=loaded)

        check_voltage_results(expt.v3_voltage, expected_value1=0.3, expected_value2=0.2, voltage_id=3, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x, shape=[2, 2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_3D_multi_data():
    """
    Testing 3D scan, measurement and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=3, measure_function=measure_up_to_3D)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=8, loaded=loaded)

        # check the experiment has multidata measurement attributes
        check_has_multi_data(expt, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=3, loaded=loaded)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1, loaded=loaded)

        check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2, loaded=loaded)

        check_voltage_results(expt.v3_voltage, expected_value1=0.3, expected_value2=0.2, voltage_id=3, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x1, id=1, shape=[2, 2, 2], loaded=loaded)

        check_data_results(expt.x2, id=2, shape=[2, 2, 2, 2], loaded=loaded)

        check_data_results(expt.x3, id=3, shape=[2, 2, 2, 2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_4D_data():
    """
    Testing 4D scan, measurement and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=4, measure_function=measure_point)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment has intended keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=7, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=4, loaded=loaded)

        # check the experiment has data measurement attribute
        check_has_data(expt)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1, loaded=loaded)

        check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2, loaded=loaded)

        check_voltage_results(expt.v3_voltage, expected_value1=0.3, expected_value2=0.2, voltage_id=3, loaded=loaded)

        check_voltage_results(expt.v4_voltage, expected_value1=-0.1, expected_value2=0, voltage_id=4, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x, shape=[2, 2, 2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_4D_multi_data():
    """
    Testing 4D scan, measurement and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=4, measure_function=measure_up_to_3D)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=9, loaded=loaded)

        # check the experiment has multidata measurement attributes
        check_has_multi_data(expt, loaded=loaded)

        # check the experiment has the right number of voltages
        check_has_voltages(expt, num_voltages=4, loaded=loaded)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1, loaded=loaded)

        check_voltage_results(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2, loaded=loaded)

        check_voltage_results(expt.v3_voltage, expected_value1=0.3, expected_value2=0.2, voltage_id=3, loaded=loaded)

        check_voltage_results(expt.v4_voltage, expected_value1=-0.1, expected_value2=0, voltage_id=4, loaded=loaded)

        # check the data results are as expected
        check_data_results(expt.x1, id=1, shape=[2, 2, 2, 2], loaded=loaded)

        check_data_results(expt.x2, id=2, shape=[2, 2, 2, 2, 2], loaded=loaded)

        check_data_results(expt.x3, id=3, shape=[2, 2, 2, 2, 2, 2], loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_1D_repeat():
    """
    Testing 1D repeat scan, measurement and loaded file

    Returns
    --------
    None
    """

    # set up experiment
    expt = set_up_experiment(num_devices=1, measure_function=measure_point, repeat=True, repeat_num=2)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    def check_expt_attributes(expt, loaded=False):
        # check the experiment keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=4, additional='repeat', loaded=loaded)

        # check the experiment has multidata measurement attributes
        check_has_data(expt, loaded=loaded)

    check_expt_attributes(expt)

    def check_expt_results(expt, loaded=False):
        assert len(expt.repeat) == 2, "experiment repeat length is not 2"
        assert expt.repeat[0] == 0.0, "experiment repeat[0] is not 0.0"
        assert expt.repeat[1] == 1.0, "experiment repeat[1] is not 1.0"

        # check the data results are as expected
        check_data_results(expt.x, loaded=loaded)

    check_expt_results(expt)

    # saves file name of the saved experiment data and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)
        assert temp.repeat.dtype == 'float64'

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')


def test_underscore_property():
    """
    Testing property scan, measurement and loaded file

    Returns
    --------
    None
    """
    # set up experiment
    devices = ps.ItemAttribute()
    devices.v1_device = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.scan0 = ps.PropertyScan({'v1_device': ps.drange(0, 0.1, 0.1)}, prop='voltage')

    runinfo.measure_function = measure_point

    expt = ps.Experiment(runinfo, devices)

    # check the experiment was initialized correctly
    check_expt_init(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    check_expt_runinfo(expt)

    # check the meta path was set successfully
    check_meta_path(expt)

    # run the experiment
    expt.run()

    # for checking the experiments attributes and output after running
    def check_expt_attributes(expt, loaded=False):
        # check the experiment has intended keys, runinfo, and devices attributes
        check_has_attributes(expt, intended_keys_length=4, loaded=loaded)

        # check the experiment has the right voltage attribute
        assert hasattr(expt, 'v1_device_voltage')

        # check the experiment has data measurement attribute
        check_has_data(expt)

    check_expt_attributes(expt)

    # for checking the experiments results formatting after running
    def check_expt_results(expt, loaded=False):
        # check voltage(s) are as expected
        check_voltage_results(expt.v1_device_voltage, expected_value1=0, expected_value2=0.1,
                              loaded=loaded, string_modifier='_device')

        # check the data results are as expected
        check_data_results(expt.x, loaded=loaded)

    check_expt_results(expt)

    file_name = expt.runinfo.long_name
    del expt

    # load the experiment we just ran
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # check that we load what we expect
    def check_load_expt(temp):
        # check the loaded experiment has the right attributes
        check_expt_attributes(temp, loaded=True)

        # check the loaded experiment results are accurate
        check_expt_results(temp, loaded=True)

        check_loaded_expt_further(temp)

    check_load_expt(temp)

    shutil.rmtree('./backup')
