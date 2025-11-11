import pyscan as ps
import numpy as np
import pytest


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_up_to_3D
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


class TestOptimizeScan(ps.AbstractOptimizeScan):

    def __init__(self, init_dict, prop, opt_in, sample_f_out, n_max=100):
        super().__init__(init_dict, prop, opt_in, sample_f_out, n_max=n_max)

    def step_optimizer(self, i, experiment):
        return [0] * len(self.opt_in)


@pytest.fixture
def optimize_scan():
    return TestOptimizeScan({'v1': 2.}, 'voltage', ('v1_readout',), 'vf', n_max=10)


@pytest.mark.parametrize('key,value', [
    ('init_dict', {'v1': 2.}),
    ('prop', 'voltage'),
    ('opt_in', ('v1_readout',)),
    ('scan_dict', {'iteration': np.array([])}),
    ('sample_f_out', 'vf'),
    ('dt', 0),
    ('i', 0),
    ('n', 1),
    ('n_max', 10)
])
def test_optimize_scan_init(optimize_scan, key, value):
    if key == 'scan_dict':
        for key1, value1 in value.items():
            assert np.all(optimize_scan.scan_dict[key1] == value[key1]), f"Optimize scan attribute {key} != {value}"
    else:
        assert optimize_scan[key] == value, f"Optimize scan attribute {key} != {value}"


def test_optimize_scan_iterate_m1(optimize_scan, runinfo, devices):
    runinfo.scan0 = optimize_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, -1)
    assert expt.runinfo.scan0.i == 0
    assert expt.runinfo.scan0.n == 1


def test_optimize_scan_no_iterate(optimize_scan, runinfo, devices):
    runinfo.scan0 = optimize_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 0, 0)
    assert expt.runinfo.scan0.i == 0
    assert expt.runinfo.scan0.n == 1


def test_optimize_scan_iterate_one(optimize_scan, runinfo, devices):
    runinfo.scan0 = optimize_scan
    expt = ps.Experiment(runinfo, devices)

    runinfo.scan0.iterate(expt, 1, 1)
    assert expt.runinfo.scan0.i == 1
    assert expt.runinfo.scan0.n == 2
