from pyscan.drivers.instrument_driver import InstrumentDriver


class Keithley2260B(InstrumentDriver):

    '''
    Class to control the Kiethley 2260B DC power supply.

    Limits are currently set for the 2260B-80-27 720W
    model, later we can use the *IDN query to determine the
    specific model and auto populate limits.

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from
        :func:`.new_instrument`)

    Properties
    ----------
    output : int or str
        Turns the output on or off. Values: [0, 1, 'ON', 'OFF']
    current : int
        Sets the value of the output current. Range: [0, 27] Amps.
        Use the method measure_current() to get the actual current.
    current_rising_slew_rate : float
        Sets the value of the rising slew rate for current
        Range : [0.01, 54] Amps/s
    current_falling_slew_rate : float
        Sets the value of the falling slew rate for current
        Range : [0.01, 54] Amps/s
    voltage : float
        Sets the value of the output voltage. Range: [0, 80] Volts.
        Use the method measure_voltage() to get the actual voltage.
    resistance : float
        Sets the value of the internal resistance. Range: [0, 2.963]

    Methods
    -------
    measure_current()
        Returns the measured current in Amps
    measure_voltage()
        Returns the measured voltage in Volts
    measure_power()
        Returns the measured power in Watts
    '''

    def __init__(self, instrument, debug=False):
        self.instrument = instrument
        self.debug = debug
        self.initialize_properties()

    def initialize_properties(self):

        # OUTPut properties

        self.add_device_property({
            'name': 'output',
            'write_string': 'OUTP:STAT:IMM {}',
            'query_string': 'OUTP:STAT:IMM?',
            'values': [0, 1, 'ON', 'OFF'],
            'return_type': str})

        # SOURce properties
        # SOURce:CURRent properties

        self.add_device_property({
            'name': 'current',
            'write_string': 'SOUR:CURR:LEV:IMM:AMPL {}',
            'query_string': 'SOUR:CURR:LEV:IMM:AMPL?',
            'range': [0, 27],
            'return_type': float})

        self.add_device_property({
            'name': 'current_rising_slew_rate',
            'write_string': 'SOUR:CURR:SLEW:RIS {}',
            'query_string': 'SOUR:CURR:SLEW:RIS?',
            'range': [0.01, 54.00],
            'return_type': float})

        self.add_device_property({
            'name': 'current_falling_slew_rate',
            'write_string': 'SOUR:CURR:SLEW:FALL {}',
            'query_string': 'SOUR:CURR:SLEW:FALL?',
            'range': [0.01, 54.00],
            'return_type': float})

        self.add_device_property({
            'name': 'voltage',
            'write_string': 'SOUR:VOLT:LEV:IMM:AMPL {}',
            'query_string': 'SOUR:VOLT:LEV:IMM:AMPL?',
            'range': [0, 80],
            'return_type': float})

        self.add_device_property({
            'name': 'resistance',
            'write_string': 'SOUR:RES:LEV:IMM:AMPL {}',
            'query_string': 'SOUR:RES:LEV:IMM:AMPL?',
            'range': [0, 2.963],
            'return_type': float})

    def measure_current(self):

        current = self.query('MEAS:SCAL:CURR:DC?')

        return float(current)

    def measure_voltage(self):

        voltage = self.query('MEAS:SCAL:VOLT:DC?')

        return float(voltage)

    def measure_power(self):

        power = self.query('MEAS:SCAL:POW:DC?')

        return float(power)
