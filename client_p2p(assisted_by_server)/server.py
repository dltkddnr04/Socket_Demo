from socket import *
from datetime import datetime
import threading
import pickle

# make multi thread based socket echo server
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
            receive_data = connection_socket.recv(8192)

            if not receive_data:
                console_print('info', 'Disconnected by {}'.format(address))
                break

            processed_receive_data = pickle.loads(receive_data)
            console_print('receive', '{} : {}'.format(processed_receive_data[0], processed_receive_data[1]))
            for client in client_list:
                #if client != connection_socket:
                client.send(receive_data)

        except:
            #console_print('info', 'Disconnected by {}'.format(address))
            #break
            pass

    if client in client_list:
        client_list.remove(client)

    connection_socket.close()

console_print('info', 'server started')
console_print('info', 'waiting for connection')

try:
    while True:
        connection_socket, address = server_socket.accept()
        client_list.append(connection_socket)
        console_print('info', 'connected by {} now {} user connected'.format(address, len(client_list)))
        threading.Thread(target=connection, args=(connection_socket, address)).start()

except Exception as e:
    console_print('error', e)

finally:
    server_socket.close()
