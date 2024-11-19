# %%
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Circle, Arc, Rectangle, Patch, Polygon, Ellipse, PathPatch
from matplotlib.lines import Line2D
import matplotlib.path as mpath
import os
import random

import yaml


# %%
colors = ["#FF6666", "#66CC66", "##66cc66", "#CC66FF", "#300817", "#66CC66"]

def draw_object(shape, pattern='plain', level=0, size=1.0, prefix='', save=True):
  fig, ax = plt.subplots()
  ax.set_aspect('equal')

  # Get colors
  if level >= len(colors):
    color = colors[-1]
  else:
    color = colors[level]

  # Define the main shape
  if shape == 'circle':
    obj = Circle((0.5, 0.5), 0.5 * size, facecolor=color, edgecolor='white', linewidth=1)
    clip_path = obj

  elif shape == 'square':
    obj = Rectangle((0.5 - 0.5 * size, 0.5 - 0.5 * size), size, size, facecolor=color, edgecolor='white', linewidth=1)
    clip_path = obj

  elif shape == 'triangle':
    vertices = [(0.5, 0.5 + 0.5 * size), (0.5 - 0.5 * size, 0.5 - 0.5 * size), (0.5 + 0.5 * size, 0.5 - 0.5 * size)]
    obj = Polygon(vertices, closed=True, facecolor=color, edgecolor='white', linewidth=1)
    clip_path = obj

  elif shape == 'diamond':
    scaled_size = size * 0.707
    obj = Rectangle((0.5, 0.5 - 0.5 * size), scaled_size, scaled_size, angle=45,
            facecolor=color, edgecolor='white', linewidth=1)
    clip_path = obj

  else:
    raise ValueError("Unsupported shape type. Choose from 'circle', 'square', 'triangle', or 'diamond'.")

  ax.add_patch(obj)

  # Add pattern
  if pattern == 'dots':
    for x in np.linspace(0.1, 0.9, 5):
      for y in np.linspace(0.1, 0.9, 5):
        dot = Circle((x, y), 0.05 * size, facecolor='white', edgecolor='none', alpha=0.6)
        dot.set_clip_path(clip_path)
        ax.add_patch(dot)

  elif pattern == 'stripes':
    for x in np.linspace(-0.5, 1.5, 10):
      line = Line2D([x, x + 1], [0, 1], color='white', linewidth=20, alpha=0.6)
      line.set_clip_path(clip_path, ax.transData)
      ax.add_line(line)

  elif pattern == 'checkered':
    for x in np.linspace(0.1, 0.9, 5):
      line_vertical = Line2D([x, x], [0, 1], color='white', linewidth=15, alpha=0.6)
      line_horizontal = Line2D([0, 1], [x, x], color='white', linewidth=15, alpha=0.6)
      line_vertical.set_clip_path(clip_path, ax.transData)
      line_horizontal.set_clip_path(clip_path, ax.transData)
      ax.add_line(line_vertical)
      ax.add_line(line_horizontal)

  # Set limits and remove axes for a clean look
  ax.set_xlim(0, 1)
  ax.set_ylim(0, 1)
  ax.axis('off')
  fig.patch.set_alpha(0)  # Transparent background

  if save:
    # Compose the filename based on variables
    filename = f"{prefix}{shape}_{pattern}_{level}.svg"
    plt.savefig(filename, format="svg", bbox_inches='tight', transparent=True)
    plt.close(fig)

# # Example usage:
# draw_object('circle', pattern='plain', level=2, prefix='../dlgr/griduniverse/static/images/objs/')
# draw_object('square', pattern='dots', level=3, save=False)
# draw_object('circle', pattern='stripes', level=8)
# draw_object('diamond', pattern='heckered')


# %% code up a minimal demo

file_prefix = '../dlgr/griduniverse/static/images/objs/'

all_shapes = ['circle', 'square']
all_textures = ['plain', 'dots']

items = []
all_objs = []

for shape in all_shapes:
  for texture in all_textures:

    draw_object(shape, pattern=texture, level=0, prefix=file_prefix)
    name = f"{shape}_{texture}_0"

    all_objs.append(name)

    item = {
      "sprite": "image:objs/" + name + '.svg',
      "name": name,
      "item_id": name,
      "calories": 1,
      "item_count": 1
    }
    items.append(item)


transitions = []
new_objs = []
new_items = []

for a in all_objs:
  for b in all_objs:

    # simple rule: both plain
    if a.split('_')[1] == b.split('_')[1] and a.split('_')[1] == 'plain':

      r_shape = a.split('_')[0]
      r_texture = b.split('_')[1]
      r_level = max([int(a.split('_')[2]), int(b.split('_')[2])]) + 1

      r_name = f"{r_shape}_{r_texture}_{r_level}"

      if r_name not in new_objs:
        draw_object(r_shape, pattern=r_texture, level=r_level, prefix=file_prefix)
        new_objs.append(r_name)
        item = {
          "sprite": "image:objs/" + r_name + '.svg',
          "name": r_name,
          "item_id": r_name,
          "calories": 2 * r_level,
          "item_count": 0
        }
        new_items.append(item)

      transition = {
        'actor_start': a,
        'actor_end': a,
        'target_start': b,
        'target_end': r_name,
        'modify_uses': ''
      }

    else:

      transition = {
        'actor_start': a,
        'actor_end': a,
        'target_start': b,
        'target_end': b
      }

    transitions.append(transition)


# Define the base YAML structure
data = {
    "items": items + new_items,
    "transitions": transitions
}

# Generate and save YAML content
with open("output.yaml", "w") as file:
  yaml.dump(data, file, sort_keys=False, indent=2)

print("YAML content generated and saved to output.yaml")


# %%
# try out rules
all_shapes = ['circle', 'square', 'triangle', 'diamond']
all_textures = ['plain', 'dots', 'stripes', 'checkered']

all_objs = []
for i in range(len(all_shapes)):
  for j in range(len(all_textures)):
    all_objs.append(str(i)+str(j))

all_pairs = []
for a in all_objs:
  for b in all_objs:
    all_pairs.append(a + '|' + b)


matrix = np.array(all_pairs).reshape(16, 16)

plains_collection = [obj for obj in matrix.flatten() if obj[1] == '0' and obj[4] == '0']

diffs_collection = [obj for obj in matrix.flatten() if obj[0] in ('1', '2') and obj[1] in ('1', '2') and obj[3] in ('0', '3') and obj[4] in ('0', '3') and obj[0] != obj[3] and obj[1] != obj[4] ]

hard_collection = []

for a in all_objs:

  if a[0] == a[1]:
    b = a[0] + a[1]

  elif int(a[0]) + int(a[1]) == 3:
    b = a[1] + a[0]

  elif int(a[0]) < int(a[1]):
    b = a[0] + str(3 - int(a[1]))

  else:
    b = str(3 - int(a[0])) + a[1]

  hard_collection.append(a + '|' + b)

hard_collection
