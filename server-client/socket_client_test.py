from socket import *
import threading

# get ip from dns
server_ip = gethostbyname('leestudio.iptime.org')
server_port = 18650

def command_check(command, type):
    if type == 'send':
        if command == '/exit':
            return True
    elif type == 'receive':
        if command == 'exit':
            return True
    else:
        return False

def send(socket):
    while True:
        send_data = input('>>> ')
        socket.send(send_data.encode('utf-8'))
        if command_check(send_data, 'send'):
            break

def receive(socket):
    while True:
        receive_data = socket.recv(1024)
        receive_data = receive_data.decode('utf-8')
        print('\n상대: ' + receive_data)
        if command_check(receive_data, 'receive'):
            break

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_ip, server_port))

threading.Thread(target=receive, args=(client_socket,)).start()
threading.Thread(target=send, args=(client_socket,)).start()