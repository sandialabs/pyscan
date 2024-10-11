from ...general.item_attribute import ItemAttribute
from ..exceptions.external_package_excpetion import ExternalPackageException


class HeliosImportException(ItemAttribute):

    def __init__(self, *arg, **kwarg):

        msg = "Helios SDK SD1 could not load this driver"

        raise ExternalPackageException(msg)
