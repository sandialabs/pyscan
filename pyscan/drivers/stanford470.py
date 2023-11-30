# -*- coding: utf-8 -*-
"""
Stanford470
===========
"""


from .instrumentdriver import InstrumentDriver


class Stanford470(InstrumentDriver):
    '''Class to control Stanford Research Systems SR470 - Laser shutters and controllers
    
    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument (return value
        from :func:`~pyscan.drivers.newinstrument.new_instrument`)

    Yields
    ------
    Properties which can be get and set:
        state : 
            Dict Values: {0: 'closed', 1: 'open'}
    '''

    def __init__(self, instrument):

        super().__init__(instrument)

        self.debug = False
        self.initialize_properties()

    def initialize_properties(self):

        # Modulation Commands

        self.add_device_property({
            'name': 'state',
            'write_string': 'STAT {}',
            'query_string': 'STAT',
            'dict_values': {0: 'closed', 1: 'open'},
            'return_type': dict})
