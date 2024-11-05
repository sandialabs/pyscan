import sys

name = 'libHeLIC'

try:
    import libHeLIC
    from .helioscamera import HeliosCamera
except ModuleNotFoundError:
    from .helios_exceptions import HeliosImportException as HeliosCamera
