# -*- coding: utf-8 -*-
from .abstract_driver import AbstractDriver
from ..new_instrument import new_instrument


class InstrumentDriver(AbstractDriver):
    '''
    Driver for SCPI type communications with instruments

    Parameters
    ----------
    instrument : string or pyvisa :class:`Resource`
        visa string or an instantiated instrument

    Methods
    -------
    query(string)
    query_property(settings_obj)
    write(string)
    write_property(settings_obj)
    read()
    find_first_key(dictionary, machine_value)

    Inherited Methods
    add_device_property(settings_dict)
    get_instrument_property()
    set_values_property()
    set_range_property()
    set_index_values_property()
    set_dict_values_property()
    get_pyscan_properties()
    get_property_docstring(prop_name)
    '''

    def __init__(self, instrument):
        if isinstance(instrument, str):
            self.instrument = new_instrument(instrument)
        else:
            self.instrument = instrument

        try:
            inst_str = str(type(self.instrument))
            self._driver_class = inst_str.split("'")[1].split(".")[-1]
        except Exception:
            pass

        self._instrument_driver_version = '0.2.0'

    def query(self, string):
        '''
        Wrapper to pass string to the instrument object

        Parameters
        ----------
        string: str
            The message to send to the device

        Returns
        -------
        str
            Answer from the device.
        '''

        return self.instrument.query(string)

    def query_property(self, settings_obj):
        '''
        Wrapper to pass string to the instrument object

        Parameters
        ----------
        settings_obj: PropertySettings subclass
            RangeSettings, ValuesSettings, IndexedValuesSettings, or DictValuesSettings instance

        Returns
        -------
        str
            Answer from the device.
        '''

        value = self.instrument.query(settings_obj.query_string)

        return self.format_query_return(self, value)

    def write(self, string):
        '''
        Wrapper to write string to the instrument object

        Parameters
        ----------
        string: str
            The message to be sent

        Returns
        -------
        None
        '''

        self.instrument.write(string)

    def write_property(self, settings_obj, new_value):
        '''
        Format 'new_value' from settings and send to instrument

        Parameters
        ----------
        settings_obj : PropertySettings subclass
            RangeSettings, ValuesSettings, IndexedValuesSettings, or DictValuesSettings instance
        new_value: str, int, or float
            New value to be set on the instrument

        Returns
        -------
        None
        '''

        value = settings_obj.format_write_value(new_value)

        self.instrument.write(settings_obj.write_string.format(value))

        setattr(self, settings_obj._name, new_value)

    def read(self):
        '''
        Wrapper to read string from the instrument object

        Returns
        -------
        str
            Message read from the instrument

        '''

        return self.instrument.read()

    def validate_subclass_settings(self, settings_dict):
        '''
        For ScPIPropertySettings, ensures that write_string, query_string, read_only, and write_only
        are configured properly

        Parameters
        ----------
        settings_dict : dict
            Dictionary of settings that generate a pyscan device property object

        '''

        settings_keys = list(settings_dict.keys())

        if 'read_only' in settings_keys:
            assert 'write_string' not in settings_keys, \
                f'{self.name} is set to "read_only", for "read_only" properties, "write_string" is an invalid key'
            assert 'query_string' in settings_keys, \
                f'{self.name} is missing a "query_string" key'
        elif 'write_only' in settings_keys:
            assert 'query_string' not in settings_keys, \
                f'{self.name} is set to "write_only", for "write_only" properties, "query_string" is an invalid key'
            assert 'write_string' in settings_keys, \
                f'{self.name} is missing a "write_string" key'
        else:
            assert 'query_string' in settings_keys, \
                f'{self.name} is missing a "query_string" key'
            assert 'write_string' in settings_keys, \
                f'{self.name} is missing a "write_string" key'
