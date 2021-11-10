'''
exponential
-----------------------------------------------------------
perrin w. davidson
09.11.2021
pwd@uchicago.edu
-----------------------------------------------------------
the exponential function for fitting data with an exponential
function with a background term.
-----------------------------------------------------------
inputs:
    p - initial guess for parameters p
    x - independent variable
output:
    y - fit estimate
'''


def exponential(p, x):

    # import libraries:
    import numpy

    # calculate function:
    return (p[0] * numpy.exp(-x / p[1])) + p[2]


# end function.
