# -*- coding: utf-8 -*-
from .instrument_driver import InstrumentDriver


class OxfordIPS120(InstrumentDriver):
    '''Class to control Oxford Instruments Intelligent Power Supply IPS120 Superconducting Magnet Power Supply

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value
        from :func:`~pyscan.drivers.newinstrument.new_instrument`)

    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.instrument.read_termination = '\r'
        self.instrument.write_termination = '\r'
        self.set_remote_unlocked()

        self.field_limit = 8
        self.field_rate_limit = 0.1
        self._version = "0.1.0"

        self.debug = False
        self.initialize_properties()

    def initialize_properties(self):
        self.target_field
        self.field_sweep_rate
        self.get_current
        self.get_target_current
        self.get_current_sweep_rate
        self.get_field

    def hold(self):
        self.write('$A0')

    def to_set_point(self):
        self.write('$A1')

    def to_zero(self):
        self.write('$A2')

    def clamp(self):
        self.write('$A4')

    def set_local_locked(self):
        self.write('$C0')

    def set_remote_lock(self):
        self.write('$C1')

    def set_local_unlocked(self):
        self.write('$C2')

    def set_remote_unlocked(self):
        self.write('$C3')

    def get_current(self):
        self._current = float(self.query_until_return('R2').replace('R', ''))
        return self._current

    def get_target_current(self):
        self._target_current = float(self.query_until_return('R5').replace('R', ''))
        return self._target_current

    def get_current_sweep_rate(self):
        self._current_sweep_rate = float(self.query_until_return('R6').replace('R', ''))
        return self._current_sweep_rate

    def get_field(self):
        self._field = float(self.query_until_return('R7').replace('R', ''))
        return self._field

    @property
    def target_field(self):
        self._target_field = float(self.query_until_return('R8').replace('R', ''))
        return self._target_field

    @target_field.setter
    def target_field(self, new_value):
        if (new_value >= -self.field_limit) and (new_value < self.field_limit):
            self.write('$J{}'.format(round(new_value, 4)))
            self._target_field = round(new_value, 4)
        else:
            print('Target field out of range, must be 0 < set point < {}'.format(self.field_limit))

    @property
    def field_sweep_rate(self):
        self._field_sweep_rate = float(self.query_until_return('R9').replace('R', ''))
        return self._field_sweep_rate

    @field_sweep_rate.setter
    def field_sweep_rate(self, new_value):
        if (new_value >= 0) and (new_value < self.field_rate_limit):
            self.write('$T{}'.format(round(new_value, 3)))
            self._field_sweep_rate = round(new_value, 3)
        else:
            print('Sweep rate out of range, must be 0 < rate < {}'.format(self.field_rate_limit))

    def set_heat_on(self):
        return self.query('&H0')

    def set_heat_off(self):
        return self.query('&H1')

    def set_target_field(self, new_value):
        self.write('$J{}'.format(round(new_value, 4)))

    def get_status(self):

        status = self.query_until_return('X')

        X1 = {0: 'Normal',
              1: 'Quenched',
              2: 'Over Heated',
              4: 'Warming Up',
              8: 'Fault'}
        status1 = X1[int(status[1])]

        # X2 = {0: 'Normal',
        #       1: 'On Positive Voltage Limit',
        #       2: 'On Negative Voltage Limit',
        #       4: 'Outside Negative Current Limit',
        #       8: 'Outside Positive Current Limit'}

        status2 = X1[int(status[2])]

        print('Status: {}, {}'.format(status1, status2))

        A = {0: 'Hold',
             1: 'To Set Point',
             2: 'To Zero',
             4: 'Clamped'}

        activity = A[int(status[4])]

        print('Activity: {}'.format(activity))

        C = {0: 'Local & Locked',
             1: 'Remote & Locked',
             2: 'Local & Unlocked',
             3: 'Remote & Unlocked',
             4: 'Auto-Run-Down',
             5: 'Auto-Run-Down',
             6: 'Auto-Run-Down',
             7: 'Auto-Run-Down'}

        loc = C[int(status[6])]

        print('Local/Remote Status: {}'.format(loc))

        H = {0: 'Off, Magnet at Zero',
             1: 'On',
             2: 'Off, Maget at Field',
             5: 'Heater Fault',
             8: 'No Switch Fitted'}

        heater = H[int(status[8])]

        print('Heater: {}'.format(heater))

        M1 = {0: 'Amps, Fast',
              1: 'Tesla, Fast',
              4: 'Amps, Slow',
              5: 'Tesla, Slow'}

        M2 = {0: 'at rest',
              1: 'Sweeping',
              2: 'Sweep Limit',
              3: 'Sweeping & Sweep Limiting'}

        mode1 = M1[int(status[10])]
        mode2 = M2[int(status[11])]

        print('Mode: {}; {}'.format(mode1, mode2))

    def query_until_return(self, query, n=10):

        message = self.query(query)

        for i in range(n):

            if len(message) != 0:
                return message
            else:
                message = self.query('&')
