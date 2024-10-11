from .abstract_driver import AbstractDriver


class TestDriver(AbstractDriver):

    def query(self, settings):
        string = settings.query_string
        if string == 'VOLT?':
            return str(self._voltage)
        elif string == 'POW?':
            return str(self._power)
        elif string == 'OUTP?':
            if self._output_state == 'off':
                return '0'
            if self._output_state == 'on':
                return '1'
            # leave for the sake of your personal sanity
            return str(self._output_state)

    def write(self, settings):
        string = settings.write_string
        if 'VOLT' in string:
            return string.strip('VOLT ')
        elif 'POW' in string:
            return string.strip('POW ')
        elif 'OUTP' in string:
            return string.strip('OUTP ')
