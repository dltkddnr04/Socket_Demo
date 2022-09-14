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
    user_list = receive_data
    print(user_list)
    
    while True:
        try:
            receive_data = stun_server_socket.recv(8192)
            receive_data = pickle.loads(receive_data)
            user_list.append(receive_data)
            print(user_list)

        except:
            pass

def peer_to_peer_connection_start():
    while True:
        try:
            for user in user_list:
                if user not in connected_user_list and user[1] != get_local_ip():
                    peer_to_peer_socket = socket(AF_INET, SOCK_STREAM)
                    try:
                        peer_to_peer_socket.connect((user[1], 18651))
                        connected_user_list.append(user)
                        #threading.Thread(target=connection, args=(peer_to_peer_socket)).start()
                        print('connected to {} using local ip'.format(user[0]))
                    except:
                        try:
                            peer_to_peer_socket.connect((user[2], 18651))
                            connected_user_list.append(user)
                            #threading.Thread(target=connection, args=(peer_to_peer_socket)).start()
                            print('connected to {} using public ip'.format(user[0]))
                        except:
                            print('연결 실패')
        except:
            pass


def connection(peer_to_peer_socket):
    while True:
        try:
            send_data = [user_nick_name, input()]
            peer_to_peer_socket.sendall(pickle.dumps(send_data))

        except:
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

# connect with stun server
threading.Thread(target=stun_server_connect, args=(server_ip, server_port)).start()
threading.Thread(target=peer_to_peer_connection_start, args=()).start()