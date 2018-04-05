#adapted from https://github.com/miguelgrinberg/Flask-SocketIO/tree/master/example

from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
thread = None
thread_lock = Lock() #we'll use this lock to prevent multiple clients from modifying thread at the same times

@socketio.on('connect') #run this when the connection starts
def test_connection():
    global thread
    with thread_lock: #lock thread in case multiple clients are connecting at the same time
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('start', 'Connected')

def background_thread():
    #this funtion does the counting
    count = 0
    while True:
        socketio.sleep(2) #wait 5 seconds
        count = count + 1 #add 1 to count
        print(count)
        socketio.emit('my_response', count) #send count to all clients


@app.route('/')
def index():
    return render_template('home.html', async_mode=socketio.async_mode)

if __name__ == '__main__':
    socketio.run(app, debug=True)
