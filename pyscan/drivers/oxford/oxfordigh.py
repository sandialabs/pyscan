# -*- coding: utf-8 -*-
from ..instrument_driver import InstrumentDriver


class OxfordIGH(InstrumentDriver):

    def __init__(self, instrument):

        # super().__init__(instrument)

        self.instrument = instrument
        self.instrument.read_termination = '\r'
        self.instrument.write_termination = '\r'
        self.set_remote_unlocked()

        self.debug = False
        self._version = "0.1.0"

        self.initialize_properties()

    def initialize_properties(self):
        pass

    def set_local_locked(self):
        self.write('C0')

    def set_remote_lock(self):
        self.query('C1')

    def set_local_unlocked(self):
        self.query('C2')

    def set_remote_unlocked(self):
        self.query('C3')

    def get_mc_temperature(self):
        # R3 reads the full range to 1 mK
        # R32 reads the low temperature range to 0.1 mK
        result = self.query('R32')
        temperature = float(result[2:]) / 10000

        return temperature

    def get_status(self):

        status = self.query_until_return('X')
        return status

    def query_until_return(self, query, n=10):

        message = self.query(query)

        for i in range(n):

            if len(message) != 0:
                return message
            else:
                message = self.query('&')
