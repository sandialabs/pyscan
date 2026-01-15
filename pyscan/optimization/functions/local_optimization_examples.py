def paraboloid_2D(x0, x1, e0=0., e1=0.):
    """
    2D paraboloid function to demonstrate local optimization with single minimum.

    Parameters
    ----------
    x0 : float
        input dimension 0
    x1 : float
        input dimension 1
    e0 : float
        dimension 0 minimum coordinate
    e1 : float
        dimension 1 minimum coordinate

    Returns
    -------
    float
        Parabolic mapping from inputs
    """
    return (x0 - e0)**2 + (x1 - e1)**2
