import json
import numpy as np


class CustomJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder subclass that extends json.JSONEncoder to provide
    serialization for additional Python data types not supported by the default
    JSON encoder.

    This encoder is capable of handling the following data types directly:
    - NoneType: Serialized to JSON null.
    - Callable objects: Serialized by their name using the __name__ attribute.
    - Objects with a __dict__ attribute: Serialized as dictionaries, excluding
      specified keys to skip.
    - Dictionaries: Serialized as JSON objects, excluding specified keys to skip.
    - Lists: Serialized as JSON arrays.
    - Range and Tuple: Serialized as lists by converting them to lists.
    - Boolean, String, Integer, and Float: Serialized to their corresponding JSON types.
    - Numpy integers and floating values: Serialized by converting them to Python
      int or float types.
    - Numpy arrays: Serialized as lists by converting them using the tolist() method.

    Attributes that are not directly serializable and not explicitly handled will
    be passed to the super().default() method, which may raise a TypeError if the
    type is not supported.

    Parameters:
    - obj (any): The object to serialize.

    Returns:
    - The serialized object, ready for JSON encoding.

    Note:
    - Certain keys can be skipped during the serialization of objects with __dict__
      attributes by adding them to the `keys_to_skip` set.
    """

    def default(self, obj):
        # Print the type of the object being processed for debugging
        # print(f"Processing object type: {type(obj)}")

        keys_to_skip = {'logger', 'expt_thread', 'data_path', 'instrument', 'module_id_string', 'spec'}

        if obj is None:
            # Explicitly handle None, although this should be handled by the default encoder
            # print("Object is None, which is serializable by default.")
            return obj
        if hasattr(obj, "__call__"):
            # print(f"Object is callable, returning name: {obj.__name__}")
            return obj.__name__
        elif hasattr(obj, "__dict__"):
            # print("Object has __dict__, processing dictionary items...")
            return {k: self.default(v) for k, v in obj.__dict__.items() if k not in keys_to_skip}
        elif isinstance(obj, dict):
            # Handle dictionaries explicitly
            # print("Object is a dictionary, processing dictionary items...")
            return {k: self.default(v) for k, v in obj.items() if k not in keys_to_skip}
        elif isinstance(obj, list):
            # Handle lists explicitly
            # print("Object is a list, processing list items...")
            return [self.default(item) for item in obj]
        elif isinstance(obj, (range, tuple)):
            # Handle range objects by converting them to lists
            # print("Object is a range or tuple, converting to list")
            return list(obj)
        elif isinstance(obj, (bool, str, int, float)):
            return obj
        # Handle numpy integers
        elif isinstance(obj, (np.integer, np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64,
                              np.uint8, np.uint16, np.uint32, np.uint64)):
            # print("Object is a numpy integer, converting to int")
            return int(obj)
        # Handle numpy floating values
        elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            # print("Object is a numpy floating value, converting to float")
            return float(obj)
        # Handle numpy arrays
        elif isinstance(obj, np.ndarray):
            # print("Object is a numpy array, converting to list")
            return obj.tolist()
        else:
            # print(f"Attempting to use super().default for object {obj} of type {type(obj)}")
            return super().default(obj)
