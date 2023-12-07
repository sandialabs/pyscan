'''
Pytest functions to test the pointbypoint experiment class
'''
import pyscan as ps
from random import random
import sys
import shutil

sys.path.append('../../../pyscan')


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


# for checking the experiment (expt) upon initialization
def checkOne(expt):
    assert hasattr(expt, 'keys'), "experiment missing attribute 'keys'"
    assert len(expt.keys()) == 2, "wrong number of experiment keys"

    assert hasattr(expt, 'runinfo'), "experiment missing runinfo attribute"
    assert hasattr(expt, 'devices'), "experiment missing devices attribute"

    assert expt.runinfo.data_path.exists(), "experiment data path does not exist"
    assert expt.runinfo.data_path.is_dir(), "experiment data path is not a directory"
    assert str(expt.runinfo.data_path) == 'backup', "experiment data path does not equal 'backup'"
    
    assert len(expt.runinfo.measured) == 0


# for checking whether the check experimental run info succeeded
def checkTwo(expt):
    assert expt.check_runinfo(), "check_runinfo failed"
    
    assert hasattr(expt.runinfo, 'long_name'), "experiment runinfo long name not initialized by check_runinfo"
    assert hasattr(expt.runinfo, 'short_name'), "experiment runinfo long name not initialized by check_runinfo"


def checkThree(meta_path):
    assert meta_path.is_file()


def test_0D_multi_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.RepeatScan(1)

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    checkOne(expt)
        
    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 6
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'repeat')
        assert hasattr(expt, 'x1')
        assert hasattr(expt, 'x2')
        assert hasattr(expt, 'x3')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.repeat) == 1
        assert issubclass(type(expt.x1), float)

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))
    
    def checkSix(temp):
        assert len(temp.keys()) == 6
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'repeat')
        assert hasattr(temp, 'x1')
        assert hasattr(temp, 'x2')
        assert hasattr(temp, 'x3')
        assert temp.x1.dtype == 'float64'

    checkSix(temp)

    shutil.rmtree('./backup')


def test_1D_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """
    
    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    checkOne(expt)
    
    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 4
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
    
    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.x) == 2
    
    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
        assert len(temp.keys()) == 4
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'

    checkSix(temp)

    shutil.rmtree('./backup')


def test_1D_multi_data():
    """
    Testing 1D scan, measuring 1D, 2D, and 3D data and loaded file

    Returns
    --------
    None
    """

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    global current_test_title
    current_test_title = "test_1D_multi_data"
    global current_tests_failed
    current_tests_failed = 0

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 6
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'x1')
        assert hasattr(expt, 'x2')
        assert hasattr(expt, 'x3')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        len(expt.x1) == 2
        list(expt.x2.shape) == [2, 2]
        list(expt.x3.shape) == [2, 2, 2]

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
        assert len(temp.keys()) == 6
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'x1')
        assert hasattr(temp, 'x2')
        assert hasattr(temp, 'x3')
        assert temp.x1.dtype == 'float64'
        assert temp.x2.dtype == 'float64'
        assert temp.x3.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'

    checkSix(temp)

    shutil.rmtree('./backup')


def test_2D_data():
    """
    Testing 2D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')

    runinfo.measure_function = measure_point

    expt = ps.Sweep(runinfo, devices)

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 5
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'x')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        assert list(expt.x.shape), [2, 2]

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
        assert len(temp.keys()) == 5
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_voltage')
        assert hasattr(temp, 'v2_voltage')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.v1_voltage.dtype == 'float64'
        assert temp.v2_voltage.dtype == 'float64'

    checkSix(temp)

    shutil.rmtree('./backup')


def test_2D_multi_data():
    """
    Testing 2D scan, measurement and loaded file

    Returns
    --------
    None
    """ 

    devices = ps.ItemAttribute()        
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()

    runinfo = ps.RunInfo()

    runinfo.loop0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage')
    runinfo.loop1 = ps.PropertyScan({'v2': ps.drange(0.1, 0.1, 0)}, 'voltage')

    runinfo.measure_function = measure_up_to_3D

    expt = ps.Sweep(runinfo, devices)

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 7
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'x1')
        assert hasattr(expt, 'x2')
        assert hasattr(expt, 'x3')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        list(expt.x1.shape) == [2, 2]
        list(expt.x2.shape) == [2, 2]
        list(expt.x3.shape) == [2, 2, 2]

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
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

    checkSix(temp)

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

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 6
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'v3_voltage')
        assert hasattr(expt, 'x')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x.shape) == [2, 2, 2]

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
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

    checkSix(temp)

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

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 8
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'v3_voltage')
        assert hasattr(expt, 'x1')
        assert hasattr(expt, 'x2')
        assert hasattr(expt, 'x3')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x1.shape) == [2, 2, 2]
        list(expt.x2.shape) == [2, 2, 2, 2]
        list(expt.x3.shape) == [2, 2, 2, 2, 2]

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
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

    checkSix(temp)

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

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 7
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_voltage')
        assert hasattr(expt, 'v2_voltage')
        assert hasattr(expt, 'v3_voltage')
        assert hasattr(expt, 'v4_voltage')
        assert hasattr(expt, 'x')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x.shape) == [2, 2, 2, 2]

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
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

    checkSix(temp)

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

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
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

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_voltage) == 2
        assert len(expt.v2_voltage) == 2
        assert len(expt.v3_voltage) == 2
        assert len(expt.v3_voltage) == 2
        list(expt.x1.shape) == [2, 2, 2, 2]
        list(expt.x2.shape) == [2, 2, 2, 2, 2]
        list(expt.x3.shape) == [2, 2, 2, 2, 2, 2]

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))

    def checkSix(temp):
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

    checkSix(temp)

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

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 4
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'repeat')
        assert hasattr(expt, 'x')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.repeat) == 2
        assert len(expt.x) == 2

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))
    
    def checkSix(temp):
        assert len(temp.keys()) == 4
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'repeat')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.repeat.dtype == 'float64'
        assert len(temp.x) == 2
        assert len(temp.repeat) == 2

    checkSix(temp)

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

    checkOne(expt)

    expt.check_runinfo()

    checkTwo(expt)

    expt.save_metadata()
    meta_path = expt.runinfo.data_path / '{}.hdf5'.format(expt.runinfo.long_name)

    checkThree(meta_path)

    expt.run()

    def checkFour(expt):
        assert len(expt.keys()) == 4
        assert hasattr(expt, 'runinfo')
        assert hasattr(expt, 'devices')
        assert hasattr(expt, 'v1_device_other_voltage')
        assert hasattr(expt, 'x')

    checkFour(expt)

    def checkFive(expt):
        assert len(expt.v1_device_other_voltage) == 2
        assert len(expt.x) == 2

    checkFive(expt)

    file_name = expt.runinfo.long_name
    del expt

    # Test that we load what we expect
    temp = ps.load_experiment('./backup/{}'.format(file_name))
    
    def checkSix(temp):
        assert len(temp.keys()) == 4
        assert hasattr(temp, 'runinfo')
        assert hasattr(temp, 'devices')
        assert hasattr(temp, 'v1_device_other_voltage')
        assert hasattr(temp, 'x')
        assert temp.x.dtype == 'float64'
        assert temp.v1_device_other_voltage.dtype == 'float64'
        assert len(temp.x) == 2
        assert len(temp.v1_device_other_voltage) == 2

    checkSix(temp)

    shutil.rmtree('./backup')
