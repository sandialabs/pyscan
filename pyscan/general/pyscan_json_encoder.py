import json
import numpy as np
from ..general.item_attribute import ItemAttribute
from ..drivers.instrument_driver import InstrumentDriver
from ..drivers.property_settings.abstract_property_settings import AbstractPropertySettings
from pyvisa.resources import (
    # FirewireInstrument,
    GPIBInstrument,
    # PXIInstrument,
    SerialInstrument,
    TCPIPInstrument,
    USBInstrument,
    # VXIInstrument,
)
import inspect
from pathlib import Path, WindowsPath


class PyscanJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder subclass that extends json.JSONEncoder to handle additional Python data types
    not supported by the default JSON encoder. This includes handling of custom objects, numpy data types,
    function objects, and pathlib Path objects, among others.

    The encoder attempts to serialize various non-standard objects to a JSON-compatible format, applying
    specific conversions based on the object type. If an object is already JSON serializable, the encoder
    falls back to the default method provided by the superclass.
    """

    def default(self, obj, debug=False):
        """
        Convert non-serializable objects to a serializable format.

        Parameters:
        - obj: The object to serialize.

        Returns:
        - A serializable representation of `obj` or raises a TypeError if the object cannot be serialized.
        """
        if debug is True:
            print(f"Processing object {obj} of type: {type(obj)}")
            try:
                print(f"Obj name is: {obj.__name__}")
            except:
                pass
        # keys_to_skip = {'logger', 'expt_thread', 'data_path', 'instrument', 'module_id_string', 'spec'}

        if type(obj) is type:
            return obj.__name__
        elif isinstance(obj, (InstrumentDriver, ItemAttribute, AbstractPropertySettings)):
            return obj.__dict__
        elif isinstance(obj, (range, tuple)):
            return list(obj)
        # Handle numpy integers
        elif isinstance(obj, np.integer):
            return int(obj)
        # Handle numpy floating values
        elif isinstance(obj, np.floating):
            return float(obj)
        # Handle numpy arrays
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif callable(obj):
            return inspect.getsource(obj)
        elif isinstance(obj, (WindowsPath, Path)):
            return str(obj)
        elif type(obj) is type(iter(range(1))):
            return list(obj)
        elif isinstance(
            obj,
            (# FirewireInstrument,
             GPIBInstrument,
             # PXIInstrument,
             SerialInstrument,
             TCPIPInstrument,
             USBInstrument,
             # VXIInstrument)
            )
        ):
            if debug is True:
                print(f"obj {obj} is a pyvisa instrument, returning resource name.")
            return obj.resource_name
        else:
            return super().default(obj)
