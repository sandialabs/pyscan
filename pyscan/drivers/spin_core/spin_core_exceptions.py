from ...general.item_attribute import ItemAttribute
from ..exceptions.external_package_excpetion import ExternalPackageException


class SpinAPIException(ItemAttribute):

    def __init__(self, *arg, **kwarg):

        msg = "Spin Core Spin API not found, could not load this driver"

        raise ExternalPackageException(msg)
