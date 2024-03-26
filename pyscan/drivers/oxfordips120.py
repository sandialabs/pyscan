# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep, time
from .instrument_driver import InstrumentDriver


class OxfordIPS120(InstrumentDriver):
    '''Class to control Oxford Instruments Intelligent Power Supply IPS120 Superconducting Magnet Power Supply

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value from
        :func:`.new_instrument`)

    Properties
    ----------
    field_set_point
    field_set_rate

    Methods
    -------
    get_field()
        returns the magnetic field
    get_persistent_field()
        returns the magnetic field where the heater was turned off 
        and the magnet put in persistent mode
    remote()
        put the power supply in remote mode, keyword argument: locked=False
    local()
        put the power supply in local mode, keyword argument: locked=False
    heater()
        "on", "off" or "force"
    hold()
        hold the magnetic field
    to_zero()
        sweep the field to zero
    to_set_point()
        sweep hte field to the set point
    heater_status()
        True if the heater is on
    remote_status()
        True if the power supply is in remote mode (required to issue control commands)
    sweeping_status()
        True if the field is changing
    persistent_status()
        True if the magnet is in persisent mode
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.instrument.read_termination = '\r'
        self.instrument.write_termination = '\r'
        self.remote()

        # setup timeout for query_until_return
        self.timeout = 1
        
        # make sure the buffer is empty:
        # read status byte by performing a serial poll
        # bit 1: byte available
        # bit 4: message available
        # bit 6: requesting service (reset after read)
        stb = self.instrument.read_stb() 
        if not stb:
            stb = self.instrument.read_stb()
        if (stb&16):
            message = self.instrument.read()
            print(f"Message in buffer: {message}")

        self.field_limit = 8
        self.field_rate_limit = 0.2

        self.debug = False
        self.initialize_properties()

    def initialize_properties(self):
        self.get_field
        self.field_set_point
        # self.target_field # legacy
        self.field_rate
        # self.field_sweep_rate # legacy
        self.get_current
        self.get_current_set_point
        # self.get_target_current # legacy
        self.get_current_rate
        # self.get_current_sweep_rate # legacy

    def __repr__(self):
        status = self.status()
        value = ""
        if self.quench_status():
            value += "QUENCHED"
        if self.heater_status():
            value += "Heater on"
        else:
            value += "Heater off"
        value += "\n"
        if self.sweeping_status():
            value += "Field is changing"
        else:
            value += "At rest"
        if self.persistent_status():
            value += "\n"
            value += "Magnet is persistent"
            value += "\n"
            value += f"get_persistent_field() = {self.get_persistent_field()}"
        value += "\n"
        value += f"activity: {status.A_value()}"
        value += "\n"
        value += f"get_field() = {self.get_field()}"
        value += "\n"
        value += f"field_set_point = {self.field_set_point}"
        value += "\n"
        value += f"field_rate = {self.field_rate}"

        return value

    def hold(self):

        if not self.remote_status():
            raise IPS120Error('Control commands require the power supply to be in remote mode')

        self.query_until_return('A0')

    def to_set_point(self):

        if not self.remote_status():
            raise IPS120Error('Control commands require the power supply to be in remote mode')

        self.query_until_return('A1')

    def to_zero(self):

        if not self.remote_status():
            raise IPS120Error('Control commands require the power supply to be in remote mode')

        self.query_until_return('A2')

    def clamp(self):

        if not self.remote_status():
            raise IPS120Error('Control commands require the power supply to be in remote mode')

        self.query_until_return('A4')

    def local(self, locked=False):
        '''
        Set local mode.
        Keyword arguments:
            locked: boolean, defaults to unlocked
        '''

        if locked:
            self.write('$C0')
        else:
            self.write('$C2')

    def remote(self, locked=False):
        '''
        Set remote mode.
        Keyword arguments:
            locked: boolean, defaults to unlocked
        '''

        if locked:
            self.write('$C1')
        else:
            self.write('$C3')

    def heater(self, state):
        '''
        Set the state of the heater.  Record the time when the heater was changed
        '''

        if not self.remote_status():
            raise IPS120Error('Control commands require the power supply to be in remote mode')

        if state == 'on':
            if not self.heater_status():
                self.time_heater_toggle = datetime.now()
                _ = self.query_until_return('H1')
        elif state == 'off':
            if self.heater_status():
                self.time_heater_toggle = datetime.now()
                _ = self.query_until_return('H0')
        elif state == 'force':
            # need to add some checks before allowing heater to be forced
            _ = self.query_until_return('H2')
        else:
            print("State must be 'on', 'off' or 'force'")

    @property
    def field_set_point(self):
        self._field_set_point = float(self.query_until_return('R8').replace('R', ''))
        return self._field_set_point

    @field_set_point.setter
    def field_set_point(self, new_value):
        if (new_value >= -self.field_limit) and (new_value <= self.field_limit):
            # normal resolution 0.0001 T
            self.write('$J{}'.format(round(new_value, 4)))
            self._field_set_point = round(new_value, 4)
            # extended resolution 0.00001 T (see Q4 to set extended resolution)
        else:
            print(f'field_set_point out of range, must be {-self.field_limit} <= set point <= {self.field_limit}')

    @property
    def field_rate(self):
        self._field_rate = float(self.query_until_return('R9').replace('R', ''))
        return self._field_rate

    @field_rate.setter
    def field_rate(self, new_value):
        if (new_value > 0) and (new_value <= self.field_rate_limit):
            # normal resolution 0.001 T/min
            self.write('$T{}'.format(round(new_value, 3)))
            self._field_rate = round(new_value, 3)
            # extended resolution 0.0001 T/min (see Q4 to set extended resolution)
        else:
            print(f'field_rate out of range, must be 0 < rate <= {self.field_rate_limit}')

    def get_field(self):
        self._field = float(self.query_until_return('R7').replace('R', ''))
        return self._field

    def get_persistent_field(self):
        self._field = float(self.query_until_return('R18').replace('R', ''))
        return self._field

    def status(self):

        status_string = self.query_until_return('X')
        return Status(status_string)

    def quench_status(self):
        '''
        True when the magnet quenched
        '''

        status = self.status()
        if status.X1 == 1:
            return True

    def heater_status(self):
        '''
        heater() True for on and False for off
        '''

        status = self.status()
        if status.H==0:
            return False
        elif status.H==1:
            return True
        else:
            # magnet persistant or heater fault - may need to have a heater_status object in future
            return False

    def sweeping_status(self):
        '''
        True when the field is changing, False when the field is at rest
        '''

        status = self.status()
        if status.M2 == 0:
            return False
        else:
            return True

    def remote_status(self):
        '''
        True when magnet is in remote mode, False when it is in local mode.
        '''

        status = self.status()
        if (status.C == 1) or (status.C ==3):
            return True
        else:
            return False

    def persistent_status(self):
        '''
        True when the magnet is in persistent mode
        '''

        status = self.status()
        if status.H==2:
            return True
        else:
            return False

    def get_current(self):
        self._current = float(self.query_until_return('R2').replace('R', ''))
        return self._current

    def get_current_set_point(self):
        self._current_set_point = float(self.query_until_return('R5').replace('R', ''))
        return self._current_set_point

    def get_current_rate(self):
        self._current_rate = float(self.query_until_return('R6').replace('R', ''))
        return self._current_rate

    def query_until_return(self, query, n=10, debug=False):

        # message = self.query(query)
        self.write(query)
        stb = self.instrument.read_stb()
        # wait for message
        i = 0
        start_time = time()
        while (time()-start_time)<self.timeout:
            while not (stb&16):
                if debug:
                    if (stb&2):
                        print("byte available but not message")
                stb = self.instrument.read_stb()
                i += 1
            if debug:
                # typically i=4, time = 0.01
                print(f"needed to wait {i}; {time()-start_time} seconds")
            message = self.read()
            return message

        raise IPS120Error("query_until_return Timeout")

        # for i in range(n):
        #
        #     if len(message) != 0:
        #         return message
        #     else:
        #         # &: ignore ISOBUS control characters, $: don't send a reply
        #         message = self.query('&')
        #         print("query again")

    # --- legacy commands below here ---
    # legacy
    def set_local_locked(self):
        self.write('$C0')

    # legacy
    def set_remote_lock(self):
        self.write('$C1')

    # legacy
    def set_local_unlocked(self):
        self.write('$C2')

    # legacy
    def set_remote_unlocked(self):
        self.write('$C3')

    # legacy, use heater('on') and these are reversed
    def set_heat_on(self):
        return self.query('&H0')

    # legacy, use heater('off') and these are reversed
    def set_heat_off(self):
        return self.query('&H1')

    # legacy, must use field_set_point attribute
    def set_target_field(self, new_value):
        self.write('$J{}'.format(round(new_value, 4)))
        print("deprecated: use 'field_set_point = value'")

    # legacy, use field_set_point()
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

    # legacy, use get_current_set_point
    def get_target_current(self):
        self._target_current = float(self.query_until_return('R5').replace('R', ''))
        return self._target_current

    # legacy, use get_current_rate
    def get_current_sweep_rate(self):
        self._current_sweep_rate = float(self.query_until_return('R6').replace('R', ''))
        return self._current_sweep_rate

    # legacy, use field_rate
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

    # legacy, use status()
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


class Status():
    def __init__(self, status_string='X00A1C3H1M10P03'):
        '''
        Returns:
            Tuple of dictionaries, X1, X2, A, C, H, M1 and M2
            Each dictionary has a 
                'description': what status is reported
                'value': integer from status string
                'states': text explanation of the status from the integer value
        '''

        # get index values
        self.X1_name = 'system status (operation)'
        self.X1 = int(status_string[1])
        self.X2_name = 'system status (voltage)'
        self.X2 = int(status_string[2])
        self.A_name = 'Activity'
        self.A = int(status_string[4])
        self.C_name = 'LOC/REM status'
        self.C = int(status_string[6])
        self.H_name = 'Heater'
        self.H = int(status_string[8])
        self.M1_name = 'Mode (rate)'
        self.M1 = int(status_string[10])
        self.M2_name = 'Mode (sweep)'
        self.M2 = int(status_string[11])

    def __repr__(self):
        value = "\n"
        value += f"{ self.X1_name } : {self.X1_value()} (X1={self.X1})"
        value += "\n"
        value += f"{ self.X2_name } : {self.X2_value()} (X2={self.X2})"
        value += "\n"
        value += f"{ self.A_name } ; {self.A_value()} (A={self.A})"
        value += "\n"
        value += f"{ self.C_name } ; {self.C_value()} (C={self.C})"
        value += "\n"
        value += f"{ self.H_name } ; {self.H_value()} (H={self.H})"
        value += "\n"
        value += f"{ self.M1_name } ; {self.M1_value()} (M1={self.M1})"
        value += "\n"
        value += f"{ self.M2_name } ; {self.M2_value()} (M2={self.M2})"

        return value

    def X1_value(self):
        indexed_values = {
            0: 'Normal',
            1: 'Quenched',
            2: 'Over Heated',
            4: 'Warming Up',
            8: 'Fault'}
        return indexed_values[self.X1]

    def X2_value(self):
        indexed_values = {
            0: 'Normal',
            1: 'On Positive Voltage Limit',
            2: 'On Negative Voltage Limit',
            4: 'Outside Negative Current Limit',
            8: 'Outside Positive Current Limit'}
        return indexed_values[self.X2]

    def A_value(self):
        indexed_values = {
            0: 'Hold',
            1: 'To Set Point',
            2: 'To Zero',
            4: 'Clamped'}
        return indexed_values[self.A]

    def C_value(self):
        indexed_values = {
            0: 'Local & Locked',
            1: 'Remote & Locked',
            2: 'Local & Unlocked',
            3: 'Remote & Unlocked',
            4: 'Auto-Run-Down',
            5: 'Auto-Run-Down',
            6: 'Auto-Run-Down',
            7: 'Auto-Run-Down' }
        return indexed_values[self.C]

    def H_value(self):
        indexed_values = {
            0: 'Off Magnet at Zero',
            1: 'On',
            2: 'Off Magnet at Field',
            5: 'Heater Fault',
            8: 'No Switch Fitted' }
        return indexed_values[self.H]

    def M1_value(self):
        indexed_values = {
            0: 'Amps, Immediate, Fast',
            1: 'Tesla, Immediate, Fast',
            2: 'Amps, Sweep, Fast',
            3: 'Tesla, Sweep, Fast',
            4: 'Amps, Immediate, Slow',
            5: 'Tesla, Immediate, Slow',
            6: 'Amps, Sweep, Slow',
            7: 'Tesla, Sweep, Slow', }
        return indexed_values[self.M1]

    def M2_value(self):
        indexed_values = {
            0: 'At Rest',
            1: 'Sweeping',
            2: 'Sweep Limiting',
            3: 'Sweeping & Sweep Limiting',
            4: 'Polarity Fault',
            5: 'Sweeping & Polarity Fault',
            6: 'Amps, Sweep, Slow',
            7: 'Tesla, Sweep, Slow', }
        return indexed_values[self.M2]


class IPS120Error(Exception):
    pass
