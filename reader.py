from apscheduler.schedulers.blocking import BlockingScheduler as scheduler
import feedparser
from html2image import Html2Image
import telebot
from telebot import types
import urllib.parse
import pandas as pd

import os
import glob
from dotenv import load_dotenv
load_dotenv()

# create schedule loop
def timerFunction():
    # clear image folder
    files = glob.glob('img/*')
    for f in files:
        os.remove(f)

    # get token from .env
    token = os.environ.get("token")

    # You can set parse_mode by default. HTML or MARKDOWN
    bot = telebot.TeleBot(token, parse_mode="HTML")

    # html to image object
    hti = Html2Image()
    hti.output_path = 'img'

    # out chat id
    chat_id = -469613389

    # rss link
    feed = feedparser.parse("https://cointelegraph.com/rss")

    # load json
    try:
        lastItem = pd.read_json('json/lastItem.json')
        lastItemId = lastItem['id'].iloc[0]
        pubTime = lastItem['pubDate'].iloc[0]
        firstRun = 0
    except:
        lastItemId = None
        pubTime = "Thu, 14 Oct 2021 01:01:01 +0100"
        firstRun = 1


    # create a dataframe to add rss items
    item_df = pd.DataFrame(columns=['id', 'pubDate', 'description', 'image'])

    # start item loop
    for entry in feed.entries:
        # get necessary data
        if 'media_content' in entry:
            mediaContent = entry.media_content[0]['url']
        title = entry.title
        pubDate = entry.published
        id = entry.id


        # skip if exsisting post or previous post
        if((lastItemId==id) | (pd.to_datetime(pubDate)<=pd.to_datetime(pubTime))):
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

        # get the html and save as image
        instant_url = 'https://ceyloncash.com/instants/?text='+urllib.parse.quote_plus(description)+'&imgurl='+mediaContent
        hti.screenshot(url=(instant_url), save_as=file_name,size=(1080, 1080))

        # send image to the chat
        photo = open('img\\'+file_name, 'rb')
        markup = types.InlineKeyboardMarkup(row_width=2)
        itembtn1 = types.InlineKeyboardButton('Broadcast', callback_data='/send')
        itembtn2 = types.InlineKeyboardButton('Ignore', callback_data='/ignore')
        itembtn3 = types.InlineKeyboardButton('Read More..', url=id)

        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_photo(chat_id,photo, caption=description+" | "+mediaContent, reply_markup=markup)

        # If first run take only first item
        if(firstRun==1):
            break

    # save last item
    item_df = item_df.head(1)
    item_df.to_json('json/lastItem.json')


# Execute your code before starting the scheduler
print('Starting scheduler, ctrl-c to exit!')

# create and run the scheduler object
sch = scheduler()
sch.add_job(timerFunction, 'interval', seconds=60)
sch.start()