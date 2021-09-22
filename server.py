from socketserver import *
import os
import winsound
from os import listdir
from os.path import isfile, join

host = '26.112.25.183'  # IP сервера в локальной сети
port = 26795
addr = (host, port)
socket = None
flag = 0
users = []


def getUser(address):  # Получить игрока по адресу
    for u in users:
        if u.addr == address:
            return u


def send_data(user):
    path = os.path.abspath(os.getcwd()) + os.sep + "data"
    onlyfans = [f for f in listdir(path) if isfile(join(path, f))]
    packet = "data;" + ";".join(onlyfans)
    user.sendPacket(socket, packet)


class User:
    def __init__(self, addr):
        self.addr = addr
        users.append(self)

    def sendPacket(self, socket, packet):  # Отправить данные игроку
        socket.sendto(packet.encode(), self.addr)


class MyUDPHandler(DatagramRequestHandler):  # Обработка пакетов от пользователей
    def handle(self):
        global flag, socket
        socket = self.request[1]
        packet = self.request[0].decode()
        action = packet.split(";")[0]
        user = getUser(self.client_address)
        if user is None:
            user = User(self.client_address)
        if action == "get_fnames":
            send_data(user)
        if action == "playsound":
            print(packet)
            sound = "data" + os.sep + packet.split(";")[1]
            try:
                winsound.PlaySound(sound, winsound.SND_ASYNC)
            except Exception:
                user.sendPacket(socket, "error;Ты еблан?")


if __name__ == "__main__":  # Запуск сервера
    server = UDPServer(addr, MyUDPHandler)
    print('Запускаем пыщ-машину')
    server.serve_forever()
    print('Да ты чё')
