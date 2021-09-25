import logging

from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import threading
from socket import *

host = '26.112.25.183'
port = 777
addr = (host, port)
udp_socket = socket(AF_INET, SOCK_DGRAM)


def handlePacket(packet):
    ptype = packet.split(";")[0]
    if ptype == "data":
        print("\n".join(packet.split(";")[1:]))


def sendPacket(packet):  # Отправка пакетов на сервер
    udp_socket.sendto(packet.encode(), addr)


def cikle():
    while True:
        try:
            sms = udp_socket.recvfrom(1024)
            if sms[0].decode() == '':
                continue
            handlePacket(sms[0].decode())
        except OSError:
            continue


client_handler = threading.Thread(
    target=cikle,
    args=(),
    daemon=True
)
client_handler.start()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("\n".join(["playsound <имя звука> - если надо громко брухнуть",
                                         "help - если ты долбаёб"]))


def playsound_command(update: Update, context: CallbackContext) -> None:
    sound = update.message.text.split()[1]
    if ".wav" not in sound:
        sound = sound.split(".")[0] + ".wav"
    sendPacket("playsound;" + sound)
    update.message.reply_text(f"Воспроизведён звук '{sound}'. А может и нет. Я чё, ебу?")


def open_command(update: Update, context: CallbackContext) -> None:
    if len(update.message.text.split()) == 1:
        name = ""
    else:
        name = update.message.text.split()[1]
    if ".jpg" not in name and ".png" not in name and ".gif" not in name:
        name = name.split(".")[0] + ".jpg"
    sendPacket("open;" + name)
    update.message.reply_text(f"Открыт файл '{name}'. А может и нет. Я чё, ебу?")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    updater = Updater("2025798666:AAHqa8W5Pwgk-4EFR40bZ1Fm5BJC9RozO-8")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("playsound", playsound_command))
    dispatcher.add_handler(CommandHandler("open", open_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
