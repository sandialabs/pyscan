import json
import numpy as np
from pyscan.general.item_attribute import ItemAttribute
from pyscan.drivers.instrument_driver import InstrumentDriver
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
        elif isinstance(obj, (InstrumentDriver, ItemAttribute)):
            if debug is True:
                print(f"obj {obj} was instance of InstrumentDriver and or ItemAttribute.")
            return obj.__dict__
        elif isinstance(obj, (range, tuple)):
            if debug is True:
                print(f"obj {obj} was instance of {type(obj)}.")
            return list(obj)
        # Handle numpy integers
        elif isinstance(obj, np.integer):
            if debug is True:
                print(f"Object {obj} is a numpy integer, converting to int.")
            return int(obj)
        # Handle numpy floating values
        elif isinstance(obj, np.floating):
            if debug is True:
                print(f"Object {obj} is a numpy floating value, converting to float.")
            return float(obj)
        # Handle numpy arrays
        elif isinstance(obj, np.ndarray):
            if debug is True:
                print(f"Object {obj} is a numpy array, converting to list.")
            return obj.tolist()
        elif callable(obj):
            if debug is True:
                print(f"obj {obj} is a function, returning source code.")
            return inspect.getsource(obj)  # Talk with Andy about this and perhaps implementing in load_expt?
        elif isinstance(obj, (WindowsPath, Path)):  # This covers both WindowsPath and PosixPath
            if debug is True:
                print(f"obj {obj} is a Path or WindowsPath, returning string of the path.")
            return str(obj)
        else:
            return super().default(obj)
