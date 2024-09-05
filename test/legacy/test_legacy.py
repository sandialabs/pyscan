import pyscan as ps


def test_legacy():
    devices = ps.ItemAttribute()
    runinfo = ps.RunInfo()
    sweep = ps.Sweep(runinfo, devices)

    err_msg = "Legacy nomenclature failed. Sweep not initialized as Experiment or MetaSweep not as Abstract Experiment."
    assert isinstance(sweep, ps.Experiment), err_msg
