#!/usr/bin/env python
"""
FADE FUNCTIONS
"""

def bezier(x):
    """
    Calculate the bezier coefficient.

    :param x: The parameter value of the bezier function.
    :type x: int

    :return: The bezier coefficient.
    :rtype: float
    """

    x = x / STEPS
    return x * x * (3.0 - 2.0 * x) # bezier
