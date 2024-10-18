# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver
import numpy as np
from time import sleep


class Stanford830(InstrumentDriver):
    '''
    Class to control Stanford Research Systems SR830 DSP Dual Phase Lock-In Amplifier

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    id : read-only
        Gets the id string of the device.
    phase : float
        Gets/sets the phase of the device. Range: [-180, 180]
    reference_source : str
        Get/sets the reference source. Indexed_values: ['external', 'internal'].
    frequency : float
        Gets/sets/ the frequency. Range: [0.001, 102000]
    reference_slope : int
        Gets/sets the slope of the frequency refeference.
        Indexed_values: ['sine zero', 'ttl rising', 'ttl falling'].
    harmonic : int
        Gets/sets the demodulation harmonic. Range: [1, 19999]
    amplitude : float
        Gets/sets the output amplitude. Range: [0.004, 5.0]
    input_configuration : str
        Gets/sets the analog input mode.
        Indexed_values:  ['A', 'A-B', 'Ie6', 'Ie8'].
    input_ground : str
        Get/sets the input ground.
        Indexed_values: ['AC', 'DC']
    input_coupling : str
        Gets/sets the input coupling.
        Indexed_values: ['AC', 'DC']
    input_line_filter : str
        Gets/sets the line filer of the input.
        Indexed_values: ['none', 'line', '2xline', 'both']
    sensitivity : float
        Gets/sets the sensitivy (max input).
        Indexed_values:  [2e-9, 5e-9, 10e-9, 20e-9, 50e-5,
                            100e-9, 200e-9, 500e-9,
                            1e-6, 2e-6, 5e-6,
                            10e-6, 20e-6, 50e-6,
                            100e-6, 200e-6, 500e-6,
                            1e-3, 2e-3, 5e-3,
                            10e-3, 20e-3, 50e-3,
                            100e-3, 200e-3, 500e-3,
                            1]
    reserve_mode : str
        Gets/sets the dynamic reserver
        Indexed_values:  ['high', 'normal', 'low']
    time_constant : float
        Gets/sets the time constant in seconds
        Indexed_values:  [10e-6, 30e-6, 100e-6, 300e-6,
                            1e-3, 3e-3, 10e-3, 30e-3, 100e-3,
                            300e-3,
                            1, 3, 10, 30, 100, 300, 1000, 3000,
                            10000, 30000]
    filter_slope : int
        Gets/sets the slope of the filter in dB/oct
        Indexed_values:  [6, 12, 18, 24]
    synchronous_filter : str
        Gets/sets the synchronous filter state
        Indexed_values:  ['off', 'on']
    display1_output_source : str
        Gets/sets the displayed source on display 1
        Indexed values ['x', 'display']
    display2_output_source : str
        Gets/sets the displayed source on display 2
        Indexed values['y', 'display']
    auxiliary_voltage1 : float
        Gets/sets the channel 1 auxiliary output voltage
        range - [-10.5, 10.500]
    auxiliary_voltage2 : float
        Gets/sets the channel 2 auxiliary output voltage
        range - [-10.5, 10.500]
    auxiliary_voltage3 : float
        Gets/sets the channel 3 auxiliary output voltage
        range - [-10.5, 10.500]
    auxiliary_voltage4 : float
        Gets/sets the channel 4 auxiliary output voltage
        range - [-10.5, 10.500]
    sample_rate : float
        Get/sets the sample rate in Hz
        Indexed_values:  [0.0625, .125, .250, .5, 1,
                                    2, 4, 8,
                                    16, 32, 64, 128,
                                    256, 512, 'trigger']
    end_buffer_mode : str
        Gets/sets the end mode for th data buffer
        Indexed_values: ['one shot', 'loop']
    trigger_mode : int
        Gets/sets the trigger mode state
        Indexed_values':  ['off', 'on']
    buffer_points : read-only
        Gets the number of points stored in the buffer.

    Methods
    -------
    get_display(display_number)
    set_display(display_number, source, ratio)
    get_channel_offset_expand(channel)
    set_channel_offset_expand(channel, offset, expand)
    read_aux_input(index)
    auto_gain()
    auto_reserve()
    auto_phase()
    auto_offset()
    trigger()
    start()
    pause()
    reset()
    read(source)
    read_display(display)
    snap(*args)
    read_ascii_buffer()
    read_binary_buffer()
    reset_to_default_settings()
    clear_status_bytes()
    set_buffer_mode(sample_rate)
    wait_for_trigger()
    snap_xy()

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self._version = "1.0.3"

        self.black_list_for_testing = [
            '_input_configuration',
            "_time_constant",
            "_amplitude",
            "_sensitivity"]

        self.initialize_properties()
        self.update_properties()

    def initialize_properties(self):

        # Reference and Phase properties

        self.add_device_property({
            'name': 'id',
            'query_string': '*IDN?',
            'read_only': True,
            'return_type': str})

        self.add_device_property({
            'name': 'phase',
            'write_string': 'PHAS {}',
            'query_string': 'PHAS?',
            'range': [-180, 180],
            'return_type': float})

        self.add_device_property({
            'name': 'reference_source',
            'write_string': 'FMOD {}',
            'query_string': 'FMOD?',
            'indexed_values': ['external', 'internal'],
            'return_type': int})

        self.add_device_property({
            'name': 'frequency',
            'write_string': 'FREQ {}',
            'query_string': 'FREQ?',
            'range': [0.001, 102000],
            'return_type': float})

        self.add_device_property({
            'name': 'reference_slope',
            'write_string': 'RSLP {}',
            'query_string': 'RSLP?',
            'indexed_values': ['sine zero', 'ttl rising', 'ttl falling'],
            'return_type': float})

        self.add_device_property({
            'name': 'harmonic',
            'write_string': 'HARM {}',
            'query_string': 'HARM?',
            'range': [1, 19999],
            'return_type': int})

        self.add_device_property({
            'name': 'amplitude',
            'write_string': 'SLVL {}',
            'query_string': 'SLVL?',
            'range': [0.004, 5.0],
            'return_type': float})

        # Input and Filter Properties:

        self.add_device_property({
            'name': 'input_configuration',
            'write_string': 'ISRC {}',
            'query_string': 'ISRC?',
            'indexed_values': ['A', 'A-B', 'Ie6', 'Ie8'],
            'return_type': int})

        self.add_device_property({
            'name': 'input_ground',
            'write_string': 'IGND {}',
            'query_string': 'IGND?',
            'indexed_values': ['AC', 'DC'],
            'return_type': int})

        self.add_device_property({
            'name': 'input_coupling',
            'write_string': 'ICPL {}',
            'query_string': 'ICPL?',
            'indexed_values': ['AC', 'DC'],
            'return_type': int})

        self.add_device_property({
            'name': 'input_line_filter',
            'write_string': 'ILIN {}',
            'query_string': 'ILIN?',
            'indexed_values': ['none', 'line', '2xline', 'both'],
            'return_type': int})

        # Gain and Time Constant

        self.add_device_property({
            'name': 'sensitivity',
            'write_string': 'SENS {}',
            'query_string': 'SENS?',
            'indexed_values': [
                2e-9, 5e-9,
                10e-9, 20e-9, 50e-9,
                100e-9, 200e-9, 500e-9,
                1e-6, 2e-6, 5e-6,
                10e-6, 20e-6, 50e-6,
                100e-6, 200e-6, 500e-6,
                1e-3, 2e-3, 5e-3,
                10e-3, 20e-3, 50e-3,
                100e-3, 200e-3, 500e-3,
                1],
            'return_type': int})

        self.add_device_property({
            'name': 'reserve_mode',
            'write_string': 'RMOD {}',
            'query_string': 'RMOD?',
            'indexed_values': ['high', 'normal', 'low'],
            'return_type': int})

        self.add_device_property({
            'name': 'time_constant',
            'write_string': 'OFLT {}',
            'query_string': 'OFLT?',
            'indexed_values': [
                10e-6, 30e-6, 100e-6, 300e-6,
                1e-3, 3e-3, 10e-3, 30e-3, 100e-3,
                300e-3,
                1, 3, 10, 30, 100, 300, 1000, 3000,
                10000, 30000],
            'return_type': int})

        self.add_device_property({
            'name': 'filter_slope',
            'write_string': 'OFSL {}',
            'query_string': 'OFSL?',
            'indexed_values': [6, 12, 18, 24],
            'return_type': int})

        self.add_device_property({
            'name': 'synchronous_filter',
            'write_string': 'SYNC {}',
            'query_string': 'SYNC?',
            'dict_values': {'off': 0, 'on': 1, '0': 0, '1': 1, 0: 0, 1: 1},
            'return_type': int})

        # Display and Output Properties:

        self.add_device_property({
            'name': 'display1_output_source',
            'write_string': 'FPOP 1, {}',
            'query_string': 'FPOP? 1',
            'indexed_values': ['x', 'display'],
            'return_type': int})

        self.add_device_property({
            'name': 'display2_output_source',
            'write_string': 'FPOP 2, {}',
            'query_string': 'FPOP? 2',
            'indexed_values': ['y', 'display'],
            'return_type': int})

        # auxiliary Input/Ouput Properties

        self.add_device_property({
            'name': 'auxiliary_voltage1',
            'write_string': 'AUXV 1, {}',
            'query_string': 'AUXV? 1',
            'range': [-10.5, 10.500],
            'return_type': float})

        self.add_device_property({
            'name': 'auxiliary_voltage2',
            'write_string': 'AUXV 2, {}',
            'query_string': 'AUXV? 2',
            'range': [-10.5, 10.500],
            'return_type': float})

        self.add_device_property({
            'name': 'auxiliary_voltage3',
            'write_string': 'AUXV 3, {}',
            'query_string': 'AUXV? 3',
            'range': [-10.5, 10.500],
            'return_type': float})

        self.add_device_property({
            'name': 'auxiliary_voltage4',
            'write_string': 'AUXV 4, {}',
            'query_string': 'AUXV? 4',
            'range': [-10.5, 10.500],
            'return_type': float})

        # Data Storgae Properties

        self.add_device_property({
            'name': 'sample_rate',
            'write_string': 'SRAT {}',
            'query_string': 'SRAT?',
            'indexed_values': [
                0.0625, .125, .250, .5, 1,
                2, 4, 8,
                16, 32, 64, 128,
                256, 512, 'trigger'],
            'return_type': int})

        self.add_device_property({
            'name': 'end_buffer_mode',
            'write_string': 'SEND {}',
            'query_string': 'SEND?',
            'indexed_values': ['one shot', 'loop'],
            'return_type': int})

        self.add_device_property({
            'name': 'trigger_mode',
            'write_string': 'TSTR {}',
            'query_string': 'TSTR?',
            'dict_values': {'off': 0, 'on': 1, '0': 0, '1': 1, 0: 0, 1: 1},
            'return_type': int})

        self.add_device_property({
            'name': 'buffer_points',
            'query_string': 'SPTS?',
            'read_only': True,
            'return_type': int})

    # Display and Output Methods
    def get_display(self, display_number):
        '''
        Gets the source and ratio for a display

        Parameters
        ----------
        display_number: int
            Display for which to get the source and ratio

        Returns
        -------
        str - source being displayed
        str - value which the source is being devided by
        '''
        assert display_number in [1, 2], 'Display must be either 1 or 2'

        if display_number == 1:
            sources = ['x', 'r', 'xn', 'aux1', 'aux2']
            ratios = ['none', 'aux1', 'aux2']
        else:
            sources = ['y', 'theta', 'yn', 'aux3', 'aux4']
            ratios = ['none', 'aux3', 'aux4']

        response = self.query('DDEF? {}'.format(display_number)).strip('\n')
        response = response.split(',')
        response = [int(r) for r in response]

        return sources[response[0]], ratios[response[1]]

    def set_display(self, display_number, source, ratio):
        '''
        Sets the source and ratio paramter for a display

        Paremeters
        -----------
        display_number: int
            Display for which to set the source and ratio
        source: str
            The source to be displayed
            display 1: x, r, xn, aux1, aux2
            display 2: y, theta, yn, aux3, aux4
        ratio: str
            Data source to divide the main data source by
            display1: none, aux1, aux2
            display2: none, aux3, aux4
        '''

        assert display_number in [1, 2], 'Display must be either 1 or 2'
        if display_number == 1:
            sources = ['x', 'r', 'xn', 'aux1', 'aux2']
            ratios = ['none', 'aux1', 'aux2']
        else:
            sources = ['y', 'theta', 'yn', 'aux3', 'aux4']
            ratios = ['none', 'aux3', 'aux4']

        assert source in sources, 'Source must be ' + (', '.join(sources))
        assert ratio in ratios, 'Ratio must be ' + (', '.join(ratios))

        index1 = sources.index(source)
        index2 = ratios.index(ratio)

        self.write('DDEF {}, {}, {}'.format(display_number, index1, index2))

    def get_channel_offset_expand(self, channel):
        '''
        Queries the offset and expand for a channel

        Parameters
        ----------
        channel: int
            The channl to query: 1 or 2

        Returns
        --------
        float
            The percent offset of the total range given by the sensitivity
        int
            The value of the expand setting, 1, 10, or 100

        '''
        # expand_values = [1, 10, 100]

        response = self.query('OEXP? {}'.format(channel)).strip('\n')
        response = response.split(',')

        setattr(self, '_channel{}_offset', response[0])
        setattr(self, '_channel{}_expand', response[1])

        return response

    def set_channel_offset_expand(self, channel, offset, expand):
        '''
        Sets the offset and expand for a channel

        Parameters
        ----------
        channel: int
            Channel to set values for: 1 or 2
        offset: float
            Percent offset for specified channel in percent
            -105 to 105
        expand: int
            The gain of the channel to digitize with more accuracy
            Can be 1, 10, or 100

        '''

        expand_values = [1, 10, 100]

        assert channel in [1, 2], 'channel must be 1 or 2'
        assert (offset >= -105) and (offset <= 105), 'Offset must be between -105 and 105 in units of percent'
        assert expand in expand_values, 'Expand in put must be 1, 10, or 100'

        index = expand_values.index(expand)

        self.write('OEXP {}, {}, {}'.format(channel, offset, index))

    # auxiliary Input/Ouptut Methods

    def read_aux_input(self, index):
        '''
        Reads the voltage input to an auxiliary input channel

        Parameters
        ----------
        index: int
            auxiliary input channel number 1, 2, 3, or 4
        '''

        indicies = [1, 2, 3, 4]
        assert index in indicies, 'auxiliary input index must be 1, 2, 3, or 4'

        return float(self.query('OAUX ? {}'.format(index)))

    # Auto Functions

    def auto_gain(self):
        '''
        Automatically sets the gain of the singal input
        '''

        self.write('AGAN')

    def auto_reserve(self):
        '''
        Automatically sets the reserve based on instruments settings
        and data values
        '''

        self.write('ARSV')
        sleep(1)
        self.reserve_mode

    def auto_phase(self):
        '''
        Automatically sets the instrument phase
        '''

        self.write('APHS')
        sleep(1)
        self.phase

    def auto_offset(self, source):
        '''
        Automatically sets the offset to the current value of the
        data source

        Parameters
        -----------
        source: str
            Data source for auto offset to be applided
            Can be x, y, or r

        '''

        sources = ['x', 'y', 'r']

        assert source in sources, 'Auto Offset source must be x, y, or r'

        index = sources.index(source) + 1

        self.write('AOFF {}'.format(index))

    # Data storage methods
    def trigger(self):
        '''
        Executes a software trigger
        '''
        self.write('TRIG')

    def start(self):
        '''
        Starts buffer data accumulation
        '''
        self.write('STRT')

    def pause(self):
        '''
        Pauses buffer data accumulation
        '''
        self.write('PAUS')

    def reset(self):
        '''
        Resets the data buffer, deleting all data
        '''
        self.write('REST')

    # Data transfer methods

    def read(self, source):
        '''
        Reads the value from a single source

        Parameters
        ----------
        source: str
            Source to be read from. Can be x, y, r, theta

        Returns
        float
            Value read, theta is retuned in degrees

        '''

        sources = ['x', 'y', 'r', 'theta']

        assert source in sources, 'Readable values are x, y, z, and theta'

        index = sources.index(source) + 1
        if source in ['x', 'y', 'r']:
            return (float(self.query('OUTP? {}'.format(index))))
        else:
            return (float(self.query('OUTP? {}'.format(index)))
                    * 180 / 3.14159)

    def read_display(self, display):
        '''
        Read the value on the display

        Parameters
        ---------
        display: int
            Indicates which display to read: 1 or 2

        Returns
        -------
        float
            value read from display

        '''
        displays = [1, 2]

        assert display in displays, 'Readable displayas are 1 or 2'

        return float(self.query('OUTR? {}'.format(display).strip('\n')))

    def snap(self, *args):
        '''
        Simultaniously queryes 2 to 6 different values from the instrument

        Parameters
        ----------
        2 to 6 args: str
            must be x, y, r, theta, aux1, aux2, aux3, aux4,
            frequency, display1, or display2

        Returns
        2 to 6 float values
            phase will be returned in degrees

        '''

        sources = ['x', 'y', 'r', 'theta', 'aux1', 'aux2', 'aux3',
                   'aux4', 'frequency', 'display1', 'display2']

        assert (len(args) >= 2) and (len(args) <= 6), 'Snap accepts 2 to 6 readable sources'

        for source in args:
            assert source in sources, (
                'Readable sources include x, y, r, theta, aux1, aux2, aux3, aux4, frequency, display1, display2')

        indicies = [str(sources.index(arg) + 1) for arg in args]
        query_string = 'SNAP? ' + ', '.join(indicies)
        responses = self.query(query_string).strip('\n')

        responses = responses.split(',')
        formatted_response = []
        for response, source, in zip(responses, args):
            if source != 'theta':
                formatted_response.append(float(response))
            else:
                formatted_response.append(float(response) * 180 / 3.14159)

        return formatted_response

    @property
    def bufferpoints(self):
        '''
        Property returning the number of buffer points. Read-only
        '''

        return int(self.query('SPTS?'))

    def read_ascii_buffer(self, channel, start, points):
        '''
        Read the values of the lock-in buffer streamed as ascii.

        Parameters
        ----------
        channel : int
            either 1 (x-channel) or 2 (y-channel)
        start : int
            initial point to read.  First buffer point is 0
        points : int
            number of points to read
        '''

        assert channel in [1, 2], 'Channel must be 1 or 2 '

        values = self.insturment.query_ascii_values(
            'TRCA? {}, {}, {}'.format(channel, start, points))

        return np.array(values).astype(float)

    def read_binary_buffer(self, channel, start, points):
        '''
        Read the values of the lock-in binary buffer.

        Parameters
        ----------
        channel : int
            either 1 (x-channel) or 2 (y-channel)
        start : int
            initial point to read.  First buffer point is 0
        points : int
            number of points to read
        '''

        assert channel in [1, 2], 'Channel must be 1 or 2 '

        values = self.instrument.query_binary_values(
            'TRCB? {}, {}, {}'.format(channel, start, points),
            datatype=u'f', header_fmt='empty')

        return np.array(values)

    # Interface Methods

    def reset_to_default_settings(self):
        '''
        Resets the instrument settings to default
        '''
        self.write('*RST')
        sleep(1)
        self.update_properties()

    def get_identificaiton_string(self):
        '''
        Gets the identification string
        '''
        return self.query('*IDN?').strip('\n')

    # Status Methods

    def clear_status_bytes(self):
        '''
        Clears all status bytes
        '''
        self.write('*CLS')

    # Custom Multi-Settings Methods

    def set_buffer_mode(self, sample_rate):
        '''
        Commands to prepare to use the lock-in buffer.  The buffer is paused
        and reset.

        Parameters
        ----------
        sample_rate :
            buffer sample rate
        '''

        self.pause()

        self.sample_rate = sample_rate
        self.trigger_mode = 'on'
        self.buffer_mode = 'off'
        self.reset()

    def wait_for_trigger(self):
        '''
        Pauses the buffer accumulation then resets the buffer
        '''

        self.pause()

        self.reset()

    def snap_xy(self):
        '''
        Shortcut to just snap the x and y data

        Returns
        -------
        [float, float]
            array of two values that are the currently read x and y values
        '''

        return self.snap('x', 'y')

    # Get noise is depreciated, nees to be reworekd

    # def get_x_values(self, N=128, sample_rate=None):
    #     '''
    #     Using the binary buffer, read a set of in-phase values from the lockin.

    #     Parameters
    #     ----------
    #     N : int, optional
    #         Number of values to read. Defaults to 128.
    #     sample_rate : optional
    #         sample rate. Defaults to None, which results in existing sample rate being used.
    #     '''

    #     sample_rate_initial = self.sample_rate
    #     if sample_rate is not None:
    #         self.sample_rate = sample_rate

    #     self.pause()
    #     self.reset()
    #     sleep(0.01)
    #     wait_time = N / self.sample_rate
    #     self.start()
    #     sleep(wait_time)
    #     self.pause()
    #     n_points = self.bufferpoints

    #     # channel 1 is x
    #     values = self.read_binary_buffer(1, 0, n_points)

    #     if n_points > N:
    #         values = values[:N]

    #     # return the sample rate to the original value
    #     self.sample_rate = sample_rate_initial

    #     return values

    # def get_noise(self, gain=1, normalized=False, N=25):
    #     '''
    #     Return the in-phase noise using N points.

    #     Parameters
    #     ----------
    #     gain : optional
    #         prefactor to account for pre-amplification chain. Defaults to 1.
    #     normalized : bool, optional
    #         noise returned as voltage (False) or voltage/rtHz (True). Defaults to False.
    #     N : int, optional
    #         number of points to use to calculate noise. Defaults to 25.
    #     '''

    #     tc = self.time_constant
    #     slope = self.filter_slope
    #     # set the sample rate so that points are independent
    #     wait_dict = {6: 5 * tc, 12: 7 * tc, 18: 9 * tc, 24: 10 * tc}
    #     bw_dict = {6: 1 / (4 * tc), 12: 1 / (8 * tc), 18: 3 / (32 * tc), 24: 5 / (64 * tc)}

    #     available_rates = self.sample_rate_['values'][:-2]
    #     sample_rate = available_rates[
    #         np.bisect_left(available_rates, 1 / wait_dict[slope])]

    #     data = self.get_x_values(N=N, sample_rate=sample_rate) / gain

    #     v_noise = data.std()
    #     if normalized:
    #         v_noise /= np.sqrt(bw_dict[slope])

    #     return v_noise
