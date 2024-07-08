from pyvisa import ResourceManager, VisaIOError


def get_resources(list_resources=True):
    rm = ResourceManager()
    rs = rm.list_resources()

    for r in rs:
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

    return rs


def capture_resource(unique_identifier):
    assert type(unique_identifier) is str, "unique identifier parameter input not a string."
    rm = ResourceManager()
    rs = rm.list_resources()

    target_found = False
    target = None
    err_str = "Multiple resources found with the same 'unique' identifier. Choose an exclusive identifier."
    for r in rs:
        try:
            # Connect to the instrument
            res = rm.open_resource(r)
        except VisaIOError:
            continue

        # Check if there is a target and if it is in the resource string
        if unique_identifier in r:
            print(f"Target found in resource {r}")

            if target_found:
                target.close()
                res.close()
                assert False, err_str

            target = res
            target_found = True
            continue

        try:
            # Try to query the I.D. of the instrument
            name = res.query('*IDN?')
            # Check if there is a target resource and whether this is it
            if unique_identifier in name:
                print(f"Target found in resource {r} with name {name}")

                if target_found:
                    target.close()
                    res.close()
                    assert False, err_str

                target = res
                target_found = True
                continue

        except VisaIOError:
            pass
        # Important. Close the connection.
        res.close()

    if target_found:
        return target
    else:
        assert False, "Target not found. Make sure your unique identifier in resource string or id query response."


def old_get_resources(black_list=[], target=None):
    """
    Function that scans for connected VISA resources,
    optionally filtering out specified resources, and
    can return a specific target resource or list available resources.

    This function uses the PyVISA library to list all connected instruments that are accessible via VISA.
    The blacklist is for instruments that the PyVISA resource manager detects but can't connect to/open.
    The target parameter can be used to search for and return a specific instrument based on a target identifier
    found either in the resource string or the instrument's identity query response.

    Parameters
    ----------
    black_list : (list, optional)
        A list of resource strings to ignore when listing or searching for resources. Defaults to an empty list.
    target : (str, optional)
        A substring to search for within the resource strings or the instrument identity query responses.
        If specified, the function attempts to find an instrument that matches this target. Defaults to None.

    Returns
    -------
    If a target is specified and found, returns the PyVISA resource object
        corresponding to the target instrument. Otherwise, returns None.
    If no target is specified, the function does not return a value but
        prints information about the connected resources.

    Raises
    ------
    AssertionError: If a VisaIOError occurs while trying to connect to an instrument it returns an error
        indicating it might already be connected elsewhere and should be considered diagnostics or blacklisting.

    Note:
    - It is recommended to specify a non-empty blacklist if there are known resources that should always be ignored
        to avoid unnecessary connection attempts and errors.
    """

    rm = ResourceManager()
    rs = rm.list_resources()
    list_resources = True
    if target is not None:
        list_resources = False

    if list_resources is True:
        print("Connected resources are: ", rs, "\n")

    target_found = False
    for r in rs:
        if r in black_list:
            continue
        try:
            # Connect to the instrument
            res = rm.open_resource(r)
        except VisaIOError as e:
            err_str = f"{e}, instrument may already be connected elsewhere."
            assert False, err_str + " If available diagnose the connection or consider blacklisting."

        # Check if there is a target and if it is in the resource string
        if (target is not None) and (target in r):
            print(f"Target found in resource {r}")
            # If the target is found break to return the target resource
            target_found = True
            break

        try:
            # Try to query the I.D. of the instrument
            name = res.query('*IDN?')
            # Check if there is a target resource and whether this is it
            if (target is not None) and (target in name):
                print(f"Target found in resource {r} with name {name}")
                # If the target is found break to return the target resource
                target_found = True
                break
            # If found, print the resource as well as the I.D.
            if list_resources is True:
                print(r, name)

        except VisaIOError:
            pass
        # Important. Close the connection.
        res.close()

    if target is not None:
        if target_found is True:
            try:
                print(f"Returning target resource: {res.query('*IDN?')}")
            except VisaIOError:
                pass
            return res
        else:
            print("Target not found, ensure you are trying to access the right resource and that it is available.")
