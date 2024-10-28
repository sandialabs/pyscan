from pyscan.drivers.testing.test_instrument_driver import TestInstrumentDriver
from pyscan.drivers.testing.test_voltage import TestVoltage
from pyscan.drivers.testing.auto_test_driver_properties import auto_test_driver_properties
import pytest


def test_drivers_test_unit():
    test_instrument = TestInstrumentDriver()
    auto_test_driver_properties(test_instrument, skip_log=True)

    # This NEEDS to fail and is critical to safety
    bad_driver_entry = TestInstrumentDriver()
    # sets bad value to be included in blacklist. Mimics a mispelling or other accident.
    bad_driver_entry.black_list_for_testing = ['_nonexistent_property']
    with pytest.raises(AttributeError):
        auto_test_driver_properties(bad_driver_entry, skip_log=True)

    # This NEEDS to fail and is critical to safety
    bad_driver_entry2 = TestInstrumentDriver()
    # sets bad value to be included in blacklist. Mimics a mispelling or other accident.
    bad_driver_entry2.black_list_for_testing = ['_values', '_values']
    with pytest.raises(Exception):
        auto_test_driver_properties(bad_driver_entry2, skip_log=True)

    # Include additional tests to more thoroughly ensure driver test unit flags all blacklist discrepancies.

    test_voltage = TestVoltage()

    # query functions for test voltage have been bypassed to decouple dependencies so it remains modifiable
    auto_test_driver_properties(test_voltage, skip_log=True)
