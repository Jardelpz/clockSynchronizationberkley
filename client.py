import threading
import socket
import time

from datetime import datetime, timedelta
from random import randint


def random_date():
    random_seconds = randint(60, 10000)
    if random_seconds % 2 == 0:
        return datetime.now() + timedelta(seconds=random_seconds)
    else:
        return datetime.now() - timedelta(seconds=random_seconds)


cur_date = random_date().replace(microsecond=0)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 5555))
    except socket.error:
        return print('It was not possible connect with server!\n')

    thread1 = threading.Thread(target=sendMessages, args=[client, ])
    thread2 = threading.Thread(target=receiveMessages, args=[client, ])

    thread1.start()
    thread2.start()


def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if 'input' in msg:
                print(f'Server - {msg}')
                global cur_date
                print(f'My time is - {cur_date}')
                sendMessages(client, str(cur_date))
            else:
                print(f'Server - Please update your time to {msg}')
                cur_date = datetime.strptime(msg, '%Y-%m-%d %H:%M:%S')
                print(f'my current date was updated, now its: {cur_date}')

        except socket.error as e:
            print('It was not possible to keep connected with server!\n')
            print('Press <Enter> to continue...')
            client.close()
            break

        except Exception as e:
            print(e)


def sendMessages(client, msg=None):
    if msg:
        client.send(msg.encode('utf-8'))
    
    return

main()
