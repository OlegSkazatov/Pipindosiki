from socketserver import *
import os
import sys
import winsound
import threading
from os import listdir
from os.path import isfile, join
import pygame

host = '26.112.25.183'  # IP сервера в локальной сети
port = 777
addr = (host, port)
socket = None
flag = 0
users = []
running = True


def load_image(name):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def pyhgame_window(image_name=None):
    global running
    print("a")
    running = True
    pygame.init()
    pygame.display.set_caption('')
    if image_name is None:
        infoObject = pygame.display.Info()
        width, height = infoObject.current_w, infoObject.current_h
        image = None
    else:
        image = load_image(f"data{os.sep}{image_name}")
        width, height = image.get_width(), image.get_height()
    size = width, height
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    if image is not None:
        screen.blit(image, (0, 0))
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    running = False
    pygame.quit()


def getUser(address):
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

    def sendPacket(self, socket, packet):
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
        if action == "open":
            if len(packet.split(";")) == 1:
                image_name = None
            else:
                image_name = packet.split(";")[1]
            pyhgame = threading.Thread(
                target=pyhgame_window(image_name),
                args=(),
                daemon=True
            )
            pyhgame.start()


if __name__ == "__main__":  # Запуск сервера
    server = UDPServer(addr, MyUDPHandler)
    print('Запускаем пыщ-машину')
    server.serve_forever()
    print('Да ты чё')
