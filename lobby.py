import datetime
from battleship import *

class Lobby:
  def __init__(self, lobby_name, mode, size, ship_types):
    self.lobby_name = lobby_name
    self.mode = mode
    self.size = size
    self.ship_types = ship_types
    self.created_at = datetime.datetime.now()
    self.players = []
    self.started = False
    self.game = Game.random(size, ship_types)
    self._ready = dict()
    self.sids = [None, None]
  def add_player(self, user):
    self.players.append(user)
    self._ready[user] = False
  def to_json(self, user):
    return {
      'lobby_name': self.lobby_name,
      'mode': self.mode,
      'size': self.size,
      'ship_types': self.ship_types,
      'created_at': self.created_at.isoformat(),
      'players': self.players,
      'started': self.started,
      'board': self.game.boards[self.player(user)].to_json(),
      'shot_board': {
        'size': self.size,
        'shots': [
          [cell if cell != 1 else 0 for cell in row]
          for row in self.game.boards[1 - self.player(user)].board.tolist()
        ],
      },
      'ready': self._ready,
      'turn': self.game.current_player == self.player(user),
      'winner': self.game.winner,
      'is_won': self.game.is_won,
    }
  def player(self, user):
    return self.players.index(user)
  def ready(self, user):
    self._ready[user] = True
    if len(self.players) != 2: return
    if self._ready.get(self.players[0]) and self._ready.get(self.players[1]):
      self.started = True