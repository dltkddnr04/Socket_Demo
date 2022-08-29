from socket import *
from datetime import datetime
import threading
import time

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 18650))
server_socket.listen()

client_list = []

def console_print(type, message):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[{}][{}] {}'.format(time, type, message))

def connection(connection_socket, address):
    while True:
        try:
            receive_data = connection_socket.recv(1024)

            if not receive_data:
                console_print('info', 'Disconnected by {}'.format(address))
                break

            console_print('receive', '{} : {}'.format(address[0], receive_data.decode('utf-8')))
            for client in client_list:
                if client != connection_socket:
                    # 접속을 시도한 본인이 아닐경우엔 접속을 시도한 유저의 데이터를 전송해준다
                    client.send(connection_socket)
                else:
                    # 접속을 시도한 본인일 경우 전체 접속자 리스트를 전송해준다
                    client.send(client_list)

        except:
            console_print('info', 'Disconnected by {}'.format(address))
            break

    if client in client_list:
        client_list.remove(client)

    connection_socket.close()


try:
    while True:
        connection_socket, address = server_socket.accept()
        client_list.append(connection_socket)
        threading.Thread(target=connection, args=(connection_socket, address)).start()
        console_print('info', 'connected by {} now {} user connected'.format(address, len(client_list)))

except Exception as e:
    console_print('error', e)

finally:
    server_socket.close()