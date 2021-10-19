'''
fitEnergies
-----------------------------------------------------------
this script fits energies collected during lab 1 of PHYS 21101.
'''
# import libraries ----------------------------------------
import pandas as pd
import numpy as np
from scipy import interpolate
from functions.exponential import exponential
from functions.data_fit import data_fit
from functions.thomson import thomson
from functions.plot_data import plot_data
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# read inputs ---------------------------------------------
# set input names:
io_path = 'io/inputs/'
data_file = 'gammaEnergies.xlsx'
file_name = io_path + data_file

# read data:
data_137cs = pd.read_excel(
    file_name,
    '137cs'
)
data_22na = pd.read_excel(
    file_name,
    '22na'
)
data_133ba = pd.read_excel(
    file_name,
    '133ba'
)

# re-set filename and load nist data:
data_file = 'nist_mu_al.txt'
file_name = io_path + data_file
nist_al = pd.read_table(
    file_name
)

# clean data ----------------------------------------------ds
# turn mm to cm:
data_137cs['x'] = data_137cs['x'] / 10
data_137cs['dx'] = data_137cs['dx'] / 10
data_22na['x'] = data_22na['x'] / 10
data_22na['dx'] = data_22na['dx'] / 10
data_133ba['x'] = data_133ba['x'] / 10
data_133ba['dx'] = data_133ba['dx'] / 10

# fit data ------------------------------------------------
# 137cs - 32 keV:
my_guess_137cs_32 = [10, 1, 5]
pf_137cs_32, pferr_137cs_32, chisq_137cs_32, dof_137cs_32 = data_fit(
    my_guess_137cs_32,
    exponential,
    data_137cs['x'].to_numpy(),
    data_137cs['r_32'].to_numpy(),
    data_137cs['dr_32'].to_numpy(),
    'Exponential Fit: 137Cs (32 keV)'
)

# 137cs - 32 keV:
my_guess_137cs_662 = [10, 1, 5]
pf_137cs_662, pferr_137cs_662, chisq_137cs_662, dof_137cs_662 = data_fit(
    my_guess_137cs_662,
    exponential,
    data_137cs['x'].to_numpy(),
    data_137cs['r_662'].to_numpy(),
    data_137cs['dr_662'].to_numpy(),
    'Exponential Fit: 137Cs (662 keV)'
)

# 22na - 511 keV:
my_guess_22na_511 = [10, 1, 5]
pf_22na_511, pferr_22na_511, chisq_22na_511, dof_22na_511 = data_fit(
    my_guess_22na_511,
    exponential,
    data_22na['x'].to_numpy(),
    data_22na['r_511'].to_numpy(),
    data_22na['dr_511'].to_numpy(),
    'Exponential Fit: 22Na (511 keV)'
)

# 22na - 1275 keV:
my_guess_22na_1275 = [10, 1, 5]
pf_22na_1275, pferr_22na_1275, chisq_22na_1275, dof_22na_1275 = data_fit(
    my_guess_22na_1275,
    exponential,
    data_22na['x'].to_numpy(),
    data_22na['r_1275'].to_numpy(),
    data_22na['dr_1275'].to_numpy(),
    'Exponential Fit: 22Na (1275 keV)'
)

# 133ba - 31 keV:
my_guess_133ba_31 = [10, 1, 5]
pf_133ba_31, pferr_133ba_31, chisq_133ba_31, dof_133ba_31 = data_fit(
    my_guess_133ba_31,
    exponential,
    data_133ba['x'].to_numpy(),
    data_133ba['r_31'].to_numpy(),
    data_133ba['dr_31'].to_numpy(),
    'Exponential Fit: 133Ba (31 keV)'
)

# 133ba - 81 keV:
my_guess_133ba_81 = [10, 1, 5]
pf_133ba_81, pferr_133ba_81, chisq_133ba_81, dof_133ba_81 = data_fit(
    my_guess_133ba_81,
    exponential,
    data_133ba['x'].to_numpy(),
    data_133ba['r_81'].to_numpy(),
    data_133ba['dr_81'].to_numpy(),
    'Exponential Fit: 133Ba (81 keV)'
)

# 133ba - 356 keV:
my_guess_133ba_356 = [10, 1, 5]
pf_133ba_356, pferr_133ba_356, chisq_133ba_356, dof_133ba_356 = data_fit(
    my_guess_133ba_356,
    exponential,
    data_133ba['x'].to_numpy(),
    data_133ba['r_356'].to_numpy(),
    data_133ba['dr_356'].to_numpy(),
    'Exponential Fit: 133Ba (356 keV)'
)

