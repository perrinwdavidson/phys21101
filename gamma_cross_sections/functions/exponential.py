'''
exponential
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
the exponential function for fitting data. taken from the
intro. python coding lab. attributed to dr. david mccowan.
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
    return (p[0] * numpy.exp(-p[1] * x)) + p[2]


# end function.
