import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# --- Function to Create Sphere Animation ---
def create_sphere():
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 25)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z

# Sphere data
x, y, z = create_sphere()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xticks([]), ax.set_yticks([]), ax.set_zticks([]), ax.grid(False), ax.set_axis_off()
norm = mcolors.Normalize(vmin=z.min(), vmax=z.max())
color_map = cm.rainbow(norm(z))
sphere = ax.plot_surface(x, y, z, facecolors=color_map, rstride=1, cstride=1)

def update(frame):
    ax.view_init(elev=10, azim=frame)

ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)