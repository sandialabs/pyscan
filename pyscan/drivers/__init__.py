# Objects
from .instrumentdriver import InstrumentDriver

# Instrument Drivers
from .agilent33500 import Agilent33500
from .agilent34410 import Agilent34410
from .agilentdso900series import AgilentDSO900Series
from .agilent8267d import AgilentE8267D
from .agilent8275n import Agilent8275N
from .americanmagnetics430 import AmericanMagnetics430
from .blueforslog import BlueForsLog
from .bkprecision9130b import BKPrecision9130B, BKHelmholtz
from .hp34401a import HP34401A
from .keithley2400 import Keithley2400
from .kepcoBOP import KepcoBOP
from .keysitem3302adaq import KeysiteM3302ADAQ
from .keysitem3302aawg import KeysiteM3302AAWG
from .keysite53230a import Keysite53230A
from .oxfordips120 import OxfordIPS120
from .pulselaser import PulseLaser
from .stanford396 import Stanford396
from .stanford400 import Stanford400
from .stanford470 import Stanford470
from .stanford620 import Stanford620
from .stanford830 import Stanford830
from .stanford860 import Stanford860
from .stanford900 import Stanford900
from .stanford928 import Stanford928
from .stanford928 import stanford928 # deprecated, here for backwards compat.
from .tpi1002a import TPI1002A
from .yokogawags200 import YokogawaGS200
from .actonsp2300 import ActonSP2300

try:
    from .baslercamera import BaslerCamera
except ModuleNotFoundError:
    print('Basler Camera software not found, BaserCamera not loaded')

try:
    from .helios import HeliosCamera
except ModuleNotFoundError:
    print('Helios Camera not installed')

try:
    from .bsc203 import BSC203
except ModuleNotFoundError:
    print('msl not installed, Thorlabs BSC203 driver not loaded')
    
try:
    from .oceanopticsqepro import OceanOpticsQEPro
except ModuleNotFoundError:
    print('seabreeze module not found, Ocean Optics not imported')
try:
    from .pulseblaster import PulseBlaster
    from .pulseblasternv import NVPulseBlaster
except NameError:
    print('spinapi is not installed, PulseBlaster driver not loaded.')
try:
    from .thorlabsbsc203 import ThorlabsBSC203
except ModuleNotFoundError:
    print('Thorlabs Kinesis not found, ThorlabsBSC203 not loaded')
try:
    from .thorlabsbpc303 import ThorlabsBPC303
    from .thorlabsbpc303 import ThorlabsBSC303 # deprecated, here for backwards compat.
except ModuleNotFoundError:
    print('Thorlabs Kinesis not found, ThorlabsBPC303 not loaded')
try:
    from .thorlabsmff101 import ThorlabsMFF101
except ModuleNotFoundError:
    print('Thorlabs Kinesis not found, ThorlabsMFF101 not loaded')

# Methods
from .newinstrument import new_instrument

# Test Devices
from .testvoltage import TestVoltage
