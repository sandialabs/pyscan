try:
    from .pulse_blaster_esrpro500 import PulseBlasterESRPro500
    from .nv_pulse_blaster import NVPulseBlaster
except OSError:
    from .spin_core_exceptions import SpinAPIException as PulseBlasterESRPro500
