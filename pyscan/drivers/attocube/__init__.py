import sys

name = 'pylablib'
try:
    import pylablib
    from .attocubeANC350 import AttocubeANC350
except ModuleNotFoundError:
    from .attocube_exceptions import PylabLibMissingException as AttocubeANC350
