def check_initial_state(device, property_name, initial_state):
    '''
    Check if the properties have changed from their intial state after a property has been tested

    Parameters
    ----------
    device : subclass of pyscan.drivers.AbstractDriver
        Instance of a driver subclassed from AbstractDriver
    property_name : str
        Name of the property that was just tested or changed
    initial_state : dict
        key, value pairs of property names and their initial values
    '''

    for key, value in initial_state.items():

        new_value = device[key]

        if new_value != value:
            print(f'Warning, changing {property_name} changed {key} from {value} to {new_value}')
            device[key] = value
