import pyscan as ps
import pytest


@pytest.mark.parametrize("key,value", [
    ("measured", []),
    ("measure_function", None),
    ("initial_pause", 0.1),
    ("_pyscan_version", ps.get_pyscan_version()),
    ("scans", []),
    ("dims", ()),
    ("average_dims", ()),
    ("dims", ()),
    ('ndim', 0),
    ('n_average_dim', 0),
    ('indicies', ()),
    ('average_indicies', ()),
    ('average_index', -1),
    ('has_average_scan', False)])
def test_runinfo_init_attributes_and_properties(key, value):
    runinfo = ps.RunInfo()
    if (value is None) or (value is False):
        assert runinfo[key] is value, f"Initialized RunInfo {key} is not {value}"
    else:
        assert runinfo[key] == value, f"Initialized RunInfo {key} is not {value}"


@pytest.mark.parametrize("key,value,t", [
    ("measured", [], list),
    ("measure_function", None, None),
    ("initial_pause", 0.1, float),
    ("_pyscan_version", ps.get_pyscan_version(), str),
    ("scan0", '_', ps.PropertyScan),
    ("scans", '_', list),
    ("dims", (2,), tuple),
    ("average_dims", (), tuple),
    ("dims", (2,), tuple),
    ("ndim", 1, int),
    ("n_average_dim", 0, int),
    ("indicies", (0,), tuple),
    ("average_indicies", (), tuple),
    ("average_index", -1, int),
    ("has_average_scan", False, bool)])
def test_runinfo_1D_attributes_and_properties(key, value, t):
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, prop='voltage')

    if value == '_':
        pass
    elif (value is None) or (value is False):
        assert runinfo[key] is value, f"RunInfo 1D {key} is not {value}"
    else:
        assert runinfo[key] == value, f"RunInfo 1D {key} is not {value}"

    if t is None:
        pass
    else:
        assert isinstance(runinfo[key], t), f"RunInfo 1D {key} is not of type {t}"


def test_bad_scan_order():
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 0.1)}, prop='voltage')
    runinfo.scan2 = ps.PropertyScan({'v2': ps.drange(0, 0.1, 0.1)}, prop='voltage')

    with pytest.raises(AssertionError):
        runinfo.check()


def test_repeat_property_scan():
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 1)}, prop='voltage')
    runinfo.scan1 = ps.PropertyScan({'v1': ps.drange(0, 0.1, 1)}, prop='voltage')

    with pytest.raises(AssertionError):
        runinfo.check()


def test_multi_repeat():
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.RepeatScan(1)
    runinfo.scan1 = ps.RepeatScan(1)

    with pytest.raises(AssertionError):
        runinfo.check()


def test_multi_average():
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.AverageScan(2)
    runinfo.scan1 = ps.AverageScan(2)

    with pytest.raises(AssertionError):
        runinfo.check()


def test_multi_continuous_scan():
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.ContinuousScan(2)
    runinfo.scan1 = ps.ContinuousScan(2)

    with pytest.raises(AssertionError):
        runinfo.check()


def test_low_continuous_scan():
    runinfo = ps.RunInfo()
    runinfo.scan0 = ps.ContinuousScan(2)
    runinfo.scan1 = ps.RepeatScan(2)

    with pytest.raises(AssertionError):
        runinfo.check()
