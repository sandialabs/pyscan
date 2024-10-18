# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver
from time import sleep
import serial


class PulseLaser(InstrumentDriver):

    def __init__(self, com):
        print(com)
        self._version = "0.1.0"

        self.instrument = serial.Serial(port=com,
                                        baudrate=9600,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS,
                                        xonxoff=True,
                                        timeout=1,
                                        write_timeout=1
                                        )

    def set_cw(self):
        self.instrument.write('LAS\r'.encode())

    def set_ext(self):
        self.instrument.write('EXT\r'.encode())

    def set_off(self):
        self.instrument.write('*OFF\r'.encode())

    def set_stop(self):
        self.instrument.write('STOP\r'.encode())

    def set_reset(self):
        self.instrument.write('*RST\r'.encode())

    def set_on(self):
        self.instrument.write('*ON\r'.encode())

    def set_power(self, value):
        self.instrument.write('PWR{}\r'.format(value).encode())

    def get_power(self):
        self.instrument.write('PWR?\r'.encode())
        sleep(0.5)
        return self.instrument.read(self.instrument.in_waiting)
