# -*- coding: utf-8 -*-
import numpy as np


def drange(start, delta, stop):
    '''
    Returns an array from `start`, with steps of size `delta` to
    `stop`, inclusive.

    - If ``stop-start`` is not divisible by `delta`,
      it fits as many integer steps of `delta` as possible,
      then adds `stop` as the final step.
    - If ``stop-start < delta`` returns ``[start, stop]``.
    - If ``stop == start`` returns ``[start]``.

    Parameters
    ----------
    start : float or int
        Start value.
    delta : float or int
        Distance between points.
    stop : float or int
        Last value.

    Returns
    -------
    numpy.ndarray
    '''

    delta = abs(delta)

    if stop == start:
        return [start]
    elif np.abs(stop - start) < delta:
        return [start, stop]

    sign = (stop - start) / np.abs(stop - start)  # 1 or -1

    isdivisible = not ((stop - start) / delta) % 1 > 0

    if isdivisible:
        values = np.linspace(start, stop, int(np.abs(stop - start) / (delta) + 1))
    else:
        n = int(np.floor(np.abs(stop - start) / delta))

        values = [start + sign * delta * i for i in range(n + 1)]
        values += [stop]

    return values
