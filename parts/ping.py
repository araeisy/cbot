from __main__ import *
from utils import *
patterns = [
r'^[#/!][Pp][Ii][Nn][Gg]$',
]
name = "ping"
cron = None
def run(msg, matches):
    send_msg(msg, "Pong !")
