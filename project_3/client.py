import threading
import socket
import json
from datetime import datetime


HOST = socket.gethostbyname(socket.gethostname())
PORT = int(input('Choose connection port: ')) #8000 or 8001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

stop_thread = False

id = input("Provide your id: ")

if id != 'admin':
   with open('keys.txt', 'r') as f:
        gen_key = f.readlines()[0]
   print(f'Your generated key is: {gen_key}')
   key = input("Provide your key: ")

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def receive():
    while True:
        global stop_thread
        if stop_thread: break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'ID':
                client.send(id.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == "KEY":
                    client.send(key.encode('ascii'))
                    if client.recv(1024).decode('ascii') == "REFUSE":
                        print('Connection error: wrong key')
                        stop_thread = True
            else:
                print(message)
        except:
            print('An error has occurred')
            client.close()
            break

def write():
    while True:
        if stop_thread: break
        message = f'{id}: {input("")}'
        client.send(message.encode('ascii'))
        server_log = {}
        server_log[f'{id}'] = []
        server_log[f'{id}'].append({'id': id,'message':message, 'time': current_time})
        with open('server_log.txt', 'a',) as outfile:
            json.dump(server_log, outfile,indent=1)


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()