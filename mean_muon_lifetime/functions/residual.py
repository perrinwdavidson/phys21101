'''
residuals
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
the function for calculating the residuals of a fit. taken
from the intro. python coding lab. attributed to dr. david
mccowan.
-----------------------------------------------------------
inputs:
    p     - initial guess for parameters p0
    func  - the function we're fitting to
    xvar  - independent variable
    yvar  - dependent variable
    err   - dependent variable error
output:
    resid - residual array
'''


def residual(p, func, xvar, yvar, err):
    return (func(p, xvar) - yvar) / err


# end function.