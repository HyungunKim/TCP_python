#### multiconn-client.py ####
import socket
from . rules import *
from _thread import *

class CallClient():
    def __init__(self, name='CallClient', listen = ['ResponseClient']):
        self.name = name
        self.listen = listen

        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

        self.client_socket.connect((HOST, PORT)) 

        Send(self.client_socket, {'name':name, 'listen':listen})

    def __call__(self, data):
        Send(self.client_socket, data)
        response_data = Receive(self.client_socket)
        return response_data

    def __del__(self,):
        self.client_socket.close()
        super().__del__()

class ResponseClient:
    def __init__(self, name='ResponseClient', listen = ['CallClient'], process=lambda x: x+1):
        self.name = name
        self.listen = listen

        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

        self.client_socket.connect((HOST, PORT)) 

        Send(self.client_socket, {'name':name, 'listen':listen})

        self.process = process

        self.thread = start_new_thread(self.main, ())

    def main(self):
        while True: 
            response_data = Receive(self.client_socket)

            #print('Received from the server :', response_data) 

            data = self.process(response_data)

            Send(self.client_socket, data)


    def __del__(self,):
        self.client_socket.close()
        super().__del__()
