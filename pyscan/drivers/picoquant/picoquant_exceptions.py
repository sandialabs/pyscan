from ...general.item_attribute import ItemAttribute
from ..exceptions.external_package_excpetion import ExternalPackageException


class PicoQuantException(ItemAttribute):

    def __init__(self, *arg, **kwarg):

        msg = "PicoQuant dlls not found, driver not loaded"

        raise ExternalPackageException(msg)
