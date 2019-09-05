from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime
from requests import get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
  return render_template('session.html',
                         get=get)

def messageReceived(methods=['GET', 'POST']):
  print('SUCCESS! Message received')

@socketio.on('chat_event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
  if 'message' in json and json['message'] == 'chucknorris':
    chuck_norris_joke = get('https://api.chucknorris.io/jokes/random').json()['value']
    json['message'] = chuck_norris_joke
  print('received event: ' + str(json))
  socketio.emit('chat_response', json, callback=messageReceived)

if __name__ == '__main__':
  socketio.run(app, debug=True)
