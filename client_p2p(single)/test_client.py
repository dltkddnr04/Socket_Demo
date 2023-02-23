import socket
import datetime
import json
import threading

SERVER_IP = ''
SERVER_PORT = 4040
# but client-client connection port is 4041

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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    data = {
        'nick': 'nick',
        'message': 'connection'
    }
    sock.sendall(json.dumps(data).encode())

    data = sock.recv(1024)
    if data:
        osc_ip = None
        while osc_ip is None:
            try:
                processed_data = json.loads(data.decode())
                osc_ip = processed_data[0]
            except:
                pass

        p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p2p_socket.connect((osc_ip, 4041))
        while True:
            message = input()
            p2p_socket.sendall(message.encode())
            threading.Thread(target=sock_recv, args=(p2p_socket,)).start()
            threading.Thread(target=sock_send, args=(p2p_socket,)).start()

if __name__ == '__main__':
    server_connection()