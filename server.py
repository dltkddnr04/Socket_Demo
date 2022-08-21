from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 18650))
server_socket.listen(16)

def start_connection():
    connection_socket, address = server_socket.accept()
    print('Connected by', address)

    while True:
        receive_data = connection_socket.recv(1024)
        print(receive_data)

        if receive_data == '/exit':
            connection_socket.close()
            break

start_connection()