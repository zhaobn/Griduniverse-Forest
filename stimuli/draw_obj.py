# %%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
from matplotlib.lines import Line2D

# %%
colors = ['#FF0000', '#FF7F00', '#CCCC00', '#008000', '#0000FF', '#8B00FF', '#4B0082']
default_color = '#d3d3d3'

def draw_object(shape, pattern='plain', level=0, size=1.0, prefix='', save=True):

  # set color
  color = default_color if level >= len(colors) else colors[level]

  # draw object
  fig, ax = plt.subplots()
  ax.set_aspect('equal')

  # define the main shape
  if shape == 'circle':
    obj = Circle((0.5, 0.5), 0.5 * size, facecolor=color, edgecolor='white', linewidth=1)

  elif shape == 'square':
    obj = Rectangle((0.5 - 0.5 * size, 0.5 - 0.5 * size), size, size, facecolor=color, edgecolor='white', linewidth=1)

  elif shape == 'triangle':
    vertices = [(0.5, 0.5 + 0.5 * size), (0.5 - 0.5 * size, 0.5 - 0.5 * size), (0.5 + 0.5 * size, 0.5 - 0.5 * size)]
    obj = Polygon(vertices, closed=True, facecolor=color, edgecolor='white', linewidth=1)

  elif shape == 'diamond':
    scaled_size = size * 0.707
    obj = Rectangle((0.5, 0.5 - 0.5 * size), scaled_size, scaled_size, angle=45,
            facecolor=color, edgecolor='white', linewidth=1)

  else:
    raise ValueError("Unsupported shape type. Choose from 'circle', 'square', 'triangle', or 'diamond'.")

  ax.add_patch(obj)
  clip_path = obj.get_path()
  clip_transform = obj.get_transform()

  # add pattern
  if pattern == 'dots':
    for x in np.linspace(0.1, 0.9, 5):
      for y in np.linspace(0.1, 0.9, 5):
        dot = Circle((x, y), 0.05 * size, facecolor='white', edgecolor='none', alpha=0.6)
        dot.set_clip_path(clip_path, clip_transform)
        ax.add_patch(dot)

  elif pattern == 'stripes':
    for x in np.linspace(-0.5, 1.5, 10):
      line = Line2D([x, x + 1], [0, 1], color='white', linewidth=20, alpha=0.6)
      line.set_clip_path(clip_path, clip_transform)
      ax.add_line(line)

  elif pattern == 'checkered':
    for x in np.linspace(0.1, 0.9, 5):
      line_vertical = Line2D([x, x], [0, 1], color='white', linewidth=15, alpha=0.6)
      line_horizontal = Line2D([0, 1], [x, x], color='white', linewidth=15, alpha=0.6)
      line_vertical.set_clip_path(clip_path, clip_transform)
      line_horizontal.set_clip_path(clip_path, clip_transform)
      ax.add_line(line_vertical)
      ax.add_line(line_horizontal)

  # set limits and remove axes for a clean look
  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)
  ax.axis('off')
  fig.patch.set_alpha(0)  # Transparent background

  if save:
    # compose the filename based on variables
    filename = f"{prefix}{shape}_{pattern}_{level}.svg"
    plt.savefig(filename, format="svg", bbox_inches='tight', transparent=True)
    plt.close(fig)

# %% Example usage:
# draw_object('circle', pattern='plain', level=2, prefix='../dlgr/griduniverse/static/images/objs/')
# draw_object('square', pattern='dots', level=3, save=False)
# draw_object('circle', pattern='stripes', level=8, save=False)
# draw_object('diamond', pattern='checkered', save=False)

# %% Generate stimuli img for experiment
all_shapes = ['circle', 'square', 'triangle', 'diamond']
all_textures = ['plain', 'dots', 'stripes', 'checkered']
max_level = 6
file_prefix = '../dlgr/griduniverse/static/images/objs/'

for k in range(max_level):
  for i in all_shapes:
    for j in all_textures:
      draw_object(i, j, k, 1, file_prefix, True)
