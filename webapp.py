#adapted from https://github.com/miguelgrinberg/Flask-SocketIO/tree/master/example

from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)
thread = None
thread_lock = Lock()


def background_thread():
    count = 0
    while True:
        socketio.sleep(10) #wait 10 seconds
        count += 1 #add 1 to count
        socketio.emit('my_response', count) #send count to all clients

@app.route('/')
def index():
    return render_template('home.html', async_mode=socketio.async_mode)


@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock: #lock thread in case multiple clients are connecting at the same time
        #create one thread for all clients
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('start', 'Connected')
    #to use emit: emit(event, data)

if __name__ == '__main__':
    socketio.run(app, debug=True)