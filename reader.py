from base64 import encodestring
import feedparser
import webbrowser
from html2image import Html2Image
import telebot
from telebot import types
import urllib.parse
import pandas as pd

import os
import glob
from dotenv import load_dotenv
load_dotenv()

# clear image folder
files = glob.glob('img/*')
for f in files:
    os.remove(f)

token = os.environ.get("token")

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(token, parse_mode="HTML")

hti = Html2Image()
hti.output_path = 'img'
chat_id = -469613389
feed = feedparser.parse("https://cointelegraph.com/rss")

# load json
try:
    lastItem = pd.read_json('json/lastItem.json')
    lastItemId = lastItem['id'].iloc[0]
    firstRun = 0
except:
    lastItemId = None
    firstRun = 1

item_df = pd.DataFrame(columns=['id', 'pubDate', 'description', 'image'])

for entry in feed.entries:
    if 'media_content' in entry:
        mediaContent = entry.media_content[0]['url']
    title = entry.title
    pubDate = entry.published
    id = entry.id

    # skip if exsisting post
    if(lastItemId==id):
        # if no new post get previous df
        if(item_df.shape[0]==0):
            item_df = lastItem.copy()
        break

    try:
        hashtag = "#"+entry.category.replace(" ","")
    except:
        hashtag = ""

    slug =entry.guid.rsplit('/', 1)[1]
    file_name = slug+'.png'
    description = title+" "+hashtag

    print(file_name)
    print(hashtag)
    print("################")

    row = {'id': id, 'pubDate': pubDate, 'description': description, 'image': mediaContent}
    item_df = item_df.append(row, ignore_index=True)

    instant_url = 'https://ceyloncash.com/instants/?text='+urllib.parse.quote_plus(description)+'&imgurl='+mediaContent
    hti.screenshot(url=(instant_url), save_as=file_name,size=(1080, 1080))

    photo = open('img\\'+file_name, 'rb')
    markup = types.InlineKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton('Broadcast',callback_data='/send')
    itembtn2 = types.InlineKeyboardButton('Ignore',callback_data='/ignore')
    markup.add(itembtn1, itembtn2)
    bot.send_photo(chat_id,photo, caption=description+" | "+mediaContent+" | "+id, reply_markup=markup)

    # If first run take only first item
    if(firstRun==1):
        break

    # bot.send_photo(chat_id, photo)
    # bot.send_message(chat_id,description)

item_df['pubDate'] = pd.to_datetime(item_df['pubDate'])
item_df = item_df.head(1)
item_df.to_json('json/lastItem.json')