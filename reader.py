import feedparser
import webbrowser
from html2image import Html2Image
hti = Html2Image()

feed = feedparser.parse("https://cointelegraph.com/rss")

# feed_title = feed['feed']['title']  # NOT VALID
feed_entries = feed.entries

for entry in feed.entries:
    if 'media_content' in entry:
        mediaContent = entry.media_content[0]['url']
    title = entry.title
    hashtag = "#"+entry.category.replace(" ","")
    slug =entry.guid.rsplit('/', 1)[1]
    print(title)
    print(mediaContent)
    print(slug)
    print(hashtag)
    instant_url = 'https://ceyloncash.com/instants/?text='+title+'&imgurl='+mediaContent
    hti.screenshot(url='file:///F:/Nisal/CryptoRoomInstants/cryptoroom-instants.html', save_as='img/'+slug+'.png',size=(1080, 1080))
