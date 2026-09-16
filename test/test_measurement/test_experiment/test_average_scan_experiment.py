import pyscan as ps
import numpy as np
import pytest

N_AVERAGE = 4
MEAN_PASS = (N_AVERAGE - 1) / 2
V1 = np.array([0.0, 1.0])
V2 = np.array([0.0, 1.0, 2.0])


@pytest.fixture()
def devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    return devices


def measure_pass_and_voltages(expt):
    runinfo = expt.runinfo
    average_pass = runinfo.scans[runinfo.average_index].i

    d = ps.ItemAttribute()

    d.count = average_pass
    d.point = average_pass + 10 * expt.devices.v1.voltage + 100 * expt.devices.v2.voltage
    d.line = [d.point, 2 * d.point]
    d.grid = [[d.point, d.point + 1], [d.point + 2, d.point + 3]]

    return d


def make_layout(layout):
    '''
    Returns the scans for a layout and the expected mean of d.point at each non-average scan index
    '''
    average = ps.AverageScan(N_AVERAGE)
    v1 = ps.PropertyScan({'v1': V1}, 'voltage', dt=0)
    v2 = ps.PropertyScan({'v2': V2}, 'voltage', dt=0)
    mean_2D = MEAN_PASS + 10 * V1[:, np.newaxis] + 100 * V2[np.newaxis, :]

    return {
        'average_only': ([average], np.array(MEAN_PASS)),
        'average_first': ([average, v1], MEAN_PASS + 10 * V1),
        'average_last': ([v1, average], MEAN_PASS + 10 * V1),
        'average_middle': ([v1, average, v2], mean_2D),
        'average_last_2D': ([v1, v2, average], mean_2D),
    }[layout]


@pytest.mark.parametrize('layout', ['average_only', 'average_first', 'average_last', 'average_middle', 'average_last_2D'])
def test_average_experiment_saves_mean(devices, tmp_path, layout):
    scans, point = make_layout(layout)

    runinfo = ps.RunInfo()
    for i, scan in enumerate(scans):
        runinfo['scan{}'.format(i)] = scan
    runinfo.measure_function = measure_pass_and_voltages
    runinfo.initial_pause = 0

    expt = ps.Experiment(runinfo, devices, data_dir=tmp_path)
    expt.run()
    saved = ps.load_experiment(str(tmp_path / '{}.hdf5'.format(expt.runinfo.file_name)))

    for key, value in [
            ('count', np.full(point.shape, MEAN_PASS)),
            ('point', point),
            ('line', point[..., np.newaxis] * np.array([1, 2])),
            ('grid', point[..., np.newaxis, np.newaxis] + np.array([[0, 1], [2, 3]]))]:
        assert np.shape(expt[key]) == value.shape, 'Shape of {} is not {}'.format(key, value.shape)
        assert np.allclose(expt[key], value), 'Value of {} is {}, not the mean {}'.format(key, expt[key], value)
        assert np.allclose(saved[key], value), 'Saved {} is {}, not the mean {}'.format(key, saved[key], value)
