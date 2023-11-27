"""
ArduinoHelmholtz
================
"""
import serial,time
from .instrumentdriver import InstrumentDriver


class ArduinoHelmholtz(InstrumentDriver):
    ''' Inherits from :class:`~pyscan.drivers.instrumentdriver.InstrumentDriver`.
    
    Parameters
    ----------
    com : str
        Serial port connected to device
    baud : int
        Baud rate, defaults to `9600`.
    timeout : float
        Serial timeout in s, defaults to 5.

    Yields
    ------
    Properties which can be get and set : 
        x : bool
            Values: [True, False]
        y : bool
            Values: [True, False]
        z : bool
            Values: [True, False]
        a : bool
            Values: [True, False]
    Properties which can be get only : 
        state : list
            Queries state, returns list of bool
        pins : list
            Queries pins, returns list of pins

    '''
    def __init__(self,com,baud=9600,timeout=5):
        self.ser=serial.Serial(com,baud,timeout=timeout)
        time.sleep(1)

        self.debug=False
        self.initialize_properties()

    def read(self):
        return self.ser.readline().decode('utf-8').replace('\r\n','')

    def write(self,cmd):
        if len(cmd)!=2:
            print('Arduino Helmholtz commands are two characters long ([xyz][01f?], ??).')
            return -1
        else:
            self.ser.write((cmd+'\n').encode())
            return self.read()

    def query(self,cmd):
        return self.write(cmd)

    def flip_all(self):
        """Flip all outputs"""
        self.query('ff')

    def __del__(self):
        self.ser.close()

    def initialize_properties(self):
        def string_to_bool(string):
            return bool(int(string))
        self.add_device_property({
            'name':'x',
            'write_string': 'x{:d}',
            'query_string':'x?',
            'values':[True,False],
            'return_type': string_to_bool})

        self.add_device_property({
            'name':'y',
            'write_string': 'y{:d}',
            'query_string':'y?',
            'values':[True,False],
            'return_type': string_to_bool})
        
        self.add_device_property({
            'name':'z',
            'write_string': 'z{:d}',
            'query_string':'z?',
            'values':[True,False],
            'return_type': string_to_bool})
        
        self.add_device_property({
            'name':'a',
            'write_string': 'a{:d}',
            'query_string':'a?',
            'values':[True,False],
            'return_type': string_to_bool})

        self.add_device_property({
            'name':'state',
            'query_string':'??',
            'return_type':lambda t: [string_to_bool(q) for q in t]})

        self.add_device_property({
            'name':'pins',
            'query_string':'pp',
            'return_type':lambda t:[int(q) for q in t.split(',')]})
