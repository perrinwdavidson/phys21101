'''
mean_muon
-----------------------------------------------------------
perrin w. davidson
10.11.2021
pwd@uchicago.edu
-----------------------------------------------------------
performing the data analysis for the mean lifetime of a
muon.
'''
# Load packages -------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from functions.data_fit import data_fit
from functions.exponential import exponential
from functions.linear import linear

# Load data -----------------------------------------------
# Set input path:
inputs_basepath = 'io/inputs/'

# Read distribution:
filename = 'lifetime_muon.tsv'
spectrum = pd.read_csv(
    inputs_basepath + filename,
    sep='\t'
)

# Read time calibration:
filename = 'time_calibration.xlsx'
time_calib = pd.read_excel(
    inputs_basepath + filename
)

# Set total run time:
s2min = 60  # s min-1
us2s = 10 ** 6
runtime = 249174.29 / s2min  # minutes
d_runtime = 0.2 / (us2s * s2min)  # minutes, precision of measurement

# Set system parameters:
r_muon = 1381
d_r_muon = 1
muon_decay_perc = 0.01
t_pha = 15 / (us2s * s2min)  # minutes, T < 20 us
d_t_pha = 1 / (us2s * s2min)  # minutes, T < 20 us

# Quality control data ------------------------------------
# Remove energy from spectrum:
spectrum = spectrum.drop(['Energy'], axis=1)

# Set start and stop channels:
start_channel = 13
stop_channel = 511 + 1
spectrum = spectrum.iloc[start_channel:stop_channel, :].reset_index(drop=True)

# notice that we cut the data. this is because we are dealing with a wide spectrum
# and there were some abnormalities at either end of the spectrum. we believe that
# these data were poor given the decrease in precision of the TAC at either end of
# its range, which is at the lower and upper channel levels.

# Remove counts with 0:
spectrum = spectrum.loc[~(spectrum['Counts'] == 0), :]

# Calculate uncertainties:
spectrum['d_counts'] = np.sqrt(spectrum['Counts'])

# Fit time calibration ------------------------------------
# Set guess:
p0_time_calib = [(4 / 100), 1.5]

# Calculate the Day 1 fit:
pf_time1, pferr_time1, chisq_time1, dof_time1 = data_fit(
    p0_time_calib,
    linear,
    time_calib['channel_d1'].dropna(),
    time_calib['delay_d1'].dropna(),
    time_calib['d_delay_d1'].dropna(),
    'Linear Fit: Day 1 Time Calibration'
)

# Calculate the Day 2 fit:
pf_time2, pferr_time2, chisq_time2, dof_time2 = data_fit(
    p0_time_calib,
    linear,
    time_calib['channel_d2'].dropna(),
    time_calib['delay_d2'].dropna(),
    time_calib['d_delay_d2'].dropna(),
    'Linear Fit: Day 2 Time Calibration'
)

# We will use this fit to convert our tau = x in the linear fit equation
# once we fit the data.

# Average values:
p_time = (pf_time1 + pf_time2) / 2
d_p_time = np.sqrt(((pferr_time1[0] / 2) ** 2)
                   + ((pferr_time2[0] / 2) ** 2))  # taken from part. deriv. error prop.

# Plot time calibration -----------------------------------
# Make channel axis:
channel_plot = np.linspace(
    min(time_calib[['channel_d1', 'channel_d2']].to_numpy().flatten()),
    max(time_calib[['channel_d1', 'channel_d2']].to_numpy().flatten()),
    5000
)

# Make figure and axis:
fig_time, ax = plt.subplots(figsize=(6, 5), dpi=300)

# Plot Day 1 calibration:
ax.errorbar(
    time_calib['channel_d1'],
    time_calib['delay_d1'],
    time_calib['d_delay_d1'],
    fmt='.r',
    label='Day 1'
)

# Plot Day 1 fit:
ax.plot(
    channel_plot,
    linear(pf_time1, channel_plot),
    '--r'
)

