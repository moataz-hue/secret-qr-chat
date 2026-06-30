import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_123'
socketio = SocketIO(app, cors_allowed_origins="*", max_content_length=50 * 1024 * 1024)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('system_message', {'msg': 'تم الاتصال بالطرف الآخر بنجاح', 'status': 'connected'}, to=room, include_self=False)

@socketio.on('send_message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    msg_type = data.get('type', 'text')
    emit('receive_message', {'msg': msg, 'sender': request.sid, 'type': msg_type}, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
