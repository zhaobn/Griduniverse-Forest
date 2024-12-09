# %%
import yaml

# %% Setup - double-check with draw_obj.py

all_shapes = ['circle', 'square', 'triangle', 'diamond']
all_textures = ['plain', 'dots', 'stripes', 'checkered']
max_level = 6
file_prefix = '../dlgr/griduniverse/static/images/objs/'


all_objs = []
for s in all_shapes:
  for t in all_textures:
    all_objs.append(f'{s}_{t}')

# %% Rules to functions

def get_shape(obj):
  return obj.split('_')[0]

def get_texture(obj):
  return obj.split('_')[1]

def get_level(obj):
  return int(obj.split('_')[2])

def compose_obj(shape, color, level):
  return f'{shape}_{color}_{level}'




def is_same_shape (obj_arr):
  return (
    get_shape(obj_arr[0]) == get_shape(obj_arr[1]) and
    get_shape(obj_arr[0]) != 'circle'
  )

def is_diff (obj_arr):
  return (
    get_shape(obj_arr[0]) != get_shape(obj_arr[1]) and get_texture(obj_arr[0]) != get_texture(obj_arr[1]) and
    get_shape(obj_arr[0]) == 'circle'
  )

def is_impossible (obj_arr):
  obj_a_shape_index = all_shapes.index(get_shape(obj_arr[0]))
  obj_a_texture_index = all_textures.index(get_texture(obj_arr[0]))
  obj_b_shape_index = all_shapes.index(get_shape(obj_arr[1]))
  obj_b_texture_index = all_textures.index(get_texture(obj_arr[1]))

  if obj_a_shape_index != obj_a_texture_index:

    if obj_a_shape_index + obj_b_shape_index == 3 and obj_a_texture_index + obj_b_texture_index == 3:
      return True

    if obj_b_shape_index == obj_a_texture_index and obj_b_texture_index == obj_a_shape_index:
      return True


  if obj_a_shape_index == obj_a_texture_index or obj_a_shape_index + obj_a_texture_index == 3:

    if obj_b_shape_index == obj_a_shape_index and obj_b_texture_index + obj_a_texture_index == 3:
      return True

    if obj_b_texture_index == obj_a_texture_index and obj_b_shape_index + obj_a_shape_index == 3:
      return True

  return False

# Debug
# all_pairs = []
# for o1 in all_objs:
#   for o2 in all_objs:
#     if o1 != o2:
#       all_pairs.append(f'{o1}|{o2}')

# filtered_list = [pair for pair in all_pairs if is_impossible(pair.split('|'))]
# len(filtered_list)

#%%

def get_new_obj(obj_a, obj_b):
  new_level = max(get_level(obj_a), get_level(obj_b)) + 1
  return get_shape(obj_a) + '_' + get_texture(obj_b) + '_' + str(new_level)


def obj_to_item(obj_name, default_count=0):

  # point_step = level_int // 3
  # points = 4**point_step * 5**(level_int-point_step)

  points = 10**(get_level(obj_name))

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
     'target_start': b,
     'target_end': r,
    }
  return transition


def flatten_dict(dict):
  return [el for sublist in dict.values() for el in sublist]


# %%

env_objs = {} # obj name, shape_texture_level
env_items = {} # yaml entry
env_recipes = {} # yaml entry

for level in range(max_level):

  level_name =  f'level_{level}'
  item_default_count = 0

  next_level = level + 1
  next_level_name =  f'level_{next_level}'

  # Base level
  if level == 0:
    env_objs[level_name] = [f'{x}_0' for x in all_objs]
    env_items[level_name] = []
    item_default_count = 1

  # Prep items
  for obj in env_objs[level_name]:

    item = obj_to_item(obj, item_default_count)
    env_items[level_name].append(item)

  # Transit to next level
  env_recipes[level_name] = []

  if level < max_level:
    env_objs[next_level_name] = []
    env_items[next_level_name] = []

  new_obj_names = list(set([x['name'] for x in env_items[level_name]]))
  current_obj_names = list(set([x['name'] for x in flatten_dict(env_items)]))


  for a_name in new_obj_names:
    for b_name in current_obj_names:

      if level == max_level:

        transition = fmt_transition(a_name, b_name, '')
        transition_dir = fmt_transition(b_name, a_name, '')
        env_recipes[level_name].append(transition)

      elif level < max_level - 1 and is_diff([a_name, b_name]):

        r_name = get_new_obj(a_name, b_name)
        env_objs[next_level_name].append(r_name)

        transition = fmt_transition(a_name, b_name, r_name)
        env_recipes[level_name].append(transition)

      elif level < max_level - 1 and is_impossible([b_name, a_name]):

        r_name = get_new_obj(b_name, a_name)
        env_objs[next_level_name].append(r_name)

        transition = fmt_transition(a_name, b_name, r_name)
        env_recipes[level_name].append(transition)

      else:
        transition = fmt_transition(a_name, b_name, '')
        transition_dir = fmt_transition(b_name, a_name, '')

        env_recipes[level_name].append(transition)
        env_recipes[level_name].append(transition_dir)

  env_objs[next_level_name] = list(set(env_objs[next_level_name]))
  env_recipes[level_name] = [dict(t) for t in {tuple(d.items()) for d in env_recipes[level_name]}]



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
