import pytest
import pyscan as ps
from pyscan.drivers.heliotis.exceptions import HeliosImportException
from pyscan.drivers.keysight.exceptions import KeysightSD1Error
from pyscan.drivers.spin_core.exceptions import SpinAPIException
from pyscan.drivers.thorlabs.exceptions import ThorlabsKinesisImportException


def test_bad_imports():
    with pytest.raises(HeliosImportException):
        ps.HeliosCamera()

    with pytest.raises(KeysightSD1Error):
        ps.KeysightM3302ADAQ()

    with pytest.raises(KeysightSD1Error):
        ps.KeysightM3302AAWG()

    with pytest.raises(SpinAPIException):
        ps.PulseBlasterESRPro500()

    with pytest.raises(ThorlabsKinesisImportException):
        ps.ThorlabsBPC303()

    with pytest.raises(ThorlabsKinesisImportException):
        ps.ThorlabsBSC203()

    with pytest.raises(ThorlabsKinesisImportException):
        ps.ThorlabsMFF101()
