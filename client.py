import socket
import threading
import json
import time

HOST = '127.0.0.1'
PORT = 8080
clientMessage = 'Hello!'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
isChat = False

def handleServerIn():
  while True:
    try:
      data = client.recv(1024).decode()
      if len(data) == 0 or not data:
        break
      data = json.loads(data)
      client.sendall('ok'.encode())
      return data
    except Exception as e:
      print(e)
      continue

def receiveChatMessage():
  global isChat
  while isChat:
    try:
      data = handleServerIn()
      if data['type'] == 'chat':
        print(data['result'])
      elif data['type'] == 'info' and data['result'] == 'Goodbye':
        isChat = False
        print(data['result'])
      elif data['type'] == 'info' and data['result'] != 'Goodbye':
        print(data['result'])
    except Exception as e:
      print(e)
      continue

def sendChatMessage():
  global isChat
  while isChat:
    try:
      clientMessage = input('')
      if len(clientMessage) == 0:
        continue
      if clientMessage == ':q':
        isChat = False
      data = json.dumps({'type': 'chat', 'data': clientMessage})
      client.sendall(data.encode())
    except Exception as e:
      print(e)
      continue

name = input('Your name: ')
client.send(name.encode())
result = handleServerIn()
print(result['result'])
result = handleServerIn()
print(result['result'])


while True:
  while not isChat:
    time.sleep(0.1)
    try:
      option = int(input('1 - Create chatroom\n2 - Join chatroom\n3 - Query Weather\n4 - Exit\n> '))
      data = ""
      if option == 1:
        roomName = input('Room name: ')
        data = json.dumps({'type': 'createChat', 'data': roomName})
      elif option == 2:
        roomName = input('Room name: ')
        data = json.dumps({'type': 'joinChat', 'data': roomName})
      elif option == 3:
        city = input('City: ')
        data = json.dumps({'type': 'weather', 'data': city})
      elif option == 4:
        print('Goodbye!')
        exit()
      client.sendall(data.encode())
      result = handleServerIn()
      # print('Resceive option result')
      if result['type'] == 'error':
        print(result['result'])
      elif option == 1 or option == 2:
        print(result['result'])
        isChat = True        
        threading.Thread(target=receiveChatMessage).start()
        threading.Thread(target=sendChatMessage).start()
      elif option == 3:
        print(result['result'])
      if not isChat: print()
    except ValueError:
      print('Please input a number!\n')
      continue
