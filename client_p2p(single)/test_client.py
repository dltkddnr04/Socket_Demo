from socket import *
import datetime
import json
import time
import threading

SERVER_IP = '10.0.0.145'
SERVER_PORT = 4040
# but client-client connection port is 4041
P2P_PORT = 4041

def console_print(message):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[{time}] {message}".format(time=now_time, message=message))

def sock_send(sock):
    while True:
        try:
            message = input("message: ")
            if message == 'exit':
                break
            sock.sendall(message.encode())
        except:
            console_print("connection error")
            break

def sock_recv(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                console_print(data.decode())
                if data.decode() == 'exit':
                    break
        except:
            console_print("connection error")
            break

def server_connection():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    data = {
        'nick': 'nick',
        'message': 'connection'
    }
    sock.sendall(json.dumps(data).encode())

    osc_ip = None
    while osc_ip is None:
        data = sock.recv(1024)
        if data:
            try:
                processed_data = json.loads(data.decode())
                osc_ip = processed_data[0]
            except:
                pass

    p2p_socket = socket(AF_INET, SOCK_STREAM)
    p2p_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    p2p_socket.bind(('', P2P_PORT))
    for i in range(10):
        try:
            p2p_socket.connect((osc_ip, P2P_PORT))
            threading.Thread(target=sock_send, args=(p2p_socket,)).start()
            threading.Thread(target=sock_recv, args=(p2p_socket,)).start()
        except:
            continue

    while True:
        time.sleep(60)

if __name__ == '__main__':
    server_connection()