import socket
import threading

HOST = '127.0.0.1'
PORT = 8080
clientMessage = 'Hello!'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def HandleServerIn():
  while True:
    try:
      data = client.recv(1024)
      if len(data) == 0:
        break
      print(data.decode())
    except:
      continue

def HandleServerOut():
  while True:
    try:
      clientMessage = input()
      client.sendall(clientMessage.encode())
    except Exception as e:
      print(e)
      continue

name = input()
client.send(name.encode())
# print(client.recv(1024).decode())
# print(client.recv(1024).decode())

threading.Thread(target=HandleServerIn).start()
threading.Thread(target=HandleServerOut).start()