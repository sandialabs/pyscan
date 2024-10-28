from ...general.get_pyscan_version import get_pyscan_version
from .test_properties import (
    test_values_property,
    test_range_property,
    test_indexed_property,
    test_dict_values_property,
    test_read_only_property)
from ..property_settings import (
    ValuesPropertySettings, RangePropertySettings, IndexedPropertySettings,
    DictPropertySettings)
from .check_initial_state import check_initial_state
import os
from datetime import datetime
import re
import pprint

'''
WARNING!
If used without first creating a proper blacklist of _properties that cannot be safely
changed to any value in their range of options based on the driver settings may
cause instruments to self destruct, or lead to significant injury and even DEATH.
Depending on the instrument and how it's set up this may or may not be a relevant issue.
If there are any settings that could be changed to risk harming some or the instrument
blacklist them before proceeding by adding a self.black_list_for_testing property at the end
of the instrument driver's __init__.
ONLY RUN THIS TEST UNIT IF YOU ARE CERTAIN ALL SUCH ATTRIBUTES HAVE BEEN PROPERLY BLACKLISTED!
'''

# not incluing booleans since they can be interpreted ambiguously as ints. Should it?
BAD_INPUTS = [-19812938238312948, -1.11123444859, 3.2222111234, 985767665954, 890992238.2345,
              'not ok', 'bad value',
              [1, 2412, 19], [1, 191, 13, -5.3],
              {'Alfred': "Batman's uncle", 'or': 'imposter'}]


prop_err_str1 = ("attempted to set {} property {} to {} but when queried returned {}."
                 + "\n This is often a sign of interdependent properties that are not suitable for this auto testing."
                 + "test for interdependence and consider blacklisting.")
prop_err_str2 = ("set {} property {} to {} but _{} returned {}."
                 + "\n This is often a sign of interdependent properties that are not suitable for this auto testing."
                 + "test for interdependence and consider blacklisting.")


def auto_test_driver_properties(device, detailed_dependence=False, skip_log=False, verbose=True):
    '''
    Automatically tests driver properties and documnetation

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    detailed_dependenced : bool, optional
        Tests the interdependence between properties and reports the results, by default False
    skip_log : bool, optional
        Skip the logging of the test results, by default False
    verbose : bool, optional
        Print the results of the tests, by default True
    '''

    test_properties(device, detailed_dependence, verbose)

    print(
        f"\033[92m Property implementation tests passed, instrument: {device.__class__.__name__}. \033[0m")

    test_doc_string(device)
    print("\033[92m Docstring tests passed. \033[0m")

    if skip_log is False:
        write_log(device)

    print(f"\033[1;32m {device.__class__.__name__} test results logged. \033[0m")


def test_properties(device, detailed_dependence, verbose=False):
    '''
    Automatically finds all of the PropertySettings properties of device and tests that they work

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    verbose : bool, optional
        Print the results of the tests, by default False
    '''

    assert hasattr(device, '_version'), \
        "The instrument had no attribute _version, assign the driver a _version attribute"

    property_names = device.get_pyscan_properties()

    initial_state = get_initial_state(device, property_names)

    property_names = validate_blacklist(device, property_names)

    values_counter, range_counter, indexed_values_counter, dict_values_counter = 0, 0, 0, 0

    instrument_name = device.__class__.__name__

    if verbose:
        print("Initial state for the {} was: ".format(instrument_name))
        pprint.pprint(initial_state)
        print("\n")

    print("\nBeginning tests for: ", device.__class__.__name__, " version ", device._version)

    for property_name in property_names:
        settings_name = f"_{property_name}_settings"
        settings = device[settings_name]

        if property_name in device['black_list_for_testing']:
            continue

        if hasattr(settings, 'read_only'):
            test_read_only_property(device, property_name)

        if hasattr(settings, 'write_only'):
            continue

        if isinstance(settings, ValuesPropertySettings):
            values_counter += 1
            test_values_property(device, property_name, detailed_dependence, initial_state)
        elif isinstance(settings, RangePropertySettings):
            range_counter += 1
            test_range_property(device, property_name, detailed_dependence, initial_state)
        elif isinstance(settings, IndexedPropertySettings):
            indexed_values_counter += 1
            test_indexed_property(device, property_name, detailed_dependence, initial_state)
        elif isinstance(settings, DictPropertySettings):
            dict_values_counter += 1
            test_dict_values_property(device, property_name, detailed_dependence, initial_state)
        else:
            raise KeyError("No valid type present in setting: {}. Must be one of {}.".format(
                property_name, ['values', 'range', 'indexed_values', 'dict_values']))

        device[property_name] = initial_state[property_name]

        print(property_name)

        check_initial_state(device, property_name, initial_state)

    for key, value in initial_state.items():
        device[key] = value

    n_properties = len(property_names)

    mid_string = 'properties found and tested out of'
    print("\n{} range {} {} total settings found.".format(range_counter, mid_string, n_properties))
    print("{} values {} {} total settings found.".format(values_counter, mid_string, n_properties))
    print("{} indexed values {} {} total settings found.".format(indexed_values_counter, mid_string, n_properties))
    print("{} dict values {} {} total settings found.".format(dict_values_counter, mid_string, n_properties))

    print(
        "{} blacklisted settings not testing (likely due to interdependencies not suitable for automated testing)".format(
            len(device.black_list_for_testing)))

    total_tested = range_counter + values_counter + indexed_values_counter + dict_values_counter
    print("{} properties tested out of {} total settings.".format(total_tested, n_properties))

    if verbose:
        print("\nSettings restored to: ")
        pprint.pprint(initial_state)


