from base64 import encodestring
import feedparser
import webbrowser
from html2image import Html2Image
import telebot
from telebot import types
import urllib
from dotenv import load_dotenv
load_dotenv()
import os
token = os.environ.get("token")

bot = telebot.TeleBot(token, parse_mode="HTML") # You can set parse_mode by default. HTML or MARKDOWN

hti = Html2Image()
hti.output_path = 'img'
chat_id = -469613389
feed = feedparser.parse("https://cointelegraph.com/rss")

# feed_title = feed['feed']['title']  # NOT VALID
feed_entries = feed.entries

for entry in feed.entries:
    if 'media_content' in entry:
        mediaContent = entry.media_content[0]['url']
    title = entry.title
    hashtag = "#"+entry.category.replace(" ","")
    slug =entry.guid.rsplit('/', 1)[1]
    file_name = slug+'.png'
    description = title+" "+hashtag
    print(description)
    print(mediaContent)
    print(file_name)
    print(hashtag)
    print("################")
    
    instant_url = 'https://ceyloncash.com/instants/?text='+description+'&imgurl='+mediaContent
    hti.screenshot(url=(instant_url), save_as=file_name,size=(1080, 1080))

    photo = open('img\\'+file_name, 'rb')
    markup = types.InlineKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton('Broadcast',callback_data='/send')
    itembtn2 = types.InlineKeyboardButton('Ignore',callback_data='/ignore')
    markup.add(itembtn1, itembtn2)
    bot.send_photo(chat_id,photo, caption=description+"", reply_markup=markup)
    break
    # bot.send_photo(chat_id, photo)
    # bot.send_message(chat_id,description)