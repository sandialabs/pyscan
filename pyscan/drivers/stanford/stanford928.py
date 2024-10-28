# -*- coding: utf-8 -*-
from .stanford900 import Stanford900
from math import floor


class Stanford928(Stanford900):  # pragma: no cover

    def __init__(self, instrument, port, debug=False):
        '''Class to control Stanford Research Systems SIM928 - Small
        Instrumentation Modules (SIM) Isolated Voltage Source.

        To use: Confirm stanford research system 928SIM box, and identify port on the
        SIM928 that the instrument will communicate with
        '''

        # initialize SRS SIM900 instrument for message-based communications
        super().__init__(instrument, port, debug=debug)
        # Stanford900.__init__(self, instrument, port)

        self._version = "0.1.0"
        self.init_settings()

        self.update_properties()

        if self._service_indicator == 1:
            print('Device indicates service is required for SIM928 {}'.format(self.port))

    def init_settings(self):
        self.gain = 1

        self.inst_voltage_settings = {}
        self.inst_voltage_settings['range'] = (-20.0, 20.0)

        self.output_settings = {}
        self.output_settings['string_values'] = ['off', 'on']
        self.output_settings['int_values'] = [0, 1]

        self.voltage_settings = {}
        self.voltage_settings['range'] = (-20.0, 20.0)

    # consider using instrument drivers update_properties() if possible.
    def update_properties(self):
        self.voltage

        self.output

        self.battery_cycles
        self.max_battery_cycles
        self.battery_percent

        self.service_indicator

    @property
    def inst_voltage(self):
        '''
        Get the SIM928 instrument voltage (no gain included).

        Returns
        -------
        float
            voltage value at the instrument
        '''

        self._inst_voltage = float(self.query_port('VOLT?'))

        return self._inst_voltage

    @inst_voltage.setter
    def inst_voltage(self, new_value):
        '''
        Set the SIM928 instrument voltage (no gain included).

        Parameters
        ----------
        new_value : float
            Voltage value to set at the instrument
        '''

        vmin, vmax = self.inst_voltage_settings['range']

        if vmin <= new_value <= vmax:
            vstart = self.inst_voltage
            vend = new_value

            if vend == vstart:
                pass
            elif abs(vend - vstart) < 0.01:
                self.write_port('VOLT {:.3f}'.format(vend))
            else:
                dv = vend - vstart
                vsgn = abs(dv) / dv
                vsteps = range(floor(abs(vend - vstart) / 0.01))
                vsteps = [float('{0:.3f}'.format(
                    vstart + (v + 1) * 0.01 * vsgn)) for v in vsteps]
                if vsteps[-1] != vend:
                    vsteps.append(vend)
                for v in vsteps:
                    self.write_port('VOLT {:.3f}'.format(v))

                # wait until this operation is complete
                self.write_port('*OPC?')
                message = self.read_port()
                self.logger.debug('inst_voltage: operation complete = {}'.format(message))

            self._inst_voltage = vend
        else:
            print('Range Error:')
            print('Voltage must be between {} and {} V'.format(vmin, vmax))

    @property
    def voltage(self):
        return self.inst_voltage * self.gain

    @voltage.setter
    def voltage(self, new_value):
        vmin, vmax = self.voltage_settings['range']

        if vmin <= new_value <= vmax:
            self.inst_voltage = new_value / self.gain
        else:
            print('Range Error:')
            print('Voltage must be between {} and {} V'.format(vmin, vmax))

    @property
    def output(self):
        '''
        Check if SIM928 output is on or off.

        Returns
        -------
        int
            0 or 1
        '''

        self._output = int(self.query_port('EXON?'))

        return self._output

    @output.setter
    def output(self, new_value):

        string_values = self.output_settings['string_values']
        int_values = self.output_settings['int_values']

        if new_value in int_values:
            self.write_port('EXON {}'.format(new_value))
            self._output = new_value
        elif new_value.lower() in string_values:
            self.write_port('EXON {}'.format(new_value))
            self._output = new_value
        else:
            print('Value Error:')
            print('Output can be:')
            print('{} ({})'.format(string_values[0], int_values[0]))
            print('{} ({})'.format(string_values[1], int_values[1]))

    @property
    def battery_cycles(self):
        '''
        Query number of battery cycles since last reset by SRS

        Returns
        -------
        float
            Number of cycles since last reset
        '''

        self._battery_cycles = int(self.query_port('BIDN? 3'))

        return self._battery_cycles

    @property
    def max_battery_cycles(self):
        self._max_battery_cycles = int(self.query_port('BIDN? 2'))

        return self._max_battery_cycles

    @property
    def battery_percent(self):
        return self.battery_cycles / self.max_battery_cycles * 100

    @property
    def service_indicator(self):
        '''
        Check battery service indicator

        Returns
        -------
        status of indicator
        '''

        values = self.query_port('BATS?')

        self._service_indicator = int(values.strip().split(',')[2])

        return self._service_indicator


class stanford928(Stanford928):  # pragma: no cover
    '''Class for indicating to users of older versions of pyscan how to update code'''

    def __init__(self, inst, port):
        print('class "stanford928" is deprecated.  Use Stanford928')
        super().__init__(inst, port)
