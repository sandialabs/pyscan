import pyscan as ps
import numpy as np
import pytest
from pathlib import PosixPath
from typing import Callable


@pytest.fixture(scope='session')
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage', dt=0)
    runinfo.scan1 = ps.PropertyScan({'v2': ps.drange(0, 0.1, 0.2)}, 'voltage', dt=0)
    runinfo.scan2 = ps.PropertyScan({'v3': ps.drange(0, 0.1, 0.3)}, 'voltage', dt=0)
    return runinfo

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


def test_experiment_post_measure_3D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, value, t, shape in [
        ('v1_voltage', np.array([0, 0.1]), np.ndarray, (2,)),
        ('v2_voltage', np.array([0, 0.1, 0.2]), np.ndarray, (3,)),
        ('v3_voltage', np.array([0, 0.1, 0.2, 0.3]), np.ndarray, (4,)),
        ('x1', np.array((list(np.zeros((3, 4))), list(np.ones((3, 4))))), np.ndarray, (2, 3, 4)),
        ('x2', np.array((list(np.zeros((3, 4, 2))), list(np.ones((3, 4, 2))))), np.ndarray, (2, 3, 4, 2)),
        ('x3', np.array((list(np.zeros((3, 4, 2, 2))), list(np.ones((3, 4, 2, 2))))), np.ndarray, (2, 3, 4, 2, 2))]:

        assert hasattr(expt, key), 'Experiment does not have key {}'.format(key)
        assert isinstance(expt[key], t), 'Value of {} is not {}'.format(key, t)
        assert np.allclose(expt[key], value), 'Value of {} is not {}'.format(key, value)
        assert expt[key].shape == shape, 'Shape of {} is not {}'.format(key, shape)


def test_runinfo_contents_post_measure_3D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, value in [
        ('measured', ['x1', 'x2', 'x3']),
        ('initial_pause', 0.1),
        ('continuous', False),
        ('time', False),
        ('has_average_scan', False),
        ('running', False),
        ('_dims', (2, 3, 4)),
        ('_ndim', 3),
        ('_indicies', [1, 2, 3]),
        ('complete', True)]:
        assert expt.runinfo[key] == value, 'Value of {} is not {}'.format(key, value)


def test_runinfo_types_post_measure_3D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, t in [
        ('measure_function', Callable),
        ('scan0', ps.PropertyScan),
        ('scan1', ps.PropertyScan),
        ('scan2', ps.PropertyScan),
        ('data_path', PosixPath),
        ('_pyscan_version', str),
        ('file_name', str)]:
        assert isinstance(expt.runinfo[key], t), 'Value of {} is not {}'.format(key, t)
