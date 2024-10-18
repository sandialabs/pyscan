import serial
import time
from ..instrument_driver import InstrumentDriver


class ActonSP2300(InstrumentDriver):
    '''
    Driver for ActionSP2300 spectrometer

    Parameters
    ----------
    com : str
        Serial port where device is connected to, e.g. "COM3".
    baud : int, optional
        Serial baud rate, defaults to 9600.
    timeout : int, optional
        Timeout in s for serial connection, defaults to 5.

    Attributes
    ----------
    (Properties)
    serial : str
        Serial port
    grating : int
        From 1 to 9
    gratings :
        List of available gratings
    wavelength : float
        From 0 to 1400
    wavelength_speed : float
        Speed in nm/min
    done_moving : bool
        Whether the instrument is done moving

    '''

    def __init__(self, com, baud=9600, timeout=5):

        self.ser = serial.Serial(com, baud, timeout=timeout)
        time.sleep(1)

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()

    def flush(self):
        readline = self.ser.readline().decode('utf-8')
        return readline

    def read(self):
        '''Read lines from serial until "ok" is read. Used by :func:`write` to read instrument response.

        Returns
        -------
        str
        '''
        readline = self.ser.readline().decode('utf-8')
        lines = ''
        while 'ok' not in readline:
            lines += readline
            readline = self.ser.readline().decode('utf-8')
        lines += readline
        return lines

    def write(self, cmd):
        ''' Writes a `cmd` to the serial.

        Parameters
        ----------
        cmd : str
            Command to write to the serial

        Returns
        -------
        str
            Response
        '''
        self.ser.write((cmd + '\r').encode())
        return self.read()

    def query(self, cmd):
        ''' Wrapper to write a `cmd` to serial. Passes cmd to :func:`write`

        Parameters
        ----------
        cmd : str
            Command to write to serial

        Returns
        -------
        str
            Response
        '''
        return self.write(cmd)

    def __del__(self):
        self.ser.close()

    def initialize_properties(self):
        def parse_response(resptype):
            def inner(resp):
                if resp[-3:] != 'ok\r':
                    print('ActonSP2300: Communication error "%s"' % resp)
                return resptype(resp[:-4].strip())
            return inner

        self.add_device_property({
            'name': 'serial',
            'query_string': 'SERIAL',
            'return_type': parse_response(str)})

        self.add_device_property({
            'name': 'grating',
            'write_string': '{} GRATING',
            'query_string': '?GRATING',
            'values': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'return_type': parse_response(int)})

        self.add_device_property({
            'name': 'gratings',
            'query_string': '?GRATINGS',
            'return_type': parse_response(str)})

        self.add_device_property({
            'name': 'wavelength',
            'query_string': '?NM',
            'write_string': '{} GOTO',
            'range': [0, 1400],
            'return_type': lambda t: float(parse_response(str)(t).split(' ')[0])})

        self.add_device_property({
            'name': 'wavelength_speed',
            'query_string': '?NM/MIN',
            'write_string': '{} NM/MIN',
            'return_type': lambda t: float(parse_response(str)(t).split(' ')[0])})

        self.add_device_property({
            'name': 'done_moving',
            'query_string': 'MONO-?DONE',
            'return_type': parse_response(bool)})