# calculate linear attenuation coefficient ----------------
# make data frame:
energies = np.transpose([32, 662, 511, 1275, 31, 81, 356])
energies = np.sort(energies)
blanks = np.empty((np.shape(energies)))
blanks[:] = np.nan
lin_atten = pd.DataFrame({'energies': energies,
                          'mu': blanks,
                          'd_mu': blanks,
                          'nist_mu': blanks,
                          'd_nist_mu': blanks})

# interpolate nist values:
nist_err = 0.03
f_nist = interpolate.UnivariateSpline(
    nist_al['E (keV)'],
    nist_al['mu (cm^-1)'],
    w=1 / (nist_err * nist_al['mu (cm^-1)'])
)
lin_atten['nist_mu'] = f_nist(energies)

# interpolate nist error values:
f_nist_err = interpolate.UnivariateSpline(
    nist_al['E (keV)'],
    nist_err * nist_al['mu (cm^-1)']
)
lin_atten['d_nist_mu'] = f_nist_err(energies)

# put values into array:
lin_atten.loc[lin_atten['energies'] == 32, 'mu'] = pf_137cs_32[1]
lin_atten.loc[lin_atten['energies'] == 662, 'mu'] = pf_137cs_662[1]
lin_atten.loc[lin_atten['energies'] == 511, 'mu'] = pf_22na_511[1]
lin_atten.loc[lin_atten['energies'] == 1275, 'mu'] = pf_22na_1275[1]
lin_atten.loc[lin_atten['energies'] == 31, 'mu'] = pf_133ba_31[1]
lin_atten.loc[lin_atten['energies'] == 81, 'mu'] = pf_133ba_81[1]
lin_atten.loc[lin_atten['energies'] == 356, 'mu'] = pf_133ba_356[1]

# put errors into array:
lin_atten.loc[lin_atten['energies'] == 32, 'd_mu'] = pferr_137cs_32[1]
lin_atten.loc[lin_atten['energies'] == 662, 'd_mu'] = pferr_137cs_662[1]
lin_atten.loc[lin_atten['energies'] == 511, 'd_mu'] = pferr_22na_511[1]
lin_atten.loc[lin_atten['energies'] == 1275, 'd_mu'] = pferr_22na_1275[1]
lin_atten.loc[lin_atten['energies'] == 31, 'd_mu'] = pferr_133ba_31[1]
lin_atten.loc[lin_atten['energies'] == 81, 'd_mu'] = pferr_133ba_81[1]
lin_atten.loc[lin_atten['energies'] == 356, 'd_mu'] = pferr_133ba_356[1]

# calculate observational cross section -------------------
# set electron density of aluminium:
rho = 2.70 * 1000  # kg/m3
Z = 13  # electrons/atom
A = 26.9815384 / 1000  # kg/mol
AvoNum = 6.02214E23  # atom/mol
n_al = (rho * Z * AvoNum) / A  # kg/m3 * electrons/atom * atom/mol * mol/kg = electrons/m3

# make data frame:
cross_section = pd.DataFrame({'energies': energies,
                              'sigma': blanks,
                              'd_sigma': blanks})

# calculate values:
cross_section.loc[cross_section['energies'] == 32, 'sigma'] = pf_137cs_32[1] / n_al
cross_section.loc[cross_section['energies'] == 662, 'sigma'] = pf_137cs_662[1] / n_al
cross_section.loc[cross_section['energies'] == 511, 'sigma'] = pf_22na_511[1] / n_al
cross_section.loc[cross_section['energies'] == 1275, 'sigma'] = pf_22na_1275[1] / n_al
cross_section.loc[cross_section['energies'] == 31, 'sigma'] = pf_133ba_31[1] / n_al
cross_section.loc[cross_section['energies'] == 81, 'sigma'] = pf_133ba_81[1] / n_al
cross_section.loc[cross_section['energies'] == 356, 'sigma'] = pf_133ba_356[1] / n_al

