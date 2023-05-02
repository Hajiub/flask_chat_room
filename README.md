# Python Chat Room Project with Flask Framework and SocketIO
This Python chat room project is built with the Flask web framework and SocketIO library for real-time communication. The front-end is implemented with JavaScript.

# Project Overview
The goal of this project is to create a chat room web application where users can chat with each other in real-time. Users can join different chat rooms and send messages to other users in the same room. The chat room interface is implemented with HTML, CSS, and JavaScript using the SocketIO library for real-time communication with the server.

The project is built with the Flask web framework, which provides a lightweight and flexible environment for building web applications in Python. The SocketIO library is used to enable real-time communication between the client and server, allowing messages to be sent and received in real-time without the need for constant polling.

# Project Features
##### . Chat room creation  
##### . Real-time messaging between users in the same chat room
##### .Chat room history and message persistence
# Technologies Used
##### . Python 3.x

##### . Flask web framework

##### . Flask_SocketIO library

##### . JavaScript

##### . HTML

##### . CSS

# Project Setup
To run the project, follow these steps:

Install Python 3.x and pip
```bash
# cd to the porject folder
cd flask_chat_room
# create a python env
python3 -m venv .env
# activate the env
source .env/bin/activate
```
Install the required dependencies by running `pip install -r requirements.txt`
Start the server by running `python3 app.py`
Open the web browser and navigate to http://localhost:8080
To run the project, follow these steps:
### Docker

Install Docker on your machine.
Run the following command to build the Docker image:
```bash
# sudo docker build -t flask_chat_room .
docker build -t flask_chat_room .
```
Once the image is built, run the following command to start the Docker container:
```bash
#sudo docker run flask_chat_room
docker run flask_chat-room
```
Open your web browser and navigate to http://localhost:8080.

Or you can pull the Docker image
```bash
docker pull abrahamel/flask_chat_room
```