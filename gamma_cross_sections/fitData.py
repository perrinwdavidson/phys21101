'''
fitData
-----------------------------------------------------------
perrin w. davidson
7.10.2021
pwd@uchicago.edu
-----------------------------------------------------------
this script fits data collected during lab 1 of PHYS 21101.
'''
# import libraries ----------------------------------------
import pandas as pd
import numpy as np
from scipy import interpolate
from functions.exponential import exponential
from functions.data_fit import data_fit
from functions.thomson import thomson
from functions.plot_data import plot_data

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

# clean data ----------------------------------------------
# set the number data collected:
sampNo_137cs = 8
sampNo_22na = 8
sampNo_133ba = 8

# cut data:
data_137cs = data_137cs.iloc[:sampNo_137cs + 1, :]
data_22na = data_22na.iloc[:sampNo_22na + 1, :]
data_133ba = data_133ba.iloc[:sampNo_133ba + 1, :]

# turn mm to cm:
data_137cs['x'] = data_137cs['x'] / 10
data_137cs['dx'] = data_137cs['dx'] / 10

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
f_nist = interpolate.interp1d(
    nist_al['E (keV)'],
    nist_al['mu (cm^-1)'],
    kind='cubic'
)
lin_atten['nist_mu'] = f_nist(energies)
lin_atten['d_nist_mu'] = 0.3 * lin_atten['nist_mu']

# put values into array:
lin_atten.loc[lin_atten['energies'] == 32, 'mu'] = pf_137cs_32[1]
lin_atten.loc[lin_atten['energies'] == 662, 'mu'] = pf_137cs_662[1]

# put errors into array:
lin_atten.loc[lin_atten['energies'] == 32, 'd_mu'] = pferr_137cs_32[1]
lin_atten.loc[lin_atten['energies'] == 662, 'd_mu'] = pferr_137cs_662[1]

# calculate observational cross section -------------------
# set electron density of aluminium:
n_al = 18.1E28

# make data frame:
cross_section = pd.DataFrame({'energies': energies,
                              'sigma': blanks,
                              'd_sigma': blanks})

# calculate values:
cross_section.loc[cross_section['energies'] == 32, 'sigma'] = pf_137cs_32[1] / n_al
cross_section.loc[cross_section['energies'] == 662, 'sigma'] = pf_137cs_662[1] / n_al

# calculate errors:
cross_section.loc[cross_section['energies'] == 32, 'd_sigma'] = pferr_137cs_32[1] / n_al
cross_section.loc[cross_section['energies'] == 662, 'd_sigma'] = pferr_137cs_662[1] / n_al

# calculate thomson cross section -------------------------
# initialize:
cross_section['thomson'] = blanks

# set inputs:
qe = 1.602176634E-19
me = 9.1093837015E-31

# calculate:
cross_section.loc[cross_section['energies'] == 32, 'thomson'] = thomson(qe, me)
cross_section.loc[cross_section['energies'] == 662, 'thomson'] = thomson(qe, me)

# plot data -----------------------------------------------
# 137cs (32 keV):
xplot = np.linspace(data_137cs['x'].min(), data_137cs['x'].max(), 500)
plot_data(
     data_137cs['x'].to_numpy(),
     data_137cs['r_32'].to_numpy(),
     data_137cs['dr_32'].to_numpy(),
     xplot,
     exponential(pf_137cs_32, xplot),
     pf_137cs_32,
     pferr_137cs_32,
     chisq_137cs_32,
     dof_137cs_32,
     'Gamma Transmission Intensity  \n ($^{137}$Cs, Al, E = 32 keV)',
     'Thickness, $x$ (cm)',
     'Count Rate, $R$ (counts/s)',
     'io/outputs/plots/137cs_32.pdf'
)

# 137cs (662 keV):
xplot = np.linspace(data_137cs['x'].min(), data_137cs['x'].max(), 500)
plot_data(
     data_137cs['x'].to_numpy(),
     data_137cs['r_662'].to_numpy(),
     data_137cs['dr_662'].to_numpy(),
     xplot,
     exponential(pf_137cs_662, xplot),
     pf_137cs_662,
     pferr_137cs_662,
     chisq_137cs_662,
     dof_137cs_662,
     'Gamma Transmission Intensity  \n ($^{137}$Cs, Al, E = 662 keV)',
     'Thickness, $x$ (cm)',
     'Count Rate, $R$ (counts/s)',
     'io/outputs/plots/137cs_662.pdf'
)

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
