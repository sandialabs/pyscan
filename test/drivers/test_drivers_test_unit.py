from test_instrument_driver import TestInstrumentDriver
from pyscan.drivers.test_voltage import TestVoltage
from drivers_test_unit import test_driver


def test_drivers_test_unit():
    test_instrument = TestInstrumentDriver()
    test_driver(test_instrument)

    test_voltage = TestVoltage()

    # query functions for test voltage have been bypassed to decouple dependencies so it remains modifiable
    #test_driver(test_voltage)


test_drivers_test_unit()
