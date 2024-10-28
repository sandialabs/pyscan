try:
    from .pulse_blaster_esrpro500 import PulseBlasterESRPro500
except OSError:
    from .spin_core_exceptions import SpinAPIException as PulseBlasterESRPro500
