import pyscan as ps
import numpy as np
import pytest


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()

    def do_nothing(value):
        pass

    runinfo.measure_function = measure_up_to_3D
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, 'voltage', dt=0)
    runinfo.scan1 = ps.FunctionScan(do_nothing, [0, 1, 2], dt=0)

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


def test_repeat_experiment_2D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()

    for key, value, t, shape in [
        ('v1_voltage', np.array([0, 0.1]), np.ndarray, (2,)),
        ('do_nothing', np.array([0, 1, 2]), np.ndarray, (3,)),
        ('x1', np.array([[0., 0., 0.], [1., 1., 1.]]), np.ndarray, (2, 3)),
        ('x2', np.array(
            [[[0., 0.], [0., 0.], [0., 0.]],
            [[1., 1.], [1., 1.], [1., 1.]]]), np.ndarray, (2, 3, 2)),
        ('x3', np.array((list(np.zeros((3, 2, 2))), list(np.ones((3, 2, 2))))), np.ndarray, (2, 3, 2, 2))]:
        assert hasattr(expt, key), 'Experiment does not have key {}'.format(key)
        assert isinstance(expt[key], t), 'Value of {} is not {}'.format(key, t)
        assert np.allclose(expt[key], value), 'Value of {} is not {}'.format(key, value)
        assert expt[key].shape == shape, 'Shape of {} is not {}'.format(key, shape)
