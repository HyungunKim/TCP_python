#### multiconn-server.py ####

import socket
from _thread import *
import pickle
from collections import defaultdict
from rules import *
import sys

# 쓰레드에서 실행되는 코드
# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 함


HEADER_LENGTH = 10
USERS = defaultdict(lambda: {'listen':[], 'speak':[], 'socket':None})

threads = []

lock = allocate_lock()
 
def threaded(client_socket, addr):
    global USERS, RUN
    hello = Receive(client_socket)
    name = hello['name']
    listen = hello['listen']

    #################################
    lock.acquire()
    USERS[name]['listen'] = listen
    USERS[name]['socket'] = client_socket
    print()
    print('Connected by :' + name + '@' + addr[0], ':', addr[1])

    for other in listen:
        USERS[other]['speak'].append(name)

    lock.release()
    #################################
    # 클라이언트가 접속을 끊을 때 까지 반복
    while True:
        data = Receive(client_socket)
        if not data:
            print('Disconnnected by :' + name )
            break

        print('Received from ' + addr[0], ':', addr[1], data)

        for other in  USERS[name]['speak']:
            try:
                Send(USERS[other]['socket'], data)

            except ConnectionResetError as e:
                print('Disconnnected by ' + other)

    client_socket.close()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('server start')


# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
counter = 0
while True: 
    server_socket.settimeout(2)
    print(f'\rwait {"."*(counter%4)}', end="")
    counter += 1
    try:
        client_socket, addr = server_socket.accept() 
        threads.append(start_new_thread(threaded, (client_socket, addr)))
    except socket.timeout:
        continue
    except (KeyboardInterrupt, SystemExit):
        sys.exit()



# cd Documents\programming\TCP