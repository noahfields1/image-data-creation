import numpy as np
import matplotlib.pyplot as plt

# Read the data from the file
with open('median_gabe.txt', 'r') as f:
    lines = f.readlines()

# Extract x, y values
data = [line.strip().split(',') for line in lines]
x_values = [float(row[0]) for row in data]
y_values = [float(row[1]) for row in data]

# Create a 2D histogram of x, y values
heatmap, x_edges, y_edges = np.histogram2d(x_values, y_values, bins=(240, 240), range=[[0, 240], [0, 240]])

# Plot the heatmap
plt.imshow(heatmap.T, cmap='hot', origin='lower', extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]])
plt.colorbar()

# Set labels and title
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Gabe 2D Heatmap')

# Show the plot
plt.show()

