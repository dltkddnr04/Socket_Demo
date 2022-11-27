import socket
import datetime

HOST = ''
PORT = 4040

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()

    with open('test2.iso', 'wb') as f:
        connection_socket, address = sock.accept()
        while True:
            data = connection_socket.recv(8192)
            if data != b'':
                f.write(data)
            else:
                break
        connection_socket.close()