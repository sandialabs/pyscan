import sys

# For illustrative purposes.
name = 'seabreeze'

try:
    import seabreeze
    from .oceanopticsqepro import OceanOpticsQEPro
except ModuleNotFoundError:
    from .oceanoptics_exceptions import SeabreezeMissingException as OceanOpticsQEPro
