import numpy as np


class Ship:
  def __init__(self, shape, name):
    self.shape = np.array(shape, dtype=int)
    self.name = name
    self.x = None
    self.y = None
    self.size = np.sum(self.shape != 0)
    self.side_neighbors = np.zeros((self.shape.shape[0] + 2, self.shape.shape[1] + 2), dtype=int)
    self.side_neighbors[:-2,1:-1] |= self.shape
    self.side_neighbors[1:-1,:-2] |= self.shape
    self.side_neighbors[1:-1,1:-1] |= self.shape
    self.side_neighbors[1:-1,2:] |= self.shape
    self.side_neighbors[2:,1:-1] |= self.shape
    self.neighbors = np.zeros((self.shape.shape[0] + 2, self.shape.shape[1] + 2), dtype=int)
    self.neighbors[:-2,:-2] |= self.shape
    self.neighbors[:-2,1:-1] |= self.shape
    self.neighbors[:-2,2:] |= self.shape
    self.neighbors[1:-1,:-2] |= self.shape
    self.neighbors[1:-1,1:-1] |= self.shape
    self.neighbors[1:-1,2:] |= self.shape
    self.neighbors[2:,:-2] |= self.shape
    self.neighbors[2:,1:-1] |= self.shape
    self.neighbors[2:,2:] |= self.shape
  def copy(self):
    ship = Ship(np.copy(self.shape), self.name)
    ship.x = self.x
    ship.y = self.y
    return ship
  def rotate(self):
    self.shape = np.rot90(self.shape)
    self.side_neighbors = np.rot90(self.side_neighbors)
    self.neighbors = np.rot90(self.neighbors)
    return self
  def flip_vertical(self):
    self.shape = np.flipud(self.shape)
    self.side_neighbors = np.flipud(self.side_neighbors)
    self.neighbors = np.flipud(self.neighbors)
    return self
  def flip_horizontal(self):
    self.shape = np.fliplr(self.shape)
    self.side_neighbors = np.fliplr(self.side_neighbors)
    self.neighbors = np.fliplr(self.neighbors)
    return self
  def transform(self, string):
    for action in string:
      if action == 'V':
        self.flip_vertical()
      elif action == 'H':
        self.flip_horizontal()
      elif action == 'R':
        self.rotate()
    return self
  def __str__(self):
    return '\n'.join([' '.join(['O' if self.shape[i,j] == 1 else 'X' if self.shape[i,j] == 2 else '.' for j in range(self.shape.shape[1])]) for i in range(self.shape.shape[0])])
  __repr__ = __str__
  @property
  def sunk(self):
    return np.sum(self.shape == 1) == 0
  def fire(self, size, x, y):
    if 0 <= (x := x - self.x) < self.shape.shape[0] and 0 <= (y := y - self.y) < self.shape.shape[1]:
      if self.shape[x,y] == 1:
        self.shape[x,y] = 2
        if self.sunk:
          self.shape[self.shape == 2] = 4
          return 2
        return 1
      self.shape[x,y] = 3
    return 0
  def onboard(self, size):
    if self.x + self.shape.shape[0] > size[0] or self.y + self.shape.shape[1] > size[1] or self.x < 0 or self.y < 0:
      return False
    shape = np.zeros(size, dtype=int)
    shape[self.x:self.x + self.shape.shape[0], self.y:self.y + self.shape.shape[1]] += self.shape
    side_neighbors = np.zeros((size[0] + 2, size[1] + 2), dtype=int)
    side_neighbors[self.x:self.x + self.side_neighbors.shape[0], self.y:self.y + self.side_neighbors.shape[1]] += self.side_neighbors
    side_neighbors[side_neighbors > 1] = 1
    neighbors = np.zeros((size[0] + 2, size[1] + 2), dtype=int)
    neighbors[self.x:self.x + self.neighbors.shape[0], self.y:self.y + self.neighbors.shape[1]] += self.neighbors
    neighbors[neighbors > 1] = 1
    return shape, side_neighbors[1:-1,1:-1], neighbors[1:-1,1:-1]
  def position(self, x, y):
    self.x = x
    self.y = y
    return self
  def to_json(self):
    return {
      'name': self.name,
      'x': self.x,
      'y': self.y,
      'shape': self.shape.tolist()
    }
  @staticmethod
  def from_json(json):
    ship = Ship(np.array(json['shape']), json['name'])
    ship.position(json['x'], json['y'])
    return ship

