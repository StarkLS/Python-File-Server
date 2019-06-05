# imports
import os
from socket import *
# variables
directory = '/home/pi/NAS/'
spacer = '/'  
address_own = ''
port = 7767
action = ''

# define functions


def shut_client():
    client.shutdown(SHUT_RDWR)
    client.close()


def files_list():
    print('Files:')
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(str(file))
            client.send(str(file).encode())
            client.recv(1024)
    client.send('final'.encode())


def file_accept():
    print('wait for file infos')
    new_file_name = (client.recv(1024)).decode()
    f = open(directory+spacer+new_file_name, mode='wb')
    f.write(client.recv(1024))
    f.close()
    print('file ' ,new_file_name, ' was added to NAS-Pi')


def file_send():
    files_list()
    while True:
        send_file = (client.recv(1024)).decode()
        print(send_file)
        try:
            f = open(directory+spacer+send_file, mode='rb')
            print('true')
            client.send('True'.encode())
            print(client.recv(1024).decode())
            client.send(f.read(1024))
            print(f.read(1024))
            f.close()
            print(send_file,' donwloaded')
            break
        except FileNotFoundError:
            print('File error')
            client.send('False'.encode())
            down_decide = (client.recv(1024)).decode()
            if down_decide == 'n':
                break


def file_delete():
    files_list()
    while True:
        del_file = (client.recv(1024)).decode()
        print(del_file)
        try:
            f = open(directory+spacer+del_file, mode='rb')
            f.close()
            client.send('True'.encode())
            data = client.recv(1024)
            if data.decode() == 'j':
                os.remove(directory+spacer+del_file)
                print(del_file, ' deleted')
                break
            else:
                print('deletion cancelled')
                break
        except FileNotFoundError:
            print('File error')
            client.send('False'.encode())
            del_decide = (client.recv(1024)).decode()
            if del_decide == 'n':
                break


# program
server = socket(AF_INET, SOCK_STREAM)
server.bind ((address_own, port))
while True: # serving loop
    server.listen(1)
    client, client_address = server.accept()
    print('connected by ', client_address)
    while True:
        action = (client.recv(1024)).decode()
        if action == '0':
            print('client ended connection')
            break
        elif action == '1':
            file_accept()
        elif action == '2':
            file_send()
        elif action == '3':
            file_delete()
        elif action == '4':
            files_list()
        shut_client()
        print('connection closed after action')
        break
server.close()
