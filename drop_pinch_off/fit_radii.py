'''
fit_radii
-----------------------------------------------------------
fitting radii for drop pinch of
'''
# Load packages -------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions.data_fit import data_fit
from functions.power import power
from matplotlib.ticker import MultipleLocator
import matplotlib.font_manager as fm

# Load data -----------------------------------------------
# Set input path:
input_data_basepath = 'io/inputs/data/'
output_data_basepath = 'io/outputs/data/'

# Set file name:
filename = 'radii_obs.xlsx'

# Set pixel to m:
px2m = 164090
dpx2m = 29360

# Read data:
radii_data = pd.read_excel(
    input_data_basepath + filename
)

# Make data:
radii = pd.DataFrame(
    {'time': radii_data['time'],
     'radius': radii_data['radius'] / px2m,
     'd_radius': radii_data['d_radius'] / px2m}
)

# Quality control -----------------------------------------
# Add in FPS correction:
fps_correct = 7 / 38565

# Correct time:
radii['time'] = radii['time'] * fps_correct

# Uncertainty ---------------------------------------------
# Add in uncertainty in conversion:
new_error = np.sqrt(((radii['d_radius'] / px2m) ** 2) + (((radii['radius'] / (px2m ** 2)) * dpx2m) ** 2))
radii['d_radius'] = new_error

# Save:
radii.to_csv(output_data_basepath + 'radii_edit.csv', index=False)

# Separate data by regime ---------------------------------
# NB: The 12th point is the switch of regimes. Set:
iRegime = 8

# Segment data:
regime2 = radii.loc[:iRegime, :].reset_index(drop=True)
regime1 = radii.loc[(iRegime + 1):, :].reset_index(drop=True)

# Plot data -----------------------------------------------
# Initialize figure and axis:
fig, ax = plt.subplots(figsize=(10, 8))

# Plot Regime 1:
ax.loglog(
    regime1['time'],
    regime1['radius'],
    '.b',
    label='Regime 1'
)

# Plot Regime 2:
ax.loglog(
    regime2['time'],
    regime2['radius'],
    '.r',
    label='Regime 2'
)

# Add in labels:
ax.set_xlabel('Time (s)')
ax.set_ylabel('Radius (m)')
ax.set_title('Drop Pinch-Off Radius over Time')

# Add in legend:
ax.legend()

# Show plot:
#plt.show()

# Fit regime 1 --------------------------------------------
# set initial guesses:
my_guess_r1 = [1E-5, (2 / 3)]

# calculate the gaussian fit:
pf_r1, pferr_r1, chisq_r1, dof_r1 = data_fit(
    my_guess_r1,
    power,
    regime1['time'].to_numpy(),
    regime1['radius'].to_numpy(),
    regime1['d_radius'].to_numpy(),
    'Power Fit: Regime 1'
)

# plot fit:
xr1 = np.linspace(min(regime1['time']), max(regime1['time']), 5000)
figr1, ax = plt.subplots(figsize=(8, 6), dpi=300)
ax.errorbar(
    regime1['time'].to_numpy(),
    regime1['radius'].to_numpy(),
    regime1['d_radius'].to_numpy(),
    fmt='rd',
    ecolor='k',
    elinewidth=0.75,
    capsize=1.5,
    capthick=0.75,
    ms=2.5,
    label='Data'
)
ax.plot(
    xr1,
    power(pf_r1, xr1),
    'k-',
    label='Fit'
)
ax.plot(
    xr1,
    power([pf_r1[0], (2 / 3)], xr1),
    'k--',
    label='Ideal Fit'
)
ax.legend()
#plt.show()

# Fit regime 2 --------------------------------------------
# set initial gaussian guesses:
my_guess_r2 = [1E-5, 1]

# calculate the gaussian fit:
pf_r2, pferr_r2, chisq_r2, dof_r2 = data_fit(
    my_guess_r2,
    power,
    regime2['time'].to_numpy(),
    regime2['radius'].to_numpy(),
    regime2['d_radius'].to_numpy(),
    'Power Fit: Regime 2'
)

# plot fit:
xr2 = np.linspace(min(regime2['time']), max(regime2['time']), 10000)
figr2, ax = plt.subplots(figsize=(8, 6), dpi=300)
ax.errorbar(
    regime2['time'].to_numpy(),
    regime2['radius'].to_numpy(),
    regime2['d_radius'].to_numpy(),
    fmt='rd',
    ecolor='k',
    elinewidth=0.75,
    capsize=1.5,
    capthick=0.75,
    ms=2.5,
    label='Data'
)
ax.plot(
    xr2,
    power(pf_r2, xr2),
    'k-',
    label='Fit'
)
ax.plot(
    xr2,
    power([pf_r2[0], 1], xr2),
    'k--',
    label='Ideal Fit'
)
ax.legend()
#plt.show()

# Plot one plot -------------------------------------------
# get font and style:
gs_font = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/GillSans.ttc')
plt.style.use('io/inputs/old-style.mplstyle')

# Initialize figure and axis:
figr12, ax = plt.subplots(figsize=(8, 6))

# Set loglog plot:
ax.set_xscale('log', base=10)
ax.set_yscale('log', base=10)

# Plot Regime 1:
ax.errorbar(
    regime1['time'].to_numpy(),
    regime1['radius'].to_numpy(),
    regime1['d_radius'].to_numpy(),
    fmt='rd',
    ecolor='k',
    elinewidth=0.75,
    capsize=1.5,
    capthick=0.75,
    ms=5,
    label='Data'
)

# Plot Regime 1 fit:
ax.plot(
    xr1,
    power(pf_r1, xr1),
    'k--',
    label='R1 Fit'
)

