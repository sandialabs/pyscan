from .thorlabsitc4001 import ThorLabsITC4001
import importlib.util
import sys

name = 'thorlabs_kinesis'


if name in sys.modules:
    from .thorlabsbpc303 import ThorlabsBPC303
    from .thorlabsbsc203 import ThorlabsBSC203
    from .thorlabsmff101 import ThorlabsMFF101
else:
    from .thorlabs_exceptions import ThorlabsKinesisImportException as ThorlabsBPC303
    from .thorlabs_exceptions import ThorlabsKinesisImportException as ThorlabsBSC203
    from .thorlabs_exceptions import ThorlabsKinesisImportException as ThorlabsMFF101
