from http import server
import select
import socket
import struct
import sys

HOST = '127.0.0.1'
PORT = 8080
clientMessage = 'Hello!'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
  room = input('Enter room number: ')
  client.sendall(room.encode())

  room_size = str(client.recv(1024), encoding='utf-8') # receive the size of the chat record
  print('Room size: ' + room_size)
  room_size = int(room_size)

  while room_size != 0:
    serverMessage = str(client.recv(5), encoding='utf-8')# receive the chat record
    print('<Server> ' + serverMessage)
    room_size -= 1
  
  # list = [sys.stdin, server]
  # read, write, error = select.select(list, [], [])

  # for sock in read:
  #   if sock == server:
  #     message = str(sock.recv(1024), encoding='utf-8')
  #     print('server message:' + message)
  #   else:
  #     client.sendall(sys.stdin.readline().encode())
  #     sys.stdout.flush()

  # clientMessage = input('Sending message:')
  # client.sendall(clientMessage.encode())

client.close()