import os
import asyncio
import redis
import telepot
import telepot.async
import json
import importlib
import requests
import sys
import re
import time
from termcolor import colored
import threading
from telepot.namedtuple import *
config = importlib.import_module("config")
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
pool = redis.ConnectionPool(host='localhost', port=6379, db=0, password=None,decode_responses=True)
db = redis.Redis(connection_pool=pool)
bot = telepot.Bot(config.TOKEN)

def markdown_escape(text):
    text = text.replace("_", "\\_")
    text = text.replace("[", "\\{")
    text = text.replace("*", "\\*")
    text = text.replace("`", "\\`")
    return text

def send_hello(message):
    yield from bot.sendMessage(message['chat']['id'], "Hello there!")

def is_sudo(user_id):
    return user_id in config.sudo_users

def is_premium(user_id):
    return user_id in config.premium_users

def download(file_id, path):
    yield from bot.download_file(file_id, path)
    return path
def send_msg(msg, text):
    bot.sendChatAction(msg['chat']['id'], "typing")
    if msg["chat"]["type"] == "private":
        bot.sendMessage(msg['chat']['id'], text, "Markdown", True, False, False)
    else:
        bot.sendMessage(msg['chat']['id'], text, "Markdown", True, False, msg["message_id"])
    return
