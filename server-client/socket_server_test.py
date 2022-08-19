from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 18650))
server_socket.listen(1)

def connection():
    connection_socket, address = server_socket.accept()
    print('Connected by', address)

    while True:
        try:
            receive_data = connection_socket.recv(1024)
            receive_data = receive_data.decode('utf-8')
            print('Received: ' + receive_data)

            if receive_data[0:1] == '/':
                query = receive_data[1:]

                if query == 'exit':
                    send_data = 'exit'
                    connection_socket.send(send_data.encode('utf-8'))
                    print('Disconnected by', address)
                    break
                
                elif query == 'help':
                    send_data = '/exit, /help'
                    connection_socket.send(send_data.encode('utf-8'))

                else:
                    send_data = 'command not found'
                    connection_socket.send(send_data.encode('utf-8'))

            else:
                send_data = 'return ' + receive_data
                connection_socket.send(send_data.encode('utf-8'))

        except:
            print('Disconnected by', address)
            break

while True:
    connection()