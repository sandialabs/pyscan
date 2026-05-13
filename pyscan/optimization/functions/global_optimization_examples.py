import numpy as np


def townsend(x0, x1):
    """
    Townsend function to demonstrate global optimization with multiple minima.
    https://en.wikipedia.org/wiki/Test_functions_for_optimization
    https://botorch.org/docs/notebooks_community/clf_constrained_bo/
    From article:
    Townsend, Alex (January 2014). "Constrained optimization in Chebfun". chebfun.org.
    https://www.chebfun.org/examples/opt/ConstrainedOptimization.html
    Two local minima on domain [-2.5, 2.5], [-2.5, 2.5] subject to heart-shaped constraint.
    Four local maxima on domain [-2.5, 2.5], [-1.5, 1.5].

    Parameters
    ----------
    x0 : float
        input dimension 0
    x1 : float
        input dimension 1

    Returns
    -------
    float
        Mapping from inputs
    """
    return -np.cos((x0 - 0.1) * x1) ** 2 - x0 * np.sin(3 * x0 + x1)
