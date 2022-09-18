from socket import *
import threading

opponent_user_ip = '10.0.0.21'
opponent_user_port = 18651

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
client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
client_socket.bind(('', 18651))
for i in range(5):
    try:
        client_socket.connect((opponent_user_ip, opponent_user_port))
        threading.Thread(target=receive_data, args=(client_socket,)).start()
        threading.Thread(target=send_data, args=(client_socket,)).start()
    except:
        continue