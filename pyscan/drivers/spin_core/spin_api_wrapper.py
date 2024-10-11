from ctypes import (
    c_char_p,
    c_double,
    c_int,
    CDLL)

try:
    spinapi = CDLL("spinapi64")
except:
    spinapi = CDLL("spinapi")

get_version = spinapi.pb_get_version
get_version.restype = (c_char_p)

get_error = spinapi.pb_get_error
get_error.restype = (c_char_p)

count_boards = spinapi.pb_count_boards
count_boards.restype = (c_int)

init = spinapi.pb_init.restype
init.restype = (c_int)

select_board = spinapi.pb_select_board
select_board.argtype = (c_int)
select_board.restype = (c_int)

set_debug = spinapi.pb_set_debug
set_debug.argtype = (c_int)
set_debug.restype = (c_int)

set_defaults = spinapi.pb_set_defaults
set_defaults.restype = (c_int)

core_clock = spinapi.pb_core_clock
core_clock.argtype = (c_double)
core_clock.restype = (c_int)

write_register = spinapi.pb_write_register
write_register.argtype = (c_int, c_int)
write_register.restype = (c_int)

start_programming = spinapi.pb_start_programming
start_programming.argtype = (c_int)
start_programming.restype = (c_int)

stop_programming = spinapi.pb_stop_programming
spinapi.pb_stop_programming.restype = (c_int)

start = spinapi.pb_start
start.restype = (c_int)

stop = spinapi.pb_stop
stop.restype = (c_int)

reset = spinapi.pb_reset
reset.restype = (c_int)

close = spinapi.pb_close
close.restype = (c_int)

inst_pbonly = spinapi.pb_inst_pbonly
inst_pbonly.argtype =\
    (c_int,  # flags
     c_int,  # inst
     c_int,  # inst_data
     c_double)  # timing value)
inst_pbonly.restype = (c_int)
