import os
import requests
from telebot import types 
import telebot
from bs4 import BeautifulSoup

##################
bot = telebot.TeleBot("7129861515:AAHT9vapWKogsluyC4jgIG2MifgTL7oj3jE")
##################

#########(Keyboard)#########
VIP = types.InlineKeyboardButton(text = "- VIP CODER .", url="t.me/altaee_z")    
dev = types.InlineKeyboardButton(text ="- By .", url="t.me/my00002")
keybo = types.InlineKeyboardMarkup()
keybo.row_width = 2
keybo.add(VIP,dev)
#########(Startbot)#########
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f"🤖 مرحبا, [{message.from_user.first_name}](tg://user?id={message.from_user.id}).\n- ارسل رابط تحميل الخاص بك.\n- ",parse_mode ="Markdown")
#########(check)#########
def get_mediafire_download_link(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        download_link = soup.find('a', {'id': 'downloadButton'})['href']
        return download_link
    except Exception as e:
        print(f"An Error : {e}")
        return None
#########(downlaod)#########
@bot.message_handler(func=lambda message: True)
def download_mediafire(message):
    text = message.text
    if text.startswith('http://www.mediafire.com/') or text.startswith('https://www.mediafire.com/'):
        ims=bot.reply_to(message, "Uploading...")
        file_url = text
        direct_download_link = get_mediafire_download_link(file_url)

        if direct_download_link:
            file_response = requests.get(direct_download_link, stream=True, timeout=60)
            file_name = direct_download_link.split('/')[-1]
            file_size = int(file_response.headers['Content-Length'])

            if file_size <= 50 * 1024 * 1024:
                bot.send_chat_action(message.chat.id, 'upload_document')
                bot.delete_message(chat_id=message.chat.id,message_id=ims.message_id)

                with open(file_name, 'wb') as file:
                    file.write(file_response.content)

                with open(file_name, 'rb') as file:
                    bot.send_document(message.chat.id, file, caption=f"Done ✓\nName file : {file_name} .",reply_markup = keybo)

                os.remove(file_name)
            else:
                bot.reply_to(message, "File size > 50mb.")
        else:
            bot.reply_to(message, "Error in Get download link.")
    else:
        bot.reply_to(message, "Please send avaliable link ✓")
print("تم✅")
bot.polling()
#@IBatMaan
#VIP CODER | @findaIl
