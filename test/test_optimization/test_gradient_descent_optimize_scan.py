import pyscan as ps
import pytest
from time import sleep


@pytest.fixture()
def runinfo():
    runinfo = ps.RunInfo()
    runinfo.measure_function = measure_paraboloid_2D
    return runinfo


@pytest.fixture()
def devices():
    devices = ps.ItemAttribute()
    devices.v1 = ps.TestVoltage()
    devices.v2 = ps.TestVoltage()
    return devices


def measure_paraboloid_2D(expt):

    devices = expt.devices

    d = ps.ItemAttribute()

    d.v1_readout = devices.v1.voltage
    d.v2_readout = devices.v2.voltage
    d.vf = ps.paraboloid_2D(d.v1_readout, d.v2_readout, e0=4., e1=6.)

    return d


@pytest.fixture
def v1_prop():
    return ps.GradientDescentOptimizeDeviceProperty(device_name='v1', property_name='voltage', initial_value=2.,
                                                    optimizer_input='v1_readout',
                                                    input_epsilon=1e-1, learning_rate=1e-1, update_epsilon=1e-1)


@pytest.fixture
def v2_prop():
    return ps.GradientDescentOptimizeDeviceProperty(device_name='v2', property_name='voltage', initial_value=1.,
                                                    optimizer_input='v2_readout',
                                                    input_epsilon=1e-1, learning_rate=1e-1, update_epsilon=1e-1)


@pytest.fixture
def gradient_descent_optimize_scan_early_stop(v1_prop, v2_prop):
    return ps.GradientDescentOptimizeScan((v1_prop, v2_prop),
                                          'vf',
                                          dt=0., n_max=100)


@pytest.fixture
def gradient_descent_optimize_scan_n_max(v1_prop, v2_prop):
    return ps.GradientDescentOptimizeScan((v1_prop, v2_prop),
                                          'vf',
                                          dt=0., n_max=10)


def test_gradient_descent_optimization_early_stop(gradient_descent_optimize_scan_early_stop,
                                                  runinfo, devices):

    runinfo.scan0 = gradient_descent_optimize_scan_early_stop
    expt = ps.Experiment(runinfo, devices)

    expt.start_thread()

    while expt.runinfo.running:
        sleep(1.)

    assert expt.runinfo.scan0.i < expt.runinfo.scan0.n_max - 1
    v1_len = len(expt.v1_readout)
    assert v1_len - 1 == expt.runinfo.scan0.i
    assert v1_len == expt.runinfo.scan0.n
    v2_len = len(expt.v2_readout)
    assert v2_len - 1 == expt.runinfo.scan0.i
    assert v2_len == expt.runinfo.scan0.n
    vf_len = len(expt.vf)
    assert vf_len - 1 == expt.runinfo.scan0.i
    assert vf_len == expt.runinfo.scan0.n
    assert abs(expt.v1_readout[-1] - 4.) < 1e-1
    assert abs(expt.v2_readout[-1] - 6.) < 1e-1
    assert abs(expt.vf[-1] - 0.) < 1e-1
    # TODO: check ends on smallest discovered input


def test_gradient_descent_optimization_n_max(gradient_descent_optimize_scan_n_max,
                                             runinfo, devices):

    runinfo.scan0 = gradient_descent_optimize_scan_n_max
    expt = ps.Experiment(runinfo, devices)

    expt.start_thread()

    while expt.runinfo.running:
        sleep(1.)

    assert expt.runinfo.scan0.i == expt.runinfo.scan0.n_max - 1
    assert expt.runinfo.scan0.n == expt.runinfo.scan0.n_max
    v1_len = len(expt.v1_readout)
    assert v1_len - 1 == expt.runinfo.scan0.i
    assert v1_len == expt.runinfo.scan0.n
    v2_len = len(expt.v2_readout)
    assert v2_len - 1 == expt.runinfo.scan0.i
    assert v2_len == expt.runinfo.scan0.n
    vf_len = len(expt.vf)
    assert vf_len - 1 == expt.runinfo.scan0.i
    assert vf_len == expt.runinfo.scan0.n
