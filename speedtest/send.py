import socket
import datetime

HOST = '127.0.0.1'
PORT = 4040

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    start_time = datetime.datetime.now()
    with open('test.iso', 'rb') as f:
        data = f.read()
        sock.sendall(data)
    end_time = datetime.datetime.now()

    # print time including microseconds
    print(end_time - start_time)

    sock.close()
    exit()