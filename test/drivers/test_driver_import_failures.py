import pytest
import pyscan as ps
from pyscan.drivers.heliotis.exceptions import HeliosImportException
from pyscan.drivers.keysight.exceptions import KeysightSD1Error
from pyscan.drivers.spin_core.exceptions import SpinAPIException
from pyscan.drivers.thorlabs.exceptions import ThorlabsKinesisImportException


def test_bad_imports():
    with pytest.raises(BaseException):
        ps.HeliosCamera()

    with pytest.raises(BaseException):
        ps.KeysightM3302ADAQ()

    with pytest.raises(BaseException):
        ps.KeysightM3302AAWG()

    with pytest.raises(BaseException):
        ps.PulseBlasterESRPro500()

    with pytest.raises(BaseException):
        ps.ThorlabsBPC303()

    with pytest.raises(BaseException):
        ps.ThorlabsBSC203()

    with pytest.raises(BaseException):
        ps.ThorlabsMFF101()
