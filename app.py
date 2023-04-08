from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-key'

socketio = SocketIO(app)

rooms = {}

def generate_code(length):
    """ 
    Generate a random code consisting of uppercase ASCII characters of a specified length,
    and return the code. The code is guaranteed to not already exist in the `rooms` list.
    """
    while True:
        code = ''.join(random.choice(ascii_uppercase) for _ in range(length))
        if code not in rooms:
            break
    return code

# Define the home page view for the chat application.
@app.route('/', methods=('GET', 'POST'))
def home_view():
    # Clear the session to start fresh.
    session.clear()

    # If the form is submitted.
    if request.method == 'POST':
        # Get the name and code from the form.
        name = request.form.get('name')
        code = request.form.get('code')

        # Check if the user wants to join or create a room.
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        # Validate the form inputs.
        if not name:
            # If the name is missing, show an error message.
            return render_template('home.html', error_message='Please enter a name.', name=name, code=code)
        elif join != False and not code:
            # If the user wants to join a room but the code is missing, show an error message.
            return render_template('home.html', error_message='Please enter a room code.', name=name, code=code)

        # Set the default room to be the code entered by the user.
        room = code

        # If the user wants to create a room.
        if create != False:
            # Generate a random 6-digit code for the new room.
            room = generate_code(6)
            # Add the new room to the dictionary of rooms.
            rooms[room] = {'members': 0, 'messages': []}
        # If the user wants to join a room but the code is not valid.
        elif code not in rooms:
            # Show an error message.
            return render_template('home.html', error_message='Room does not exist.', name=name, code=code)

        # Store the room code and user name in the session.
        session['room'] = room
        session['name'] = name

        # Redirect the user to the room page.
        return redirect(url_for('room_view'))

    # If the form is not submitted, show the home page.
    return render_template('home.html')
# Define the room page view for the chat application.
@app.route('/room')
def room_view():
    """ 
    defines the view for the chat room page
    It retrieves the room from the session and ensures the user is logged in and the room exists
    If the user is not logged in or the room does not exist, it redirects to the home page
    Otherwise, it renders the room template with the room name and messages for that room.
    """
    # Get the room  from the session 
    room = session.get('room')
    
    if room is None or session.get('name') is None or room not in rooms:
        return redirect(url_for('home_view'))

    return render_template('room.html', room=room, messages=rooms[room]['messages'], members=rooms[room]['members'])

@socketio.on('message')
def handle_message(data):
    # Get the current room and user name from the session
    room = session.get('room')
    name = session.get('name')
    # If the room does not exist return
    if room not in rooms:
        return 
    # Construct the message content
    content = {'name': name, 'message': data['data']}
    # Send the message to all clients in the room
    send(content, to=room)
    # Add the content to the room's message history 
    rooms[room]['messages'].append(content)
    

@socketio.on('connect')
def handle_connect(auth):
    # Get the current room and user name from the session
    room = session.get('room')
    name = session.get('name')

    if not name or not room:
        return 
    elif room not in rooms:
        leave_room(room)
        return 
    # Join the room if does exist
    join_room(room)
    # Send a message to the room indicating that the user has entered
    send({'name': name, 'message': 'has entered the room'}, to=room)
    # Add a member
    rooms[room]['members'] += 1
    
# This function should be called when a client disconnects from the server
@socketio.on('disconnect')
def handle_disconnect():
    # Sessions can be used to store and retrieve data for a specific client.
    # Get the current room and user name from the session
    room = session.get('room')
    name = session.get('name')
    # Check if the room is in the dictionary of active rooms
    if room in rooms:

        # Reduce the member count for the room
        rooms[room]['members'] -= 1
        # If the room has no more members, remove it from the active rooms dictionary
        if rooms[room]['members'] == 0:
            del rooms[room]
    # Send a message to the room indicating that the user has left
    send({'name': name, 'message': 'has left the room'}, to=room)
    

if __name__ == '__main__':
    socketio.run(app, host='localhost',port=8080,debug=True)


