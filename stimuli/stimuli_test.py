# %% Setup - double-check with draw_obj.py

all_shapes = ['circle', 'square', 'triangle', 'diamond']
all_textures = ['plain', 'dots', 'stripes', 'checkered']

all_objs = []
for s in all_shapes:
  for t in all_textures:
    all_objs.append(f'{s}_{t}')


all_pairs = []
for o1 in all_objs:
  for o2 in all_objs:
    if o1 != o2:
      all_pairs.append(f'{o1}|{o2}')

len(all_pairs)

def get_shape(obj):
  return obj.split('_')[0]

def get_texture(obj):
  return obj.split('_')[1]

def get_level(obj):
  return int(obj.split('_')[2])

def compose_obj(shape, color, level):
  return f'{shape}_{color}_{level}'


# %%
def plain_diff_shapes (obj_arr):
  return (
    get_shape(obj_arr[0]) != get_shape(obj_arr[1]) and
    get_texture(obj_arr[0]) == 'plain'
  )
filtered_list = [pair for pair in all_pairs if plain_diff_shapes(pair.split('|'))]
len(filtered_list) # 48


# %%
def is_same_shape (obj_arr):
  return (
    get_shape(obj_arr[0]) == get_shape(obj_arr[1])
  )
filtered_list = [pair for pair in all_pairs if is_same_shape(pair.split('|'))]
len(filtered_list) # 48


# %%
def complex_rule (obj_arr):
  return (
    get_shape(obj_arr[0]) in ('circle', 'square') and
    get_texture(obj_arr[1]) in ('plain', 'dots') and
    get_shape(obj_arr[1]) != 'circle'
  )
filtered_list = [pair for pair in all_pairs if complex_rule(pair.split('|'))]
len(filtered_list) # 46

# %%
