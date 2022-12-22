import socket, threading  # импорт библиотек

host = '127.0.0.1'  # локальный хост компьютера
port = 8081 # выбор незарезервированного порта

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # инициализация сокета
server.bind((host, port))  # назначение хоста и порта к сокету
server.listen()

clients = []
nicknames = []


def broadcast(message):  #функция связи
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:  # получение сообщений от клиентов
            message = client.recv(1024)
            broadcast(message)
        except:  # удаление клиентов
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} ушел!'.format(nickname).encode('геа-8'))
            nicknames.remove(nickname)
            break

def receive():  # подключение нескольких пользователей
    while True:
        client, address = server.accept()
        print("Соеденен с {}".format(str(address)))
        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print("имя пользователя {}".format(nickname))
        broadcast("{}присоединился!".format(nickname).encode('utf-8'))
        client.send('Подключен к серверу!'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()