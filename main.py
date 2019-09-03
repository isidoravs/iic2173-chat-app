from flask import Flask, render_template
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
  return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
  print('SUCCESS! Message received')

@socketio.on('chat_event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
  print('received event: ' + str(json))
  socketio.emit('chat_response', json, callback=messageReceived)

if __name__ == '__main__':
  socketio.run(app, debug=True)