# calculate errors:
cross_section.loc[cross_section['energies'] == 32, 'd_sigma'] = pferr_137cs_32[1] / n_al
cross_section.loc[cross_section['energies'] == 662, 'd_sigma'] = pferr_137cs_662[1] / n_al
cross_section.loc[cross_section['energies'] == 511, 'd_sigma'] = pferr_22na_511[1] / n_al
cross_section.loc[cross_section['energies'] == 1275, 'd_sigma'] = pferr_22na_1275[1] / n_al
cross_section.loc[cross_section['energies'] == 31, 'd_sigma'] = pferr_133ba_31[1] / n_al
cross_section.loc[cross_section['energies'] == 81, 'd_sigma'] = pferr_133ba_81[1] / n_al
cross_section.loc[cross_section['energies'] == 356, 'd_sigma'] = pferr_133ba_356[1] / n_al

# calculate thomson cross section -------------------------
# initialize:
cross_section['thomson'] = blanks

# set inputs:
qe = 1.602176634 * (10 ** -19)
dqe = 0
me = 9.1093837015 * (10 ** -31)
dme = 0.0000000028 * (10 ** -31)

# calculate values:
cross_section.loc[cross_section['energies'] == 32, 'thomson'] = thomson(qe, me)
cross_section.loc[cross_section['energies'] == 662, 'thomson'] = thomson(qe, me)
cross_section.loc[cross_section['energies'] == 511, 'thomson'] = thomson(qe, me)
cross_section.loc[cross_section['energies'] == 1275, 'thomson'] = thomson(qe, me)
cross_section.loc[cross_section['energies'] == 31, 'thomson'] = thomson(qe, me)
cross_section.loc[cross_section['energies'] == 81, 'thomson'] = thomson(qe, me)
cross_section.loc[cross_section['energies'] == 356, 'thomson'] = thomson(qe, me)

# calculate error:
cross_section.loc[:, 'd_thomson'] = cross_section.loc[:, 'thomson'] * 2 * (dme / me)

# set up plotting:
gs_font = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/GillSans.ttc')
plt.style.use('io/inputs/old-style.mplstyle')

# plot:
fig, ax = plt.subplots(1, 1, figsize=(7, 7))
ax.errorbar(
    cross_section['energies'],
    cross_section['sigma']*100 / 1e-28,
    cross_section['d_sigma']*100 / 1e-28,
    fmt='rd',
    ecolor='k',
    elinewidth=0.75*2,
    capsize=1.5*2,
    capthick=0.75*2,
    ms=2.5*2,
    label='Experimental'
)

# plot thomson:
ax.errorbar(
    cross_section['energies'],
    cross_section['thomson'] / 1e-28,
    cross_section['d_thomson'] / 1e-28,
    fmt='k--',
    elinewidth=0.75*2,
    capsize=1.5*2,
    capthick=0.75*2,
    ms=2.5*2,
    label='Thomson'
)

ax.xaxis.set_minor_locator(MultipleLocator(100))
ax.yaxis.set_minor_locator(MultipleLocator(0.25))
ax.set_xlabel(' '.join('ENERGY (keV)'), fontproperties=gs_font, fontsize=14)
ax.set_ylabel(' '.join('CROSS SECTION ($10^{-28}$M$^2$)'), fontproperties=gs_font, fontsize=16)
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
#ax.set_title(' '.join(title), fontproperties=gs_font, fontsize=16)

# output:
#plt.legend()
plt.savefig('io/outputs/reports/images/sigma.png', dpi=300)
plt.show()

# plot data -----------------------------------------------
gs_font = fm.FontProperties(fname='/System/Library/Fonts/Supplemental/GillSans.ttc')
plt.style.use('io/inputs/old-style.mplstyle')

# make figure:
fig, ((ax32, ax662, axNo1), (ax511, ax1275, axNo2), (ax31, ax81, ax356)) = plt.subplots(3, 3, figsize=(26, 21), dpi=300)

# 137cs (32 keV) -----------------
xplot = np.linspace(data_137cs['x'].min(), data_137cs['x'].max(), 500)
plot_data(
     ax32,
     data_137cs['x'].to_numpy(),
     data_137cs['r_32'].to_numpy(),
     data_137cs['dr_32'].to_numpy(),
     xplot,
     exponential(pf_137cs_32, xplot),
     pf_137cs_32,
     pferr_137cs_32,
     chisq_137cs_32,
     dof_137cs_32,
     '32 keV',
     '',
     '$^{137}$Cs',
     'io/outputs/plots/137cs_32.pdf',
     1
)

