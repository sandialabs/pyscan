try:
    from .picoharp300 import PicoHarp300
except OSError:
    from .exceptions import PicoQuantException as PicoHarp300
