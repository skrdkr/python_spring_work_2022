# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50008              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(bytes('GET ava.jpg', encoding='UTF-8'))
    data = s.recv(1024)
print('Received', data)