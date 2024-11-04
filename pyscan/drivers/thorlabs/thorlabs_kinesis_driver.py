from ..instrument_driver.abstract_driver import AbstractDriver
from .check_for_error import check_return_for_error
from ctypes import c_char_p


class ThorlabsKinesisDriver(AbstractDriver):

    def __init__(self, serial_number, debug=False):
        self.serial_number = c_char_p(bytes(str(serial_number), "utf-8"))

    def query_property(self, settings_obj):

        if 'channel' in settings_obj:
            ret = settings_obj.query_function(self.serial_number, settings_obj.channel)
        else:
            ret = settings_obj.query_function(self.serial_number)

        return ret

    def write_property(self, settings_obj, new_value):

        if 'channel' in settings_obj:
            ret = settings_obj.write_function(self.serial_number, settings_obj.channel, new_value)
        else:
            ret = settings_obj.write_function(self.serial_number, new_value)

        if settings_obj.check_for_error:
            check_return_for_error(ret)
        return ret

    def validate_subclass_settings(self, settings_obj):

        keys = settings_obj.__dict__.keys()

        if 'check_for_error' not in keys:
            settings_obj.check_for_error = False

        return settings_obj
