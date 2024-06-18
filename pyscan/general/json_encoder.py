import json
import numpy as np


class CustomJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder subclassing json.JSONEncoder to handle additional data types.
    Used in pyscan to properly format data for json.dumps when saving metadata.

    This encoder extends the default JSONEncoder to support serialization of several
    additional Python data types, including NumPy data types and objects with a __dict__
    attribute, making it suitable for serializing more complex Python objects into JSON format.

    The encoder handles the following data types specifically:
    - None: Serialized as the string 'None'.
    - Boolean, String, Integer, Float: Serialized using the default JSON serialization.
    - Callable objects: Serialized by converting their __dict__ attribute using recursive_to_dict.
    - Dictionaries: Serialized using recursive_to_dict to handle nested dictionaries.
    - Classes (type objects): Serialized as is (may require custom handling).
    - NumPy integers and floats: Serialized as standard Python integers and floats.
    - NumPy arrays: Serialized as lists using the tolist() method.
    - Objects with a __dict__ attribute: Serialized by converting their __dict__ attribute using recursive_to_dict.
    - Iterators (excluding strings, bytes, and byte arrays): Serialized as lists.

    For any other data types not explicitly handled, the encoder falls back to the default
    JSONEncoder handling, which may raise a TypeError if the type is not serializable.

    Methods
    -------
    default(obj):
        Overridden method from json.JSONEncoder that specifies how to serialize the supported data types.

    recursive_to_dict(obj_dict):
        Helper method to recursively serialize objects and dictionaries, particularly useful for
        objects with nested dictionaries or __dict__ attributes.

    Example
    -------
    >>> import numpy as np
    >>> data = {
    ...     "numpy_int": np.int32(10),
    ...     "numpy_float": np.float64(3.14),
    ...     "numpy_array": np.array([1, 2, 3]),
    ...     "custom_object": CustomObject()
    ... }
    >>> encoded_str = json.dumps(data, cls=CustomJSONEncoder)
    """

    def default(self, obj):
        if obj is None:
            return 'None'
        elif isinstance(obj, (bool, str, int, float)):
            return obj
        elif hasattr(obj, '__call__'):
            return self.recursive_to_dict(obj.__dict__)
        elif isinstance(obj, dict):
            return self.recursive_to_dict(obj)
        elif isinstance(obj, type):
            return obj
        # Handle numpy integers
        elif isinstance(obj, (np.integer, np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64,
                              np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        # Handle numpy floating values
        elif isinstance(obj, (np.floating, np.float16, np.float32, np.float64)):
            return float(obj)
        # Handle numpy arrays
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        # Handle objects with a __dict__ attribute
        elif hasattr(obj, "__dict__"):
            return self.recursive_to_dict(obj.__dict__)
        # Handle iterators (excluding strings, bytes, and byte arrays)
        elif hasattr(obj, "__iter__"):
            return list(obj)
        # Fallback: use the base class handling, which handles strings and types serializable by default json encoder
        else:
            return super().default(obj)

    def recursive_to_dict(self, obj_dict):
        new_dict = {}

        for key, value in obj_dict.items():
            # print(key, value)
            # is method/function
            if key in ['logger', 'expt_thread', 'data_path',
                       'instrument', 'module_id_string', 'spec']:
                pass
            elif hasattr(value, '__call__'):
                new_dict[key] = value.__name__
            elif isinstance(value, str):
                new_dict[key] = value
            # is a dict
            elif isinstance(value, dict):
                new_dict[key] = self.recursive_to_dict(value)
            # if it is a np integer
            elif isinstance(value, (np.integer, np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64,
                                    np.uint8, np.uint16, np.uint32, np.uint64)):
                new_dict[key] = int(value)
            # if it is a np floating value
            elif isinstance(value, (np.floating, np.float_, np.float16, np.float32, np.float64)):
                new_dict[key] = float(value)
            # if it is an np array
            elif isinstance(value, np.ndarray):
                new_dict[key] = value.tolist()
            # is an iterator
            elif hasattr(value, "__iter__"):
                new_dict[key] = list(value)
            # is an object
            elif hasattr(value, "__dict__"):
                new_dict[key] = self.recursive_to_dict(value.__dict__)
            # anything else
            else:
                new_dict[key] = value
                # maybe pass this, but test first

        return new_dict
