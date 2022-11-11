import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.11.76", 14444))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.send(pickle.dumps({
    "title": "test",
    "message": "test",
    "sender": "test",
    "contentimage": "test"
}))
