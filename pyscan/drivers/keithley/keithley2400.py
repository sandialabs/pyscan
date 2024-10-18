# -*- coding: utf-8 -*-
from pyscan.drivers.instrument_driver import InstrumentDriver
import numpy as np
from time import sleep
from ...general.d_range import drange


class Keithley2400(InstrumentDriver):
    '''
    Class to control Kiethey 2400 Source Measure Unit

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    inst_voltage
    voltage
    output
    source
    source_voltage_range
    source_current_range
    source_mode
    sense
    data_element
    sense_voltage_range
    sense_current_range
    voltage_compliance
    current_compliance
    '''

    def __init__(self, instrument):
        self.instrument = instrument

        self._version = "0.1.0"

        self.init_settings()

        self.update_properties()

    def init_settings(self):
        self.gain = 1

        self.inst_voltage_settings = {}
        self.inst_voltage_settings['range'] = [-10, 10]

        self.voltage_settings = {}
        self.voltage_settings['range'] = [-10, 10]

        self.output_settings = {}
        self.output_settings['string_values'] = ['off', 'on']
        self.output_settings['int_values'] = [0, 1]

        self.source_settings = {}
        self.source_settings['string_values'] = ['CURR', 'VOLT']

        self.source_mode_settings = {}
        self.source_mode_settings['string_values'] = ['FIX']

        self.source_voltage_range_settings = {}
        self.source_voltage_range_settings['values'] = [0.21, 2.1, 21]

        self.source_current_range_settings = {}
        self.source_current_range_settings['range'] = [
            1.e-6, 1.e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1]

        self.data_element_settings = {}
        self.data_element_settings['string_values'] = ['VOLT', 'CURR', 'RES']
        self.data_element_settings['translation'] = ['voltage', 'current', 'resistance']

        self.sense_settings = {}
        self.sense_settings['string_values'] = ['CURR', 'VOLT']

        self.sense_voltage_range_settings = {}
        self.sense_voltage_range_settings['values'] = []

        self.sense_current_range_settings = {}
        self.sense_current_range_settings['values'] = [1e-6, 1e-5, 1e-4]

        self.current_compliance_settings = {}
        self.current_compliance_settings['range'] = [0, 0.105]

        self.voltage_compliance_settings = {}
        self.voltage_compliance_settings['range'] = [0, 49.9]

    # consider switching to instrument driver update_properties() if possible.
    def update_properties(self):
        '''
        Update properties by querying the instrument
        '''
        self.inst_voltage
        self.voltage
        self.output

        self.source
        self.source_mode
        self.source_voltage_range
        self.source_current_range

        self.sense

    @property
    def inst_voltage(self):
        self._inst_voltage = float(self.query(';:SOUR:VOLT:LEV?'))
        return self._inst_voltage

    @inst_voltage.setter
    def inst_voltage(self, new_value):
        vmin, vmax = self.inst_voltage_settings['range']

        if vmin <= new_value <= vmax:
            self.write(';:SOUR:VOLT:LEV {}'.format(new_value))
            self._inst_voltage = new_value
        else:
            print('Range error:')
            print('Phase must be between {} and {}'.format(
                vmin, vmax))

    @property
    def voltage(self):
        return self.inst_voltage * self.gain

    @voltage.setter
    def voltage(self, new_value):

        step_size = 0.03

        start = self.voltage
        if new_value == start:
            return
        sign = (new_value - start) / np.abs(new_value - start)

        if np.abs(new_value - start) < step_size:
            self.write(';:SOUR:VOLT:LEV {}'.format(new_value))
            return

        ramp_values = drange(start + sign * step_size, sign * step_size, new_value)

        for v in ramp_values:
            sleep(0.05)
            self.write(';:SOUR:VOLT:LEV {}'.format(v))

        self._voltage = new_value

    @property
    def output(self):
        self._output = int(self.query(':OUTP:STAT?').strip())
        return self._output

    @output.setter
    def output(self, new_value):
        if isinstance(new_value, str):
            new_value = new_value.lower()

        string_values = self.output_settings['string_values']
        int_values = self.output_settings['int_values']

        if new_value in int_values:
            self.write(
                ':OUTP:STAT {}'.format(new_value))
            self._output = string_values[new_value]
        elif new_value.lower() in string_values:
            self.write(
                'OUTP:STAT {}'.format(new_value))
            if new_value == 'once':
                self._output = 'off'
            else:
                self._output = new_value
        else:
            print('Value Error:')
            print('Output can be:')
            print('{} ({})'.format(string_values[0], int_values[0]))
            print('{} ({})'.format(string_values[1], int_values[1]))

    @property
    def source(self):
        self._source = self.query(':SOUR:FUNC?').strip()
        return self._source

    @source.setter
    def source(self, new_value):
        if isinstance(new_value, str):
            new_value = new_value.upper()

        string_values = self.source_settings['string_values']

        if new_value in string_values:
            self.write(':SOUR:FUNC {}'.format(new_value))
            self._source = new_value
        else:
            print('Value Error:')
            print('Source can be:')
            print('{} or {}'.format(*string_values))

    @property
    def source_voltage_range(self):
        self._source_voltage_range = self.query(':SOUR:VOLT:RANG?')

    @property
    def source_current_range(self):
        self._source_current_range = self.query(':SOUR:CURR:RANG?')

    @property
    def source_mode(self):
        self._source_mode = self.query(
            ':SOUR:{}:MODE?'.format(self._source)).strip()
        return self._source_mode

    @source_mode.setter
    def source_mode(self, new_value):
        if isinstance(new_value, str):
            new_value = new_value.upper()

        string_values = self.source_mode_settings['string_values']

        if new_value in string_values:
            self.write(':SOUR:{}:MODE {}'.format(self._source, new_value))
            self._source_mode = new_value
        else:
            print('Value Error:')
            print('Source Mode can be:')
            print('{}'.format(*string_values))

    @property
    def sense(self):
        self._sense = self.query(':SENS:FUNC?').strip()
        return self._sense

    @sense.setter
    def sense(self, new_value):
        if isinstance(new_value, str):
            new_value = new_value.upper()

        string_values = self.sense_settings['string_values']

        if new_value in string_values:
            self.write(':SENS:FUNC \"{}\"'.format(new_value))
            self._sense = new_value
        else:
            print('Value Error:')
            print('Sense can be:')
            print('{} or {}'.format(*string_values))

    @property
    def data_element(self):
        self._data_element = self.query(':FORM:ELEM?').strip()
        return self._data_element

    @data_element.setter
    def data_element(self, new_value):
        if isinstance(new_value, str):
            new_value = new_value.upper()

        string_values = self.data_element_settings['string_values']

        if new_value in string_values:
            self.write(':FORM:ELEM {}'.format(new_value))
            self._data_element = new_value
        else:
            print('Value Error: Bad Input\nData Element can be one of:')
            for value, trans in zip(self.data_element_settings['string_values'],
                                    self.data_element_settings['translation']):
                print('{} for {}'.format(value, trans))

    @property
    def sense_voltage_range(self):
        if self._sense != 'VOLT':
            print('Sense is {}'.format(self._sense))
            return
        self._sense_voltage_range = self.query('SENS:VOLT:RANG?'.format())

    @property
    def sense_current_range(self):
        self._sense_current_range = self.query('SENS:CURR:RANG?'.format())

    # @sense_range.setter
    # def sense_range(self, new_value):

    @property
    def voltage_compliance(self):
        self._voltage_compliance = self.query('SENS:VOLT:PROT?')

    @property
    def current_compliance(self):
        self._current_compliance = self.query('SENS:CURR:PROT?')
