try:
    from .picoharp300 import PicoHarp300
except OSError:
    from .picoquant_exceptions import PicoQuantException as PicoHarp300
