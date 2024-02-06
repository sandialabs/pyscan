'''
Pytest functions to test the Runinfo class
'''

import pyscan as ps
import pytest
import importlib
importlib.reload(ps)


def test_testvoltage():
    """
    Testing TestVoltage class

    Returns
    --------
    None
    """

    ############################ ADDDDDDDDD ERROR MESSAGES FOR THESE TESTS!!!! ###############

    # set up v1 as representative for testing
    v1 = ps.TestVoltage()

    # test voltage attribute
    assert hasattr(v1, 'voltage')
    assert type(v1.voltage) is float
    assert v1.voltage == 0.0
    assert v1._voltage == 0.0
    with pytest.raises(Exception):
        v1.voltage = -1
    with pytest.raises(Exception):
        v1.voltage = 11
    with pytest.raises(Exception):
        v1.voltage = 'bad'
    assert callable(v1.query)
    assert v1.query('VOLT?') == '0.0'
    v1.voltage = 1
    v1.voltage = 5
    v1.voltage = 10

    # test power attribute initialization
    assert hasattr(v1, 'power')
    assert type(v1.power) is int
    assert v1.power == 1
    assert v1.query('POW?') == '1'
    with pytest.raises(Exception):
        v1.power = 0
    with pytest.raises(Exception):
        v1.power = 2
    with pytest.raises(Exception):
        v1.power = 9
    with pytest.raises(Exception):
        v1.power = 11
    with pytest.raises(Exception):
        v1.power = 'superpower'
    v1.power = 10

    # test output state attribute initialization
    assert hasattr(v1, 'output_state')
    ###### not sure why v1.output_state is not working below but _output_state is...
    ############ These seem inconsistent and unpredictable in why the _output vs regular output
    ####### is acting in the way it is. It's behavior seems different from the above properties.
    ########## This _output_state should be an int and not a string.
    assert type(v1._output_state) is str
    assert v1._output_state == "'off', '0'"
    assert v1.query('OUTP?') == "'off', '0'"
    with pytest.raises(Exception):
        v1.output_state = {'orkitty ork ork': 1}
    with pytest.raises(Exception):
        v1.output_state = 'orkity ork ork'
    with pytest.raises(Exception):
        v1.output_state = -1
    with pytest.raises(Exception):
        v1.output_state = 2
    with pytest.raises(Exception):
        v1.output_state = '5'
    v1.output_state = '1'
    v1.output_state = '0'
    v1.output_state = 'on'
    assert v1._output_state == 1
    v1.output_state = 'off'
    assert v1._output_state == 0
