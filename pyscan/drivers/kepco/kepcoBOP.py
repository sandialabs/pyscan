from ..instrument_driver import InstrumentDriver
from time import sleep
import math


class KepcoBOP(InstrumentDriver):
    '''
    Class to control Kepco BOP power supply

    Parameters
    ----------
    instrument : string or pyvisa :class:`pyvisa.Resource`
        visa string or an instantiated instrument
    tesla_per_amp : float
        Defaults to 0.004201
    '''

    def __init__(self,
                 instrument,
                 tesla_per_amp=0.004201,
                 ):

        self.instrument = instrument
        self._version = "0.1.0"

        # magnetic field properties
        self.tesla_per_amp = tesla_per_amp

        # setup to operate magnet
        self.mode('curr')
        self.output_on

        # property settings
        self.current_settings = {'range': [-40, 40],
                                 'current_sweep_rate': 10,  # A/sec
                                 'delta_i': 2,            # coarse current steps
                                 }

    def update(self):

        self.current
        self.field

    # def __repr__(self):
    #     s = 'current={}, field={}\n'.format(self._current, self._field)
    #     return(s)

    def output_on(self):
        self.write('outp on')

    def output_off(self):
        self.write('outp on')

    def mode(self, bop_mode):
        '''
        Set the mode for the power supply

        Parameters
        ----------
        bop_mode :
            'current' or 'voltage' (or 4 letter abbrev.), any case
        '''

        current_keywords = ('curr', 'current')
        voltage_keywords = ('volt', 'voltage')

        if bop_mode.lower() in current_keywords:
            self.write('func:mode curr')
        elif bop_mode.lower() in voltage_keywords:
            self.write('func:mode volt')
        else:
            print('unknown mode: {}.  Use "curr" or "volt"'.format(bop_mode))

    @property
    def current(self):
        self._current = float(self.query('curr?'))
        return self._current

    @current.setter
    def current(self, new_value):

        # settings
        imin, imax = self.current_settings['range']
        delta_i = self.current_settings['delta_i']
        current_sweep_rate = self.current_settings['current_sweep_rate']

        if imin <= new_value <= imax:
            istart = self.current
            iend = new_value

            if iend == istart:
                pass
            elif abs(iend - istart) < delta_i:
                self.write('curr {}'.format(iend))
                self._current = iend
            else:
                di = iend - istart
                isgn = abs(di) / di
                steps = range(math.floor(abs(iend - istart) / delta_i))
                current_steps = [float('{0:4f}'.format(
                    istart + (i + 1) * delta_i * isgn)) for i in steps]
                current_steps.append(iend)
                for current in current_steps:
                    self.write('curr {0:.4f}'.format(current))
                    sleep(delta_i / current_sweep_rate)
                self._current = iend

        else:
            print('Range Error:')
            print('Current must be between {:.4f} and {:.4f} Amp'.format(imin, imax))

    @property
    def field(self):
        self._field = self.tesla_per_amp * self._current
        return self._field

    @field.setter
    def field(self, new_value):
        imin, imax = self.current_settings['range']
        bmin = imin * self.tesla_per_amp
        bmax = imax * self.tesla_per_amp

        new_current = new_value / self.tesla_per_amp
        if imin <= new_current <= imax:
            self.current = new_current
        else:
            print('Range Error:')
            print('Field must be between {:.5f} and {:.5f} Amp'.format(bmin, bmax))
