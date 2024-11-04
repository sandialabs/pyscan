from .thorlabsitc4001 import ThorLabsITC4001
import importlib.util
import sys

try:
    import pyscan_tlk
    from .thorlabsbpc303 import ThorlabsBPC303
    from .thorlabsbsc203 import ThorlabsBSC203
    from .thorlabsmff101 import ThorlabsMFF101
except ModuleNotFoundError:
    from .thorlabs_exceptions import ThorlabsKinesisImportException as ThorlabsBPC303
    from .thorlabs_exceptions import ThorlabsKinesisImportException as ThorlabsBSC203
    from .thorlabs_exceptions import ThorlabsKinesisImportException as ThorlabsMFF101
