# -*- coding: utf-8 -*-
import socket
import threading
HOST = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind((HOST, PORT))
server.listen(10)
con = threading.Condition()

user = []
list_of_client = []
data = ""

def HandleClient(conn, name):
    while True:
        try:
            data = conn.recv(1024).decode()
            if len(data) == 0:
                BroadCast(f'{name} left the chat.', conn)
                return

            BroadCast(f'{name}> {data}', conn)
        except:
            BroadCast(f'{name} left the chat.', conn)
            return

def BroadCast(data, conn):
    for client in list_of_client:
        if client != conn:
            client.sendall(data.encode())

while True:
    conn, addr = server.accept()
    list_of_client.append(conn)
    print('Connected by', addr)
    name = conn.recv(1024).decode()
    if name not in user:
        user.append(name)
        BroadCast(f'{name} joined the chat.', conn)
    conn.send(f'Welcome to this chatroom! Hey, {name}\n'.encode())
    conn.send(f'-----------------------------------------------------'.encode())
    threading.Thread(target=HandleClient, args=(conn, name)).start()
