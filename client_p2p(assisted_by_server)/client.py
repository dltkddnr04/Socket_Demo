from socket import *
from datetime import datetime
import threading
import pickle

# get ip from dns
server_ip = gethostbyname('127.0.0.1')
server_port = 18650

user_nick_name = None
while not user_nick_name:
    user_nick_name = input('닉네임을 입력하세요: ')

user_list = []
connected_user_list = []

def get_local_ip():
    temporary_socket = socket(AF_INET, SOCK_DGRAM)
    temporary_socket.connect(("8.8.8.8", 80))
    local_ip = temporary_socket.getsockname()[0]
    temporary_socket.close()
    return local_ip

def stun_server_connect(server_ip, server_port):
    stun_server_socket = socket(AF_INET, SOCK_STREAM)
    stun_server_socket.connect((server_ip, server_port))

    send_data = [user_nick_name, get_local_ip()]
    stun_server_socket.sendall(pickle.dumps(send_data))
    receive_data = stun_server_socket.recv(8192)
    receive_data = pickle.loads(receive_data)
    
    
    while True:
        try:
            receive_data = stun_server_socket.recv(8192)
            receive_data = pickle.loads(receive_data)

        except:
            pass

def peer_to_peer_connection_start(client_list):
    pass


def send(socket, data):
    while True:
        send_data = [user_nick_name, data]
        new_send_data = pickle.dumps(send_data)
        socket.sendall(new_send_data)
        if send_data[1] == 'exit':
            break

def receive(socket):
    while True:
        receive_data = socket.recv(8192)
        receive_data = pickle.loads(receive_data)
        print("{}: {}".format(receive_data[0], receive_data[1]))
        #print(receive_data.decode('utf-8'))

#client_socket = socket(AF_INET, SOCK_STREAM)
#client_socket.connect((server_ip, server_port))

#threading.Thread(target=receive, args=(client_socket,)).start()
#threading.Thread(target=send, args=(client_socket,)).start()

# connect with stun server
threading.Thread(target=stun_server_connect, args=(server_ip, server_port)).start()