# Plot Day 2 calibration:
ax.errorbar(
    time_calib['channel_d2'],
    time_calib['delay_d2'],
    time_calib['d_delay_d2'],
    fmt='.b',
    label='Day 2'
)

# Plot Day 2 fit:
ax.plot(
    channel_plot,
    linear(pf_time2, channel_plot),
    '--b'
)

# Set plot characteristics:
ax.set_xlabel('Channel')
ax.set_ylabel('Delay ($\mu$s)')
ax.set_title('Delay Calibration')
ax.legend()

# Show plot:
plt.show()

# Fit distribution ----------------------------------------
# Set guess:
p0_spectrum = [300, 75, 5]

# Calculate the spectrum fit:
pf_spectrum, pferr_spectrum, chisq_spectrum, dof_spectrum = data_fit(
    p0_spectrum,
    exponential,
    spectrum['Channel'],
    spectrum['Counts'],
    spectrum['d_counts'],
    'Exponential Fit: Muon Decay Spectrum'
)

# we need a background fit because we are dealing with the convolution of
# two exponentials, where the background is one of them. The background is
# not truly a constant. However, we can assume that it is a constant because
# the e-folding length is so large and the amplitude so small relative to that of the
# actual spectrum that by magnitude comparison it is essentially linear. Additionally,
# when we consider these in log scale, this means that we are dealing with a linear scale,
# so this means that we are only one transformation away and the difference in slope is
# great, supporting our assumption that we can basically consider it a constant.

# Plot fit distribution -----------------------------------
# Make channel axis:
channel_plot = np.linspace(
    min(spectrum['Channel']),
    max(spectrum['Channel']),
    5000
)

# Make figure and axis:
fig_spec, ax = plt.subplots(figsize=(6, 5), dpi=300)

# Plot Day 1 calibration:
ax.errorbar(
    spectrum['Channel'],
    spectrum['Counts'],
    spectrum['d_counts'],
    fmt='.k',
    zorder=1
)

# Plot spectrum fit:
ax.plot(
    channel_plot,
    exponential(pf_spectrum, channel_plot),
    '--r',
    zorder=2
)

# Set plot characteristics:
ax.set_xlabel('Channel')
ax.set_ylabel('Counts')
ax.set_title('Muon Decay Spectrum')

# Show plot:
plt.show()

# Get mean life time through conversion -------------------
# Extract mean lifetime:
tau_channel = pf_spectrum[1]
d_tau_channel = pferr_spectrum[1]

# Convert to time units:
tau_time = p_time[0] * tau_channel  # only slope used
d_tau_time = np.sqrt(((tau_channel * d_p_time) ** 2)
                     + ((p_time[0] * d_tau_channel) ** 2))  # again deriv. form of error

# Calculate accidental rates ------------------------------
# Calculate total number of data points:
num_data = spectrum.shape[0]
d_num_data = 1  # precision of measurement

# Calculate accident rate:
r_acc_experiment = (pf_spectrum[2] * num_data) / runtime  # counts / min
d_r_acc_experiment = np.sqrt(((num_data / runtime * pferr_spectrum[2]) ** 2)
                      + ((pf_spectrum[2] / runtime * d_num_data) ** 2)
                      + ((pf_spectrum[2] / (runtime ** 2) * d_runtime) ** 2))

# Calculate expected rate:
rate_muon = (r_muon * muon_decay_perc)  # muon min-1

# Calculate expected accidental rate:
r_acc_expected = (rate_muon ** 2) * t_pha
d_r_acc_expected = np.sqrt(((2 * r_acc_expected * t_pha * d_r_muon) ** 2)
                           + (((r_acc_expected ** 2) * d_t_pha) ** 2))

# Correct for muon environment ----------------------------
# Scale up:
tau_scale_up = 1.04

# Scale up tau:
tau_time_scaled = tau_time * tau_scale_up

# End program ---------------------------------------------
