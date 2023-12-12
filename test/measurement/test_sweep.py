'''
Pytest functions to test the pointbypoint experiment class
'''
import pyscan as ps
from random import random
import shutil
import numpy as np


# for setting runinfo measure_function to measure 1D data
def measure_point(expt):
    d = ps.ItemAttribute()

    d.x = random()

    return d


# for setting runinfo measure_function to measure (up to) 3D data
def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = random()
    d.x2 = [random() for i in range(2)]
    d.x3 = [[random() for i in range(2)] for j in range(2)]

    return d


# for setting up prestring based on loaded to differentiate loaded experiment error strings
def isLoaded(loaded):
    if (loaded is True):
        return 'loaded '
    else:
        return ''


# for checking keys, runinfo, and devices attributes
def checkHasAttributes(expt, intended_keys_length, loaded=False):
    is_loaded = isLoaded(loaded)
    assert hasattr(expt, 'keys'), is_loaded + "experiment missing attribute 'keys'"
    ks = str(len(expt.keys()))
    iks = str(intended_keys_length)
    error_string = is_loaded + "experiment has " + ks + " keys instead of " + iks + " keys"
    assert len(expt.keys()) == intended_keys_length, error_string

    assert hasattr(expt, 'runinfo'), is_loaded + "experiment missing runinfo attribute"
    assert hasattr(expt, 'devices'), is_loaded + "experiment missing devices attribute"


# for checking the experiment (expt) upon initialization
def checkExptInit(expt):
    checkHasAttributes(expt, intended_keys_length=2)

    assert expt.runinfo.data_path.exists(), "experiment data path does not exist"
    assert expt.runinfo.data_path.is_dir(), "experiment data path is not a directory"
    assert str(expt.runinfo.data_path) == 'backup', "experiment data path does not equal 'backup'"
    
    assert len(expt.runinfo.measured) == 0


# for checking whether the check experimental run info succeeded
def checkExptRunInfo(expt):
    assert expt.check_runinfo(), "check_runinfo failed"
    
    assert hasattr(expt.runinfo, 'long_name'), "experiment runinfo long name not initialized by check_runinfo"
    assert hasattr(expt.runinfo, 'short_name'), "experiment runinfo long name not initialized by check_runinfo"


# for checking that the meta path is initialized properly
def checkMetaPath(meta_path):
    assert meta_path.exists(), "meta_path not initialized"
    assert meta_path.is_file(), "meta_path is not a file"


# for checking that the experiment has data measurement attribute
def checkHasData(expt):
    assert hasattr(expt, 'x'), "experiment missing x attribute after running"


# for checking that the data results are as expected
def checkDataResults(x, id=None, dtype=np.ndarray, shape=[2], loaded=False):
    is_loaded = isLoaded(loaded)
    pre_string = is_loaded + "experiment x" + str(id) + " measurement "

    if (dtype == float or shape == [1]):
        assert type(x) is dtype, pre_string + "is not a float"
    else:
        assert type(x) is dtype, pre_string + "is not a numpy array"
        assert x.dtype == 'float64', pre_string + "data is not a float"
        assert list(x.shape) == shape, pre_string + "array does not have 2 elements"
        
        if (shape == [2, 2] or shape == [2, 2, 2] or shape == [2, 2, 2, 2] or shape == [2, 2, 2, 2, 2]):
            for i in x:
                assert type(i) is np.ndarray, pre_string + "is not a numpy array of numpy arrays"


# for checking that the experiment has multidata measurement attributes
def checkHasMultiData(expt, loaded=False):
    is_loaded = isLoaded(loaded)
    pre_string = is_loaded + "experiment missing x"
    post_string = " attribute after running"
    assert hasattr(expt, 'x1'), pre_string + "1" + post_string
    assert hasattr(expt, 'x2'), pre_string + "2" + post_string
    assert hasattr(expt, 'x3'), pre_string + "3" + post_string


