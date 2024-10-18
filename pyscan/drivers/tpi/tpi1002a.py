# -*- coding:utf-8 -*-
from struct import unpack
from ..instrument_driver import InstrumentDriver
from pyvisa.errors import VisaIOError


def print_error(errcode):
    print("TPI Error: %s"
          % ['Checksum error', 'Undefined command type (first body byte)',
             'Undefined command (second body byte)', 'Data out of range',
             'Illegal beacon message character',
             'Requested RF level < -90 dBm',
             'Internal beacon message length error',
             'Unknown script command',
             'No detector available',
             'No auxiliary input available',
             'No trigger output available',
             'Communication watchdog timeout',
             'Failed to write EEPROM',
             'Failed to read EEPROM'][errcode])
    return


def check_errors(fn):
    def wrapper(*args, **kwargs):
        retval = fn(*args, **kwargs)
        if retval[:2] == b'\x07\xff':
            errorcode = int(retval[3].hex(), 16) - 1
            print_error(errorcode)
        return retval[2:]
    return wrapper


class TPI1002A(InstrumentDriver):
    '''
    Class to control Trinity Power Incorporated TPI-1002-A Signal Generator.

    Parameters
    ----------
    instrument :
        Visa string or an instantiated instrument

    Attributes
    ----------
    (Properties)
    user_control :
        Values: [0,1]. 0 is False, 1 is True.
    output :
        Values':[0,1]. 0 is False, 1 is True.
    frequency : int
        Frequency in kHz. Range: [35000,4400000].
    amplitude : int
        Range: [-70,10]
    model_number : str
        Model number of device
    serial_number : str
        Serial number of device
    hardware_version : str
        Hardware version of device
    firmware_version : str
        Firmware version of device
    supply_voltages :
        Not tested
    state : str
        State
    '''

    def __init__(self, instrument):
        super().__init__(instrument)

        self.debug = False
        self._version = "0.1.0"
        self.instrument.baud_rate = 3000000
        self.initialize_properties()
        self.user_control = 1

    def query(self, instruction_code, return_bytes=None):
        self.write(instruction_code)
        if return_bytes is not None:
            return self.read(return_bytes)

    def write(self, instruction_code):
        self.instrument.write_raw(self.instruction_packet(instruction_code))

    def read(self, return_bytes=None, raw=False):
        """
        Set nbytes (without header/checksum) to expected number of bytes.
        If you're right, things will be fast.  If you're wrong, comm will be out of sync.
        """
        if return_bytes is not None:
            packet = self.instrument.read_bytes(return_bytes + 5)
            checksum = self.packet_checksum(packet[:-1])
            if checksum != packet[-1]:  # we done goofed
                if packet[:2] != b'\xaa\x55':
                    print("Error: Communication out of sync.")
                    return -1   # No point in returning a value
                nbytes = int(packet[2:4].hex(), 16)
                if nbytes != return_bytes:
                    print("Warning: Wrong number of bytes; expected %i, got %i.  Flushing!" % (return_bytes, nbytes))
                    self.flush()
                    return -1
        else:
            header = self.instrument.read_bytes(4)
            if header[:2] != b'\xaa\x55':
                print("Error: Communication out of sync.")
                # sync comm
                return
            nbytes = int(header[2:].hex(), 16)
            rest = self.instrument.read_bytes(nbytes + 1)
            checksum = self.packet_checksum(header + rest[:-1])
            if rest[-1] != checksum:
                print("Error: checksum does not match:\n\t%s" % (header + rest))
            packet = header + rest
        return packet if raw else packet[4:-1]

    def flush(self):
        """flush all readable bytes and return them--slow as it relies on timeout."""
        ret = b''
        while True:
            try:
                ret += self.instrument.read_bytes(1)
            except VisaIOError:
                break
        return ret

    def get_instrument_property(self, obj, settings, debug=False):
        value = obj.query(settings['query_string'], return_bytes=None if 'return_bytes' not in
                          settings else settings['return_bytes'] + 2)
        if settings['query_string'].lower() != value[:2].hex():
            if value[:2] == '\x07\xff':  # error
                print_error(value[3].hex() - 1)
                self.get_instrument_property(obj, settings, debug=debug)  # having popped the error, try again
            print("Error: Response was to another command.")
            return -1
        setattr(obj, '_' + settings['name'], settings['return_type'](value[2:]))
        return settings['return_type'](value[2:])

    @check_errors  # unfortunately TPI tends to send back the "ok" code, then the error (when we don't read it).
    def set_values_property(self, obj, new_value, settings):
        values = settings['values']
        if new_value not in values:
            print('Value error: %s must be one of %s' % (settings['name'], ', '.join(str(values))))
            return
        retval = self.query(settings['write_string'].format(new_value) if
                            'send_type' not in settings else
                            settings['write_string'].format(settings['send_type'](new_value)),
                            return_bytes=settings['ok_bytes'] + 2 if 'ok_bytes' in settings else None)
        return retval

    @check_errors
    def set_range_property(self, obj, new_value, settings):
        rng = settings['range']

        if not (rng[0] <= new_value <= rng[1]):
            print('Range error: {} must be between {} and {}.'.format(settings['name'], rng[0], rng[1]))
            return -1
        retval = self.query(settings['write_string'].format(new_value) if 'send_type' not in
                            settings else settings['write_string'].format(settings['send_type'](new_value)),
                            return_bytes=settings['ok_bytes'] + 2 if 'ok_bytes' in settings else None)
        setattr(self, '_' + settings['name'], new_value)

        return retval

    def initialize_properties(self):
        self.add_device_property({
            'name': 'user_control',
            'write_string': '0801',
            'query_string': '0701',
            'return_bytes': 1,
            'return_type': lambda x: {'00': False, '01': True}[x.hex()],
            'ok_bytes': 0,
            'values': [0, 1]})

        self.add_device_property({
            'name': 'output',
            'write_string': '080B{:02d}',
            'query_string': '070B',
            'return_bytes': 1,
            'return_type': lambda x: {'00': False, '01': True}[x.hex()],
            'ok_bytes': 0,
            'values': [0, 1]})

        self.add_device_property({
            'name': 'model_number',
            'query_string': '0702',
            'return_bytes': 16,
            'return_type': lambda x: x.decode('ASCII').strip()})

        self.add_device_property({
            'name': 'serial_number',
            'query_string': '0703',
            'return_bytes': 16,
            'return_type': lambda x: x.decode('ASCII').strip()})

        self.add_device_property({
            'name': 'hardware_version',
            'query_string': '0704',
            'return_bytes': 16,
            'return_type': lambda x: x.decode('ASCII').strip()})

        self.add_device_property({
            'name': 'firmware_version',
            'query_string': '0705',
            'return_bytes': 16,
            'return_type': lambda x: x.decode('ASCII').strip()})

        self.add_device_property({
            'name': 'supply_voltages',
            'query_string': '0707',
            'return_bytes': 24,
            'return_type': lambda x: {a: b for a, b in
                                      zip(['RF', 'VCO', 'MCU', 'OSC', 'PA', 'USB'], unpack('ffffff', x))}})

        def _get_state(x):
            """used in [state] property"""
            n0, n1 = x  # [int(w.hex(),16) for w in x]
            state = [
                'Generator',
                'Square modulation',
                'Beacon modulation',
                'Script modulation',
                'Scanning',
                'Control script'][n0]
            substate = ''
            if 1 <= n0 <= 3 and n1 > 0:
                substate = ' (auto RF on/off)'
            elif n0 == 4 and n1 == 2:
                substate = ' (paused)'
            elif n0 == 5 and n1 == 1:
                substate = ' (waiting)'
            return '%s%s' % (state, substate)

        self.add_device_property({
            'name': 'state',
            #  'write_string': '0808{:02x}{:02x}', # must shut down other states before running a state!
            #  'ok_bytes': 0,
            'query_string': '0708',
            'return_bytes': 2,
            'return_type': lambda x: _get_state(x)})

        self.add_device_property({
            'name': 'frequency',
            'query_string': '0709',
            'return_bytes': 4,
            'write_string': '0809{}',
            'ok_bytes': 0,
            'send_type': lambda x: self._int_to_hex(x, 4),
            'return_type': lambda x: self._bytes_to_int(x),
            'range': [35000, 4400000]})  # kHz

        self.add_device_property({
            'name': 'amplitude',
            'query_string': '070A',
            'return_bytes': 1,
            'ok_bytes': 1,
            'send_type': lambda x: self._int_to_hex(x, 1, signed=True),
            'return_type': lambda x: self._bytes_to_int(x, signed=True),
            'write_string': '080A{}',  # careful, will set to max/min if out of range
            'range': [-70, 10]})

    def instruction_packet(self, instruction):
        if isinstance(instruction, str):
            instruction = bytes.fromhex(instruction)
        header = b'\xaa\x55'
        ll = len(instruction)
        nbytes = '%02x%02x' % ((ll - (ll % (16 ** 2))), ll % (16 ** 2))
        nbytes = bytes.fromhex(nbytes)
        instruction_packet = header + nbytes + instruction
        instruction_packet += bytes.fromhex('%02x' % self.packet_checksum(instruction_packet))
        return instruction_packet

    def packet_checksum(self, rawpacket):
        # todo: better way to complement
        hrawpqt = rawpacket[2:].hex()
        return (sum(-int(s, 16) for s in [hrawpqt[i:i + 2] for i in
                                          range(0, len(hrawpqt), 2)]) % 256 + int('ff', 16)) % 256
        # return bytes.fromhex('%02x' % ((sum(-int(s,16) for s in [hrawpqt[i:i+2] for i
        # in range(0,len(hrawpqt),2)])%256+int('ff',16))%256))

    def _int_to_hex(self, num, bytelen, signed=False):
        return num.to_bytes(length=bytelen, byteorder='little', signed=signed).hex()

    def _int_to_bytes(self, num, bytelen, signed=False):
        """LSB first"""
        return num.to_bytes(length=bytelen, byteorder='little', signed=signed)

    def _bytes_to_int(self, bytcode, signed=False):
        """LSB first [bytcode] is a bytes object."""
        test = int(''.join([bytcode.hex()[i:i + 2] for i in range(0, len(bytcode.hex()), 2)][::-1]), 16)

        if (not signed) and test != int.from_bytes(bytcode, byteorder='little', signed=signed):
            print("TPI DRIVER TEST: the functions in bytes_to_int do differ for value '%x'" % bytcode.hex())
        return int.from_bytes(bytcode, byteorder='little', signed=signed)
