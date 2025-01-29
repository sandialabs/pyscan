import os


try:
    if os.path.exists(r'c:\Program Files (x86)\Keysight\SD1\Libraries\Python'):
        from .keysightm3302adaq import KeysightM3302ADAQ
        from .keysightm3302aawg import KeysightM3302AAWG
    else:
        from .keysite_exceptions import KeysightSD1Error as KeysightM3302ADAQ
        from .keysite_exceptions import KeysightSD1Error as KeysightM3302AAWG
except FileNotFoundError:
    from .keysite_exceptions import KeysightSD1Error as KeysightM3302ADAQ
    from .keysite_exceptions import KeysightSD1Error as KeysightM3302AAWG

from .keysight53230a import Keysight53230A
