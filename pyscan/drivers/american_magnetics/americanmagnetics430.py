from ..instrument_driver import InstrumentDriver
from time import sleep


class AmericanMagnetics430(InstrumentDriver):
    '''
    Class to control American Magnetics 430 Magnet power supply.

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    target_field : float
        Sets/queries the target field of the magnet in Tesla
    field : float
        Sets/queries the magnetic field of the magnet in Tesla.
        When setting, locks until target field is reached
    persistant_switch_state : int
        Sets/queries state of the persistant switch. Values: [0, 1] (off, on)
    magnet_voltage : float
        Queries the voltage applied to the magnet leads
    '''

    def __init__(self, instrument):

        # set up the termination characters
        instrument.read_termination = '\r\n'
        instrument.write_termination = '\r'

        self._version = "0.1.0"

        # visa object
        self.instrument = instrument

        self.instrument.clear()

        # self.update_properties()
        self.target_field

    def show_info(self):

        print('target_field: {}'.format(self._target_field))
        print('magnet field: {}'.format(self.magnet_field()))
        print('state: {}'.format(self.state()))
        switch_state = int(self.persistant_switch_state)
        if switch_state == 1:
            print('heater on')
        elif switch_state == 0:
            print('heater off')

    @property
    def target_field(self):
        self._target_field = float(self.query('FIELD:TARG?'))

        return self._target_field

    @target_field.setter
    def target_field(self, new_value):

        self.write('CONF:FIELD:TARG {}'.format(new_value))

    @property
    def magnet_voltage(self):
        magnet_voltage = self.query('VOLT:MAG?')

        return magnet_voltage

    @property
    def field(self):

        self._field = self.query('FIELD:MAG?')

        return self._field

    @field.setter
    def field(self, new_value):
        self.target_field = new_value
        while self.state()[0] == 1:
            sleep(0.1)

    def state(self):
        '''
        Queries ramping state of the power supply (ramp, pause or zero)

        1 - Raming to target field
        2 - holding
        3 - Paused
        4 - ramping in manual up
        5 - ramping in maual down
        6 - zeroing current in progress
        7 - quench detected
        8 - at zero current
        9 - heating persistent swtich
        10 - cooling persistent switch

        Returns
        -------
        tuple (int, str)
        '''

        state_meaning = {
            1: 'RAMPING to target field/current',
            2: 'HOLDING at the target field/current',
            3: 'PAUSED',
            4: 'Ramping in MANUAL UP mode',
            5: 'Ramping in MANUAL DOWN mode',
            6: 'ZEROING CURRENT (in progress)',
            7: 'Quench detected',
            8: 'At ZERO current',
            9: 'Heating persistent switch',
            10: 'Cooling persistent switch'}
        state = int(self.query('STATE?'))
        return (state, state_meaning[state])

    def ramp(self):
        '''
        Begin ramping

        Returns
        -------
        None
        '''

        # future: check that the supply is ready to ramp
        # check if ramping
        # check if heater is on
        self.write('RAMP')

    def pause(self):
        '''
        Stop ramping and wait

        Returns None
        '''

        self.write('PAUSE')

    def zero(self):
        '''
        Return to zero field

        Returns None
        '''

        self.write('ZERO')

    @property
    def persistant_switch_state(self):

        ps_state = int(self.query('PS?'))

        return ps_state

    @persistant_switch_state.setter
    def persistant_switch_state(self, new_value):

        if new_value not in [0, 1]:
            print('Persistant switch state must be 0 or 1 (off or on).')
            print('No change to heater switch.')
            return

        self.write('PS {}'.format(new_value))
