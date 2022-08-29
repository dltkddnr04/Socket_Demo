import time
from datetime import datetime

def console_print(type, message):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('[{}][{}] {}'.format(time, type, message))