# for checking that the multi data results are as expected
def checkMultiDataResults(expt, shape1=[2], shape2=[2], shape3=[2]):
    assert type(expt.x1) is float
    checkDataResults(expt.x2, shape2)
    for i in expt.x3:
        assert type(i) is np.ndarray, "experiment x3 measurement is not a numpy array of numpy arrays"
    checkDataResults(expt.x3, shape3)


# for checking the experiment has voltages
def checkHasVoltages(expt, num_voltages, loaded=False):
    is_loaded = isLoaded(loaded)

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
def checkVoltageResults(voltage, expected_value1, expected_value2, voltage_id=1, loaded=False):
    is_loaded = isLoaded(loaded)
    
    pre_string = is_loaded + "experiment v" + str(voltage_id) + "_voltage "
    assert type(voltage) is np.ndarray, pre_string + "is not a numpy array"
    assert voltage.dtype == 'float64', pre_string + "data is not a float"
    assert len(voltage) == 2, pre_string + "array does not have 2 elements"
    assert voltage[0] == expected_value1, pre_string + "value[0] is not " + str(expected_value1)
    assert voltage[1] == expected_value2, pre_string + "value[1] is not " + str(expected_value2)


def test_0D_multi_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """

    # setting up experiment
    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.RepeatScan(1)

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    # check the experiment was initialized correctly
    checkExptInit(expt)
        
    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    # check the meta path was set successfully
    checkMetaPath(meta_path)

    expt.run()

    # for checking the experiments output after running
    def checkExptOutput(expt):
        # check the experiment keys, runinfo, and devices attributes
        checkHasAttributes(expt, intended_keys_length=6)

        # check the experiment has multidata measurement attributes
        checkHasMultiData(expt)

        assert hasattr(expt, 'repeat'), "experiment missing devices attribute after running"

    checkExptOutput(expt)

    # for checking the experiments results formatting after running
    def checkExptResults(expt):
        assert len(expt.repeat) == 1, "experiment repeat length is not 1"
        assert expt.repeat == [0], "experiment repeat value is not 0"

        # check the data results are as expected
        checkDataResults(expt.x1, id=1, dtype=float, shape=[1])

        checkDataResults(expt.x2, id=2, shape=[2])

        checkDataResults(expt.x3, id=3, shape=[2, 2])

    checkExptResults(expt)

    # saves file name and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # loads the experiment
    temp = ps.load_experiment('./backup/{}'.format(file_name))
    
    # for checking the experiment is loaded as expected
    def checkLoadExpt(temp):
        # check the loaded experiment keys, runinfo, and devices attributes
        checkHasAttributes(temp, 6, loaded=True)

        # check the loaded experiment has multidata measurement attributes
        checkHasMultiData(temp, loaded=True)

        # check the loaded data results are as expected
        checkDataResults(temp.x1, id=1, shape=[1], loaded=True)

        checkDataResults(temp.x2, id=2, shape=[2], loaded=True)

        checkDataResults(temp.x3, id=3, shape=[2, 2], loaded=True)

        assert hasattr(temp, 'repeat'), "loaded experiment missing repeat attribute"

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_1D_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """
    
    # setting up experiment
    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    # check the experiment was initialized correctly
    checkExptInit(expt)
    
    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    # check the meta path was set successfully
    checkMetaPath(meta_path)

    expt.run()

    # for checking the experiments output after running
    def checkExptOutput(expt):
        # check the experiment has intended keys, runinfo, and devices attributes
        checkHasAttributes(expt, intended_keys_length=4)

        # check the experiment has the right number of voltages
        checkHasVoltages(expt, num_voltages=1)
        
        # check the experiment has data measurement attribute
        checkHasData(expt)
    
    checkExptOutput(expt)

    # for checking the experiments results formatting after running
    def checkExptResults(expt):
        # check voltage(s) are as expected
        checkVoltageResults(expt.v1_voltage, expected_value1=0, expected_value2=0.1)

        # check the data results are as expected
        checkDataResults(expt.x)
    
    checkExptResults(expt)

    # saves file name and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # loads the experiment
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # for checking the experiment is loaded as expected
    def checkLoadExpt(temp):
        # check the loaded experiment has keys, runinfo, and devices attributes
        checkHasAttributes(temp, intended_keys_length=4, loaded=True)

        # check the eloaded xperiment has the right number of voltages
        checkHasVoltages(temp, num_voltages=1)

        # check the loaded experiment has data measurement attribute
        checkHasData(temp)

        # check the loaded voltage(s) are as expected
        checkVoltageResults(temp.v1_voltage, expected_value1=0, expected_value2=0.1, loaded=True)

        # check the loaded data results are as expected
        checkDataResults(temp.x, loaded=True)

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_1D_multi_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """

    # setting up experiment
    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    # check the experiment was initialized correctly
    checkExptInit(expt)

    # check the experiment run info was initialized successfully
    expt.check_runinfo()

    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    # check the meta path was set successfully
    checkMetaPath(meta_path)

    expt.run()

    # for checking the experiments output after running
    def checkExptOutput(expt):
        # check the experiment keys, runinfo, and devices attributes
        checkHasAttributes(expt, 6)

        # check the experiment has multidata measurement attributes
        checkHasMultiData(expt)

        # check the experiment has the right number of voltages
        checkHasVoltages(expt, num_voltages=1)

    checkExptOutput(expt)

    # for checking the experiments results formatting after running
    def checkExptResults(expt):
        # check voltage(s) are as expected
        checkVoltageResults(expt.v1_voltage, expected_value1=0, expected_value2=0.1)

        # check the data results are as expected
        checkDataResults(expt.x1, id=1)

        checkDataResults(expt.x2, id=2, shape=[2, 2])

        checkDataResults(expt.x3, id=3, shape=[2, 2, 2])

    checkExptResults(expt)

    # saves file name and deletes the experiment
    file_name = expt.runinfo.long_name
    del expt

    # loads the experiment
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    # for checking the experiment is loaded as expected
    def checkLoadExpt(temp):
        # check the loaded experiment keys, runinfo, and devices attributes
        checkHasAttributes(temp, 6, loaded=True)

        # check the loaded experiment has the right number of voltages
        checkHasVoltages(temp, 1, loaded=True)

        # check the loaded experiment has multidata measurement attributes
        checkHasMultiData(temp)

        # check the data results are as expected
        checkDataResults(temp.x1, id=1, loaded=True)

        checkDataResults(temp.x2, id=2, shape=[2, 2], loaded=True)

        checkDataResults(temp.x3, id=3, shape=[2, 2, 2], loaded=True)

        # check voltage(s) are as expected
        checkVoltageResults(temp.v1_voltage, expected_value1=0, expected_value2=0.1, loaded=True)

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_2D_data():
    """
    Testing 2D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    # setting up experiment
    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    # check the experiment was initialized correctly
    checkExptInit(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    # check the meta path was set successfully
    checkMetaPath(meta_path)

    expt.run()

    # for checking the experiments output after running
    def checkExptOutput(expt):
        # check the experiment has intended keys, runinfo, and devices attributes
        checkHasAttributes(expt, intended_keys_length=5)

        # check the experiment has the right number of voltages
        checkHasVoltages(expt, num_voltages=2)

        # check the experiment has data measurement attribute
        checkHasData(expt)

    checkExptOutput(expt)

    # for checking the experiments results formatting after running
    def checkExptResults(expt):
        # check voltage(s) are as expected
        checkVoltageResults(expt.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1)

        checkVoltageResults(expt.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2)

        # check the data results are as expected
        checkDataResults(expt.x, shape=[2, 2])

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkLoadExpt(temp):
        # check the loaded experiment has keys, runinfo, and devices attributes
        checkHasAttributes(temp, intended_keys_length=5, loaded=True)

        # check the eloaded xperiment has the right number of voltages
        checkHasVoltages(temp, num_voltages=2)

        # check the loaded experiment has data measurement attribute
        checkHasData(temp)

        # check the loaded voltage(s) are as expected
        checkVoltageResults(temp.v1_voltage, expected_value1=0, expected_value2=0.1, voltage_id=1, loaded=True)

        checkVoltageResults(temp.v2_voltage, expected_value1=0.1, expected_value2=0, voltage_id=2, loaded=True)

        # check the loaded data results are as expected
        checkDataResults(temp.x, shape=[1], loaded=True)

        assert temp.x.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'
        assert temp.v2_voltage.dtype == 'float64'

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_2D_multi_data():
    """
    Testing 2D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    # setting up experiment
    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    # check the experiment was initialized correctly
    checkExptInit(expt)

    expt.check_runinfo()

    # check the experiment run info was initialized successfully
    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    # check the meta path was set successfully
    checkMetaPath(meta_path)

    expt.run()

    # for checking the experiments output after running
    def checkExptOutput(expt):
        assert len(expt.keys()) == 7
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'x1')
        assert hasattr(expt, 'x2')
        assert hasattr(expt, 'x3')

    checkExptOutput(expt)

    def checkExptResults(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        list(expt.x1.shape) == [2, 2]
        list(expt.x2.shape) == [2, 2]
        list(expt.x3.shape) == [2, 2, 2]

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkLoadExpt(temp):
        assert len(temp.keys()) == 7
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'v2_voltage')
        assert hasattr(temp, 'x1')
        assert hasattr(temp, 'x2')
        assert hasattr(temp, 'x3')
        assert temp.x1.dtype == 'float64'
        assert temp.x2.dtype == 'float64'
        assert temp.x3.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'
        assert temp.v2_voltage.dtype == 'float64'

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_3D_data():
    """
    Testing 3D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    devices.v3 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')
    runinfo.loop2 = ps.PropertyScan({'v3': ps.drange(0.3, 0.1, 0.2)}, 'voltage')

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    checkExptInit(expt)

    expt.check_runinfo()

    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkMetaPath(meta_path)

    expt.run()

    def checkExptOutput(expt):
        assert len(expt.keys()) == 6
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'v3_voltage')
        assert hasattr(expt, 'x')

    checkExptOutput(expt)

    def checkExptResults(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x.shape) == [2, 2, 2]

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkLoadExpt(temp):
        assert len(temp.keys()) == 6
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'v2_voltage')
        assert hasattr(temp, 'v3_voltage')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'
        assert temp.v2_voltage.dtype == 'float64'
        assert temp.v3_voltage.dtype == 'float64'

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_3D_multi_data():
    """
    Testing 3D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    devices.v3 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')
    runinfo.loop2 = ps.PropertyScan({'v3': ps.drange(0.3, 0.1, 0.2)}, 'voltage')

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    checkExptInit(expt)

    expt.check_runinfo()

    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkMetaPath(meta_path)

    expt.run()

    def checkExptOutput(expt):
        assert len(expt.keys()) == 8
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'v3_voltage')
        assert hasattr(expt, 'x1')
        assert hasattr(expt, 'x2')
        assert hasattr(expt, 'x3')

    checkExptOutput(expt)

    def checkExptResults(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x1.shape) == [2, 2, 2]
        list(expt.x2.shape) == [2, 2, 2, 2]
        list(expt.x3.shape) == [2, 2, 2, 2, 2]

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkLoadExpt(temp):
        assert len(temp.keys()) == 8
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'v2_voltage')
        assert hasattr(temp, 'v3_voltage')
        assert hasattr(temp, 'x1')
        assert hasattr(temp, 'x2')
        assert hasattr(temp, 'x3')
        assert temp.x1.dtype == 'float64'
        assert temp.x2.dtype == 'float64'
        assert temp.x3.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'
        assert temp.v2_voltage.dtype == 'float64'
        assert temp.v3_voltage.dtype == 'float64'

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_4D_data():
    """
    Testing 4D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    devices.v3 = ps.TestVoltage()
    devices.v4 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')
    runinfo.loop2 = ps.PropertyScan({'v3': ps.drange(0.3, 0.1, 0.2)}, 'voltage')
    runinfo.loop3 = ps.PropertyScan({'v4': ps.drange(-0.1, 0.1, 0)}, 'voltage')

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    checkExptInit(expt)

    expt.check_runinfo()

    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkMetaPath(meta_path)

    expt.run()

    def checkExptOutput(expt):
        assert len(expt.keys()) == 7
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'v3_voltage')
        assert hasattr(expt, 'v4_voltage')
        assert hasattr(expt, 'x')

    checkExptOutput(expt)

    def checkExptResults(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x.shape) == [2, 2, 2, 2]

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkLoadExpt(temp):
        assert len(temp.keys()) == 7
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'v2_voltage')
        assert hasattr(temp, 'v3_voltage')
        assert hasattr(temp, 'v4_voltage')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'
        assert temp.v2_voltage.dtype == 'float64'
        assert temp.v3_voltage.dtype == 'float64'
        assert temp.v4_voltage.dtype == 'float64'

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_4D_multi_data():
    """
    Testing 4D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    devices.v3 = ps.TestVoltage()
    devices.v4 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')
    runinfo.loop2 = ps.PropertyScan({'v3': ps.drange(0.3, 0.1, 0.2)}, 'voltage')
    runinfo.loop3 = ps.PropertyScan({'v4': ps.drange(-0.1, 0.1, 0)}, 'voltage')

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    checkExptInit(expt)

    expt.check_runinfo()

    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkMetaPath(meta_path)

    expt.run()

    def checkExptOutput(expt):
        assert len(expt.keys()) == 9
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'v3_voltage')
        assert hasattr(expt, 'v4_voltage')
        assert hasattr(expt, 'x1')
        assert hasattr(expt, 'x2')
        assert hasattr(expt, 'x3')

    checkExptOutput(expt)

    def checkExptResults(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x1.shape) == [2, 2, 2, 2]
        list(expt.x2.shape) == [2, 2, 2, 2, 2]
        list(expt.x3.shape) == [2, 2, 2, 2, 2, 2]

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkLoadExpt(temp):
        assert len(temp.keys()) == 9
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'v2_voltage')
        assert hasattr(temp, 'v3_voltage')
        assert hasattr(temp, 'v4_voltage')
        assert hasattr(temp, 'x1')
        assert hasattr(temp, 'x2')
        assert hasattr(temp, 'x3')
        assert temp.x1.dtype == 'float64'
        assert temp.x2.dtype == 'float64'
        assert temp.x3.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'
        assert temp.v2_voltage.dtype == 'float64'
        assert temp.v3_voltage.dtype == 'float64'
        assert temp.v4_voltage.dtype == 'float64'

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_1D_repeat():
    """
    Testing 1D repeat scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.RepeatScan(2)

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    checkExptInit(expt)

    expt.check_runinfo()

    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkMetaPath(meta_path)

    expt.run()

    def checkExptOutput(expt):
        assert len(expt.keys()) == 4
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'repeat')
        assert hasattr(expt, 'x')

    checkExptOutput(expt)

    def checkExptResults(expt):
        assert len(expt.repeat) == 2
        assert len(expt.x) == 2

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))
    
    def checkLoadExpt(temp):
        assert len(temp.keys()) == 4
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'repeat')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.repeat.dtype == 'float64'
        assert len(temp.x) == 2
        assert len(temp.repeat) == 2

    checkLoadExpt(temp)

    shutil.rmtree('./backup')


def test_underscore_property():
    """
    Testing property scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()
    devices.v1_device = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1_device': ps.drange(0, 0.1, 0.1)}, prop='other_voltage')

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    checkExptInit(expt)

    expt.check_runinfo()

    checkExptRunInfo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkMetaPath(meta_path)

    expt.run()

    def checkExptOutput(expt):
        assert len(expt.keys()) == 4
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_device_other_voltage')
        assert hasattr(expt, 'x')

    checkExptOutput(expt)

    def checkExptResults(expt):
        assert len(expt.v1_device_other_voltage) == 2
        assert len(expt.x) == 2

    checkExptResults(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))
    
    def checkLoadExpt(temp):
        assert len(temp.keys()) == 4
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_device_other_voltage')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.v1_device_other_voltage.dtype == 'float64'
        assert len(temp.x) == 2
        assert len(temp.v1_device_other_voltage) == 2

    checkLoadExpt(temp)

    shutil.rmtree('./backup')
