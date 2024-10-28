# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver
import re
from ...general.d_range import drange
import numpy as np


class Agilent33500(InstrumentDriver):
    '''
    Class to control Agilent33500 Arbitrary waveform generator.

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument
    channel : int
        channel of instrument, 1 or 2

    Attributes
    ----------
    gain :
        multiplication factor for voltages at the device, defaults to 1.
    channel :
        Channel instrument is running on
    debug : bool
        Defaults to False
    (Properties)
    frequency : float
        sets/queries instrument frequency. Range: [0.001, 30e6]
    instrument_amplitude : float
        set/queries amplitude output. Range: [-10, 10]
    instrument_voltage : float
        set/queries voltage. Range: [-10, 10]
    voltage_autorange : str or int
        sets/querqies voltage autoranging. Values: [0, 'off', 1, 'on'], returns str
    function : str
        sets/queries instrument function. Values:  ["SIN","SQU","TRI","RAMP","PULS","PRBS","NOIS","ARB","DC",]
    arb_advance_mode : str
        sets/queries Advancement method for arbitrary waveforms. Values: ["TRIG", "SRAT"]
    arb_filter : str
        Values: ["NORM", "STEP", "OFF"]
    arb_sample_rate : float
        Range: [1e-6, 250e6]
    burst_mode : str
        Values: ['TRIG', 'GAT']
    burst_cycles : float
        Range: [1, 10000]
    burst_state : str or int
        Values: [0, 'Off', 1, 'ON'], returns str
    output : str
        Values: [0, 'Off', 1, 'ON'], returns str
    output_load : float or str
        Values: [50, 'INF'], returns float
    trigger_source : str
        Values: ["IMM", "EXT", "TIM", "BUS"]

    '''

    def __init__(self, instrument, channel):

        super().__init__(instrument)

        assert channel in [1, 2], 'Only channels 1 or 2 are allowed'
        self.channel = channel

        self.gain = 1
        self._version = "0.1.0"

        self.debug = False
        self.initialize_properties()

    def initialize_properties(self):

        self.add_device_property({
            'name': 'frequency_chan1',
            'write_string': 'SOUR1:FREQ {}',
            'query_string': 'SOUR1:FREQ?',
            'range': [0.001, 30e6],
            'return_type': float})

        self.add_device_property({
            'name': 'frequency_chan2',
            'write_string': 'SOUR2:FREQ {}',
            'query_string': 'SOUR2:FREQ?',
            'range': [0.001, 30e6],
            'return_type': float})

        self.add_device_property({
            'name': 'instrument_amplitude_chan1',
            'write_string': 'SOUR1:VOLT {}',
            'query_string': 'SOUR1:VOLT?',
            'range': [-10, 10],
            'return_type': float})

        self.add_device_property({
            'name': 'instrument_amplitude_chan2',
            'write_string': 'SOUR2:VOLT {}',
            'query_string': 'SOUR2:VOLT?',
            'range': [-10, 10],
            'return_type': float})

        self.add_device_property({
            'name': 'instrument_voltage_chan1',
            'write_string': 'SOUR1:VOLT:OFFS {}',
            'query_string': 'SOUR1:VOLT:OFFS?',
            'range': [-10, 10],
            'return_type': float})

        self.add_device_property({
            'name': 'instrument_voltage_chan2',
            'write_string': 'SOUR2:VOLT:OFFS {}',
            'query_string': 'SOUR2:VOLT:OFFS?',
            'range': [-10, 10],
            'return_type': float})

        self.add_device_property({
            'name': 'voltage_autorange_chan1',
            'write_string': 'SOUR1:VOLT:RANG:AUTO {}',
            'query_string': 'SOUR1:VOLT:RANG:AUTO?',
            'values': [0, 'off', 1, 'on'],
            'return_type': str})

        self.add_device_property({
            'name': 'voltage_autorange_chan2',
            'write_string': 'SOUR2:VOLT:RANG:AUTO {}',
            'query_string': 'SOUR2:VOLT:RANG:AUTO?',
            'values': [0, 'off', 1, 'on'],
            'return_type': str})

        self.add_device_property({
            'name': 'function_chan1',
            'write_string': 'SOUR1:FUNC {}',
            'query_string': 'SOUR1:FUNC?',
            'values': [
                "SIN",
                "SQU",
                "TRI",
                "RAMP",
                "PULS",
                "PRBS",
                "NOIS",
                "ARB",
                "DC", ],
            'return_type': str})

        self.add_device_property({
            'name': 'function_chan2',
            'write_string': 'SOUR2:FUNC {}',
            'query_string': 'SOUR2:FUNC?',
            'values': [
                "SIN",
                "SQU",
                "TRI",
                "RAMP",
                "PULS",
                "PRBS",
                "NOIS",
                "ARB",
                "DC", ],
            'return_type': str})

        self.add_device_property({
            'name': 'arb_advance_mode_chan1',
            'write_string': 'SOUR1:FUNC:ARB:ADV {}',
            'query_string': 'SOUR1:FUNC:ARB:ADV?',
            'values': ["TRIG", "SRAT"],
            'return_type': str})

        self.add_device_property({
            'name': 'arb_advance_mode_chan2',
            'write_string': 'SOUR2:FUNC:ARB:ADV {}',
            'query_string': 'SOUR2:FUNC:ARB:ADV?',
            'values': ["TRIG", "SRAT"],
            'return_type': str})

        self.add_device_property({
            'name': 'arb_filter_chan1',
            'write_string': 'SOUR1:FUNC:ARB:FILT {}',
            'query_string': 'SOUR1:FUNC:ARB:FILT?',
            'values': ["NORM", "STEP", "OFF"],
            'return_type': str})

        self.add_device_property({
            'name': 'arb_filter_chan2',
            'write_string': 'SOUR2:FUNC:ARB:FILT {}',
            'query_string': 'SOUR2:FUNC:ARB:FILT?',
            'values': ["NORM", "STEP", "OFF"],
            'return_type': str})

        self.add_device_property({
            'name': 'arb_sample_rate_chan1',
            'write_string': 'SOUR1:FUNC:ARB:SRAT {}',
            'query_string': 'SOUR1:FUNC:ARB:SRAT?',
            'range': [1e-6, 250e6],
            'return_type': float})

        self.add_device_property({
            'name': 'arb_sample_rate_chan2',
            'write_string': 'SOUR2:FUNC:ARB:SRAT {}',
            'query_string': 'SOUR2:FUNC:ARB:SRAT?',
            'range': [1e-6, 250e6],
            'return_type': float})

        self.add_device_property({
            'name': 'burst_mode_chan1',
            'write_string': 'SOUR1:BURS:MODE {}',
            'query_string': 'SOUR1:BURS:MODE?',
            'values': ['TRIG', 'GAT'],
            'return_type': str})

        self.add_device_property({
            'name': 'burst_mode_chan2',
            'write_string': 'SOUR2:BURS:MODE {}',
            'query_string': 'SOUR2:BURS:MODE?',
            'values': ['TRIG', 'GAT'],
            'return_type': str})

        self.add_device_property({
            'name': 'burst_cycles_chan1',
            'write_string': 'SOUR1:BURS:NCYC {}',
            'query_string': 'SOUR1:BURS:NCYC?',
            'range': [1, 10000],
            'return_type': float})

        self.add_device_property({
            'name': 'burst_cycles_chan2',
            'write_string': 'SOUR2:BURS:NCYC {}',
            'query_string': 'SOUR2:BURS:NCYC?',
            'range': [1, 10000],
            'return_type': float})

        self.add_device_property({
            'name': 'burst_state_chan1',
            'write_string': 'SOUR1:BURS:STAT {}',
            'query_string': 'SOUR1:BURS:STAT?',
            'values': [0, 'Off', 1, 'ON'],
            'return_type': str})

        self.add_device_property({
            'name': 'burst_state_chan2',
            'write_string': 'SOUR2:BURS:STAT {}',
            'query_string': 'SOUR2:BURS:STAT?',
            'values': [0, 'Off', 1, 'ON'],
            'return_type': str})

        self.add_device_property({
            'name': 'output_chan1',
            'write_string': 'OUTP1 {}',
            'query_string': 'OUTP1?',
            'values': [0, 'Off', 1, 'ON'],
            'return_type': str})

        self.add_device_property({
            'name': 'output_chan2',
            'write_string': 'OUTP2 {}',
            'query_string': 'OUTP2?',
            'values': [0, 'Off', 1, 'ON'],
            'return_type': str})

        self.add_device_property({
            'name': 'output_load_chan1',
            'write_string': 'OUTP1:LOAD {}',
            'query_string': 'OUTP1:LOAD?',
            'values': [50, 'INF'],
            'return_type': float})

        self.add_device_property({
            'name': 'output_load_chan2',
            'write_string': 'OUTP2:LOAD {}',
            'query_string': 'OUTP2:LOAD?',
            'values': [50, 'INF'],
            'return_type': float})

        self.add_device_property({
            'name': 'trigger_source_chan1',
            'write_string': 'TRIG1:SOUR {}',
            'query_string': 'TRIG1:SOUR?',
            'values': ["IMM", "EXT", "TIM", "BUS"],
            'return_type': str})

        self.add_device_property({
            'name': 'trigger_source_chan2',
            'write_string': 'TRIG2:SOUR {}',
            'query_string': 'TRIG2:SOUR?',
            'values': ["IMM", "EXT", "TIM", "BUS"],
            'return_type': str})

        self.update_properties()
        self.check_errors()

    @property
    def frequency(self):
        self._frequency = getattr(self, 'frequency_chan{}'.format(self.channel))
        return self._frequency

    @frequency.setter
    def frequency(self, new_value):
        setattr(self, 'frequency_chan{}'.format(self.channel), new_value)

    @property
    def instrument_amplitude(self):
        self._instrument_amplitude = getattr(self, 'instrument_amplitude_chan{}'.format(self.channel))
        return self._instrument_amplitude

    @instrument_amplitude.setter
    def instrument_amplitude(self, new_value):
        setattr(self, 'instrument_amplitude_chan{}'.format(self.channel), new_value)

    @property
    def instrument_voltage(self):
        self._instrument_voltage = getattr(self, 'instrument_voltage_chan{}'.format(self.channel))
        return self._instrument_voltage

    @instrument_voltage.setter
    def instrument_voltage(self, new_value):
        setattr(self, 'instrument_voltage_chan{}'.format(self.channel), new_value)

    @property
    def voltage_autorange(self):
        self._voltage_autorange = getattr(self, 'voltage_autorange_chan{}'.format(self.channel))
        return self._voltage_autorange

    @voltage_autorange.setter
    def voltage_autorange(self, new_value):
        setattr(self, 'voltage_autorange_chan{}'.format(self.channel), new_value)

    @property
    def function(self):
        self._function = getattr(self, 'function_chan{}'.format(self.channel))
        return self._function

    @function.setter
    def function(self, new_value):
        setattr(self, 'function_chan{}'.format(self.channel), new_value)

    @property
    def arb_advance_mode(self):
        self._arb_advance_mode = getattr(self, 'arb_advance_mode_chan{}'.format(self.channel))
        return self._arb_advance_mode

    @arb_advance_mode.setter
    def arb_advance_mode(self, new_value):
        setattr(self, 'arb_advance_mode_chan{}'.format(self.channel), new_value)

    @property
    def arb_filter(self):
        self._arb_filter = getattr(self, 'arb_filter_chan{}'.format(self.channel))
        return self._arb_filter

    @arb_filter.setter
    def arb_filter(self, new_value):
        setattr(self, 'arb_filter_chan{}'.format(self.channel), new_value)

    @property
    def arb_sample_rate(self):
        self._arb_sample_rate = getattr(self, 'arb_sample_rate_chan{}'.format(self.channel))
        return self._arb_sample_rate

    @arb_sample_rate.setter
    def arb_sample_rate(self, new_value):
        setattr(self, 'arb_sample_rate_chan{}'.format(self.channel), new_value)

    @property
    def burst_mode(self):
        self._burst_mode = getattr(self, 'burst_mode_chan{}'.format(self.channel))
        return self._burst_mode

    @burst_mode.setter
    def burst_mode(self, new_value):
        setattr(self, 'burst_mode_chan{}'.format(self.channel), new_value)

    @property
    def burst_cycles(self):
        self._burst_cycles = getattr(self, 'burst_cycles_chan{}'.format(self.channel))
        return self._burst_cycles

    @burst_cycles.setter
    def burst_cycles(self, new_value):
        setattr(self, 'burst_cycles_chan{}'.format(self.channel), new_value)

    @property
    def burst_state(self):
        self._burst_state = getattr(self, 'burst_state_chan{}'.format(self.channel))
        return self._burst_state

    @burst_state.setter
    def burst_state(self, new_value):
        setattr(self, 'burst_state_chan{}'.format(self.channel), new_value)

    @property
    def output(self):
        self._output = getattr(self, 'output_chan{}'.format(self.channel))
        return self._output

    @output.setter
    def output(self, new_value):
        setattr(self, 'output_chan{}'.format(self.channel), new_value)

    @property
    def output_load(self):
        self._output_load = getattr(self, 'output_load_chan{}'.format(self.channel))
        return self._output_load

    @output_load.setter
    def output_load(self, new_value):
        setattr(self, 'output_load_chan{}'.format(self.channel), new_value)

    @property
    def trigger_source(self):
        self._trigger_source = getattr(self, 'trigger_source_chan{}'.format(self.channel))
        return self._trigger_source

    @trigger_source.setter
    def trigger_source(self, new_value):
        setattr(self, 'trigger_source_chan{}'.format(self.channel), new_value)

    def arb_upload_ascii(self, name, points):
        """upload arb waveform to instrument in ASCII for

        This will take an array of data points and upload it to and arb file on
        the instrument

        Parameters
        ----------
        name : str
            name you want this arb to be saved as
        points : array
            array of data points between 0 and 1 to be uploaded

        Returns
        -------
        None

        """
        points = [int(32767 * x) for x in points]
        points_string = ", ".join(map(str, points))
        self.write("SOUR{}:DATA:ARB:DAC {}, {}".format(self.channel, name, points_string))

    def clear_volatile_memory(self):
        """Sends command to clear volatile memory on instrument

        Returns
        -------
        None

        """
        self.write("SOUR{}:DATA:VOL:CLE".format(self.channel))

    def wait_for_ready(self):
        """Blocks until operation has finished

        * OPC? code will sit and wait until operation finishes before returning 1

        Returns
        -------
        done: bool
            Returns 1 after operation has finished

        """

        return int(self.query('*OPC?'))

    def firmware_check(self, minimum):
        """Checks to make sure firmware is above minimum

        Returns
        -------
        bool
            True if version is above minimum

        """
        if self.firmware < minimum:
            return True
        else:
            raise ValueError("Firmware {} is below the minimum of {}".format(self.firmware, minimum))

    def check_errors(self):
        """ Reads error messages and checks for specific messages the user should know about

        Returns
        -------
        None

        """
        # TODO: implement set of error codes

        for error in self.errors:
            error = error.replace('"', '').split(',')
            # check against known errors

    @property
    def amplitude(self):
        self._amplitude = self.instrument_amplitude * self.gain
        return self._amplitude

    @amplitude.setter
    def amplitude(self, new_value):
        self.instrument_amplitude = new_value / self.gain
        self._amplitude = new_value

    @property
    def voltage(self):
        self._voltage = self.instrument_voltage * self.gain
        return self._voltage

    @voltage.setter
    def voltage(self, new_value):
        self.instrument_voltage = new_value / self.gain
        self._voltage = new_value

    @property
    def firmware(self):
        """ Retrieve firmware version

        Returns
        -------
        firmware : float
            firmware version in form A.aaa

        """
        ID = self.query('*IDN?')
        ID = ID.split(',')
        firmwares = ID[-1].split('-')
        self.firmware_ = float(re.sub("[^0-9]", "", firmwares[0]))
        return self.firmware_

    @property
    def errors(self):
        """Retrieve errors one by one and clear them

        Returns
        -------
        list
            list of errors

        """

        self._errors = []

        while True:
            error = self.query('SYST:ERR?')
            if '+0,"No error"' in error:
                break
            else:
                self._errors.append(error)
        return self._errors

    # Source > Data properties and methods

    def trigger(self):
        """Sends trigger signal to instrument

        Returns
        -------
        None

        """
        self.write("TRIG")

    def dc_mode(self, v):
        """Sets the instrument in DC mode at specified voltage

        Burst state must also be set to off when DC mode is used

        Parameters
        ----------
        v : float
            DC voltage value

        Returns
        -------
        None

        """
        self.burst_state = 0
        self.function = "DC"
        self.voltage = v

    def sweep_mode(self, values, srate):
        """runs a sweep of voltages at a given sample rate

        This method will take an array of voltages and a sample rate to create a waveform
        that will be loaded and played back on a channel of the AWG. This method will also
        add a ramp back to base voltage to the end of the array provided to ensure smoother operation.


        Parameters
        ----------
        values : list or array
            Array of voltages to sweep across
        srate : int
            a sample rate  in Hz at which the voltages in the array will be played back

        Returns
        -------
        Scaled_values : array
            an array of the scaled values created with ending ramp attached.

        """

        # old firmware use legacy method for sweep
        if self.firmware <= 1.12:
            return self.legacy_sweep_mode(values, srate)

        self.dc_mode(self.voltage)

        # TODO decide when the best place to check for output = 'ON' (also check with ranging)
        # self.output = 'ON'

        self.arb_sample_rate = srate
        self.arb_advance_mode = "SRAT"
        # "STEP" filter causes incomplete playing of the waveform
        self.arb_filter = "OFF"

        voltage_offset = values.min()
        if (values[-1] - values[0]) != 0:
            step = abs(values[0] - values[1])
            vsign = -(values[-1] - values[0]) / abs(values[-1] - values[0])
            rampdown = drange(values[-1], vsign * step, values[0])
            values = np.append(values, rampdown)

        # scale the values, find the peak-to-peak amplitude and the dc offset
        # TODO deal with amplitudes smaller than or larger than available range
        voltage_amplitude = values.max() - values.min()

        try:
            scaled_values = (values - voltage_offset) / voltage_amplitude
            scaled_amplitude = abs(scaled_values.max() - scaled_values.min())
            fullscale_amplitude = 2 * (voltage_amplitude / scaled_amplitude)
        except ZeroDivisionError:
            scaled_values = values - voltage_offset
            # for a dc trace
            fullscale_amplitude = 0.1

        # bring the dc voltage to this offset voltage
        self.dc_mode(voltage_offset)

        self.clear_volatile_memory()

        # creating .arb file on the pc, and then transferring it to the internal
        # memory of the AWG
        self.arb_pc_to_int(
            "sweep",
            scaled_values,
            amplitude=fullscale_amplitude,
            offset=voltage_offset,
            srate=srate,
            filter=self.arb_filter,
        )

        # loading arb file to volatile memory in prepartion for playing
        self.arb_int_to_vol("sweep")
        # play the arb file
        self.arb_set("sweep")

        self.function = "ARB"

        # function should already be set to arb before trying to burst
        self.trigger_source = 'EXT'
        self.burst_mode = "TRIG"
        self.burst_cycles = 1
        self.burst_state = 1

        return scaled_values

    def legacy_sweep_mode(self, values, srate, ramp_down_step=0.5):
        """runs a sweep of voltages at a given sample rate

                This method will take an array of voltages and a sample rate to create a waveform
                that will be loaded and played back on a channel of the AWG. This method will also
                add a ramp back to base voltage to the end of the array provided to ensure smoother operation.

                This functionality is the same as sweep mode but changes the way in which it loads the waveform


                Parameters
                ----------
                values : array
                    Array of voltages to sweep across
                srate : int
                    a sample rate  in Hz at which the voltages in the array will be played back
                ramp_down_step : float, optional
                    defaults to 0.5

                Returns
                -------
                Scaled_values : array
                    an array of the scaled values created with ending ramp attached.

                """

        self.dc_mode(self.voltage)

        self.output = 'ON'

        self.arb_sample_rate = srate
        self.arb_advance_mode = 'SRAT'
        self.arb_filter = "OFF"

        # go from the last point back to the first point in 0.1 V steps
        voltage_offset = values.min()

        if (values[-1] - values[0]) != 0:
            step = abs(ramp_down_step)
            vsign = -(values[-1] - values[0]) / abs(values[-1] - values[0])
            rampdown = drange(values[-1], vsign * step, values[0])
            values = np.append(values, rampdown)

        # scale the values, find the peak-to-peak amplitude and the dc offset
        # TODO deal with amplitudes smaller than or larger than available range
        voltage_amplitude = values.max() - values.min()
        try:
            scaled_values = (values - voltage_offset) / voltage_amplitude
            scaled_amplitude = abs(scaled_values.max() - scaled_values.min())
            fullscale_amplitude = 2 * (voltage_amplitude / scaled_amplitude)
        except ZeroDivisionError:
            scaled_values = values - voltage_offset
            # for a dc trace
            fullscale_amplitude = 0.1

        self.dc_mode(voltage_offset)

        self.clear_volatile_memory()
        self.arb_upload_ascii('sweep', scaled_values)
        self.set_arb('sweep')

        self.function = 'ARB'
        self.trigger_source = 'EXT'
        self.burst_mode = 'TRIG'
        self.burst_cycles = 1
        self.burst_state = 1

        self.amplitude = abs(fullscale_amplitude / 2)
        self.voltage = voltage_offset

        return scaled_values

    def set_arb(self, name):
        """Sets the instrument to use an arb from memory with name provided

        This attempts to tell the instrument to load a waveform with the name provided that is
        saved on the instrument

        Parameters
        ----------
        name : str
            name of the ARB to load

        Returns
        -------
        None

        """
        self.write('SOUR{}:FUNC:ARB {}'.format(self.channel, name))

    def ttl_mode(self):
        """Sets the instrument in TTL mode

        TTL mode is a pulse burst of 5 volts
        Useful for setting a channel as a trigger pulse

        Returns
        -------
        None

        """

        self.function = "PULS"
        self.voltage = 2.5
        self.amplitude = 5

        self.pulse_width = 200e-6
        self.pulse_period = 0.01

        self.edge_time = "MIN"
        self.trigger_source = "BUS"

        self.burst_mode = "TRIG"
        self.burst_cycles = 1
        self.burst_state = 1

    def pulse_sequence_mode(self, arb_sample_rate):
        """Sets pulse sequance mode at giben sample rate

        Parameters
        ----------
        arb_sample_rate  : int
            sample rate for pulse sequance

        Returns
        -------
        None

        """

        self.function = "ARB"

        self.arb_sample_rate = arb_sample_rate
        self.arb_filter = "STEP"
        self.arb_advance_mode = "SRATE"

        self.burst_state = 0
        self.trigger_source = "EXT"

    def arb_int_to_vol(self, name):
        """Load an arbitrary waveform from the internal memory

        Load an arbitrary waveform from the internal memory to the volatile
        memory in preparation for playing the waveform to the output.


        Parameters
        ----------
        name : str
            relative or absolute name of device in flash memory
            default prefix: int:\\
            default extension: .arb


        Returns
        -------
        None

        """

        # TODO fails if the name exists in volatie memory (check volatile memory, and then clear it)
        name = self.absolute_name(name)
        self.write('mmem:load:data{} "{}"'.format(self.channel, name))

    def arb_int_file_exists(self, name):
        """Utility to check if file exists.

        At this time, the check is only for the root folder in the 33500 internal memory.

        Parameters
        ----------
        name : str
            relative or absolute name in the internal memory

        Returns
        -------
        name : str

        """

        # TODO code to identify absolute, relative path consistent with 33500
        # check root folder
        response = self.instrument.query('mmem:cat:data:arb? "INT:\\"')
        files_info_list = re.findall(r"\"(.+?)\"", response)
        filenames = [info.split(",")[0].lower() for info in files_info_list]

        return self.relative_name(name) in filenames

    def arb_pc_to_int(
        self, name, normalized_waveform, amplitude=0.1, offset=0, srate=1e3, filter=filter
    ):
        """ Generate arb waveform contents on the pc, and then transfer to flash memory of the instrument.

        Parameters
        ----------
        name : str
            elative or absolute name (absolute name is required, but can be internally generated)
        normalized_waveform : array
            8 or more points between -1 and 1 defining the arbitrary waveform.
        amplitude : float, optional
            peak to peak amplitude of waveform, defaults to `0.1`.
        offset : float, optional
            dc voltage offset of waveform, defaults to 0.
        srate : float, optional
            sample rate in Hz, defaults to 1e3.
        filter : str
            filter mode

        Returns
        -------
        None

        """

        # generate file header and data
        arb_contents = self.arb_generate(
            normalized_waveform, amplitude, offset, srate, filter=filter
        )
        # prepend the binblock
        bytes_to_send = self.binblock_prefix(arb_contents) + arb_contents
        # open the file and send data from pc to internal flash memory of the arb
        name = self.absolute_name(name)
        self.write('mmem:down:fname "{}"'.format(self.absolute_name(name)))
        try:
            self.instrument.inst.write_raw(
                "mmem:down:data {}\n".format(bytes_to_send.decode("ascii"))
            )
        except AttributeError:
            self.instrument.write_raw("mmem:down:data {}\n".format(bytes_to_send.decode("ascii")))

    def arb_pc_to_int_set(self):
        pass

    def arb_set(self, name):
        """Play an arbitrary waveform that is already loaded in volatile memory

        Parameters
        ----------
        name : str
            name - absolute name, relative name or partial name of the arb file

        Returns
        -------
        None

        """

        name = self.absolute_name(name)
        self.write('sour{}:func:arb "{}"'.format(self.channel, name))

    def arb_sync(self):
        """Synchronize channel 1 and 2 outputs.

        This is only available on 33500B models.
        Returns
        -------
        None

        """
        self.write("sour{}:func:arb:sync".format(self.channel))

    def arb_generate(self, waveform, amplitude=0.1, offset=0, srate=1e3, filter="OFF"):
        """Create contents of a Keysight 33500 .arb file in memory.

        creates  a waveform file to be loaded into memory of the instrument

        Parameters
        ----------
        waveform : array
            normalized waveform for single output
        amplitude : float, optional
            peak to peak amplitude of scaled waveform
            (voltage range from -1 to +1 even if the actual waveform
            does not utilize the entire -1 to +1 range), defaults to `0.1`.
        offset : float, optional
             dc voltage offset of waveform, defaults to `0`.
        srate : float, optional
            sample rate in Hz, defaults to `1e3`.
        filter : str, optional
            filter state, defaults to "OFF".

        Returns
        -------
        None

        """
        n_points = len(waveform)
        vhigh = amplitude / 2 * max(waveform) + offset
        vlow = amplitude / 2 * min(waveform) + offset

        header = b"File Format:1.10\r\n"
        header += b"Channel Count:1\r\n"  # 1 for single, 2 for IQ
        header += b"Sample Rate:%12.6f\r\n" % srate
        header += b"High Level:%8.6f\r\n" % vhigh
        header += b"Low Level:%8.6f\r\n" % vlow
        header += b"Marker Point:%d\r\n" % (n_points // 2)
        header += b'Data Type:"SHORT"\r\n'
        header += b'Filter:"%b"\r\n' % filter.encode()
        header += b"Data Points:%d\r\n" % n_points
        header += b"Data:\r\n"

        # prepare data as ascii-encoded bytes for .arb file
        unsigned_int16_max = int("0xffff", base=16)
        # np.floor: -1 -> -32768, +1->32767
        # data = np.floor(unsigned_int16_max*waveform/2).astype('int16')
        # //2: -1->32767, +1->32767
        data = ((unsigned_int16_max // 2) * waveform).astype("int16")
        data_list = [str(abs(value)) for value in data]
        data_str = "\r\n".join(data_list) + "\r\n"
        data_bytes = bytes(data_str.encode("ascii"))

        arb_contents = header + data_bytes

        return arb_contents

    def binblock_prefix(self, values):
        """Returns the binary block prefix for a bytes or string object
        Returns
        -------
        binary block prefix

        """

        num_bytes = len(values)
        num_num_bytes = len(str(num_bytes))

        return b"#%d%d" % (num_num_bytes, num_bytes)

    def absolute_name(self, name):
        """Utility to determine absolute filename given absolute, relative or partial name

        Parameters
        ----------
        name : str
            absolute, relative or partial name

        Returns
        -------
        name : str
            absolute path with extension

        """
        arb_extensions = [".arb", ".barb", ".seq"]
        arb_default_extension = ".arb"
        arb_prefixes = ["int:\\", "usb:\\"]
        arb_default_prefix = "int:\\"

        # if not startswith a prefix, add the default prefix
        known_prefix = [name.startswith(prefix) for prefix in arb_prefixes]
        if not any(known_prefix):
            name = arb_default_prefix + name

        # if not endswith an extension, add the extension
        known_extension = [name.endswith(extension) for extension in arb_extensions]
        if not any(known_extension):
            name = name + arb_default_extension

        # for object oriented, have a list of all files in memory on initialization
        # of the object (at least in the root folder to start with)

        return name

    def relative_name(self, name):
        """Utility to determine relative filename given absolute or relative name

        Parameters
        ----------
        name : str
            absolute, relative or partial name

        Returns
        -------
        name : str
            relative file name

        """

        return name.split("\\")[-1]
