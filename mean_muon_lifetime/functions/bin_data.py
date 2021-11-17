'''
bin_data
-----------------------------------------------------------
perrin w. davidson
10.11.2021
pwd@uchicago.edu
-----------------------------------------------------------
the function for binning spectral data.
-----------------------------------------------------------
inputs:
    spectrum - spectrum to be binned
    channel - channels to bin over
    binsize - size of the news bins in number of all bins
output:
    new_spectrum - newly binned spectrum
'''


def bin_data(channel, spectrum, binsize):

    # Import libraries:
    import numpy as np

    # Determine the new number of channels:
    numdata = int((binsize * (len(spectrum)) / binsize))

    # Make new spectrum:
    new_spectrum = np.sum((spectrum[0:numdata]).reshape(-1, binsize), axis=1)

    # Make new channel:
    new_channel = np.mean((channel[0:numdata]).reshape(-1, binsize), axis=1)

    # Return binned data:
    return new_channel, new_spectrum

