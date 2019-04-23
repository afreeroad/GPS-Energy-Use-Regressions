# Import libraries
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

# Create figure object
fig = plt.figure()

# Get the current axes, creating one if necessary.
ax = fig.gca(projection='3d')

# Get the dataset: from 'GPS' folder, file named: 'full_Dataframe.csv'
# Must run the 'worldbankdata.py' file first, to create most up-to-date .csv file. But, this should be fine.
# Only includes trust data, as of April 3rd, 2019
data = pd.read_csv('full_Dataframe.csv')

# Create a list of colors for each point corresponding to x and y
c_list = data['region_val'].tolist()

# By using zdir='y', the y value of these points is fixed to the zs value 0
# and the (x,y) points are plotted on the x and z axes.
ax.scatter(data['delta_GDPPC_CAGR'], data['mean_trust'], data['delta_EnergyUse_CAGR'], c=c_list)  # / 2e6,

# Set labels according to axis
plt.xlabel('GDP per Capita Growth, 2000-2010 (CAGR)')
plt.ylabel('Trust Preferences')
ax.set_zlabel('Energy Use Growth, 2000-2010 (CAGR)')

# Create customized legends
legend_elements = [Line2D([0], [0], marker='o', color='w',
                          label='GDP per Capita Growth, 2000-2010 (CAGR)',
                          markerfacecolor='r', markersize=10),
                   Line2D([0], [0], marker='o', color='w',
                          label='Energy Use Growth, 2000-2010 (CAGR)',
                          markerfacecolor='g', markersize=10),
                   Line2D([0], [0], marker='o', color='w',
                          label='Trust Preferences',
                          markerfacecolor='b', markersize=10)
                   ]

# Make legend
ax.legend(handles=legend_elements, loc='best')

plt.show()
