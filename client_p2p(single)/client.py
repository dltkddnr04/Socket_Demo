from socket import *
from datetime import datetime
import threading
import pickle
import time

# stun_server_domain = 'stun.agaya.network'
# stun_server_ip = gethostbyname(stun_server_domain)
stun_server_ip = '10.0.0.116'

stun_socket = socket(AF_INET, SOCK_DGRAM)
stun_socket.bind(('', 18650))

client_p2p_socket = socket(AF_INET, SOCK_DGRAM)
client_p2p_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
client_p2p_socket.bind(('', 18650))

def get_internal_ip():
    temporary_socket = socket(AF_INET, SOCK_DGRAM)
    temporary_socket.connect(("8.8.8.8", 80))
    local_ip = temporary_socket.getsockname()[0]
    temporary_socket.close()
    return local_ip

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

stun_socket.connect((stun_server_ip, 18650))
stun_socket.send(get_internal_ip().encode())

opponent_user_ip = stun_socket.recv(1024)
stun_socket.close()

for i in range(5):
    try:
        client_p2p_socket.connect((opponent_user_ip, 18650))
        threading.Thread(target=receive_data, args=(client_p2p_socket,)).start()
        threading.Thread(target=send_data, args=(client_p2p_socket,)).start()
    except:
        continue