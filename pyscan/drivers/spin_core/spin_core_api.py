from ...general.item_attribute import ItemAttribute
import ctypes
from . import spin_api_wrapper as pb


PULSE_PROGRAM = 0
FREQ_REGS = 1


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


class SpinCoreAPI(ItemAttribute):
    '''
    Driver for PulseblasterESRPro Cards

    Parameters
    ----------
    clock : int
        Clock frequency in MHz, defaults to 500
    board : int
        Index of board, defaults to 0

    Methods
    -------
    init_pb()
        Initializes the pluse blastert
    get_error()
        Returns the error code
    count_boards()
        Returns the number of boards in the system
    init()
        Initilizes the currently selected board
    set_debug(debug)
        Sets debug mode parameter
    select_board(board_number)
        Selects the board to be used
    set_defaults()
        Sets board defauts, bust be called when using any ohter board functions
    core_clock(clock)
        Sets the core clock of the currently selected board
    write_register(address, value)
        Writes value at register at address
    start_programming()
        Starts the programming of the pulse sequence
    stop_programming()
        Stops the progamming of the pulse sequence
    inst(*args)
        Adds an instruction to the program
    start()
        Starts running the pulse program
    stop()
        Stops running the pulse program
    reset()
        Resets the pulse program
    close()
        Close the connection to the pulse blaster
    instruction(instruction)
        Converts an instruction string to an int
    # Multi setting methods
    setup_single_ttl(ttl_chans, always_on_chans, total_time, ttl_time)
        Programs a single pulse on ttl_chans for ttl_time seconds,
        with some channels always on for total_time, seconds
    '''

    def __init__(self, clock, board=0, debug=False, **kwarg):

        for key, value in kwarg.items():
            self[key] = value

        self._version = "0.1.0"

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
        ret = pb.get_error()
        return str(ctypes.c_char_p(ret).value.decode("utf-8"))

    def count_boards(self):
        """Return the number of boards detected in the system."""
        return pb.count_boards()

    def init(self):
        """Initialize currently selected board."""
        return pb.init()

    def set_debug(self, debug):
        return pb.set_debug(debug)

    def select_board(self, board_number):
        """Select a specific board number"""
        return pb.select_board(board_number)

    def set_defaults(self):
        """
        Set board defaults. Must be called before using any other board functions.
        """
        return pb.set_defaults()

    def core_clock(self, clock):
        return pb.core_clock(ctypes.c_double(clock))

    def write_register(self, address, value):
        return pb.write_register(address, value)

    def start_programming(self):
        return pb.start_programming(0)

    def stop_programming(self):
        return pb.stop_programming()

    def inst(self, *args):
        t = list(args)
        # Argument 13 must be a double
        t[-1] = ctypes.c_double(t[-1])
        args = tuple(t)
        return pb.inst_pbonly(*args)

    def start(self):
        return pb.start()

    def stop(self):
        return pb.stop()

    def reset(self):
        return pb.reset()

    def close(self):
        return pb.close()

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
