from ...general.item_attribute import ItemAttribute
from ..exceptions.external_package_excpetion import ExternalPackageException


class PylabLibMissingException(ItemAttribute):

    def __init__(self, *arg, **kwarg):

        msg = "pylablib module not found in sys.modules, could not load this driver\n"
        msg += "re-install pyscan or pip install pylablib"

        raise ExternalPackageException(msg)
