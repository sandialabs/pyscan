from itemattribute import ItemAttribute
from ..exceptions.external_package_excpetion import ExternalPackageException


class SeabreezeMissingException(ItemAttribute):

    def __init__(self, *arg, **kwarg):

        msg = "seabreeze module not found in sys.modules, could not load this driver\n"
        msg += "re-install pyscan or pip install seabreeze"

        raise ExternalPackageException(msg)
