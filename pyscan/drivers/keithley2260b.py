from pyscan.drivers.instrument_driver import InstrumentDriver


class Keithley2260B(InstrumentDriver):

    '''
    Class to control the Kiethley 2260B DC power supply.

    Limits are queried when initalized and depend on the model

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    ouptut_on_delay: float
        Delay before output is turned on [0.00, 99.99]s
    ouptut_off_delay: float
        Delay before output is turned off [0.00, 99.99]s
    ouptut_mode: str
        CVHS - constant voltage high speed
        CCHS - constast current high speed
        CVLS - constant voltage low speed
        CCLS - constant current low speed
    output : int or str
        Turns the output on or off. Values: [0, 'off', 1, 'on']
    output_trigger_state: int or str
        Sets or queries the output trigger state[0, 'off', 1, 'on']

    smoothing: str
        Sets or queries the level of smoothing ['low', 'middle', 'high]

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

        super().__init__(instrument)

        self.debug = False

        # Get current limits
        self.max_current = float(self.query('CURR? MAX').strip('\n'))
        self.min_current = float(self.query('CURR? MIN').strip('\n'))

        self.max_current_trigger_ampliutde = float(self.query('CURR:TRIG? MAX').strip('\n'))
        self.min_current_trigger_ampliutde = float(self.query('CURR:TRIG? MIN').strip('\n'))

        self.max_over_current_level = float(self.query('CURR:PROT? MAX').strip('\n'))
        self.min_over_current_level = float(self.query('CURR:PROT? MIN').strip('\n'))

        self.max_current_rising_slew_rate = float(self.query('CURR:SLEW:RIS? MAX').strip('\n'))
        self.min_current_rising_slew_rate = float(self.query('CURR:SLEW:RIS? MIN').strip('\n'))

        self.max_current_falling_slew_rate = float(self.query('CURR:SLEW:FALL? MAX').strip('\n'))
        self.min_current_falling_slew_rate = float(self.query('CURR:SLEW:FALL? MIN').strip('\n'))

        # Get resistance limits
        self.max_resistance = float(self.query('RES? MAX').strip('\n'))
        self.min_resistance = float(self.query('RES? MIN').strip('\n'))

        # Get voltage limits
        self.max_voltage = float(self.query('VOLT? MAX').strip('\n'))
        self.min_voltage = float(self.query('VOLT? MIN').strip('\n'))

        self.max_voltage_trigger_ampliutde = float(self.query('VOLT:TRIG? MAX').strip('\n'))
        self.min_voltage_trigger_ampliutde = float(self.query('VOLT:TRIG? MIN').strip('\n'))

        self.max_over_voltage_level = float(self.query('VOLT:PROT? MAX').strip('\n'))
        self.min_over_voltage_level = float(self.query('VOLT:PROT? MIN').strip('\n'))

        self.max_voltage_rising_slew_rate = float(self.query('VOLT:SLEW:RIS? MAX').strip('\n'))
        self.min_voltage_rising_slew_rate = float(self.query('VOLT:SLEW:RIS? MIN').strip('\n'))

        self.max_voltage_falling_slew_rate = float(self.query('VOLT:SLEW:FALL? MAX').strip('\n'))
        self.min_voltage_falling_slew_rate = float(self.query('VOLT:SLEW:FALL? MIN').strip('\n'))

        self.initialize_properties()

        self.black_list_for_testing = ['_current', "_voltage", "_output"]

    def initialize_properties(self):

        # OUTPut properties
        self.add_device_property({
            'name': 'output_on_delay',
            'write_string': 'OUTP:DEL:ON {}',
            'query_string': 'OUTP:DEL:ON?',
            'range': [0.00, 99.99],
            'return_type': float})

        self.add_device_property({
            'name': 'output_off_delay',
            'write_string': 'OUTP:DEL:OFF {}',
            'query_string': 'OUTP:DEL:OFF?',
            'range': [0.00, 99.99],
            'return_type': float})

        self.add_device_property({
            'name': 'output_mode',
            'write_string': 'OUTP:MODE {}',
            'query_string': 'OUTP:MODE?',
            'indexed_values': ['CVHS', 'CCHS', 'CVLS', 'CCLS'],
            'return_type': int})

        self.add_device_property({
            'name': 'output',
            'write_string': 'OUTP {}',
            'query_string': 'OUTP?',
            'dict_values': {'Off': 0, 0: 0,
                            'On': 1, 1: 1},
            'return_type': int})

        self.add_device_property({
            'name': 'output_trigger_state',
            'write_string': 'OUTP:TRIG {}',
            'query_string': 'OUTP:TRIG?',
            'dict_values': {'Off': 0, 0: 0,
                            'On': 1, 1: 1},
            'return_type': int})

        # SENS:AVER:COUN properties
        self.add_device_property({
            'name': 'smoothing',
            'write_string': 'SENS:AVER:COUN {}',
            'query_string': 'SENS:AVER:COUN?',
            'indexed_values': ['low', 'middle', 'high'],
            'return_type': int})

        # SOURce properties
        # SOURce:CURRent properties

        self.add_device_property({
            'name': 'current',
            'write_string': 'CURR {}',
            'query_string': 'CURR?',
            'range': [self.min_current,
                      self.max_current],
            'return_type': float})

        self.add_device_property({
            'name': 'current_trigger_amplitude',
            'write_string': 'CURR:TRIG {}',
            'query_string': 'CURR:TRIG?',
            'range': [self.min_current_trigger_ampliutde,
                      self.max_current_trigger_ampliutde],
            'return_type': float})

        self.add_device_property({
            'name': 'over_current_level',
            'write_string': 'CURR:PROT {}',
            'query_string': 'CURR:PROT?',
            'range': [self.min_over_current_level,
                      self.max_over_current_level],
            'return_type': float})

        self.add_device_property({
            'name': 'current_protection_state',
            'write_string': 'CURR:PROT:STAT {}',
            'query_string': 'CURR:PROT:STAT?',
            'dict_values': {'Off': 0, 0: 0,
                            'On': 1, 1: 1},
            'return_type': float})

        self.add_device_property({
            'name': 'current_rising_slew_rate',
            'write_string': 'SOUR:CURR:SLEW:RIS {}',
            'query_string': 'SOUR:CURR:SLEW:RIS?',
            'range': [self.min_current_rising_slew_rate,
                      self.max_current_rising_slew_rate],
            'return_type': float})

        self.add_device_property({
            'name': 'current_falling_slew_rate',
            'write_string': 'SOUR:CURR:SLEW:FALL {}',
            'query_string': 'SOUR:CURR:SLEW:FALL?',
            'range': [self.min_current_falling_slew_rate,
                      self.max_current_falling_slew_rate],
            'return_type': float})

        # SOURce:RESistance
        self.add_device_property({
            'name': 'resistance',
            'write_string': 'RES {}',
            'query_string': 'RES?',
            'range': [self.min_resistance,
                      self.max_resistance],
            'return_type': float})

        # SOURce:VOLTage properties

        self.add_device_property({
            'name': 'voltage',
            'write_string': 'VOLT {}',
            'query_string': 'VOLT?',
            'range': [self.min_voltage,
                      self.max_voltage],
            'return_type': float})

        self.add_device_property({
            'name': 'voltage_trigger_amplitude',
            'write_string': 'VOLT:TRIG {}',
            'query_string': 'VOLT:TRIG?',
            'range': [self.min_voltage_trigger_ampliutde,
                      self.max_voltage_trigger_ampliutde],
            'return_type': float})

        self.add_device_property({
            'name': 'over_voltage_level',
            'write_string': 'VOLT:PROT {}',
            'query_string': 'VOLT:PROT?',
            'range': [self.min_over_voltage_level,
                      self.max_over_voltage_level],
            'return_type': float})

        self.add_device_property({
            'name': 'voltage_rising_slew_rate',
            'write_string': 'SOUR:VOLT:SLEW:RIS {}',
            'query_string': 'SOUR:VOLT:SLEW:RIS?',
            'range': [self.min_voltage_rising_slew_rate,
                      self.max_voltage_rising_slew_rate],
            'return_type': float})

        self.add_device_property({
            'name': 'voltage_falling_slew_rate',
            'write_string': 'SOUR:VOLT:SLEW:FALL {}',
            'query_string': 'SOUR:VOLT:SLEW:FALL?',
            'range': [self.min_voltage_falling_slew_rate,
                      self.max_voltage_falling_slew_rate],
            'return_type': float})

        # TRIG Properties

        self.add_device_property({
            'name': 'transient_trigger_source',
            'write_string': 'TRIG:TRAN:SOUR {}',
            'query_string': 'TRIG:TRAN:SOUR?',
            'values': ['BUS', 'IMM'],
            'return_type': str})

        self.add_device_property({
            'name': 'output_trigger_source',
            'write_string': 'TRIG:OUTP:SOUR {}',
            'query_string': 'TRIG:OUTP:SOUR?',
            'values': ['BUS', 'IMM'],
            'return_type': str})

        self.update_properties()

    def update_properties(self):

        self.output_on_delay
        self.output_off_delay
        self.output_mode
        self.output
        self.output_trigger_state

        self.smoothing

        self.current
        self.current_trigger_amplitude
        self.over_current_level
        self.current_protection_state
        self.current_rising_slew_rate
        self.current_falling_slew_rate

        self.resistance

        self.voltage
        self.voltage_trigger_amplitude
        self.over_voltage_level
        self.voltage_rising_slew_rate
        self.voltage_falling_slew_rate

        self.transient_trigger_source
        self.output_trigger_source

    def measure_current(self):

        current = self.query('MEAS:SCAL:CURR:DC?')

        return float(current)

    def measure_voltage(self):

        voltage = self.query('MEAS:SCAL:VOLT:DC?')

        return float(voltage)

    def measure_power(self):

        power = self.query('MEAS:SCAL:POW:DC?')

        return float(power)

    def transient_trigger(self):

        self.write('TRIG:TRAN')

    def output_trigger(self):

        self.write('TRIG:OUTP')
