from socket import *
from datetime import datetime
import threading
import pickle

# make multi thread based socket echo server
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', 18650))
server_socket.listen()

client_list = []
socket_list = []

def console_print(type, message):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[{}][{}] {}'.format(time, type, message))

def data_process(user_nick_name, user_local_ip, user_external_ip):
    return [user_nick_name, user_local_ip, user_external_ip]

def connection(connection_socket, address):
    while True:
        try:
            receive_data = connection_socket.recv(8192)
            receive_data = pickle.loads(receive_data)

            user_nick_name = receive_data[0]
            user_local_ip = receive_data[1]
            user_external_ip = address[0]

            processed_personal_data = data_process(user_nick_name, user_local_ip, user_external_ip)

            client_list.append(processed_personal_data)

            if not receive_data:
                console_print('info', 'Disconnected by {}'.format(address))
                break

            console_print('receive', '{} : {}'.format(receive_data[0], receive_data[1]))
            for client_socket in socket_list:
                if client_socket != connection_socket:
                    client_socket.send(pickle.dumps(processed_personal_data))
                else:
                    client_socket.send(pickle.dumps(client_list))

        except:
            #console_print('info', 'Disconnected by {}'.format(address))
            #break
            pass

    if client_socket in socket_list:
        socket_list.remove(client_socket)
        client_list.remove(processed_personal_data)

    connection_socket.close()

console_print('info', 'server started')
console_print('info', 'waiting for connection')

try:
    while True:
        connection_socket, address = server_socket.accept()
        socket_list.append(connection_socket)
        console_print('info', 'connected by {} now {} user connected'.format(address, len(socket_list)))
        threading.Thread(target=connection, args=(connection_socket, address)).start()

except Exception as e:
    console_print('error', e)

finally:
    server_socket.close()
