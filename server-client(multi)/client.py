from socket import *
import threading

# get ip from dns
server_ip = gethostbyname('127.0.0.1')
server_port = 18650

def send(socket):
    while True:
        send_data = input('>>> ')
        socket.send(send_data.encode('utf-8'))
        if send_data == 'exit':
            break

def receive(socket):
    while True:
        receive_data = socket.recv(8192)
        receive_data = receive_data.decode('utf-8')
        print('상대: ' + receive_data)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_ip, server_port))

threading.Thread(target=receive, args=(client_socket,)).start()
threading.Thread(target=send, args=(client_socket,)).start()