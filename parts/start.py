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
    #del_user(msg)
    user_id = msg['from']['id']
    if re.match(r"^[#/!][Ss][Tt][Aa][Rr][Tt]$", msg["text"]) and db.sismember("started_users", user_id):
        text = lang[get_user_lang(user_id)]["folder"].format(lang[get_user_lang(user_id)]["root_folder"])
        sub_folders = get_folders_text(str(user_id) + "_0")
        if sub_folders:
            text += "\n" + sub_folders + "\n\n"
        text += lang[get_user_lang(user_id)]["select_options"]
        k = InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text = lang[get_user_lang(user_id)]["new_folder"], callback_data = "/newfolder")],
                     ])
        send_msg(Message(user_id).set_text(text, reply_markup=k))
        return
    langs = ['English', "فارسی"]
    if "!!" in msg['text']:
        if matches[0] in langs:
            db.hset("users:"+str(user_id), "lang", matches[0])
            db.hdel("users:"+str(user_id), "step")
            hide_keyboard = {'hide_keyboard': True}
            send_msg(Message(user_id).set_text(lang[get_user_lang(user_id)]["select_lang"].format(matches[0]),
                    reply_markup = hide_keyboard))
            if not db.sismember("started_users", user_id):
                setup_user(msg)
            text = lang[get_user_lang(user_id)]["folder"].format(lang[get_user_lang(user_id)]["root_folder"])
            sub_folders = get_folders_text(str(user_id) + "_0")
            if sub_folders:
                text += "\n" + sub_folders + "\n\n"
            text += lang[get_user_lang(user_id)]["select_options"]
            k = InlineKeyboardMarkup(inline_keyboard=[
                             [InlineKeyboardButton(text = lang[get_user_lang(user_id)]["new_folder"], callback_data = "/newfolder")],
                         ])
            send_msg(Message(user_id).set_text(text, reply_markup=k))
        else:
            send_msg(Message(user_id).set_text(lang[get_user_lang(user_id)]["wrong"]))
    else:
        keyboard = {'keyboard': [langs]}
        send_msg(Message(user_id).set_text(lang[get_user_lang(user_id)]["start"], reply_markup=keyboard))
        db.hset("users:"+str(user_id), "step", "start")
