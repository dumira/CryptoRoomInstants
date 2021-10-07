import feedparser
import webbrowser
from html2image import Html2Image
hti = Html2Image()
hti.output_path = 'img'

feed = feedparser.parse("https://cointelegraph.com/rss")

# feed_title = feed['feed']['title']  # NOT VALID
feed_entries = feed.entries

for entry in feed.entries:
    if 'media_content' in entry:
        mediaContent = entry.media_content[0]['url']
    title = entry.title
    hashtag = "#"+entry.category.replace(" ","")
    slug =entry.guid.rsplit('/', 1)[1]
    instant_url = 'https://ceyloncash.com/instants/?text='+title+'&imgurl='+mediaContent
    file_name = slug+'.png'

    print(title)
    print(mediaContent)
    print(file_name)
    print(hashtag)
    print("################")

    hti.screenshot(url=instant_url, save_as=file_name,size=(1080, 1080))
