from pyvisa import ResourceManager, VisaIOError


def get_resources(list_resources=True):
    """
    Returns a list of connected VISA GPIB addresses and optionally (by default)
    tries to print them paired with their corresponding ID strings.

    This function uses the PyVISA library to return a list of all resources (instruments) available to the system.
    It tries to connect to each instrument and prints the error message if unable to.
    If `list_resources` is set to True, it attempts to query and print the IDs of each instrument.

    Parameters
    ----------
    list_resources : bool
        If True (default), queries and prints instrument connection addresses paired with their ID strings if available.
        If False, only returns the available resources without querying their IDs.

    Returns
    -------
    resources_listed : tuple
        A list of resource connections (strings) representing the instruments detected by the system.
    """
    rm = ResourceManager()
    resources_listed = rm.list_resources()

    for r in resources_listed:
        try:
            # Connect to the instrument
            res = rm.open_resource(r)
        except VisaIOError as e:
            print(f"{e}\n Could not connect to instrument {r}, may already be connected elsewhere.")
            continue

        if list_resources is True:
            try:
                # Try to query the I.D. of the instrument
                name = res.query('*IDN?')
                # If found, print the resource as well as the I.D.
                print(r, name)
            except VisaIOError:
                pass

        # Important. Close the connection.
        res.close()

    return resources_listed
