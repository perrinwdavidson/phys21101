'''
power
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
the function for fitting data. taken from the intro.
python coding lab.
'''


# linear fit function:
def power(p, x):
    return p[0] * (x ** p[1])

