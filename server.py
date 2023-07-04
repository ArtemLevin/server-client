import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clientsDict = {}


def broadcast(message):
    for client in clientsDict.keys():
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            broadcast('{} left!'.format(clientsDict[client]).encode('ascii'))
            clientsDict.pop(client)
            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clientsDict.setdefault(client, nickname)

        print("Nickname is {}".format(clientsDict[client]))
        broadcast("{} joined!".format(clientsDict[client]).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server if listening...")
receive()
