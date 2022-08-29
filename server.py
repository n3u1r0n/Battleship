from flask import Flask
from flask_socketio import SocketIO

app = Flask('Battleship')
app.secret_key = 'Battleship'
socketio = SocketIO(app)

from routes import *