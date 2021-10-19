'''
data_fit
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
the function for plotting fitting data. taken from the intro.
python coding lab. attributed to dr. david mccowan.
-----------------------------------------------------------
inputs:
    p    - fitted parameters
    func - the function we're fitting to
    xvar - independent variable
    yvar - dependent variable
    err  - dependent variable error
    tmi  - intermediate data needed (can be set to 1 or 2)
output:
    a plot
'''


def plot_data(ax, x, y, dy, xfit, yfit, p, perr, chi, dof, title, xlab, ylab, save_name, numyticks):

    # import libraries:
    import matplotlib.font_manager as fm
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator

    # get font and style:
    gs_font = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/GillSans.ttc')
    plt.style.use('io/inputs/old-style.mplstyle')

    # start plot:
    #fig, ax = plt.subplots(figsize=(10, 8))

    # plot exp1 data:
    ax.errorbar(
        x,
        y,
        dy,
        fmt='rd',
        ecolor='k',
        elinewidth=0.75*2,
        capsize=1.5*2,
        capthick=0.75*2,
        ms=2.5*2
    )

    # plot fit:
    ax.plot(
        xfit,
        yfit,
        'k-',
        label='Fit'
    )

    ax.xaxis.set_minor_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(numyticks))
    #ax.set_xlabel(' '.join('CHANNEL'), fontproperties=gs_font, fontsize=14)
    ax.set_ylabel(' '.join(ylab), fontproperties=gs_font, fontsize=18)
    #ax.set_xlim(0, int(cs137['channel'].max()))
    #ax.set_ylim(0, int(cs137['counts'].max()) + 50)
    ax.tick_params('x', which='both', top=True, bottom=True)
    ax.tick_params('y', which='both', right=True, left=True)
    for tick in ax.get_xticklabels():
        tick.set_fontname("Gill Sans")
        tick.set_fontsize(14)
    for tick in ax.get_yticklabels():
        tick.set_fontname("Gill Sans")
        tick.set_fontsize(14)
    ax.set_title(' '.join(title), fontproperties=gs_font, fontsize=18)

    # set axis 1 labels:
    # ax.set_title(title, fontsize=20)
    # ax.set_ylabel(ylab, fontsize=16)
    # #ax.set_xlabel(xlab, fontsize=16)
    # ax.tick_params(labelsize=16)

    # # make exp1 fit text:
    #textfit = '$R(x) = R_0e^{-\\lambda x} + B$ \n'
    textfit = '$R_0 = {:.0f} \\pm {:.0f}$ (counts/s) \n'.format(p[0], perr[0])
    textfit += '$\\lambda = {:.4f} \\pm {:.4f}$ (1/cm) \n'.format(p[1], perr[1])
    textfit += '$B = {:.0f} \\pm {:.0f}$ (counts/s) \n'.format(p[2], perr[2])
    textfit += '$\\chi^2= {:.2f}$ \n'.format(chi)
    textfit += '$N_\\nu = {}$  \n'.format(dof)
    textfit += '$\\chi^2_\\nu = {:.2f}$'.format(chi / dof)

    # include exp1 fit text:
    ax.text(
        0.55,
        0.95,
        textfit,
        transform=ax.transAxes,
        fontsize=16,
        verticalalignment='top',
        fontproperties=gs_font
    )

    # set limits for axis 1:
    ax.set_xlim([x.min() - 1, x.max() + 1])
    #ax.legend(loc='lower left', fontsize=16)

    # save:
    #plt.savefig(save_name)
    #plt.show()


# end function.
