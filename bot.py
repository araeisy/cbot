from utils import *


plugins = []


def load_bot():
    #print bot info
    print(bot.getMe())
    #load_plugins
    for x in os.listdir('parts'):
        if(x.endswith('.py') and not 'init' in x):
            module_name = 'parts' + '.' + x.split('.')[0]
            plugins.append(importlib.import_module(module_name))
            print(colored("Plugin " + x.split('.')[0]+ " loaded","red"))


@asyncio.coroutine
def download(file_id, path):
    yield from bot.download_file(file_id, path)
    return path

def cron_job():#cron job function
    while True:
        print("cron job")
        time.sleep(5)





cron = threading.Thread(target = cron_job)#cron job
cron.start()#start the cron
load_bot()#Load bot
@asyncio.coroutine
def msg_processor(msg):
    if "data" in msg:
        msg["chat"] = {}
        msg["chat"]["type"] = "callback"
        msg["text"] = "!!callback " + msg["data"]
        if "message" in msg:
            msg["chat"]["id"] = msg["message"]["chat"]["id"]
            msg["message_id"] = msg["message"]["message_id"]
    if "query" in msg:
        msg["chat"] = {}
        msg["chat"]["type"] = "inline"
        msg["text"] = "!!inline " + msg["query"]
    print(msg)
    if "text" in msg:
        for plugin in plugins:
            for k in plugin.patterns:
                if re.match(k, msg["text"]):
                    print(colored("Trigerred", "red"))
                    matches = list(re.match(k, msg["text"]).groups())
                    res = threading.Thread(target = plugin.run, args=(msg, matches,))
                    res.start()


bot = telepot.async.Bot(config.TOKEN)
answerer = telepot.async.helper.Answerer(bot)
loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': msg_processor,'callback_query': msg_processor,'inline_query': msg_processor,}))
print('Bot Started')
loop.run_forever()
