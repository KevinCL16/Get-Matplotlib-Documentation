import matplotlib.pyplot as plt
import numpy as np

# Sample data for boxplots
data = [np.random.normal(0, 1, 100),
        np.random.normal(0, 2, 100),
        np.random.normal(0, 1, 100),
        np.random.normal(0, 3, 100)]

# Custom styles for boxplots
boxprops = dict(linestyle='--', linewidth=2, color='blue')
medianprops = dict(linestyle='-', linewidth=2, color='orange')
whiskerprops = dict(linestyle='-', linewidth=2, color='green')

# Create a figure and axes
fig, ax = plt.subplots()

# Create boxplots with customization
boxplot = ax.boxplot(data,
                     vert=True,  # Vertical orientation
                     patch_artist=True,  # Fill with color
                     showmeans=True,  # Show mean values
                     boxprops=boxprops,  # Custom box style
                     medianprops=medianprops,  # Custom median style
                     whiskerprops=whiskerprops)  # Custom whisker style

# Customize labels and title
ax.set_xticklabels(['A', 'B', 'C', 'D'])
ax.set_title('Customized Boxplots')

# Customize colors
colors = ['red', 'blue', 'green', 'purple']
for patch, color in zip(boxplot['boxes'], colors):
    patch.set_facecolor(color)

# Show the plot
plt.show()
