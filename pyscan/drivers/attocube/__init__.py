import sys

name = 'pylablib'

if name in sys.modules:
    from .attocubeANC350 import AttocubeANC350
else:
    from .attocube_exceptions import PylabLibMissingException as AttocubeANC350
