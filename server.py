import threading
import socket
import time 

from datetime import datetime, timedelta

clients = []
clients_time = {}


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen()
    except socket.error:
        return print('It was not possible to start server!\n')
    
    thread_message_sync = threading.Thread(target=sync_message, args=[])
    thread_message_sync.start()
    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=messages_treatment, args=[client,])
        thread.start()


def sync_message():
    while True:
        msg = input('Would you like to sync the time? \n')
        if msg == 's':
            for client in clients:
                broadcast('input your time', client)
                time.sleep(0.1)


def messages_treatment(client):
    while True:
        try:
            msg = client.recv(2048)
            process_message(client, msg.decode("utf-8"))
        except socket.error as e:
            print(f'Something went wrong, error {e}')
            delete_client(client)
            break


def sync_time_berkley():
    difference_time = []
    clients_difference = {}
    cur_date = datetime.now().replace(microsecond=0)
    print(f"My current time is {cur_date}")
    count = 0
    for client, client_time in clients_time.items():
        count += 1
        diff_time = cur_date - client_time
        difference_time.append(float(diff_time.total_seconds()))
        clients_difference.update({client: diff_time})

        print(f"Client {count} time is {client_time} and diff is {diff_time.total_seconds()/60} minutes")

    average_time = sum(difference_time) / (len(clients) + 1)
    print(f"the average time is {average_time/60} minutes")

    count2 = 0
    for client, client_time in clients_time.items():
        count2 += 1
        sync_time = (client_time + timedelta(seconds=(clients_difference[client] * - 1).total_seconds() + average_time)).replace(microsecond=0)
        print(f"Client {count2} time updated is {sync_time}")
        broadcast(str(sync_time), client)


def process_message(client, msg):
    clients_time.update({client: datetime.strptime(msg, '%Y-%m-%d %H:%M:%S')})
    if len(clients) == len(clients_time):
        sync_time_berkley()
        clients_time.clear()


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem == client:
            try:
                clientItem.send(msg.encode('utf-8'))
                break
            except Exception as e:
                print(e)
                delete_client(clientItem)


def delete_client(client):
    clients.remove(client)


main()
