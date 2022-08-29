import numpy as np
from string import ascii_lowercase, ascii_uppercase
import re


def random_string(length):
  return ''.join(np.random.choice(list(ascii_lowercase + ascii_uppercase), length))


def parse_form(form):
  lobby_name = form.get('lobbyname')
  mode = form.get('mode')
  x = form.get('x')
  y = form.get('y')
  ships_1x2 = form.get('1x2')
  ships_1x3 = form.get('1x3')
  ships_1x4 = form.get('1x4')
  ships_1x5 = form.get('1x5')
  ships_lightning = form.get('lightning')
  ships_small_l = form.get('small_l')
  ships_large_l = form.get('large_l')
  ships_long_l = form.get('long_l')
  ships_small_t = form.get('small_t')
  ships_large_t = form.get('large_t')
  if not re.match(r'^[a-zA-Z]*$', lobby_name) or mode not in ['0', '1', '2']:
    return None
  if not re.match(r'^[0-9]*$', x) or not re.match(r'^[0-9]*$', y):
    return None
  if ships_1x2 not in list(map(str, range(6))):
    return None
  if ships_1x3 not in list(map(str, range(6))):
    return None
  if ships_1x4 not in list(map(str, range(6))):
    return None
  if ships_1x5 not in list(map(str, range(6))):
    return None
  if ships_lightning not in list(map(str, range(6))):
    return None
  if ships_small_l not in list(map(str, range(6))):
    return None
  if ships_large_l not in list(map(str, range(6))):
    return None
  if ships_long_l not in list(map(str, range(6))):
    return None
  if ships_small_t not in list(map(str, range(6))):
    return None
  if ships_large_t not in list(map(str, range(6))):
    return None
  return {
    'lobby_name': lobby_name,
    'mode': int(mode),
    'size': (int(x), int(y)),
    'ship_types': [
      '1x2' for i in range(int(ships_1x2))
    ] + [
      '1x3' for i in range(int(ships_1x3))
    ] + [
      '1x4' for i in range(int(ships_1x4))
    ] + [
      '1x5' for i in range(int(ships_1x5))
    ] + [
      'lightning' for i in range(int(ships_lightning))
    ] + [
      'small_l' for i in range(int(ships_small_l))
    ] + [
      'large_l' for i in range(int(ships_large_l))
    ] + [
      'long_l' for i in range(int(ships_long_l))
    ] + [
      'small_t' for i in range(int(ships_small_t))
    ] + [
      'large_t' for i in range(int(ships_large_t))
    ]
  }