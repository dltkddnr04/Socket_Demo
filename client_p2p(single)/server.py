import socket
import selectors
import datetime
import json

SERVER_IP = ''
SERVER_PORT = 4040

def console_print(message):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[{time}] {message}".format(time=now_time, message=message))

def server_run():
    selector = selectors.DefaultSelector()

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER_IP, SERVER_PORT))
    server_sock.setblocking(False)
    server_sock.listen()

    selector.register(server_sock, selectors.EVENT_READ, accept)
    while True:
        for (key, mask) in selector.select():
            srv_sock, callback = key.fileobj, key.data
            callback(srv_sock, selector)

    '''
        SelectorKey.fileobj - 소켓
        SelectorKey.fd - 저수준 파일 디스크립터
        SelectorKey.events - 해당 IO가 대기하는 이벤트
        SelectorKey.data - 등록시 사용된 임의의 데이터
    '''

def accept(sock, sel):
    conn, addr = sock.accept()
    console_print('accepted from {}'.format(addr))
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(sock, sel):
    # recive all data
    payload = sock.recv(8192)
    peer_name = sock.getpeername()
    if payload:
        payload = payload.decode()
        json_data = json.loads(payload)
        nickname = json_data["nick"]
        message = json_data["message"]
        client_ip = sock.getpeername()[0]
        console_print('[received] {}: {}'.format(nickname, message))

        if message == 'exit':
            sel.unregister(sock)
            sock.close()
            console_print('closed connection to {}'.format(peer_name))
        elif message == 'connection':
            for key, mask in sel.get_map().items():
                if 'raddr=(' in str(mask.fileobj):
                    # mask.fileobj.sendall(payload.encode())
                    # send message to all client
                    if sock == mask.fileobj:
                        # send all client list
                        # get each client's ip
                        client_list = []
                        for key, mask in sel.get_map().items():
                            if 'raddr=(' in str(mask.fileobj) and sock != mask.fileobj:
                                client_ip = mask.fileobj.getpeername()[0]
                                client_list.append(client_ip)
                        client_list = json.dumps(client_list)
                        sock.sendall(client_list.encode())

                    else:
                        # send new client(sock) list
                        # get sock's ip
                        client_list = []
                        client_list.append(client_ip)
                        client_list = json.dumps(client_list)
                        mask.fileobj.sendall(client_list.encode())
        elif message == 'ext_ip':
            send_data = {
                'client_ip': client_ip
            }
            sock.sendall(json.dumps(send_data).encode())

    else:
        console_print('closed connection to {}'.format(peer_name))
        sel.unregister(sock)
        sock.close()

if __name__ == '__main__':
    server_run()