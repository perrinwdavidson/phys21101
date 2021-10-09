'''
thomson
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
cross section derived from thomson scattering for a given
charge, q.
-----------------------------------------------------------
inputs:
    q - charge of particle
    m - mass of particle
output:
    sigma - fit estimate
'''


def thomson(q, m):

    # import libraries:
    import numpy as np

    # set constants:
    c = 299792458
    epsilon0 = 8.85418782E-12

    # calculate constant:
    sigma_const = (8 * np.pi) / 3

    # calculate radius:
    rad = (q ** 2) / (4 * np.pi * epsilon0 * m * (c ** 2))

    # return:
    return sigma_const * (rad ** 2)


# end function.
