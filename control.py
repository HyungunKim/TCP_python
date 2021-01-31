import socket
from rules import * 

name = 'control'
listen = ['control']

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) 

Send(client_socket, {'name':name, 'listen':listen})
while True: 

    data = input('Enter Message : ')
    
    Send(client_socket, data)

    response_data = Receive(client_socket)

    print('Received from the server :', response_data) 
    
    if data == 'quit':
        break


client_socket.close() 