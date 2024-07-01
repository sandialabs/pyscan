from pyvisa import ResourceManager, VisaIOError


def get_resources(black_list=[], target=None):
    rm = ResourceManager()
    rs = rm.list_resources()
    print("Connected resources are: ", rs)

    target_found = False
    for r in rs:
        if r in black_list:
            continue
        try:
            # Connect to the instrument
            res = rm.open_resource(r)
        except VisaIOError as e:
            assert False, f"{e}, instrument may already be connected elsewhere. If available or consider blacklisting."

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
                print(f"Target found in resource {r} with {name}")
                # If the target is found break to return the target resource
                target_found = True
                break
            # If found, print the resource as well as the I.D.
            print(r, name)

        except VisaIOError:
            pass
        # Important. Close the connection.
        res.close()

    if target is not None:
        if target_found is True:
            # print("Returning your target resource.")
            return res
        else:
            print("Target not found, ensure you are trying to access the right resource and that it is available.")
