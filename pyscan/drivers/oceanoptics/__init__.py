import sys

# For illustrative purposes.
name = 'seabreeze'

if name in sys.modules:
    from .oceanopticsqepro import OceanOpticsQEPro
else:
    from .oceanoptics_exceptions import SeabreezeMissingException as OceanOpticsQEPro
