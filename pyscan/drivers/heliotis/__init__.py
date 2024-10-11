import sys

name = 'libHeLIC'

if name in sys.modules:
    from .helioscamera import HeliosCamera
else:
    from .exceptions import HeliosImportException as HeliosCamera
