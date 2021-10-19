'''
fitSpectrum
-----------------------------------------------------------
fitting the spectrum of a radionuclide.
'''
# import libraries ----------------------------------------
import numpy as np
import pandas as pd
from scipy import optimize
from functions.data_fit import data_fit
from functions.gaussian import gaussian
from functions.residual import residual
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# load data -----------------------------------------------
# set input names:
io_path = 'io/inputs/spectra/'
data_file = 'Cs137-0.tsv'
file_name = io_path + data_file

# read data:
data = np.loadtxt(
    file_name,
    unpack=True,
    skiprows=26
).T

# convert to dataframe:
cs137 = pd.DataFrame({'channel': data[:, 0], 'counts': data[:, 1]})

# quality control -----------------------------------------
# calculate uncertainty:
cs137['d_counts'] = np.sqrt(cs137['counts'])

# fill in empty data:
for i, value in enumerate(cs137['d_counts']):
    if value == 0:
        cs137.loc[i, 'd_counts'] = 1.14

# set fit range:
min_fit = 460
max_fit = 575

# get fitting range data:
cs137_fit = cs137.iloc[min_fit:max_fit, :]

# fit -----------------------------------------------------
# set initial gaussian guesses:
my_guess_gauss = [1000, 500, 25, -1, 50]

# calculate the gaussian fit:
pf_gauss, pferr_gauss, chisq_gauss, dof_gauss = data_fit(
    my_guess_gauss,
    gaussian,
    cs137_fit['channel'],
    cs137_fit['counts'],
    cs137_fit['d_counts'],
    'Exponential Fit: 137Cs (512 keV)'
)

# make fit text -------------------------------------------
# make string:
textfit_gauss = '$f(x)$ & $\\frac{N}{\\sigma\\sqrt{2\\pi}} \\: e^{\\frac{-(x - \\mu)^2}{2\\sigma^2}} + mx + b$ \\\ \n'
textfit_gauss += '$N$ & ${:.2f} \pm {:.2f}$ \\\ \n'.format(pf_gauss[0], pferr_gauss[0])
textfit_gauss += '$\\mu$ & ${:.2f} \pm {:.2f}$ \\\ \n'.format(pf_gauss[1], pferr_gauss[1])
textfit_gauss += '$\\sigma$ & ${:.2f} \pm {:.2f}$ \\\ \n'.format(pf_gauss[2], pferr_gauss[2])
textfit_gauss += '$m$ & ${:.2f} \pm {:.2f}$ \\\ \n'.format(pf_gauss[3], pferr_gauss[3])
textfit_gauss += '$b$ & ${:.2f} \pm {:.2f}$ \\\ \n'.format(pf_gauss[4], pferr_gauss[4])
textfit_gauss += '$\chi^2$ & ${:.1f}$ \\\ \n'.format(chisq_gauss)
textfit_gauss += '$N$ & ${}$ \\\ \n'.format(dof_gauss)
textfit_gauss += '$\chi^2/N$ & ${:.2f}$ \\\ '.format(chisq_gauss / dof_gauss)

# write to text:
text_file = open("io/outputs/reports/tables/fit_results.txt", "w")
n = text_file.write(textfit_gauss)
text_file.close()

# plot ----------------------------------------------------
# get font and style:
gs_font = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/GillSans.ttc')
plt.style.use('io/inputs/old-style.mplstyle')

# make fit independent variable:
channel_cont = np.linspace(min(cs137_fit['channel']), max(cs137_fit['channel']), 5000)

# make figure:
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

# plot errors:
ax.errorbar(
    cs137_fit['channel'],
    cs137_fit['counts'],
    cs137_fit['d_counts'],
    fmt='rd',
    ecolor='k',
    elinewidth=0.75,
    capsize=1.5,
    capthick=0.75,
    ms=2.5,
    label='Data'
)

# plot fit:
ax.plot(
    channel_cont,
    gaussian(pf_gauss, channel_cont),
    'k-',
    label='Fit'
)


# set parameters:
ax.xaxis.set_minor_locator(MultipleLocator(10))
ax.yaxis.set_minor_locator(MultipleLocator(12.5))
ax.set_xlabel(' '.join('CHANNEL'), fontproperties=gs_font, fontsize=14)
ax.set_ylabel(' '.join('COUNT'), fontproperties=gs_font, fontsize=14)
ax.set_xlim(int(cs137_fit['channel'].min()), int(cs137_fit['channel'].max()))
ax.set_ylim(0, int(cs137_fit['counts'].max()) + 20)
ax.tick_params('x', which='both', top=True, bottom=True)
ax.tick_params('y', which='both', right=True, left=True)
for tick in ax.get_xticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)
for tick in ax.get_yticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)
#ax.set_title(' '.join('Fitted $^{137}$Cs Gamma Decay Spectrum (662 keV)'), fontproperties=gs_font, fontsize=16)
#ax.legend(loc='upper right', fontsize=14, frameon=False)

# save:
plt.savefig('io/outputs/reports/images/127cs_spectrum_fitted.png', dpi=300)

# show:
plt.show()

# end program ---------------------------------------------
