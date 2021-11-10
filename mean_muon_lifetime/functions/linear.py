'''
linear
-----------------------------------------------------------
perrin w. davidson
10.11.2021
pwd@uchicago.edu
-----------------------------------------------------------
the function for fitting data with a linear model.
-----------------------------------------------------------
inputs:
    p - initial guess for parameters p
    x - independent variable
output:
    y - fit estimate
'''


# linear fit function:
def linear(p, x):
    return (p[0] * x) + p[1]

