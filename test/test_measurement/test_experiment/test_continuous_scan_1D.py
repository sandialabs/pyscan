import pyscan as ps
import pytest
import numpy as np


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    runinfo.scan0 = ps.ContinuousScan(n_max=2)
    return runinfo


@pytest.fixture()
def devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    return devices


def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = expt.runinfo.scan0.i
    d.x2 = [d.x1 for _ in range(2)]
    d.x3 = [[expt.runinfo.scan0.i, expt.runinfo.scan0.i] for _ in range(2)]

    return d


def test_experiment_post_measure_1D(runinfo, devices):
    expt = ps.Experiment(runinfo, devices)
    expt.run()
    for key, value, t, shape in [
        ('iteration', np.array([0, 1]), np.ndarray, (2,)),
        ('x1', np.array([0.0, 1.0]), np.ndarray, (2,)),
        ('x2', np.array([[0.0, 0.0], [1.0, 1.0]]), np.ndarray, (2, 2)),
        ('x3', np.array([[[0., 0.], [0., 0.]], [[1., 1.], [1., 1.]]]), np.ndarray, (2, 2, 2))]:
        assert hasattr(expt, key), 'Experiment does not have key {}'.format(key)
        assert isinstance(expt[key], t), 'Value of {} is not {}'.format(key, t)
        assert np.allclose(expt[key], value), 'Value of {} is not {}'.format(key, value)


# def test_runinfo_contents_post_measure_1D(runinfo, devices):
#     expt = ps.Experiment(runinfo, devices)
#     expt.run()
#     for key, value in [
#         ('measured', ['x1', 'x2', 'x3']),
#         ('initial_pause', 0.1),
#         ('continuous', False),
#         ('has_average_scan', False),
#         ('running', False),
#         ('_dims', (2,)),
#         ('_ndim', 1),
#         ('_indicies', [1]),
#         ('complete', True)]:
#         assert hasattr(expt.runinfo, key), 'RunInfo does not have key {}'.format(key)
#         assert expt.runinfo[key] == value, 'Value of {} is not {}'.format(key, value)
