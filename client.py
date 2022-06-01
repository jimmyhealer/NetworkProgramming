import socket
import threading
import json
import time

HOST = '127.0.0.1'
PORT = 8080
clientMessage = 'Hello!'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def HandleServerIn():
  while True:
    try:
      data = client.recv(1024).decode()
      if len(data) == 0:
        break
      data = json.loads(data)
      client.sendall('ok'.encode())
      print(data['result'])
    except Exception as e:
      continue

def HandleServerOut():
  time.sleep(0.1)
  option = int(input('1 - Create chatroom\n2 - Join chatroom\n3 - Chat\n4 - Exit\n> '))
  data = ""
  if option == 1:
    data = json.dumps({'type': 'createChat', 'data': 'test'})
  elif option == 2:
    data = json.dumps({'type': 'joinChat', 'data': 'test'})
  
  client.sendall(data.encode())
  time.sleep(0.1)

  while True:
    try:
      clientMessage = input('')
      if len(clientMessage) == 0:
        continue
      if clientMessage == 'EXIT':
        break
      data = json.dumps({'type': 'chat', 'data': clientMessage})
      client.sendall(data.encode())
    except Exception as e:
      print(e)
      continue

name = input('Your name: ')
client.send(name.encode())

threading.Thread(target=HandleServerIn).start()
threading.Thread(target=HandleServerOut).start()