import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as collections


x = np.linspace(0, 3 * np.pi, 500)
y = np.sin(x)

# Compute the first numerical derivative
dydx = np.cos(0.5 * (x[:-1] + x[1:]))

# Build a line collection, including the vector in the z direction
verts = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([verts[:-1], verts[1:]], axis=1)

fig, ax = plt.subplots(figsize=(7, 4))
ax.add_collection(collections.LineCollection(segments, array=dydx, cmap='coolwarm', norm=plt.Normalize(dydx.min(), dydx.max()),
                  lw=3, alpha=0.7))
ax.autoscale()
fig.colorbar(ax.collections[0], ax=ax)
ax.set_title('Line Collection with colormap')

plt.show()