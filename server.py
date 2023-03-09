from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from camera import Camera
import base64
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
camera = Camera()


@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data': 'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)


@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect", {"data": f"id: {request.sid} is connected"})


@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ", str(data))
    for i in range(0, 10):
        emit("data", {'data': data, 'id': request.sid}, broadcast=True)


@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect", f"user {request.sid} disconnected", broadcast=True)


@socketio.on("request-frame")
def camera_frame_requested(message):
    frame, data = camera.get_frame()
    if frame is not None:
        emit("new-frame", {
            "base64": base64.b64encode(frame).decode("ascii"),
            "rec": data
        })
        # print("fgfgfggfgfg")


if __name__ == '__main__':
    camera.start()
    socketio.run(app, debug=True, port=5001)
