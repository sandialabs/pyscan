from ctypes import c_char_p


def string_buffer_to_str(sb):
    return c_char_p(sb.raw).value.decode('ascii')


def string_buffer_to_c_char(sb):
    return c_char_p(sb.raw)
