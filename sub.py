import telebot
import datetime
import requests
import splitter
import os
from os.path import exists

TOKEN=os.environ("TOKEN")
bot = telebot.TeleBot(TOKEN)

def splitfn(name,capt,message):
    capt = capt.split(",")
    splitsub = splitter.subtitles(f"./{name}")
    splitsub.split(split_time=datetime.time(int(capt[0]),int(capt[1]),int(capt[2])),split_file_1=f"PART1-{name}",split_file_2=f"PART2-{name}")
    doc = open(f'./PART1-{name}', 'rb')
    bot.send_document(message.chat.id, doc)
    doc = open(f'./PART2-{name}', 'rb')
    bot.send_document(message.chat.id, doc)
    os.remove(f"./{name}")
    os.remove(f"./PART1-{name}")
    os.remove(f"./PART2-{name}")

@bot.message_handler(commands=['start'])
def handle_welcome(message):
    bot.send_message(message.chat.id,"Welcome\nFirst you have to send me a .srt File and then reply to the File with Split Time (format: hh,mm,ss)\nExample: 1,44,50")

@bot.message_handler(content_types=['text'])
def handle_documnet(message):
    try:
        name = message.reply_to_message.document.file_name
        file_exists = exists(f"./{name}")
        if file_exists:
            pass
        else:
            id = message.reply_to_message.document.file_id
            file_info = bot.get_file(id)
            file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
            with open(name,"wb") as sub:
                sub.write(file.content)
    except:
        pass   

    try:
        name = message.reply_to_message.document.file_name
        capt = message.text
        splitfn(name,capt,message)
    except:
        bot.send_message(message.chat.id,"First you have to send me a .srt File and then reply to the File with Split Time (format: hh,mm,ss)")

@bot.message_handler(content_types=['document'])
def handle_documnet(message):
    name = message.document.file_name
    if ".srt" in name:
        id = message.document.file_id
        file_info = bot.get_file(id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path))
        with open(name,"wb") as sub:
            sub.write(file.content)
        try:
            capt = message.caption
            splitfn(name,capt,message)
        except:
            bot.send_message(message.chat.id,"Good, Now reply to the File with Split Time (format: hh,mm,ss)")   
    else:
        bot.send_message(message.chat.id,"File type not Supported")
        

bot.polling(none_stop=True, timeout=123)            