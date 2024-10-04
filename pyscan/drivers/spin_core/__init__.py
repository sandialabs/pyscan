try:
    from .pulse_blaster_esrpro500 import PulseBlasterESRPro500
except OSError:
    from .exceptions import SpinAPIException as PulseBlasterESRPro500