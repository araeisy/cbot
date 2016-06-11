from __main__ import *
from utils import *
from message import Message
from langs import *
patterns = [
r'^[#/!][Ss][Tt][Aa][Rr][Tt]$',
r'^!!start (.*)$',
]
name = "start"
cron = None
def run(msg, matches):
    chat_id = msg['chat']['id']
    langs = ['English', "فارسی"]
    if "!!" in msg['text']:
        if matches[0] in langs:
            db.hset("users:"+str(chat_id),"lang",matches[0])
            db.hdel("users:"+str(chat_id),"step")
            hide_keyboard = {'hide_keyboard': True}
            send_msg(Message(chat_id).set_text(lang[get_user_lang(chat_id)]["select_lang"].format(matches[0]),
                    reply_markup = hide_keyboard))
        else:
            send_msg(Message(chat_id).set_text(lang[get_user_lang(chat_id)]["wrong"]))
    else:
        keyboard = {'keyboard': [langs]}
        send_msg(Message(chat_id).set_text(lang[get_user_lang(chat_id)]["start"], reply_markup=keyboard))
        db.hset("users:"+str(chat_id),"step","start")
