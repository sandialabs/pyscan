from ...general.item_attribute import ItemAttribute
from ..exceptions.external_package_excpetion import ExternalPackageException


class ThorlabsKinesisImportException(ItemAttribute):

    def __init__(self, *arg, **kwarg):

        msg = "Thorlabs Kinesis Drivers not found could not load this driver"

        raise ExternalPackageException(msg)
