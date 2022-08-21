from socket import *
import threading

server_ip = '127.0.0.1'
server_port = 18650

def receive_data(socket):
    while True:
        receive_data = socket.recv(1024)
        receive_data = receive_data.decode('utf-8')
        print(receive_data)

def send_data(socket):
    while True:
        send_data = input('>>> ')
        socket.send(send_data.encode('utf-8'))
        if send_data == '/exit':
            exit()

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_ip, server_port))

threading.Thread(target=receive_data, args=(client_socket,)).start()
threading.Thread(target=send_data, args=(client_socket,)).start()