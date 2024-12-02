# %%
import yaml

# %% try out rules
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
    b = str(3 - int(a[0])) + a[1]

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
     'target_start': b,
     'target_end': r,
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

# draw_item = True

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

    # if draw_item:
    #   draw_object(obj_shape, pattern=obj_texture, level=level, prefix=file_prefix)

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
