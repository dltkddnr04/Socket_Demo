from socket import *
import threading
import pickle

# get ip from dns
server_ip = gethostbyname('127.0.0.1')
server_port = 18650

user_nick_name = None
while not user_nick_name:
    user_nick_name = input('닉네임을 입력하세요: ')

def send(socket):
    while True:
        input_data = input('>>> ')
        send_data = [user_nick_name, input_data]
        new_send_data = pickle.dumps(send_data)
        socket.sendall(new_send_data)
        if input_data == 'exit':
            socket.close()
            return

def receive(socket):
    while True:
        try:
            receive_data = socket.recv(8192)
            receive_data = pickle.loads(receive_data)
            print("{}: {}".format(receive_data[0], receive_data[1]))
            #print(receive_data.decode('utf-8'))
        
        except:
            return

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_ip, server_port))

threading.Thread(target=receive, args=(client_socket,)).start()
threading.Thread(target=send, args=(client_socket,)).start()