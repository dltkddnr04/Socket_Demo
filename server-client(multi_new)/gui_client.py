import socket
import threading
import datetime
import sys
import json
import time
import PyQt5.QtWidgets as qtwid

SERVER_IP = '127.0.0.1'
SERVER_PORT = 4040

class MyApp(qtwid.QWidget):
    def __init__(self):
        self.nickname = 'Guest'
        super().__init__()
        self.initUI()

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((SERVER_IP, SERVER_PORT))
            threading.Thread(target=self.recive_message, args=(self.server_socket,)).start()

        except:
            qtwid.QMessageBox.information(self, '서버 연결 오류', '서버에 연결할 수 없습니다.')
            sys.exit()

    def recive_message(self, server_socket):
        while True:
            #try:
            recived_message = server_socket.recv(8192)
            recived_message = recived_message.decode()
            recived_message = json.loads(recived_message)
            if recived_message != b'':
                if recived_message["nick"] != self.nickname:
                    self.console_print("recived", recived_message["nick"], recived_message["message"])
            else:
                pass

            #except:
            #    print("something")

    def console_print(self, msg_type, nick, msg):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if nick is not None:
            message = "[{}] [{}] [{}] {}".format(now_time, msg_type, nick, msg)
        else:
            message = "[{}] [{}] {}".format(now_time, msg_type, msg)

        self.chat_log.append(message)

    def initUI(self):
        self.chat_log = qtwid.QTextBrowser(self)
        self.my_msg = qtwid.QLineEdit(self)
        self.send_btn = qtwid.QPushButton('전송', self)

        grid = qtwid.QGridLayout()
        grid.addWidget(self.chat_log, 0, 0, 1, 2)
        grid.addWidget(self.my_msg, 1, 0)
        grid.addWidget(self.send_btn, 1, 1)

        self.setLayout(grid)

        self.setWindowTitle('Pizza Network Client')
        self.resize(600, 400)
        self.show()

        self.send_btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        input_message = self.my_msg.text()
        self.my_msg.setText('')

        if input_message.startswith('/'):
            type = 'COMMAND'
            # 이것은 명령어입니다.
            args = input_message.split(' ')
            command_type = args[0][1:]
            if command_type == 'nick':
                self.nickname = args[1]
                message = '닉네임을 {}(으)로 변경했습니다.'.format(self.nickname)
            elif command_type == 'exit':
                # exit command
                message = '클라이언트를 종료합니다.'

        else:
            type = 'MSG'
            data = {
                'nick': self.nickname,
                'message': input_message
            }
            message = input_message
            self.server_socket.send(json.dumps(data).encode())

        self.console_print(msg_type=type, nick=self.nickname, msg=message)
        return

if __name__ == '__main__':
    app = qtwid.QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())