'''
data_fit
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
the function for fitting data. taken from the intro.
python coding lab. attributed to dr. david mccowan.
-----------------------------------------------------------
inputs:
    p0   - initial guess for parameters p0
    func - the function we're fitting to
    xvar - independent variable
    yvar - dependent variable
    err  - dependent variable error
    tmi  - intermediate data needed (can be set to 1 or 2)
output:
    pf    - parameter estimate
    pferr - error in parameter estimate
    chisq - sum of residual reduced chi-squared
    dof   - degrees of freedom of estimate
'''


# data fitting function:
def data_fit(p0, func, xvar, yvar, err, fit_type_name, tmi=0):

    # import needed libraries:
    from scipy import optimize
    import numpy
    from functions.residual import residual

    # initialize fitting object with inputs:
    try:
        fit = optimize.least_squares(
            residual,
            p0,
            args=(
                func,
                xvar,
                yvar,
                err
            ),
            verbose=tmi
        )

    # perhaps it doesn't work:
    except Exception as error:
        print("Something has gone wrong:", error)
        return p0, numpy.zeros_like(p0), -1, -1

    # fit values:
    pf = fit['x']
    print()

    # compute the covariance matrix by finding the inverse of the Jacobian times its transpose:
    try:
        cov = numpy.linalg.inv(fit['jac'].T.dot(fit['jac']))

        # let us know if this failed:
    except:
        print('Fit did not converge')
        print('Result is likely a local minimum')
        print('Try changing initial values')
        print('Status code:', fit['status'])
        print(fit['message'])
        return pf, numpy.zeros_like(pf), -1, -1

    # calculate chi-squared sum:
    chisq = sum(residual(pf, func, xvar, yvar, err) ** 2)

    # calculate degrees of freedom of estimate:
    dof = len(xvar) - len(pf)

    # calculate reduced chi-squared:
    red_chisq = chisq / dof

    # calculate error in parameter estimate by squaring diagonal elements of the covariance matrix:
    pferr = numpy.sqrt(numpy.diagonal(cov))

    # print out fit options:
    print(fit_type_name)
    print('Converged with chi-squared {:.2f}'.format(chisq))
    print('Number of degrees of freedom, dof = {:.2f}'.format(dof))
    print('Reduced chi-squared {:.2f}'.format(red_chisq))
    print()
    Columns = ["Parameter #", "Initial guess values:", "Best fit values:", "Uncertainties in the best fit values:"]
    print('{:<11}'.format(Columns[0]), '|', '{:<24}'.format(Columns[1]), "|", '{:<24}'.format(Columns[2]), "|",
          '{:<24}'.format(Columns[3]))
    for num in range(len(pf)):
        print('{:<11}'.format(num), '|', '{:<24.3e}'.format(p0[num]), '|', '{:<24.3e}'.format(pf[num]), '|',
              '{:<24.3e}'.format(pferr[num]))

    # return outputs:
    return pf, pferr, chisq, dof


# end function.