def validate_blacklist(device, property_names):
    '''
    Validates that the black_list_for_testing attribute is present in the device and that all blacklisted properties

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    property_names : list
        List of automatically found pyscan property names

    Returns
    -------
    property_names : list
        Property names having removed the blacklisted properties
    '''

    assert hasattr(device, 'black_list_for_testing'), \
        "Driver needs black_list_for_testing attribute, assign empty list of no blacklisted properties requied"

    for black_listed_property in device.black_list_for_testing:
        if black_listed_property in property_names:
            property_names.remove(black_listed_property)

    return property_names


def get_initial_state(device, property_names):
    '''
    Gets the intial state of all properties

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    property_names : list
        List of automatically found pyscan property names

    Returns
    -------
    dict
        key, values of property names, inital value pairs
    '''

    initial_state = {}

    for property_name in property_names:
        initial_state[property_name] = device[property_name]

    return initial_state


def test_doc_string(device):
    '''
    Tests the formatting of the docstring for the driver

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    '''

    print("Testing driver doc string.")
    assert device.__doc__, "No doc string found for this driver."
    doc_string = device.__doc__

    try:
        lines = doc_string.split('\n')
    except Exception:
        assert False, "doc string found but is only one line"

    post_str = " not properly formatted or in doc string."
    assert '    Parameters' in lines, "Input parameters" + post_str
    assert '    Attributes\n    ----------\n    (Properties)\n' in doc_string, "Attributes" + post_str

    following_lines = lines[lines.index('    Parameters'):]

    for line in following_lines:
        assert line.startswith('    ') or line == '', "Improper indentation of line {}".format(repr(line))

    test_attribute_doc_string(device)

    test_attributes_from_docstring(device, doc_string)
    test_methods_from_docstring(device, doc_string)


def test_attribute_doc_string(device):
    '''
    Test the docstring for properties

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    '''
    property_names = device.get_pyscan_properties()

    for property_name in property_names:

        doc_string = device.get_property_docstring(property_name)

        lines = doc_string.split('\n')
        assert property_name in lines[0], \
            "attribute property_name not found on first line of doc_string for {}".format(property_name)
        assert len(lines) > 1, "doc string for {} found as only 1 line".format(property_name)
        assert [len(lines[1]) > 3], "doc string's second line is not long enough for {}".format(property_name)


def test_attributes_from_docstring(device, doc_string):
    '''
    Test that attributes listed in the docstring are also present in the driver

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    doc_string : str
        The docstring of the driver
    '''

    attributes = []
    in_attributes_section = False

    for line in doc_string.split('\n'):
        # test if we've reached the Methods section
        if 'Methods' in line:
            break  # Stop processing if we've reached Methods

        # test for the start of Attributes section
        if 'Attributes' in line:
            in_attributes_section = True
            continue  # Go to the next line to read attributes

        # If we are in the Attributes section, extract attributes
        if in_attributes_section:
            if line.strip() == '':
                continue  # Skip empty lines
            # Match lines that start with 4 spaces and contain a word followed by a colon
            match = re.match(r'^\s{4}(\w+)\s*:', line)
            if match:
                attributes.append(match.group(1))

    for attribute in attributes:
        assert hasattr(device, attribute), f"Attribute '{attribute}' listed in docstring but not the driver."


def test_methods_from_docstring(device, doc_string):
    '''
    Test that methods listed in the docstring are also present in the driver

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    doc_string : str
        The docstring of the driver
    '''

    methods = []
    in_methods_section = False

    for line in doc_string.split('\n'):
        if 'Methods' in line:
            in_methods_section = True
        elif in_methods_section:
            if line.strip() == '':
                break
            match = re.match(r'\s*(\w+)\s*\(', line)
            if match:
                methods.append(match.group(1))

    for method in methods:
        assert hasattr(device, method), f"Method '{method}' listed in docstring but not the driver."


def write_log(device, exception=None, save_multiple_lines=False):
    try:
        driver_file_name = str(type(device)).split("'")[1].split(".")[-2]
    except Exception:
        if exception is None:
            err_string = "The tests were passed but...\n"
            err_string = err_string + "failed to log test history. Driver class file path not as expected."
        else:
            err_string = "Tests failed with exception: \n{}\n".format(exception)
            err_string = err_string + "failed to log test history. Driver class file path not as expected."
        assert False, err_string

    if exception is None:
        pre_string = "The tests were passed but...\n"
        new_line = "Passed with {} version v{} tested on pyscan version {} at {}".format(
            driver_file_name, device._version, get_pyscan_version(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    elif exception is not None:
        pre_string = "Tests failed with exception: \n{}\n".format(exception)
        new_line = "Failed with {} version v{} tested on pyscan version {} at {}".format(
            driver_file_name, device._version, get_pyscan_version(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    driver_file_name = driver_file_name + '_test_log.txt'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(base_dir, '../testing/driver_test_logs/')
    driver_test_logs_file_names = os.listdir(directory)
    path = os.path.join(directory, driver_file_name)

    if driver_file_name in driver_test_logs_file_names:
        if save_multiple_lines:
            with open(path, 'r') as test_log:
                existing_log = test_log.read()

        with open(path, 'w') as test_log:
            test_log.write(new_line + '\n')
            if save_multiple_lines:
                test_log.write(existing_log)

    else:
        print("No test log file detected for this driver. Creating a new one.")

        with open(path, 'w') as test_log:
            test_log.write(new_line)

    try:
        with open(path, 'r') as test_log:
            test_log.read()
        print("The new test log for this driver is: ", new_line)
    except Exception:
        err_string = pre_string + "Test log seemed to save but could not be accessed."
        err_string = err_string + "Please ensure test records are saving properly."
        assert False, err_string
