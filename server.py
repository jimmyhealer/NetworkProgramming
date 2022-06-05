# -*- coding: utf-8 -*-
import datetime
import socket
import threading
import json
import requests
HOST = '127.0.0.1'
PORT = 8080
AHTHORIZATION = 'CWB-26051DF2-C34C-4D41-9061-D9652E6AEA8F'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((HOST, PORT))
server.listen(10)

class SocketSend:

    @staticmethod
    def __broadcast(chatroom, user, data: str, type='chat'):
        for client in chatroom.getUserList():
            if client.getConn() != user.getConn():
                SocketSend.sendTo(client, type, data)

    @staticmethod
    def broadcast(user, data: str, isInfo=True):
        chatroom = user.getRoom()
        if isInfo: chatroom.addMessage(user, data)
        SocketSend.__broadcast(chatroom, user, data)

    @staticmethod
    def sendTo(user, type: str, message: str):
        while True:
            data = json.dumps({'type': type, 'result': message})
            user.getConn().sendall(data.encode())
            res = SocketSend.getData(user)
            if res == 'ok':
                break

    @staticmethod
    def getData(user):
        data = user.getConn().recv(1024)
        return data.decode()

class User:
    def __init__(self, conn: socket.socket, name: str):
        self.conn = conn
        self.name = name
        self.room = Chatroom

    def __str__(self):
        return self.name
    
    def getConn(self) -> socket.socket:
        return self.conn

    def getRoom(self):
        return self.room

    def setRoom(self, chatroom):
        if self.room == chatroom:
            return
        self.room = chatroom

class Chatroom:
    def __init__(self, roomName, user: User):
        self.roomName = roomName
        self.users = [user]
        self.messages = []
        user.setRoom(self)

    def __str__(self) -> str:
        return self.roomName

    def getUserList(self) -> list:
        return self.users

    def getMessage(self) -> list:
        return self.messages

    def addUser(self, user):
        SocketSend.broadcast(user, str(user) + " has joined the chatroom.", False)
        self.users.append(user)

    def addMessage(self, user, message):
        self.messages.append({"user": user, "message": message})

users = []
chatrooms = []

def chatAPI(user: User, data: dict):
    chatroom = user.getRoom()
    if chatroom == None:
        SocketSend.sendTo(user, 'chat', 'You are not in a chatroom')
        return
    SocketSend.broadcast(user, f'{user}> {data["data"]}')

def createChatAPI(user: User, data: dict):
    if data['data'] in chatrooms:
        SocketSend.sendTo(user, 'error', 'Chat already exists')
    else:
        chatrooms.append(Chatroom(data['data'], user))
        # print(user, 'created chatroom', data['data'])
        SocketSend.sendTo(user, 'info', f'-------{data["data"]}--------')
        SocketSend.sendTo(user, 'createChat', 'Chat created')

def joinChatAPI(user: User, data: dict):
    for chatroom in chatrooms:
        if str(chatroom) == data['data']:
            user.setRoom(chatroom)
            chatroom.addUser(user)
            SocketSend.sendTo(user, 'joinChat', 'Chat joined')
            SocketSend.sendTo(user, 'info', f'-------{chatroom}--------')
            for message in chatroom.getMessage():
                SocketSend.sendTo(user, 'chat', message['message'])
            return
    SocketSend.sendTo(user, 'error', 'Chat does not exist')

def weatherAPI(user: User, data: dict):
    region = data['data']
    dateStart = datetime.datetime.now()
    dateEnd = dateStart + datetime.timedelta(days=1)

    url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-091?Authorization={AHTHORIZATION}' + \
        f'&format=JSON&locationName={region}' + \
        f'&timeFrom={dateStart.strftime("%y-%m-%dT00:00:00")}&timeTo={dateEnd.strftime("%y-%m-%dT00:00:00")}'
    r = requests.get(url, verify=False)
    result = r.json()
    weatherElement = result['records']['locations'][0]['location'][0]['weatherElement']
    rain = weatherElement[0]['description']
    rain_value = weatherElement[0]['time'][0]['elementValue'][0]['value']
    rain_measures = weatherElement[0]['time'][0]['elementValue'][0]['measures']
    temperature = weatherElement[1]['description']
    temperature_value = weatherElement[1]['time'][0]['elementValue'][0]['value']
    temperature_measures = weatherElement[1]['time'][0]['elementValue'][0]['measures']
    Humidity = weatherElement[2]['description']
    Humidity_value = weatherElement[2]['time'][0]['elementValue'][0]['value']
    Humidity_measures = weatherElement[2]['time'][0]['elementValue'][0]['measures']
    phenomenon = weatherElement[6]['description']
    phenomenon_value = weatherElement[6]['time'][0]['elementValue'][0]['value']
    comport = weatherElement[7]['description']
    comport_number = weatherElement[7]['time'][0]['elementValue'][0]['measures']
    comport_value = weatherElement[7]['time'][0]['elementValue'][1]['value']
    UVI = weatherElement[9]['description']
    UVI_value = weatherElement[9]['time'][0]['elementValue'][0]['value']
    UVI_measures = weatherElement[9]['time'][0]['elementValue'][1]['value']
    WD = weatherElement[10]['description']
    WD_value = weatherElement[10]['time'][0]['elementValue'][0]['value']
    
    weather = f'\n<{region}>\n' + \
              f'{rain}: {rain_value}{rain_measures}\n' + \
              f'{temperature}: {temperature_value}{temperature_measures}\n' + \
              f'{Humidity}: {Humidity_value}{Humidity_measures}\n' + \
              f'{phenomenon}: {phenomenon_value}\n' + \
              f'{comport}: {comport_number}{comport_value}\n' + \
              f'{UVI}: {UVI_value} {UVI_measures}\n' + \
              f'{WD}: {WD_value}'
    SocketSend.sendTo(user, 'weather', weather)

def HandleClient(user: User):
    while True:
        try:
            data = SocketSend.getData(user)
            if len(data) == 0:
                return
            data = json.loads(data)
            type = data['type']
            # print(data)
            if type == 'createChat':
                createChatAPI(user, data)
            elif type == 'joinChat':
                joinChatAPI(user, data)
            elif type == 'chat':
                chatAPI(user, data)
            elif type == 'weather':
                weatherAPI(user, data)
            else:
                SocketSend.sendTo(user, 'error', f'your no any message or error type')
        except Exception as e:
            SocketSend.sendTo(user, 'error', f'your have some errors ({e}).')
            continue

print('Server is running...')

while True:
    conn, addr = server.accept()
    print('Connected by', addr)
    name = conn.recv(1024).decode()
    user = User(conn, name)
    if user not in users:
        users.append(user)
    SocketSend.sendTo(user, 'info', f'Welcome to this chatroom! Hey, {name}')
    SocketSend.sendTo(user, 'info', f'-----------------------------------------------------')
    threading.Thread(target=HandleClient, args=(user, )).start()