# 137cs (662 keV) -----------------
xplot = np.linspace(data_137cs['x'].min(), data_137cs['x'].max(), 500)
plot_data(
     ax662,
     data_137cs['x'].to_numpy(),
     data_137cs['r_662'].to_numpy(),
     data_137cs['dr_662'].to_numpy(),
     xplot,
     exponential(pf_137cs_662, xplot),
     pf_137cs_662,
     pferr_137cs_662,
     chisq_137cs_662,
     dof_137cs_662,
     '662 keV',
     '',
     '',
     'io/outputs/plots/137cs_662.pdf',
    2.5
)

# 22na (511 keV) -----------------
xplot = np.linspace(data_22na['x'].min(), data_22na['x'].max(), 500)
plot_data(
     ax511,
     data_22na['x'].to_numpy(),
     data_22na['r_511'].to_numpy(),
     data_22na['dr_511'].to_numpy(),
     xplot,
     exponential(pf_22na_511, xplot),
     pf_22na_511,
     pferr_22na_511,
     chisq_22na_511,
     dof_22na_511,
     '511 keV',
     '',
     '$^{22}$Na',
     'io/outputs/plots/22na_511.pdf',
    5
)

# 22na (1275 keV) -----------------
xplot = np.linspace(data_22na['x'].min(), data_22na['x'].max(), 500)
plot_data(
     ax1275,
     data_22na['x'].to_numpy(),
     data_22na['r_1275'].to_numpy(),
     data_22na['dr_1275'].to_numpy(),
     xplot,
     exponential(pf_22na_1275, xplot),
     pf_22na_1275,
     pferr_22na_1275,
     chisq_22na_1275,
     dof_22na_1275,
     '1275 keV',
     '',
     '',
     'io/outputs/plots/22na_1275.pdf',
    1
)

# 133ba (31 keV) -----------------
xplot = np.linspace(data_133ba['x'].min(), data_133ba['x'].max(), 500)
plot_data(
     ax31,
     data_133ba['x'].to_numpy(),
     data_133ba['r_31'].to_numpy(),
     data_133ba['dr_31'].to_numpy(),
     xplot,
     exponential(pf_133ba_31, xplot),
     pf_133ba_31,
     pferr_133ba_31,
     chisq_133ba_31,
     dof_133ba_31,
     '31 keV',
     '',
     '$^{133}$Ba',
     'io/outputs/plots/133ba_31.pdf',
    25
)

# 133ba (81 keV) -----------------
xplot = np.linspace(data_133ba['x'].min(), data_133ba['x'].max(), 500)
plot_data(
     ax81,
     data_133ba['x'].to_numpy(),
     data_133ba['r_81'].to_numpy(),
     data_133ba['dr_81'].to_numpy(),
     xplot,
     exponential(pf_133ba_81, xplot),
     pf_133ba_81,
     pferr_133ba_81,
     chisq_133ba_81,
     dof_133ba_81,
     '81 keV',
     '',
     '',
     'io/outputs/plots/133ba_81.pdf',
    10
)

# 133ba (356 keV) -----------------
xplot = np.linspace(data_133ba['x'].min(), data_133ba['x'].max(), 500)
plot_data(
     ax356,
     data_133ba['x'].to_numpy(),
     data_133ba['r_356'].to_numpy(),
     data_133ba['dr_356'].to_numpy(),
     xplot,
     exponential(pf_133ba_356, xplot),
     pf_133ba_356,
     pferr_133ba_356,
     chisq_133ba_356,
     dof_133ba_356,
     '356 keV',
     '',
     '',
     'io/outputs/plots/133ba_356.pdf',
    10
)

# Make look nice -----------------
axNo1.axis('off')
axNo2.axis('off')
fig.add_subplot(111, frameon=False)
plt.style.use('io/inputs/old-style.mplstyle')
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel(' '.join('\n THICKNESS (CM)'), fontproperties=gs_font, fontsize=22)
plt.ylabel(' '.join('COUNT RATE (COUNTS/SEC) \n \n'), fontproperties=gs_font, fontsize=22)
#plt.title("Rates of Intensity \n \n", fontproperties=gs_font, fontsize=24)
#plt.show()
fig.tight_layout(pad=3.0)
plt.savefig('io/outputs/reports/images/linear_attenuation.png', dpi=300)

# Save output ---------------------------------------------
# linear attenuation coefficient:
lin_atten.to_excel(
    'io/outputs/data/linear_atten.xlsx'
)

# cross section:
cross_section.to_excel(
    'io/outputs/data/cross_section.xlsx'
)

# end routine
