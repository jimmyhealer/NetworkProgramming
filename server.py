# -*- coding: utf-8 -*-
import socket
HOST = '127.0.0.1'
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

while True:
    conn, addr = server.accept()

    while True:
        try:
            clientMessage = str(conn.recv(1024), encoding='utf-8')
            if len(clientMessage) == 0:
                break
            # x, y = map(int, clientMessage.split())
            print('Client message is:', clientMessage)

            serverMessage = f'{eval(clientMessage)}'
        except Exception as e:
            print(e)
            serverMessage = str(e)
        finally:
            if len(serverMessage) == 0:
                conn.close()
                break
            conn.sendall(serverMessage.encode())