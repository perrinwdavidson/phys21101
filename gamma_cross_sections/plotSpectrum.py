'''
plotSpectrum
-----------------------------------------------------------
plotting the spectrum of a radionuclide.
'''
# import libraries ----------------------------------------
import numpy as np
import pandas as pd
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

# plot ----------------------------------------------------
# get font and style:
gs_font = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/GillSans.ttc')
plt.style.use('io/inputs/old-style.mplstyle')

# make figure:
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

# plot errors:
ax.errorbar(
    cs137['channel'],
    cs137['counts'],
    cs137['d_counts'],
    fmt='rd',
    ecolor='k',
    elinewidth=0.75,
    capsize=1.5,
    capthick=0.75,
    ms=2.5
)

# set parameters:
ax.xaxis.set_minor_locator(MultipleLocator(100))
ax.yaxis.set_minor_locator(MultipleLocator(25))
ax.set_xlabel(' '.join('CHANNEL'), fontproperties=gs_font, fontsize=14)
ax.set_ylabel(' '.join('COUNT'), fontproperties=gs_font, fontsize=14)
ax.set_xlim(0, int(cs137['channel'].max()))
ax.set_ylim(0, int(cs137['counts'].max()) + 50)
ax.tick_params('x', which='both', top=True, bottom=True)
ax.tick_params('y', which='both', right=True, left=True)
for tick in ax.get_xticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)
for tick in ax.get_yticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)
#ax.set_title(' '.join('$^{137}$Cs Gamma Decay Spectrum'), fontproperties=gs_font, fontsize=16)

# annotate:
plt.annotate('IV', (505, 200), (505, 220), fontproperties=gs_font, fontsize=16, fontweight='bold')
plt.annotate('III', (345, 40), (345, 65), fontproperties=gs_font, fontsize=16, fontweight='bold')
plt.annotate('II', (172.5, 6.5), (172.5, 6.5), fontproperties=gs_font, fontsize=16, fontweight='bold')
plt.annotate('I', (148, 175), (148, 175), fontproperties=gs_font, fontsize=16, fontweight='bold')
ax.annotate("",
            xy=(10, 12.5), xycoords='data',
            xytext=(160, 12.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )
ax.annotate("",
            xy=(350, 12.5), xycoords='data',
            xytext=(200, 12.5), textcoords='data',
            arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"),
            )

# save:
plt.savefig('io/outputs/reports/images/127cs_spectrum.png', dpi=300)

# show:
plt.show()

# end program ---------------------------------------------
