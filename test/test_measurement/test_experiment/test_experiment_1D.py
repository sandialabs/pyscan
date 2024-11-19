import pyscan as ps
import numpy as np
import pytest
from pathlib import PosixPath
from typing import Callable
import re


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage', dt=0)
    return runinfo


@pytest.fixture()
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


## Test initial experiment
def test_experiment_init(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    for key in ['runinfo', 'devices']:
        assert hasattr(expt, key), 'Experiment does not have attribute {}'.format(key)


def test_measure_function_returns(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    d = expt.runinfo.measure_function(expt)
    for key, value, t, shape in [
        ('x1', 0, int, ()),
        ('x2', [0, 0], list, (2,)),
        ('x3', [[0, 0], [0, 0]], list, (2, 2))]:
        assert isinstance(d, ps.ItemAttribute), 'measure_function does not return ItemAttribute'
        assert hasattr(d, key), 'ItemAttribute does not have key {}'.format(key)
        assert d[key] == value, 'Value of {} is not {}'.format(key, value)


def test_experiment_post_measure_1D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, value, t, shape in [
        ('v1_voltage', np.array([0, 0.1]), np.ndarray, (2,)),
        ('x1', np.array([0.0, 1.0]), np.ndarray, (2,)),
        ('x2', np.array([[0.0, 0.0], [1.0, 1.0]]), np.ndarray, (2, 2)),
        ('x3', np.array([[[0., 0.], [0., 0.]], [[1., 1.], [1., 1.]]]), np.ndarray, (2, 2, 2))]:
        assert hasattr(expt, key), 'Experiment does not have key {}'.format(key)
        assert isinstance(expt[key], t), 'Value of {} is not {}'.format(key, t)
        assert np.allclose(expt[key], value), 'Value of {} is not {}'.format(key, value)


## Test experiment after running

def test_runinfo_post_measure_1D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, value, t, shape in [
        ('v1_voltage', np.array([0, 0.1]), np.ndarray, (2,)),
        ('x1', np.array([0.0, 1.0]), np.ndarray, (2,)),
        ('x2', np.array([[0.0, 0.0], [1.0, 1.0]]), np.ndarray, (2, 2)),
        ('x3', np.array([[[0., 0.], [0., 0.]], [[1., 1.], [1., 1.]]]), np.ndarray, (2, 2, 2))]:
        assert hasattr(expt, key), 'Experiment does not have key {}'.format(key)
        assert isinstance(expt[key], t), 'Value of {} is not {}'.format(key, t)
        assert np.allclose(expt[key], value), 'Value of {} is not {}'.format(key, value)


def test_runinfo_contents_post_measure_1D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, value in [
        ('measured', ['x1', 'x2', 'x3']),
        ('initial_pause', 0.1),
        ('continuous', False),
        ('has_average_scan', False),
        ('running', False),
        ('_dims', (2,)),
        ('_ndim', 1),
        ('_indicies', [1]),
        ('complete', True)]:
        assert hasattr(expt.runinfo, key), 'RunInfo does not have key {}'.format(key)
        assert expt.runinfo[key] == value, 'Value of {} is not {}'.format(key, value)


def test_runinfo_types_post_measure_1D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, t in [
        ('measure_function', Callable),
        ('scan0', ps.PropertyScan),
        ('data_path', PosixPath),
        ('_pyscan_version', str),
        ('file_name', str)]:
        assert hasattr(expt.runinfo, key), 'RunInfo does not have key {}'.format(key)
        assert isinstance(expt.runinfo[key], t), 'Value of {} is not {}'.format(key, t)


def test_file_name_format(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    assert re.match(r'^\d{8}T\d{6}(-\d+)?$', expt.runinfo.file_name), \
        "runinfo file_name is not properly formatted"
