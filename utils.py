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
    bot.sendMessage(message['chat']['id'], "Hello there!")

def is_sudo(user_id):
    return user_id in config.sudo_users

def is_premium(user_id):
    return user_id in config.premium_users

def download(file_id, path):
    bot.download_file(file_id, path)
    return path

def get_user_lang(chat_id):
    l = db.hget("users:"+str(chat_id),"lang")
    return l if l else "English"


def send_msg(message):
    if message.content_type == "text":
        r = bot.sendMessage(message.chat_id,message.text, parse_mode=message.parse_mode, disable_web_page_preview=message.disable_web_page_preview, disable_notification=message.disable_notification, reply_to_message_id=message.reply_to_message_id, reply_markup=message.reply_markup)
    elif message.content_type == "video":
        bot.sendChatAction(message.chat_id, 'upload_video')
        r = bot.sendVideo(message.chat_id, message.video, duration=message.duration, width=message.width, height=message.height, caption=message.caption, disable_notification=message.disable_notification, reply_to_message_id=message.reply_to_message_id, reply_markup=message.reply_markup)
    elif message.content_type == "document":
        bot.sendChatAction(message.chat_id, 'upload_document')
        r = bot.sendDocument(message.chat_id, message.file, caption=message.caption, disable_notification=message.disable_notification, reply_to_message_id=message.reply_to_message_id, reply_markup=message.reply_markup)
    elif message.content_type == "photo":
        bot.sendChatAction(message.chat_id, 'upload_photo')
        r = bot.sendPhoto(message.chat_id, message.photo, caption=message.caption, disable_notification=message.disable_notification, reply_to_message_id=message.reply_to_message_id, reply_markup=message.reply_markup)
    elif message.content_type == "audio":
        bot.sendChatAction(message.chat_id, 'upload_audio')
        r = bot.sendAudio(message.chat_id, message.audio, duration=message.duration, performer=message.performer, title=message.title, disable_notification=message.disable_notification, reply_to_message_id=message.reply_to_message_id, reply_markup=message.reply_markup)
    elif message.content_type == "callback_query":
        r = bot.answerCallbackQuery(message.callback_query_id, text=message.text, show_alert=message.show_alert)
    elif message.content_type == "edit_message":
        r = bot.editMessageText(message.msg_identifier, message.text, parse_mode=message.parse_mode, disable_web_page_preview=message.disable_web_page_preview, reply_markup=message.reply_markup)
    return r
