'''
plot_regimes
-----------------------------------------------------------
plotting the two to three different regimes in the
drop pinch off.
'''
# load packages -------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data -----------------------------------------------
# set input names:
io_path = 'io/inputs/'
data_file = 'radius_min.xlsx'
file_name = io_path + data_file

# read data:
data_rmin = pd.read_excel(file_name)

# set data ------------------------------------------------
# pinch off time:
t0 = 5.23  # seconds

# pixel to meter conversation rate:
px2m = 164090  # px m-1
dpx2m = 29360  # px m-1

# data conversion -----------------------------------------
# convert time to delta time:
data_rmin['t'] = t0 - data_rmin['t']

# convert pixels to meters:
data_rmin['r'] = data_rmin['r'] / px2m
data_rmin['dr'] = data_rmin['dr'] / px2m

# plot data -----------------------------------------------
# initialize figure and axis:
fig, ax = plt.subplots(figsize=(10, 8))

# plot:
ax.loglog(
    data_rmin['t'],
    data_rmin['r'],
    '.k'
)

# add in labels:
ax.set_xlabel('Time (s)')
ax.set_ylabel('Radius (m)')
ax.set_title('Drop Pinch-Off Radius over Time')

# show plot:
plt.show()

# finish routine ------------------------------------------
