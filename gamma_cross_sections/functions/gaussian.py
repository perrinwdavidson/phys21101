'''
gaussian
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
the gaussian function for fitting data. taken from the intro.
python coding lab. attributed to dr. david mccowan.
-----------------------------------------------------------
inputs:
    p - initial guess for parameters p
    x - independent variable
output:
    y - fit estimate
'''


def gaussian(p, x):

    # import needed libraries:
    import numpy

    # calculate function:
    return (p[0]/(p[2]*numpy.sqrt(2*numpy.pi))*numpy.exp(-(x-p[1])**2/(2*p[2]**2))) + p[3]*x + p[4]


# end function.
