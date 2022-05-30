from http import server
import socket

HOST = '127.0.0.1'
PORT = 8080
clientMessage = 'Hello!'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
  clientMessage = input()
  client.sendall(clientMessage.encode())

  serverMessage = client.recv(1024)
  if len(serverMessage) == 0:
    break
  print('Server:', serverMessage.decode())

client.close()