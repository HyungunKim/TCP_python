import socket 
import pickle

HOST = '127.0.0.1'
PORT = 9999
HEADER_LENGTH = 10

def Receive(sock, binary = False):
    header_recehived = False
    header = b''

    while not header_recehived:
        header += sock.recv(HEADER_LENGTH - len(header))
        if len(header) == HEADER_LENGTH:
            header_recehived = True

    data_len = int(header.decode())

    data_recehived = False
    data = b''

    while not data_recehived:
        data += sock.recv(data_len - len(data))
        if len(data) == data_len:
            data_recehived = True

    if binary:
        return data

    data = pickle.loads(data)
    return data

def Send(sock, data):

    data = pickle.dumps(data)
    header = f'{len(data): <{HEADER_LENGTH}}'.encode()

    message = header + data

    sock.send(message) 