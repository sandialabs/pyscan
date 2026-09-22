import pyscan as ps
import pytest
import numpy as np

V1 = np.array([0.0, 0.1, 0.2])
N_MAX = 3


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
    runinfo.scan0 = ps.PropertyScan({'v1': V1}, 'voltage', dt=0)
    runinfo.scan1 = ps.ContinuousScan(n_max=N_MAX)
    runinfo.initial_pause = 0
    return runinfo


@pytest.fixture()
def devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    return devices


def measure_up_to_3D(expt):
    d = ps.ItemAttribute()

    d.x1 = expt.devices.v1.voltage + 10 * expt.runinfo.scan1.i
    d.x2 = [d.x1, 2 * d.x1]
    d.x3 = [[d.x1, d.x1 + 1], [d.x1 + 2, d.x1 + 3]]

    return d


def test_experiment_post_measure_2D(runinfo, devices, tmp_path):
    expt = ps.Experiment(runinfo, devices, data_dir=tmp_path)
    expt.run()
    saved = ps.load_experiment(str(tmp_path / '{}.hdf5'.format(expt.runinfo.file_name)))

    x1 = V1[:, np.newaxis] + 10 * np.arange(N_MAX)
    for key, value in [
            ('iteration', np.arange(N_MAX)),
            ('x1', x1),
            ('x2', x1[..., np.newaxis] * np.array([1, 2])),
            ('x3', x1[..., np.newaxis, np.newaxis] + np.array([[0, 1], [2, 3]]))]:
        for source, values in [('Experiment', expt[key]), ('Saved', saved[key])]:
            assert np.shape(values) == value.shape, '{} {} has shape {}, not {}'.format(
                source, key, np.shape(values), value.shape)
            assert np.allclose(values, value), '{} {} is {}, not {}'.format(source, key, values, value)
