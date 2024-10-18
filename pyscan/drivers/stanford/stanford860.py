from time import sleep
from ..instrument_driver import InstrumentDriver


class Stanford860(InstrumentDriver):
    '''
    Class to control Stanford Research Systems SR860 - 500 kHz lock-in amplifier

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)

    id : read-only
        Gets the id string of the device.

    Reference Commands
    timebase_mode : str
        Gets/sets the timebase mode as auto or internal
    timebase_state : read-only
        Gets the timebase mode which could be external or internal
    phase : float
        Gets/sets the phase of the device. Range: [-180, 180]
    frequency : float
        Gets/sets the frequency. Range [0.001, 500000] Hz
    internal_frequency : float
        Gets the internal reference frequency
    external_frequency : float
        Gets the exteranl reference frequency
    detection_frequency : float
        Gets the actual detection frequency from dual reference mode or
        harmonics
    harmonic : int
        Gets/sets the ith harmonic of the reference frequency. Range [1, 99]
    dual_harmonic : int
        Gets/sets the ith harmonic in dual referene mode. Range [1, 99]
    chopper_blade_slots : int
        Gets/sets the number of slots for the chopper when used with the stanford540 chopper. 6 or 30
    chopper_blade_phase : float
        Gets/sets the relative phase for the chopper when used with the stanford540 chopper.
        Range[-180, 180]
    amplitude : float
        Gets/sets the output sine wave amplitude. Range [1e-9, 2]
    voltage_offset : float
        Gets/sets the output voltage offset. Range [-5, 5]
    dc_out_reference : str
        Gets/sets the reference for the output to "common" or "difference"
    reference_source : str
        Gets/sets the reference source. ["internal", "exteranl", "dual", "chop"]
    reference_trigger_mode : str
        Gets/sets the reference trigger mode. ["sine", "positive", "negative"]
    reference_impedance : int
        Gets/sets the reference impedance in Ohms. [50, 1e6]

    Signal Commands
    signal_input : str
        Gets/sets the input to "voltage" or "current"
    voltage_input_mode : str
        Gets/sets the voltage input to "A" or "A-B"
    voltage_input_coupling : str
        Gets/sets the voltage input to "ac" or "dc"
    voltage_input_shield : str
        Gets/sets the voltage input shield to "float" or "ground"
    voltage_input_range : float
        Gets/sets the voltage input range to
        1, 0.3, 0.1, 0.03, 0.01 V
    current_input_impedance : int
        Gets/sets the current input impedance to "1" or "100" MOhms
    signal_strength : read-only
        Gets the signal strenght as a integer level between 0 and 4
        where 4 is overaloaded
    voltage_sensitivity : float
        Gets/sets the voltage sensitivity in V to
        1, 0.5, 0.2, 0.1,
        0.05, 0.02, 0.01, 0.005, 0.002, 0.001,
        5e-4, 2e-4, 1e-4, 5e-5, 2e-5, 1e-5,
        5e-6, 2e-6, 1e-6, 5e-7, 2e-7, 1e-7,
        5e-8, 2e-8, 1e-8, 5e-9, 2e-9, 1e-9
    time_constant : float
        Gets/sets the filter time constant in seconds to
        1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4,
        1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3,
        1, 3, 10, 30, 100, 300, 1e3, 3e3, 10e3, 30e3
    filter_slope : int
        Get/sets the filter slope in dB/octave to
        6, 12, 18, 24
    synchronous_filter : str
        Gets/sets the synchronous filter to "off" or "on"
    advanced_filter : str
        Gets/sets the advanced filter to "off" or "on"
    equivalent_bandwidth : read-only
        Gets teh equivalent bandwidth based on the time constand
        and filter in Hz.
    Output Commands
    channel_1_output : str
        Gets/sets channel 1 output to "x" or "r"
    channel_2_output : str
        Gets/sets channel 2 output to "y" or "theta"
    x_expand : str
        Gets/sets x source to "off", "10x", or "100x"
    y_expand : str
        Gets/sets y source to "off", "10x", or "100x"
    r_expand : str
        Gets/sets r source to "off", "10x", or "100x"
    x_offset_state : str
        Gets/sets the x offset state as "off" or "on"
    y_offset_state : str
        Gets/sets the y offset state as "off" or "on"
    r_offset_state : str
        Gets/sets the r offset state as "off" or "on"
    x_offset_percent : float
        Gets/sets x offset as a percent from -999.99 to 999.99 percent
    y_offset_percent : float
        Gets/sets y offset as a percent from -999.99 to 999.99 percent
    r_offset_percent : float
        Gets/sets r offset as a percent from -999.99 to 999.99 percent
    x_ratio_state : str
        Gets/sets x ratio mode relative to aux in 3 to "off" or "on"
        where the x output is then:
        ('x'/sensitivity - offset)/(aux_in_3/1V) x expand x 10V
    y_ratio_state : str
        Gets/sets y ratio mode relative to aux in 3 to "off" or "on"
        where the y output is then:
        ('y'/sensitivity - y_offset)/(aux_in_3/1V) x y_expand x 10V
    r_ratio_state : str
        Gets/sets r ratio mode relative to aux in 4 to "off" or "on"
        where the r output is then:
        ('r'/sensitivity - r_offset)/(aux_in_4/1V) x r_expand x 10V

    # Auxiliary Input/output
    auxiliary_input_voltage_1 : read-only
        Gets the voltage input to AUX1
    auxiliary_input_voltage_2 : read-only
        Gets the voltage input to AUX2
    auxiliary_input_voltage_3 : read-only
        Gets the voltage input to AUX2
    auxiliary_input_voltage_4 : read-only
        Gets the voltage input to AUX4
    auxiliary_output_voltage_1 : float
        Gets/sets the auxiliary voltage output from -10.5 to 10.5 V
    auxiliary_output_voltage_2 : float
        Gets/sets the auxiliary voltage output from -10.5 to 10.5 V
    auxiliary_output_voltage_3 : float
        Gets/sets the auxiliary voltage output from -10.5 to 10.5 V
    auxiliary_output_voltage_4 : float
        Gets/sets the auxiliary voltage output from -10.5 to 10.5 V


    Methods
    -------
    auto_phase()
    auto_offset(source)
    read_channel(channel)
    read()
    snap()
    snap_display()
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "0.2.0"

        self.black_list_for_testing = [
            '_amplitude',
            '_voltage_offset',
            '_auxiliary_output_voltage_1',
            '_auxiliary_output_voltage_2',
            '_auxiliary_output_voltage_3',
            '_auxiliary_output_voltage_4']

        self.initialize_properties()
        self.update_properties()

    def initialize_properties(self):

        # Reference and Phase properties

        self.add_device_property({
            'name': 'id',
            'query_string': '*IDN?',
            'read_only': True,
            'return_type': str})

        # Reference Commands
        self.add_device_property({
            'name': 'timebase_mode',
            'write_string': 'TBMODE {}',
            'query_string': 'TBMODE?',
            'indexed_values': ['auto', 'internal'],
            'return_type': str})

        self.add_device_property({
            'name': 'timebase_state',
            'query_string': 'TBSTAT?',
            'indexed_values': ['internal', 'external'],
            'read_only': True,
            'return_type': str})

        self.add_device_property({
            'name': 'phase',
            'write_string': 'PHAS {}',
            'query_string': 'PHAS?',
            'range': [-180, 180],
            'return_type': float})

        self.add_device_property({
            'name': 'frequency',
            'write_string': 'FREQ {}',
            'query_string': 'FREQ?',
            'range': [0.001, 500000],
            'return_type': float})

        self.add_device_property({
            'name': 'internal_frequency',
            'query_string': 'FREQINT?',
            'read_only': True,
            'return_type': float})

        self.add_device_property({
            'name': 'external_frequency',
            'query_string': 'FREQEXT?',
            'read_only': True,
            'return_type': float})

        self.add_device_property({
            'name': 'detection_frequency',
            'query_string': 'FREQDET?',
            'read_only': True,
            'return_type': float})

        self.add_device_property({
            'name': 'harmonic',
            'write_string': 'HARM {}',
            'query_string': 'HARM?',
            'range': [1, 99],
            'return_type': int})

        self.add_device_property({
            'name': 'dual_harmonic',
            'write_string': 'HARMDUAL {}',
            'query_string': 'HARMDUAL?',
            'range': [1, 99],
            'return_type': int})

        self.add_device_property({
            'name': 'chopper_blade_slots',
            'write_string': 'BLADESLOTS {}',
            'query_string': 'BLADESLOTS?',
            'indexed_values': [6, 30],
            'return_type': int})

        self.add_device_property({
            'name': 'chopper_blade_phase',
            'write_string': 'BLADEPHASE {}',
            'query_string': 'BLADEPHASE?',
            'range': [-180, 180],
            'return_type': float})

        self.add_device_property({
            'name': 'amplitude',
            'write_string': 'SLVL {}',
            'query_string': 'SLVL?',
            'range': [1e-9, 2],
            'return_type': float})

        self.add_device_property({
            'name': 'voltage_offset',
            'write_string': 'SOFF {}',
            'query_string': 'SOFF?',
            'range': [-5, 5],
            'return_type': float})

        self.add_device_property({
            'name': 'dc_out_reference',
            'write_string': 'REFM {}',
            'query_string': 'REFM?',
            'indexed_values': ['common', 'difference']})

        self.add_device_property({
            'name': 'reference_source',
            'write_string': 'RSRC {}',
            'query_string': 'RSRC?',
            'indexed_values': ['interna', 'external', 'dual', 'chop']})

        self.add_device_property({
            'name': 'reference_trigger_mode',
            'write_string': 'RTRG {}',
            'query_string': 'RTRG?',
            'indexed_values': ['sine', 'positive', 'negative']})

        self.add_device_property({
            'name': 'reference_impedance',
            'write_string': 'REFZ {}',
            'query_string': 'REFZ?',
            'indexed_values': [50, 1e6]})

        # Signal Commands
        self.add_device_property({
            'name': 'signal_input',
            'write_string': 'IVMD {}',
            'query_string': 'IVMD?',
            'indexed_values': ['voltage', 'current']})

        self.add_device_property({
            'name': 'voltage_input_mode',
            'write_string': 'ISRC {}',
            'query_string': 'ISRC?',
            'indexed_values': ['A', 'A-B']})

        self.add_device_property({
            'name': 'voltage_input_coupling',
            'write_string': 'ICPL {}',
            'query_string': 'ICPL?',
            'indexed_values': ['ac', 'dc']})

        self.add_device_property({
            'name': 'voltage_input_shield',
            'write_string': 'IGND {}',
            'query_string': 'IGND?',
            'indexed_values': ['float', 'ground']})

        self.add_device_property({
            'name': 'voltage_input_range',
            'write_string': 'IRNG {}',
            'query_string': 'IRNG?',
            'indexed_values': [1, 0.3, 0.1, 0.03, 0.01],
            'return_type': float})

        self.add_device_property({
            'name': 'current_input_impedance',
            'write_string': 'ICUR {}',
            'query_string': 'ICUR?',
            'indexed_values': [1, 100],
            'return_type': int})

        self.add_device_property({
            'name': 'signal_strength',
            'query_string': 'ILVL?',
            'read_only': True,
            'return_type': int})

        self.add_device_property({
            'name': 'voltage_sensitivity',
            'write_string': 'SCAL {}',
            'query_string': 'SCAL?',
            'indexed_values': [
                1, 0.5, 0.2, 0.1,
                0.05, 0.02, 0.01, 0.005, 0.002, 0.001,
                5e-4, 2e-4, 1e-4, 5e-5, 2e-5, 1e-5,
                5e-6, 2e-6, 1e-6, 5e-7, 2e-7, 1e-7,
                5e-8, 2e-8, 1e-8, 5e-9, 2e-9, 1e-9],
            'return_type': int})

        self.add_device_property({
            'name': 'time_constant',
            'write_string': 'OFLT {}',
            'query_string': 'OFLT?',
            'indexed_values': [
                1e-6, 3e-6, 1e-5, 3e-5, 1e-4, 3e-4,
                1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3,
                1, 3, 10, 30, 100, 300, 1e3, 3e3, 10e3, 30e3]})

        self.add_device_property({
            'name': 'filter_slope',
            'write_string': 'OFSL {}',
            'query_string': 'OFSL?',
            'indexed_values': [6, 12, 18, 24]})

        self.add_device_property({
            'name': 'synchronous_filter',
            'write_string': 'SYNC {}',
            'query_string': 'SYNC?',
            'indexed_values': ["off", "on"]})

        self.add_device_property({
            'name': 'advanced_filter',
            'write_string': 'ADVFILT {}',
            'query_string': 'ADVFILT?',
            'indexed_values': ["off", "on"]})

        self.add_device_property({
            'name': 'equivalent_bandwidth',
            'query_string': 'ENBW?',
            'read_only': True,
            'return_type': float})

        # Output Commands
        self.add_device_property({
            'name': 'channel_1_output',
            'write_string': 'COUT 0, {}',
            'query_string': 'COUT? 0',
            'indexed_values': ["x", "r"]})

        self.add_device_property({
            'name': 'channel_2_output',
            'write_string': 'COUT 1, {}',
            'query_string': 'COUT? 1',
            'indexed_values': ["y", "theta"]})

        for source, i in zip(['x', 'y', 'r'], [0, 1, 2]):
            self.add_device_property({
                'name': f'{source}_expand',
                'write_string': f'CEXP {i}, {"{}"}',
                'query_string': f'CEXP? {i}',
                'indexed_values': ["off", "10x", "100x"]})

        for source, i in zip(['x', 'y', 'r'], [0, 1, 2]):
            self.add_device_property({
                'name': f'{source}_offset_state',
                'write_string': f'COFA {i}, {"{}"}',
                'query_string': f'COFA? {i}',
                'indexed_values': ["off", "on"]})

        for source, i in zip(['x', 'y', 'r'], [0, 1, 2]):
            self.add_device_property({
                'name': f'{source}_offset_percent',
                'write_string': f'COFP {i}, {"{}"}',
                'query_string': f'COFP? {i}',
                'range': [-999.99, 999.99],
                'return_type': float})

        for source, i in zip(['x', 'y', 'r'], [0, 1, 2]):
            self.add_device_property({
                'name': f'{source}_ratio_state',
                'write_string': f'CRAT {i}, {"{}"}',
                'query_string': f'CRAT? {i}',
                'indexed_values': ['off', 'on']})

        # Auxiliary Input/Output
        for i in range(4):
            self.add_device_property({
                'name': f'auxiliary_input_voltage_{i + 1}',
                'read_only': True,
                'query_string': f'OAUX? {i}',
                'range': [-10.5, 10.5],
                'return_type': float})

        for i in range(4):
            self.add_device_property({
                'name': f'auxiliary_output_voltage_{i + 1}',
                'write_string': f'AUXV, {i}, {"{}"}',
                'query_string': f'AUXV? {i}',
                'range': [-10.5, 10.5],
                'return_type': float})

    def auto_phase(self):
        '''
        Automatically sets the phase of the detection
        '''
        self.write('APHS')
        sleep(0.1)
        self.phase

    def auto_offset(self, source):
        '''
        Automatically sets the offset for a channel so that it is zeroed

        Parmeters
        ---------
        source : str
            Channel source to be offset "x", "y", or "r"

        Returns
        -------
        None
        '''

        sources = ['x', 'y', 'r']
        assert source in sources, 'Invalid source, must be "x", "y", or "r"'

        index = sources.index(source)

        self.write(f"OUAT {index}")
        sleep(0.1)
        getattr(self, source + '_offset_percent')

    def auto_range(self):
        '''
        Automatically sets input range of the detection
        '''
        self.write('ARNG')
        sleep(0.1)
        self.voltage_input_range

    def auto_scale(self):
        '''
        Automatically sets sensitivity of the detection
        '''
        self.write('ASCL')
        sleep(0.1)
        self.voltage_sensitivity

    def read_channel(self, channel):
        '''
        Reads and returns the value for channel 1-4

        Parameters
        ----------
        channel : int
            The channel to be read, from 1-4

        Returns
        -------
        float
            The read value
        '''

        channels = list(range(1, 5))

        assert channel in channels, 'Invalid input: Channel can be "1", "2", "3", or "4"'

        value = self.query(f'OUTR?  {channel - 1}').strip('\n')

        return float(value)

    def read(self, parameter):
        '''
        Reads and returns a single paramter from the lockin

        Parameters
        ----------
        parameter : str
            The paramter to be read, with options:
            "x", "y", "r", "theta", "aux_in_1", "aux_in_2", "aux_in_3", "aux_in_4",
            "x_noise", "y_noise", "aux_out_1", "aux_out_2", "phase"
            "amplitude", "dc_offset", "internal_frequency", "external_frequency"

        Returns
        -------
        float
            The read value
        '''

        parameters = [
            "x", "y", "r", "theta", "aux_in_1", "aux_in_2", "aux_in_3", "aux_in_4",
            "x_noise", "y_noise", "aux_out_1", "aux_out_2", "phase"
            "amplitude", "dc_offset", "internal_frequency", "external_frequency"]

        assert parameter in parameters, 'Invalid input: see doc string for valid inputs'

        value = self.query(f'OUTP?  {parameters.index(parameter)}').strip('\n')

        return float(value)

    def snap(self, *args):
        '''
        Simultaniously queryes 2 to 3 different values from the instrument

        Parameters
        ----------
        2 to 3 args: str
            "x", "y", "r", "theta", "aux_in_1", "aux_in_2", "aux_in_3", "aux_in_4",
            "x_noise", "y_noise", "aux_out_1", "aux_out_2", "phase"
            "amplitude", "dc_offset", "internal_frequency", "external_frequency"

        Returns
        -------
        2 to 3 float values
            phase will be returned in degrees
        '''

        parameters = [
            "x", "y", "r", "theta", "aux_in_1", "aux_in_2", "aux_in_3", "aux_in_4",
            "x_noise", "y_noise", "aux_out_1", "aux_out_2", "phase"
            "amplitude", "dc_offset", "internal_frequency", "external_frequency"]

        assert (len(args) >= 2) and (len(args) <= 6), 'Snap accepts 2 to 6 readable sources'

        for parameter in args:
            assert parameter in parameters, (
                f"{parameter} is an invalid input: see doc string for valid inputs")

        indicies = [str(parameters.index(arg) + 1) for arg in args]
        query_string = 'SNAP? ' + ', '.join(indicies)
        responses = self.query(query_string).strip('\n')

        responses = responses.split(',')
        formatted_response = []
        for response, parameter, in zip(responses, args):
            if parameter != 'theta':
                formatted_response.append(float(response))
            else:
                formatted_response.append(float(response) * 180 / 3.14159)

        return formatted_response

    def snap_display(self):
        ''''
        Returns the four display values all at once

        Parameters
        ----------
        None

        Returns
        -------
        [float, float, float, float]
        '''

        response = self.query('SNAPD?').strip('\n')
        response = response.split(',')
        response = [float(r) for r in response]

        return response

    # Display Methods

    def screen_cap(self):
        '''
        Takes a screen cap and saves it on a USB memory stick
        '''
        self.write('DCAP')

    def set_display_parameter(self, display, parameter):
        '''
        Assigns a parameter to a display 1-4

        Parameters
        ----------
        display : int
            Display number 1-4
        parameter : str
            Parameter to be displayed with options
            "x", "y", "r", "theta", "aux_in_1", "aux_in_2", "aux_in_3", "aux_in_4",
            "x_noise", "y_noise", "aux_out_1", "aux_out_2", "phase"
            "amplitude", "dc_offset", "internal_frequency", "external_frequency"
        '''

        displays = [1, 2, 3, 4]
        parameters = [
            "x", "y", "r", "theta", "aux_in_1", "aux_in_2", "aux_in_3", "aux_in_4",
            "x_noise", "y_noise", "aux_out_1", "aux_out_2", "phase"
            "amplitude", "dc_offset", "internal_frequency", "external_frequency"]

        assert display in displays, f"{display} is invalid: use 1-4"
        assert parameter in parameters, f"{parameter} is in valid see docstring for valid parameters"

        self.write(f'CDSP {displays.index(display)}, {parameters.index(parameter)}')

        setattr(self, f'_display_{display}_parameter', parameter)

    def get_display_parameter(self, display, parameter):
        '''
        Gets a parameter assigned to display 1-4

        Parameters
        ----------
        display : int
            Display number 1-4

        Returns
        -------
        str
            Parameter which is being displayed
        '''

        displays = [1, 2, 3, 4]
        parameters = [
            "x", "y", "r", "theta", "aux_in_1", "aux_in_2", "aux_in_3", "aux_in_4",
            "x_noise", "y_noise", "aux_out_1", "aux_out_2", "phase"
            "amplitude", "dc_offset", "internal_frequency", "external_frequency"]

        assert display in displays, f"{display} is invalid: use 1-4"
        assert parameter in parameters, f"{parameter} is in valid see docstring for valid parameters"

        setattr(
            self, f'_display_{display}_parameter',
            self.query(f'CDSP? {display}').strip('\n'))

        return getattr(self, f'_display_{display}_parameter',)
