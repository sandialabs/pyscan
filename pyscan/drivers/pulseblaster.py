# -*- coding: utf-8 -*-
from pyscan.general.itemattribute import ItemAttribute
import ctypes

PULSE_PROGRAM = 0
FREQ_REGS = 1

try:
    spinapi = ctypes.CDLL("spinapi64")
except:
    try:
        spinapi = ctypes.CDLL("spinapi")
    except:
        print("Failed to load spinapi library.")
        pass


def enum(**enums):
    return type('Enum', (), enums)


ns = 1.0
us = 1000.0
ms = 1000000.0

MHz = 1.0
kHz = 0.001
Hz = 0.000001

# Instruction enum
Inst = enum(
    CONTINUE=0,
    STOP=1,
    LOOP=2,
    END_LOOP=3,
    JSR=4,
    RTS=5,
    BRANCH=6,
    LONG_DELAY=7,
    WAIT=8,
    RTI=9
)

spinapi.pb_get_version.restype = (ctypes.c_char_p)
spinapi.pb_get_error.restype = (ctypes.c_char_p)

spinapi.pb_count_boards.restype = (ctypes.c_int)

spinapi.pb_init.restype = (ctypes.c_int)

spinapi.pb_select_board.argtype = (ctypes.c_int)
spinapi.pb_select_board.restype = (ctypes.c_int)

spinapi.pb_set_debug.argtype = (ctypes.c_int)
spinapi.pb_set_debug.restype = (ctypes.c_int)

spinapi.pb_set_defaults.restype = (ctypes.c_int)

spinapi.pb_core_clock.argtype = (ctypes.c_double)
spinapi.pb_core_clock.restype = (ctypes.c_int)

spinapi.pb_write_register.argtype = (ctypes.c_int, ctypes.c_int)
spinapi.pb_write_register.restype = (ctypes.c_int)

spinapi.pb_start_programming.argtype = (ctypes.c_int)
spinapi.pb_start_programming.restype = (ctypes.c_int)

spinapi.pb_stop_programming.restype = (ctypes.c_int)

spinapi.pb_start.restype = (ctypes.c_int)
spinapi.pb_stop.restype = (ctypes.c_int)
spinapi.pb_reset.restype = (ctypes.c_int)
spinapi.pb_close.restype = (ctypes.c_int)

spinapi.pb_inst_pbonly.argtype =\
    (ctypes.c_int,  # flags
     ctypes.c_int,  # inst
     ctypes.c_int,  # inst_data
     ctypes.c_double)  # timing value)

spinapi.pb_inst_pbonly.restype = (ctypes.c_int)


class PulseBlaster(ItemAttribute):

    def __init__(self, clock=500, board=0, debug=False, **kwarg):

        for key, value in kwarg.items():
            self[key] = value

        self.clock = clock
        self.board = board
        self.debug = debug

        self.init_pb()

    def init_pb(self):
        if self.debug:
            self.set_debug(1)
        else:
            self.set_debug(0)
        self.select_board(self.board)
        self.init()
        self.core_clock(self.clock)

    def get_error(self):
        ret = spinapi.pb_get_error()
        return str(ctypes.c_char_p(ret).value.decode("utf-8"))

    def count_boards(self):
        """Return the number of boards detected in the system."""
        return spinapi.pb_count_boards()

    def init(self):
        """Initialize currently selected board."""
        return spinapi.pb_init()

    def set_debug(self, debug):
        return spinapi.pb_set_debug(debug)

    def select_board(self, board_number):
        """Select a specific board number"""
        return spinapi.pb_select_board(board_number)

    def set_defaults(self):
        """
        Set board defaults. Must be called before using any other board functions.
        """
        return spinapi.pb_set_defaults()

    def core_clock(self, clock):
        return spinapi.pb_core_clock(ctypes.c_double(clock))

    def write_register(self, address, value):
        return spinapi.pb_write_register(address, value)

    def start_programming(self):
        return spinapi.pb_start_programming(0)

    def stop_programming(self):
        return spinapi.pb_stop_programming()

    def inst(self, *args):
        t = list(args)
        # Argument 13 must be a double
        t[-1] = ctypes.c_double(t[-1])
        args = tuple(t)
        return spinapi.pb_inst_pbonly(*args)

    def start(self):
        return spinapi.pb_start()

    def stop(self):
        return spinapi.pb_stop()

    def reset(self):
        return spinapi.pb_reset()

    def close(self):
        return spinapi.pb_close()

    def instruction(self, instruction):
        instruction = instruction.lower()

        if instruction == 'continue':
            return 0
        elif instruction == 'stop':
            return 1
        elif instruction == 'loop':
            return 2
        elif instruction == 'end_loop':
            return 3
        elif instruction == 'jsr':
            return 4
        elif instruction == 'rts':
            return 5
        elif instruction == 'branch':
            return 6
        elif instruction == 'long_delay':
            return 7
        elif instruction == 'wait':
            return 8
        elif instruction == 'rti':
            return 9
        else:
            print('Bad instruction')

    def setup_single_ttl(self,
                         ttl_chans=[],
                         always_on_chans=[],
                         total_time=1,
                         ttl_time=1e-6):

        self.stop()

        always_on = 0
        for chan in always_on_chans:
            always_on += 2**self[chan]

        ttl = 0
        for chan in ttl_chans:
            ttl += 2**self[chan]

        print(ttl, always_on)
        self.start_programming()
        self.inst(ttl + always_on, Inst.CONTINUE, 0, ttl_time * 1e9)
        self.inst(always_on, Inst.STOP, 0, total_time * 1e9)
        self.stop_programming()

        self.reset()
