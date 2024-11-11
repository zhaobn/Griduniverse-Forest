# %%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Circle, Arc, Rectangle, Patch, Polygon, Ellipse
from matplotlib.lines import Line2D
import os
import random


# %%
def draw_object(shape, color='yellow', size=1.0, pattern='plain'):
  fig, ax = plt.subplots()
  ax.set_aspect('equal')

  # Define the main shape
  if shape == 'circle':
    obj = Circle((0.5, 0.5), 0.5 * size, facecolor=color, edgecolor='white', linewidth=1)
  elif shape == 'square':
    obj = Rectangle((0.5 - 0.5 * size, 0.5 - 0.5 * size), size, size, facecolor=color, edgecolor='white', linewidth=1)
  elif shape == 'triangle':
    obj = Polygon([(0.5, 0.5 + 0.5 * size), (0.5 - 0.5 * size, 0.5 - 0.5 * size), (0.5 + 0.5 * size, 0.5 - 0.5 * size)],
            closed=True, facecolor=color, edgecolor='white', linewidth=1)
  elif shape == 'diamond':
    scaled_size = size * 0.707
    obj = Rectangle((0.5, 0.5 - 0.5 * size), scaled_size, scaled_size, angle=45,
            facecolor=color, edgecolor='white', linewidth=1)
  else:
    raise ValueError("Unsupported shape type. Choose from 'circle', 'square', 'triangle', or 'diamond'.")

  ax.add_patch(obj)

  # Add pattern
  if pattern == 'dots':
    for x in np.linspace(0.1, 0.9, 5):
      for y in np.linspace(0.1, 0.9, 5):
        dot = Circle((x, y), 0.05 * size, facecolor='white', edgecolor='none', alpha=0.6)
        ax.add_patch(dot)

  elif pattern == 'stripes':
    for x in np.linspace(-0.5, 1.5, 10):
      line = Line2D([x, x + 1], [0, 1], color='white', linewidth=20, alpha=0.6)
      ax.add_line(line)

  elif pattern == 'checkered':
    for x in np.linspace(0.1, 0.9, 5):
      line_vertical = Line2D([x, x], [0, 1], color='white', linewidth=15, alpha=0.6)
      line_horizontal = Line2D([0, 1], [x, x], color='white', linewidth=15, alpha=0.6)
      ax.add_line(line_vertical)
      ax.add_line(line_horizontal)

  # Set limits and remove axes for a clean look
  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)
  ax.axis('off')
  fig.patch.set_alpha(0)  # Transparent background

  # Compose the filename based on variables
  filename = f"{shape}_{pattern}_{color}.svg"
  plt.savefig(filename, format="svg", bbox_inches='tight', transparent=True)
  plt.close(fig)

# Example usage:
draw_object('circle', color='yellow', pattern='plain')
draw_object('square', color='red', pattern='dots')
draw_object('circle', color='green', pattern='stripes')
draw_object('diamond', color='blue', pattern='heckered')

# %%
