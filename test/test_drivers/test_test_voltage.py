'''
Pytest functions to test the Runinfo class
'''

from pyscan.drivers.testing.test_voltage import TestVoltage
from pyscan.drivers.testing.auto_test_driver import test_driver
import pytest


def test_test_voltage():
    """
    Testing TestVoltage class

    Returns
    --------
    None
    """

    # set up v1 as representative for testing
    v1 = TestVoltage()

    # ########## add 2 more test voltages for testing...

    # test voltage attribute
    assert hasattr(v1, 'voltage'), "TestVoltage missing voltage attribute"
    assert isinstance(v1.voltage, float), "TestVoltage voltage attribute is not a float"
    assert v1.voltage == 0.0, "TestVoltage voltage not initialized to 0.0"
    assert v1._voltage == 0.0, "TestVoltage _voltage does not return 0.0"
    with pytest.raises(Exception):
        v1.voltage = -1, "TestVoltage voltage can be negative"
    with pytest.raises(Exception):
        v1.voltage = 11, "TestVoltage voltage can be more than 10"
    with pytest.raises(Exception):
        v1.voltage = 'bad', "TestVoltage can be a string"
    assert callable(v1.query), "TestVoltage query is not a callable function"
    assert v1.query('VOLT?') == '0.0', "TestVoltage query of 'Volt?' does not return string of voltage"
    v1.voltage = 1
    v1.voltage = 5
    v1.voltage = 10

    # test power attribute initialization
    assert hasattr(v1, 'power'), "TestVoltage missing power attribute"
    assert isinstance(v1.power, int), "TestVoltage power is not an int"
    assert v1.power == 1, "TestVoltage  power is not initialized as 1"
    assert v1.query('POW?') == '1', "TestVoltage query of 'POW?' does not return string of power"
    with pytest.raises(Exception):
        v1.power = 0, "TestVoltage power can be set to 0"
    with pytest.raises(Exception):
        v1.power = 2, "TestVoltage power can be set to 2"
    with pytest.raises(Exception):
        v1.power = 9, "TestVoltage power can be set to 9"
    with pytest.raises(Exception):
        v1.power = 11, "TestVoltage power can be set to 11"
    with pytest.raises(Exception):
        v1.power = 'superpower', "TestVoltage power can be set to a string"
    v1.power = 10

    # test output state attribute initialization
    assert hasattr(v1, 'output_state'), "TestVoltage missing output_state attribute"
    assert isinstance(v1._output_state, str), "TestVoltage _output_state is not initially a string"
    assert v1._output_state == 'off', "TestVoltage _output_state does not initially return expected output state"
    assert v1.query('OUTP?') == '0', "TestVoltage query of 'OUTP?' does not return expected result"
    with pytest.raises(Exception):
        v1.output_state = {'orkitty ork ork': 1}, "TestVoltage output_state can be set to invalid dict"
    with pytest.raises(Exception):
        v1.output_state = 'orkity ork ork', "TestVoltage output_state can be set to invalid string"
    with pytest.raises(Exception):
        v1.output_state = -1, "TestVoltage output_state can be set to negative number"
    with pytest.raises(Exception):
        v1.output_state = 2, "TestVoltage output_state can be set to invalid integer"
    with pytest.raises(Exception):
        v1.output_state = 1, "TestVoltage output_state can be set to an integer"
    with pytest.raises(Exception):
        v1.output_state = '5', "TestVoltage output_state can be set to a non dictionary key string"
    v1.output_state = '1'
    assert v1.query('OUTP?') == '1', "TestVoltage query of 'OUTP?' does not return expected result"
    assert v1._output_state == 'on', "TestVoltage _output_state does not get machine value after '1' key user input"
    assert v1.output_state == 'on', "TestVoltage output_state does not get machine value after 'on' key user input"
    v1.output_state = '0'
    assert v1._output_state == 'off', "TestVoltage _output_state does not get machine value after 'off' key user input"
    assert v1.output_state == 'off', "TestVoltage output_state does not get machine value after 'off' key user input"
    v1.output_state = 'on'
    assert v1._output_state == 'on', "TestVoltage _output_state does not get machine value after 'on' key user input"
    assert v1.output_state == 'on', "TestVoltage output_state does not get machine value after 'on' key user input"
    v1.output_state = 'off'
    assert v1._output_state == 'off', "TestVoltage _output_state does not get machine value after 'off' key user input"
    assert v1.output_state == 'off', "TestVoltage output_state does not get machine value after 'off' key user input"

    test_driver(v1)