ship_1x2 = Ship((
  (1,1),
), '1x2')
ship_1x3 = Ship((
  (1,1,1),
), '1x3')
ship_1x4 = Ship((
  (1,1,1,1),
), '1x4')
ship_1x5 = Ship((
  (1,1,1,1,1),
), '1x5')
ship_lightning = Ship((
  (1,1,0),
  (0,1,1),
), 'lightning')
ship_small_l = Ship((
  (1,0),
  (1,1),
), 'small_l')
ship_large_l = Ship((
  (1,0,0),
  (1,0,0),
  (1,1,1),
), 'large_l')
ship_long_l = Ship((
  (1,0,0,0),
  (1,1,1,1),
), 'long_l')
ship_small_t = Ship((
  (1,1,1),
  (0,1,0),
), 'small_t')
ship_large_t = Ship((
  (1,1,1),
  (0,1,0),
  (0,1,0),
), 'large_t')


ships_dict = {
  '1x2': ship_1x2,
  '1x3': ship_1x3,
  '1x4': ship_1x4,
  '1x5': ship_1x5,
  'lightning': ship_lightning,
  'small_l': ship_small_l,
  'large_l': ship_large_l,
  'long_l': ship_long_l,
  'small_t': ship_small_t,
  'large_t': ship_large_t,
}


class Board:
  def __init__(self, size, ships):
    self.size = size
    self.ships = ships
    self.board = np.zeros(size, dtype=int)
    for ship in ships:
      self.board += ship.onboard(size)[0]
  def __str__(self):
    return '\n'.join([' '.join(['O' if self.board[i,j] == 1 else 'X' if self.board[i,j] == 2 else 'x' if self.board[i,j] == 3 else '.' for j in range(self.size[1])]) for i in range(self.size[0])])
  __repr__ = __str__
  def fire(self, x, y):
    if self.board[x,y] == 2 or self.board[x,y] == 3 or self.board[x,y] == 4:
      return None
    if self.board[x,y] == 1:
      self.board[x,y] = 2
      for ship in self.ships:
        if (result := ship.fire(self.size, x, y)) != 0:
          if result == 2:
            self.board[ship.onboard(self.size)[0] == 4] = 4
          return result
    self.board[x,y] = 3
    return 0
  @staticmethod
  def check(size, ships, mode=2):
    # modes:
    # 0: allow touching ships
    # 1: allow corner touching ships
    # 2: don't allow any touching ships
    for i in range(len(ships)):
      if (onboard := ships[i].onboard(size)) == False:
        return False
      for j in range(i):
        shape, _, _ = ships[j].onboard(size)
        if np.any(shape & onboard[mode]):
          return False
    return True
  def is_empty(self):
    return all(map(lambda ship: ship.sunk, self.ships))
  @staticmethod
  def random(size, ship_types, mode=2):
    while True:
      ships = []
      for type in ship_types:
        ships.append(
          ships_dict[type].copy()\
            .transform(np.random.choice(['', 'R', 'RR', 'RRR', 'V', 'VR', 'VRR', 'VRRR']))\
            .position(np.random.randint(size[0]), np.random.randint(size[1]))
        )
      if Board.check(size, ships, mode):
        return Board(size, ships)
  def to_json(self):
    return {
      'size': self.size,
      'ships': [ship.to_json() for ship in self.ships],
      'board': self.board.tolist()
    }
  @staticmethod
  def from_json(json):
    board = Board(json['size'], [Ship.from_json(ship) for ship in json['ships']])
    board.board = np.array(json['board'])
    return board

class Game:
  def __init__(self, size, ships):
    self.size = size
    self.boards = [Board(size, ships[0]), Board(size, ships[1])]
    self.current_player = 0
  def fire(self, x, y):
    if (result := self.boards[1 - self.current_player].fire(x, y)) != 0:
      return result
    self.current_player = 1 - self.current_player
    return 0
  @property
  def is_won(self):
    return self.boards[0].is_empty() or self.boards[1].is_empty()
  @property
  def winner(self):
    if self.boards[0].is_empty():
      return 1
    if self.boards[1].is_empty():
      return 0
    return None
  @staticmethod
  def random(size, ship_types, mode=2):
    return Game(size, [Board.random(size, ship_types, mode).ships, Board.random(size, ship_types, mode).ships])
  def __str__(self):
    return '\n'.join([
      'Player 1:',
      str(self.boards[0]),
      'Player 2:',
      str(self.boards[1]),
    ])
  __repr__ = __str__
  def to_json(self):
    return {
      'size': self.size,
      'boards': [board.to_json() for board in self.boards],
      'current_player': self.current_player
    }
  @staticmethod
  def from_json(json):
    game = Game(json['size'], [Board.from_json(board) for board in json['boards']])
    game.current_player = json['current_player']
    return game