import os
import asyncio
import redis
import telepot
import telepot.async

redis_connection = redis.StrictRedis()
sudo_members = [111111111]
TOKEN = "TOKEN_HERE"


def check_sudo(chat_id):
    return chat_id in sudo_members


def markdown_escape(text):
    text = text.replace("_", "\\_")
    text = text.replace("[", "\\{")
    text = text.replace("*", "\\*")
    text = text.replace("`", "\\`")
    return text


@asyncio.coroutine
def handle_messages(message):
    if message['text'] == "hello":
        yield from send_hello(message)


@asyncio.coroutine
def send_hello(message):
    yield from bot.sendMessage(message['chat']['id'], "Hello there!")


@asyncio.coroutine
def download(file_id, path):
    yield from bot.download_file(file_id, path)
    return path

bot = telepot.async.Bot(TOKEN)
answerer = telepot.async.helper.Answerer(bot)
loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': handle_messages}))
print('Bot Started')
loop.run_forever()

