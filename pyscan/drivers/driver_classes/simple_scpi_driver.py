from .abstract_driver import AbstractDriver
from ..new_instrument import new_instrument
from ..property_settings.property_settings import PropertySettings


class SimpleSCPIDriver(AbstractDriver):
    '''
    Attributes
    ----------
    (Properties)
    test : int
        Just a test property
    '''

    def __init__(self, instrument, debug=False):
        if isinstance(instrument, str):
            self.instrument = new_instrument(instrument)
        else:
            self.instrument = instrument

        try:
            inst_str = str(type(self.instrument))
            self._driver_class = inst_str.split("'")[1].split(".")[-1]
        except Exception:
            pass

        self.property_class = PropertySettings

        self.debug = debug

    def query(self, settings):
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

        string = settings.query_string

        return self.instrument.query(string)

    def write(self, settings, value):
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

        string = settings.format_write_string(value)

        self.instrument.write(string)

    def read(self):
        '''
        Wrapper to read string from the instrument object

        Returns
        -------
        str
            Message read from the instrument

        '''

        return self.instrument.read()
