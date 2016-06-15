from __main__ import *
from utils import *
from message import Message
from langs import *
patterns = [
r'^!!callback /newfolder$',
r'^!!newfolder (.*)$'
]
name = "start"
cron = None
def run(msg, matches):
    user_id = msg["from"]["id"]
    if "!!callback /newfolder" == msg['text']:
        send_msg(Message(user_id).set_text(lang[get_user_lang(user_id)]["enter_folder_name"]))
        db.hset("users:"+str(user_id), "step", "newfolder")
    else:
        wd = db.hget("users:" +str(user_id), "working_directory")
        db.hdel("users:"+str(user_id), "step")
        add_folder(msg, matches[0], wd)
        send_msg(Message(user_id).set_text(lang[get_user_lang(user_id)]["folder_created"]))
