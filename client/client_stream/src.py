import cv2
import socket
import pickle
import struct
import os

def do_stream(client_socket,client_address,fps,width,height):
    cap = cv2.VideoCapture('space_sample.mp4')
    cap.set(cv2.CAP_PROP_FPS,fps)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            frame_data = pickle.dumps(frame)
            client_socket.sendall(struct.pack("Q", len(frame_data)))
            client_socket.sendall(frame_data)
            if cv2.waitKey(1) == 13:
                break
        cap.release()
        cv2.destroyAllWindows()
        return 200
    except:
        cap.release()
        cv2.destroyAllWindows()
        return None

def do_connect():
    server_socket.listen(5)
    print("Stream service is listening...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} accepted")
    return client_socket, client_address


_stream_port= int(os.environ['ENV_STREAM_PORT'])
_fps= int(os.environ['ENV_FPS'])
_frame_width= int(os.environ['ENV_FRAME_WIDTH'])
_frame_height= int(os.environ['ENV_FRAME_HEIGHT'])

while True:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', _stream_port))

    client_socket,client_address=do_connect()

    ret=200
    while ret is not None:
        ret=do_stream(client_socket,client_address,fps=_fps,width=_frame_width,height=_frame_height)
