import socket
import threading

def send(s):
    while True:
        try:
            input_data = input('>>> ')
            s.sendall(input_data.encode())
            if input_data == 'exit':
                return
        except:
            return

def receive(s):
    while True:
        try:
            receive_data = s.recv(8192)
            if receive_data != b'':
                print("Received: {}".format(receive_data.decode()))
            else:
                return
        except:
            return

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 4040))

threading.Thread(target=receive, args=(s,)).start()
threading.Thread(target=send, args=(s,)).start()