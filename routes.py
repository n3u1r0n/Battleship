from flask import render_template, request, redirect, url_for, flash, abort, g, session, jsonify, json
from flask_socketio import emit, disconnect, join_room, leave_room, rooms
from server import app, socketio
from battleship import *
from helpers import *
from lobby import *

@app.before_first_request
def init_lobbies():
  global lobbies
  lobbies = dict()

@app.before_request
def init_user():
  if 'user' not in session:
    session['user'] = random_string(64)
  g.user = session['user']
  for lobby_name in list(lobbies.keys()):
    if lobbies.get(lobby_name).created_at < datetime.datetime.now() - datetime.timedelta(minutes=60):
      del lobbies[lobby_name]
    elif lobbies.get(lobby_name).game.winner is not None:
      del lobbies[lobby_name]

@app.route('/', methods=['GET', 'POST'])
def root_route():
  if request.method == 'POST':
    if not (lobby_raw := parse_form(request.form)):
      flash('Invalid form')
      return redirect(url_for('root_route'))
    if lobbies.get(lobby_name := lobby_raw['lobby_name']):
      flash('Lobby name already taken')
      return redirect(url_for('root_route'))
    lobbies[lobby_name] = Lobby(**lobby_raw)
    return redirect(url_for('lobby_setup_route', lobby_name=lobby_raw['lobby_name']))
  return render_template('main.html',
    lobby_name = random_string(5),
    ships = enumerate(map(lambda ship_name: [ship_name, 'ships/mini-' + ship_name + '.png'], ships_dict.keys()))
  )

@app.route('/lobby/<lobby_name>', methods=['GET'])
def lobby_setup_route(lobby_name):
  if not (lobby := lobbies.get(lobby_name)):
    flash('Lobby not found')
    return redirect(url_for('root_route'))
  if len(lobby.players) == 2 and g.user not in lobby.players:
    flash('Lobby full')
    return redirect(url_for('root_route'))
  if len(lobby.players) != 2 and g.user not in lobby.players:
    lobby.add_player(g.user)
  return render_template('lobby.html',
    lobby = lobby.to_json(g.user),
  )

@app.route('/ships_updated/<lobby_name>', methods=['POST'])
def ships_updated_route(lobby_name):
  if not (lobby := lobbies.get(lobby_name)) or g.user not in lobby.players or lobby._ready.get(g.user) == True:
    return abort(403)
  ships = [Ship.from_json(ship) for ship in json.loads(request.form.get('ships'))]
  if Board.check(lobby.size, ships, lobby.mode):
    lobby.game.boards[lobby.player(g.user)] = Board(lobby.size, ships)
  return jsonify(lobby.to_json(g.user))


@socketio.on('start')
def start(data):
  g.user = session['user']
  lobby_name = data.get('lobby_name')
  if not (lobby := lobbies.get(lobby_name)) or g.user not in lobby.players:
    return
  lobby.ready(g.user)
  if lobby.started:
    emit('start', {'lobby': lobby.to_json(lobby.players[0])}, room=lobby.sids[0])
    emit('start', {'lobby': lobby.to_json(lobby.players[1])}, room=lobby.sids[1])


@socketio.on('fire')
def fire(data):
  g.user = session['user']
  lobby_name = data.get('lobby_name')
  if not (lobby := lobbies.get(lobby_name)) or g.user not in lobby.players:
    return
  if lobby.game.current_player != lobby.player(g.user) or lobby.game.winner != None or not lobby.started:
    return
  x, y = data.get('x'), data.get('y')
  if x < 0 or x >= lobby.size[0] or y < 0 or y >= lobby.size[1]:
    return
  result = lobby.game.fire(x, y)
  emit('update', {'lobby': lobby.to_json(lobby.players[0]), 'result': result}, room=lobby.sids[0])
  emit('update', {'lobby': lobby.to_json(lobby.players[1]), 'result': result}, room=lobby.sids[1])
  emit('aim', {'i': None, 'j': None}, room=lobby.sids[0])
  emit('aim', {'i': None, 'j': None}, room=lobby.sids[1])

@socketio.on('join')
def connect(data):
  g.user = session['user']
  lobby_name = data.get('lobby_name')
  if not (lobby := lobbies.get(lobby_name)) or g.user not in lobby.players:
    return
  lobby.sids[lobby.player(g.user)] = request.sid

@socketio.on('aim')
def aim(data):
  g.user = session['user']
  lobby_name = data.get('lobby_name')
  if not (lobby := lobbies.get(lobby_name)) or g.user not in lobby.players:
    return
  if lobby.game.current_player != lobby.player(g.user) or lobby.game.winner != None or not lobby.started:
    return
  i, j = data.get('i'), data.get('j')
  if i < 0 or i >= lobby.size[0] or j < 0 or j >= lobby.size[1]:
    return
  emit('aim', {'i': i, 'j': j}, room=lobby.sids[0])
  emit('aim', {'i': i, 'j': j}, room=lobby.sids[1])