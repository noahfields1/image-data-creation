import numpy as np
import matplotlib.pyplot as plt

# Read the data from the first text file
file1 = 'dave_gradient015.txt'
data1 = np.loadtxt(file1)

# Read the data from the second text file
file2 = 'gabe_clean_gradient.txt'
data2 = np.loadtxt(file2)

# Create a histogram for the data from the first file
plt.hist(data1, bins=10, alpha=0.5, label='Dave_Data_015gradient')

# Create a histogram for the data from the second file
plt.hist(data2, bins=10, alpha=0.5, label='Gabe_Data_015gradient')

# Set labels and title for the histogram
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram Comparison')

# Add a legend to differentiate between the data files
plt.legend()

# Display the histogram
plt.show()