# Plot ideal Regime 1 fit:
# ax.plot(
#     xr1,
#     power([pf_r1[0], (2 / 3)], xr1),
#     'r--',
#     label='Ideal Fit',
#     linewidth=0.5
# )

# Plot Regime 2:
ax.errorbar(
    regime2['time'].to_numpy(),
    regime2['radius'].to_numpy(),
    regime2['d_radius'].to_numpy(),
    fmt='gd',
    ecolor='k',
    elinewidth=0.75,
    capsize=1.5,
    capthick=0.75,
    ms=5,
    label='Data'
)

# Plot Regime 2 fit:
xr2plot = xr2[xr2 >= min(regime2.loc[1:, 'time'])]
ax.plot(
    xr2plot,
    power(pf_r2, xr2plot),
    'k--',
    label='R2 Fit'
)

# Plot ideal Regime 2 fit:
# ax.plot(
#     xr2plot,
#     power([pf_r2[0], 1], xr2plot),
#     'r--',
#     label='Ideal Fit',
#     linewidth=0.5
# )

# set parameters:
#ax.xaxis.set_minor_locator(MultipleLocator(5))
#ax.yaxis.set_minor_locator(MultipleLocator(25))
ax.set_xlabel(' '.join('TIME (s)'), fontproperties=gs_font, fontsize=14)
ax.set_ylabel(' '.join('RADIUS (m)'), fontproperties=gs_font, fontsize=14)
ax.set_xlim(3E-5, 1.5E-3)
ax.set_ylim(3E-6, 2E-4)
ax.tick_params('x', which='both', top=True, bottom=True)
ax.tick_params('y', which='both', right=True, left=True)
for tick in ax.get_xticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)
for tick in ax.get_yticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)

# Save plot:
plt.savefig('io/outputs/plots/radii.png', dpi=300)

# Show plot:
plt.show()

# Plot ideal plot -----------------------------------------
# Independent time variable:
time = np.linspace(3E-5, 1.5E-3, 5000)

# get font and style:
gs_font = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/GillSans.ttc')
plt.style.use('io/inputs/old-style.mplstyle')

# Initialize figure and axis:
figr12ideal, ax = plt.subplots(figsize=(8, 6))

# Set loglog plot:
ax.set_xscale('log', base=10)
ax.set_yscale('log', base=10)

# Plot data:
ax.errorbar(
    radii.loc[1:, 'time'].to_numpy(),
    radii.loc[1:, 'radius'].to_numpy(),
    radii.loc[1:, 'd_radius'].to_numpy(),
    fmt='kd--',
    ecolor='k',
    elinewidth=0.75,
    capsize=1.5,
    capthick=0.75,
    ms=5,
    label='Data'
)

# Calculate regime change time:
t_rs = radii.loc[iRegime, 'time']

# Plot ideal Regime 1 fit:
r1plot = power([pf_r1[0]/2.25, (2 / 3)], time)
ax.plot(
    time[time >= t_rs],
    r1plot[time >= t_rs],
    'r-',
    linewidth=2
)
ax.plot(
    time[time < t_rs],
    r1plot[time < t_rs],
    'r--',
    linewidth=2
)

# Plot ideal Regime 2 fit:
r2plot = power([pf_r2[0] + 7.5E-2, 1], time)
ax.plot(
    time[time < t_rs],
    r2plot[time < t_rs],
    'g-',
    linewidth=2
)
ax.plot(
    time[time >= t_rs],
    r2plot[time >= t_rs],
    'g--',
    linewidth=2
)

# Plot regime change:
ax.axvline(
    x=t_rs,
    color='k',
    linestyle="--",
    linewidth=1
)

# Fill Regime 2:
ax.axvspan(
    3E-5,
    t_rs,
    alpha=0.20,
    color='green'
)

# Fill Regime 1:
ax.axvspan(
    t_rs,
    1.5E-3,
    alpha=0.20,
    color='red'
)

# set parameters:
#ax.xaxis.set_minor_locator(MultipleLocator(5))
#ax.yaxis.set_minor_locator(MultipleLocator(25))
ax.set_xlabel(' '.join('TIME (s)'), fontproperties=gs_font, fontsize=14)
ax.set_ylabel(' '.join('RADIUS (m)'), fontproperties=gs_font, fontsize=14)
# ax.set_xlim(1E-1, 1E1)
# ax.set_ylim(5E-6, 2E-4)
ax.set_xlim(3E-5, 1.5E-3)
ax.set_ylim(3E-6, 2E-4)
ax.tick_params('x', which='both', top=True, bottom=True)
ax.tick_params('y', which='both', right=True, left=True)
for tick in ax.get_xticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)
for tick in ax.get_yticklabels():
    tick.set_fontname("Gill Sans")
    tick.set_fontsize(14)

# Save plot:
plt.savefig('io/outputs/plots/radii_ideal.png', dpi=300)

# Show plot:
plt.show()

# Calculate ratios ----------------------------------------
# Close all:
plt.close('all')

# Regime 1 ratio:
c1 = pf_r1[0] ** 3

# Regime 2 ratio:
c2 = pf_r2[0]

# Calculate ratio of ratios:
c3 = c1 / c2

# Make independent variable:
rho = np.linspace(1, 1.25, 1000) * (100 ** 3)

# Make dependent variables:
gamma = c1 * rho
eta = gamma / c2

# Basic data analysis -------------------------------------
# Percent difference:
perc_diff_r1 = np.abs((2 / 3) - pf_r1[1]) / (2 / 3)
perc_diff_r2 = np.abs(1 - pf_r2[1]) / 1

# Reduced chi-squared:
chi2nu1 = chisq_r1 / dof_r1
chi2nu2 = chisq_r2 / dof_r2

# End program ---------------------------------------------
