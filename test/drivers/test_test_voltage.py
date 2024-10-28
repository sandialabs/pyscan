'''
Pytest functions to test the Runinfo class
'''

from pyscan.drivers.testing.test_voltage import TestVoltage
from pyscan.drivers.testing.auto_test_driver import test_driver


def test_test_voltage():
    """
    Testing TestVoltage class

    Returns
    --------
    None
    """

    # set up v1 as representative for testing
    v1 = TestVoltage()

    test_driver(v1)
