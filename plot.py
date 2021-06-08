from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np

# Defines the chart font style
# font = {'family' : 'Times New Roman',
#         'weight' : 'bold',
#         'size'   : 18}

# includes the chart font style
# plt.rc('font', **font)

# You can also define like this
# plt.rcParams["font.family"] = "Times New Roman"

# To define figure size
figure(num=None, figsize=(10, 6))

# Defines X-axis labels and Y-axis values
x_axis_labels = ['Proposed Solution', 'by States', 'by Population', 'by Infection']
y_axis_values = [181, 234, 240, 156]

# mab = 326;
# m2 = 363;
# m3 =362;
# m4 = 330;

# Creating n-dimensional array with evenly spaced values
y_pos=np.arange(len(x_axis_labels))

# Input bar values
# Define the bar styles with width, color, and legend labels
plt.bar(y_pos + 0, y_axis_values, width=0.5, color = 'navy', label='legend title')

# Define X-axis labels
plt.xticks(y_pos, x_axis_labels)

# Defines best position of the legend in the figure
# plt.legend(loc='best')

# Defines X and Y axis labels
plt.ylabel('Number of Death')
plt.xlabel('Vaccine Distribution Policy')

# Defines plot title
plt.title("Infection rate: (.01, .1 ,.01) ")

# Show the plot
plt.show()