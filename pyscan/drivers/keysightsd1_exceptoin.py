from itemattribute import ItemAttribute
from .exceptions.external_package_excpetion import ExternalPackageException

class KeysightSD1Error(ItemAttribute):

    def __init__(self):

        msg = "Keysight SD1 not found could not load this driver"

        raise ExternalPackageException(msg)