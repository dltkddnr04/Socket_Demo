import socket
import selectors
import datetime
import json

sel = selectors.DefaultSelector()

def console_print(msg):
    print("[{}] {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))

def accept(sock, mask):
    conn, addr = sock.accept() # Should be ready
    console_print('accepted from {}'.format(addr))
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024) # Should be ready
    peer_name = conn.getpeername()
    if data:
        data = data.decode()
        json_data = json.loads(data)
        nickname = json_data["nick"]
        message = json_data["message"]
        console_print('[received] {}: {}'.format(nickname, message))

        if data == 'exit':
            sel.unregister(conn)
            conn.close()
            console_print('closed connection to {}'.format(peer_name))
        else:
            # send back to all clients
            for key, mask in sel.get_map().items():
                if 'raddr=(' in str(mask.fileobj):
                    mask.fileobj.sendall(data.encode())

    else:
        console_print('closing {}'.format(peer_name))
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('', 4040))
sock.listen()
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)