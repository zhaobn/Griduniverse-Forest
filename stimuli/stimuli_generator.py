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

# # Example usage:
# draw_object('circle', pattern='plain', level=2, prefix='../dlgr/griduniverse/static/images/objs/')
# draw_object('square', pattern='dots', level=3, save=False)
# draw_object('circle', pattern='stripes', level=8, save=False)
# draw_object('diamond', pattern='checkered', save=False)


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


plains_collection = [obj for obj in all_pairs if obj[1] == '0' and obj[4] == '0']

diffs_collection = [obj for obj in all_pairs if obj[0] in ('1', '2') and obj[1] in ('1', '2') and obj[3] in ('0', '3') and obj[4] in ('0', '3') and obj[0] != obj[3] and obj[1] != obj[4] ]


hard_collection = []

for a in all_objs:

  if a[0] == a[1]:
    b = a[0] + a[1]

  elif int(a[0]) + int(a[1]) == 2:
    b = a[1] + a[0]

  elif int(a[0]) < int(a[1]):
    b = a[0] + str(3 - int(a[1]))

  else:
    b = str(2 - int(a[0])) + a[1]

  hard_collection.append(a + '|' + b)

hard_collection

# %% Rules to functions
def is_both_plain (obj_a, obj_b, use_name=False):

 if use_name:
   return obj_a.split('_')[1] == 'plain' and obj_b.split('_')[1] == 'plain'

 else:
  return all_textures[int(obj_a[1])] == 'plain' and all_textures[int(obj_b[1])] == 'plain'




def is_diff_in_range (obj_a, obj_b):
  return obj_a[0] in ('1', '2') and obj_a[1] in ('1', '2') and obj_b[0] in ('0', '3') and obj_b[1] in ('0', '3') and obj_a[0] != obj_b[0] and obj_a[1] != obj_b[1]




def is_hard(obj_a, obj_b):

  if obj_a[0] == obj_a[1] and obj_a == obj_b:
    return True

  if int(obj_a[0]) + int(obj_a[1]) == 2 and obj_b[0] == obj_a[1] and obj_b[1] == obj_a[0]:
    return True

  if int(obj_a[0]) < int(obj_a[1]) and obj_b[0] == obj_a[0] and int(obj_b[1]) + int(obj_a[1]) == 3:
    return True

  if int(obj_b[0]) + int(obj_a[0]) == 2 and obj_b[1] == obj_a[1]:
    return True

  return False




def get_new_obj(obj_a, obj_b):
  return obj_a[0] + obj_b[1]

def get_new_obj_from_name(obj_a_name, obj_b_name):
  level = max(int(obj_a_name.split('_')[2]), int(obj_b_name.split('_')[2])) + 1
  return '_'.join([obj_a_name.split('_')[0], obj_b_name.split('_')[1], str(int(level))])

def obj_to_name(obj, level_int):
  obj_shape = all_shapes[int(obj[0])]
  obj_texture = all_textures[int(obj[1])]
  return f"{obj_shape}_{obj_texture}_{level_int}"

def obj_to_item(obj, level_int, default_count=0):

  obj_name = obj if '_' in obj else obj_to_name(obj, level_int)

  point_step = level_int // 3
  points = 4**point_step * 5**(level_int-point_step)

  item = {
      "sprite": "image:objs/" + obj_name + '.svg',
      "name": obj_name,
      "item_id": obj_name,
      "calories": points,
      "item_count": default_count
    }
  return item


def fmt_transition(a, b, r):
  if r == '':
    transition = {
     'actor_start': a,
     'actor_end': a,
     'target_start': b,
     'target_end': b
    }
  else:
   transition = {
     'actor_start': a,
     'actor_end': a,
     'target_start': b,
     'target_end': r,
     'modify_uses': ''
    }
  return transition


def flatten_dict(dict):
  return [el for sublist in dict.values() for el in sublist]

def name_to_code(obj_name):
  shape_code = all_shapes.index(obj_name.split('_')[0])
  texture_code = all_textures.index(obj_name.split('_')[1])
  return str(shape_code) + str(texture_code)


# %%
# get pilot recipe
max_level = 6
file_prefix = '../dlgr/griduniverse/static/images/objs/'

env_objs = {}
env_items = {}
env_recipes = {}

draw_item = True

for level in range(max_level):

  level_name =  f'level_{level}'
  item_default_count = 0

  next_level = level + 1
  next_level_name =  f'level_{next_level}'

  # Base level
  if level == 0:
    env_objs[level_name] = all_objs.copy()
    env_items[level_name] = []
    item_default_count = 1

  # Prep items
  for obj in env_objs[level_name]:

    obj_shape = all_shapes[int(obj[0])]
    obj_texture = all_textures[int(obj[1])]

    if draw_item:
      draw_object(obj_shape, pattern=obj_texture, level=level, prefix=file_prefix)

    item = obj_to_item(obj, level, item_default_count)
    env_items[level_name].append(item)


  # Transit to next level
  env_recipes[level_name] = []

  env_objs[next_level_name] = []
  env_items[next_level_name] = []

  new_obj_names = [x['name'] for x in env_items[level_name]]
  current_obj_names = [x['name'] for x in flatten_dict(env_items)]

  for a_name in new_obj_names:
    for b_name in current_obj_names:

      if is_both_plain(a_name, b_name, use_name=True):

        r_name = get_new_obj_from_name(a_name, b_name)
        r = name_to_code(r_name)
        env_objs[next_level_name].append(r)

        transition = fmt_transition(a_name, b_name, r_name)
        transition = fmt_transition(b_name, a_name, r_name)

      else:
        transition = fmt_transition(a_name, b_name, '')
        transition = fmt_transition(b_name, a_name, '')

      env_recipes[level_name].append(transition)

  env_objs[next_level_name] = list(set(env_objs[next_level_name]))




# Define the base YAML structure


data = {
    "items": flatten_dict(env_items),
    "transitions": flatten_dict(env_recipes)
}

# Generate and save YAML content
with open("output.yaml", "w") as file:
  yaml.dump(data, file, sort_keys=False, indent=2)

print("YAML content generated and saved to output.yaml")

# %%
