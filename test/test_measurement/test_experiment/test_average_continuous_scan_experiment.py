import pyscan as ps
import numpy as np
import pytest

N_AVERAGE = 3
MEAN_PASS = (N_AVERAGE - 1) / 2
V1 = np.array([0.0, 1.0])
V2 = np.array([0.0, 1.0, 2.0])


@pytest.fixture()
def devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    return devices


def measure_pass_voltages_and_iteration(expt):
    runinfo = expt.runinfo
    average_pass = runinfo.scans[runinfo.average_index].i
    iteration = runinfo.scans[-1].i

    d = ps.ItemAttribute()

    d.count = average_pass
    d.point = average_pass + 10 * expt.devices.v1.voltage + 100 * expt.devices.v2.voltage + 1000 * iteration
    d.line = [d.point, 2 * d.point]
    d.grid = [[d.point, d.point + 1], [d.point + 2, d.point + 3]]

    return d


def measure_and_stop_in_second_iteration(expt):
    '''
    Stops after the second average pass at the first v1 value of the second continuous iteration
    '''
    if (expt.runinfo.scan2.i, expt.runinfo.scan1.i, expt.runinfo.scan0.i) == (1, 0, 1):
        expt.stop()

    return measure_pass_voltages_and_iteration(expt)


def make_layout(layout, n_max):
    '''
    Returns the scans for a layout and the expected mean of d.point at each non-average scan index
    '''
    average = ps.AverageScan(N_AVERAGE)
    v1 = ps.PropertyScan({'v1': V1}, 'voltage', dt=0)
    v2 = ps.PropertyScan({'v2': V2}, 'voltage', dt=0)
    continuous = ps.ContinuousScan(n_max=n_max)
    iteration = 1000 * np.arange(n_max)

    return {
        'average_only': ([average, continuous], MEAN_PASS + iteration),
        'average_first': ([average, v1, continuous], MEAN_PASS + 10 * V1[:, np.newaxis] + iteration),
        'average_last': ([v1, average, continuous], MEAN_PASS + 10 * V1[:, np.newaxis] + iteration),
        'average_middle': ([v1, average, v2, continuous],
                           MEAN_PASS + 10 * V1[:, np.newaxis, np.newaxis] + 100 * V2[:, np.newaxis] + iteration),
    }[layout]


def run_and_load(runinfo, devices, data_dir):
    runinfo.initial_pause = 0

    expt = ps.Experiment(runinfo, devices, data_dir=data_dir)
    expt.run()
    saved = ps.load_experiment(str(data_dir / '{}.hdf5'.format(expt.runinfo.file_name)))

    return expt, saved


def assert_mean_data(expt, saved, count, point):
    '''
    Asserts the experiment's and the saved file's iteration and averaged data, given the expected means of
    d.count and d.point at each non-average scan index
    '''
    for key, value in [
            ('iteration', np.arange(point.shape[-1])),
            ('count', count),
            ('point', point),
            ('line', point[..., np.newaxis] * np.array([1, 2])),
            ('grid', point[..., np.newaxis, np.newaxis] + np.array([[0, 1], [2, 3]]))]:
        for source, values in [('Experiment', expt[key]), ('Saved', saved[key])]:
            assert np.shape(values) == value.shape, '{} {} has shape {}, not {}'.format(
                source, key, np.shape(values), value.shape)
            assert np.allclose(values, value, equal_nan=True), '{} {} is {}, not {}'.format(source, key, values, value)


@pytest.mark.parametrize('n_max', [1, 3])
@pytest.mark.parametrize('layout', ['average_only', 'average_first', 'average_last', 'average_middle'])
def test_average_continuous_experiment_saves_mean(devices, tmp_path, layout, n_max):
    scans, point = make_layout(layout, n_max)

    runinfo = ps.RunInfo()
    for i, scan in enumerate(scans):
        runinfo['scan{}'.format(i)] = scan
    runinfo.measure_function = measure_pass_voltages_and_iteration

    expt, saved = run_and_load(runinfo, devices, tmp_path)

    assert_mean_data(expt, saved, np.full(point.shape, MEAN_PASS), point)


def test_stopped_average_continuous_experiment_saves_partial_mean(devices, tmp_path):
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.AverageScan(N_AVERAGE)
    runinfo.scan1 = ps.PropertyScan({'v1': V1}, 'voltage', dt=0)
    runinfo.scan2 = ps.ContinuousScan(n_max=5)
    runinfo.measure_function = measure_and_stop_in_second_iteration

    expt, saved = run_and_load(runinfo, devices, tmp_path)

    # the first iteration is fully averaged, the second has two passes at the first v1 value and none at the second
    count = np.array([[MEAN_PASS, 0.5], [MEAN_PASS, np.nan]])
    point = count + 10 * V1[:, np.newaxis] + 1000 * np.arange(2)

    assert_mean_data(expt, saved, count, point)
