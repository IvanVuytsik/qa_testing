import threading
import socket
import string
import secrets
import json

clients = []
ids = []
keywords = []

HOST = socket.gethostbyname(socket.gethostname())
port_list = []
#----------------------------------------------------------------------
for tcp_port in range(8000,8002):
   port_list.append(tcp_port)

PORT = int(input('Choose connection port: '))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def broadcast(message):
    for client in clients:
        client.send(message)

def manage(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message) #share message to all clients
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            id = ids[index]
            broadcast(f'{id} has left the session'.encode('ascii'))
            ids.remove(id)
            break


def receive():
    while True:
        client,address = server.accept()
        print(f'Connected from {str(address)}')
#-----------------------------------------------------------------------------
        alphabet = string.ascii_letters + string.digits
        generated_keyword = ''.join(secrets.choice(alphabet) for i in range(8))

        print(generated_keyword)
        with open ('keys.txt', 'w') as f:
            f.write(f'{generated_keyword}\n')
        keywords.append(generated_keyword)
#-----------------------------------------------------------------------------
        client.send('ID'.encode('ascii'))
        id = client.recv(1024).decode('ascii')
        if id != 'admin':
            client.send('KEY'.encode('ascii'))
            key = client.recv(1024).decode('ascii')
            if key != generated_keyword:
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        ids.append(id)
        clients.append(client)

        print(f'Name of the client is {id}')
        broadcast(f'{id} has joined the session'.encode('ascii'))
        client.send('You are connected to the server\n'.encode('ascii'))
        #client.send(f'Your keyword is: {generated_keyword}'.encode('ascii'))

        thread = threading.Thread(target=manage, args=(client,))
        thread.start()

print('Server is active...')
receive()
