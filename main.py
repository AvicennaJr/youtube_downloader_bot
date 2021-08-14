from pyrogram import Client, filters, emoji
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 


def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'B'


app = Client("my_bot", bot_token="") #insert bot token

@app.on_message(filters.command(commands = ['start', 'help', 's'], prefixes = ['/','!'], case_sensitive = False))
def help_message(client, message):
    message.reply_text(text = "Use ```!youtube``` or ```!y``` followed by the youtube link. Then select the resolution.\n\nEg: ```!y https://youtu.be/1O0yazhqaxs```\n\n```Unavailable``` means the video does not exist in that particular resolution.")


@app.on_message(filters.command(commands = ['youtube','y'], prefixes = ['!','/'], case_sensitive = False))
def advice_message(client, message):
    l = message.text.split()
    global stream720
    global stream480
    global stream360
    global stream240
    global stream144
    global yt

    try:
        yt = YouTube(l[1])
        stream720 = yt.streams.get_by_resolution(resolution = '720p')
        stream480 = yt.streams.get_by_resolution(resolution = '480p')
        stream360 = yt.streams.get_by_resolution(resolution ='360p')
        stream240 = yt.streams.get_by_resolution(resolution = '240p')
        stream144 = yt.streams.get_by_resolution(resolution = '144p')
        
        if stream720 != None:
            video_size720 = f"{int(format_bytes(stream720.filesize)[0]):.2f}{format_bytes(stream720.filesize)[1]}"
        else:
            video_size720 = 'Unavailable'
        if stream480 != None:
            video_size480 = f"{int(format_bytes(stream480.filesize)[0]):.2f}{format_bytes(stream480.filesize)[1]}"
        else:
            video_size480 = 'Unavailable'
        if stream360 != None:
            video_size360 = f"{int(format_bytes(stream360.filesize)[0]):.2f}{format_bytes(stream360.filesize)[1]}"
        else:
            video_size360 = 'Unavailable'
        if stream240 != None:
            video_size240 = f"{int(format_bytes(stream240.filesize)[0]):.2f}{format_bytes(stream240.filesize)[1]}"
        else:
            video_size240 = 'Unavailable'
        if stream144 != None:
            video_size144 = f"{int(format_bytes(stream144.filesize)[0]):.2f}{format_bytes(stream144.filesize)[1]}"
        else:
            video_size144 = 'Unavailable'


    
        message.reply_text(text = f'''Title {emoji.FILM_FRAMES}: ```{yt.title}```
                           \nLength {emoji.TIMER_CLOCK}: ```{convert(yt.length)}```
                           \nSize 720p {emoji.OPEN_FILE_FOLDER}: ```{video_size720}```
                           \nSize 480p {emoji.OPEN_FILE_FOLDER}: ```{video_size480}```
                           \nSize 360p {emoji.OPEN_FILE_FOLDER}: ```{video_size360}```
                           \nSize 240p {emoji.OPEN_FILE_FOLDER}: ```{video_size240}```
                           \nSize 144p {emoji.OPEN_FILE_FOLDER}: ```{video_size144}```''',
                           reply_markup = InlineKeyboardMarkup(
            [
                [ 
                    InlineKeyboardButton(  
                        "720p",
                        callback_data = "720p"
                    ),
                    InlineKeyboardButton(  
                        "480p",
                        callback_data = "480p"
                    ),
                    InlineKeyboardButton(  
                        "360p",
                        callback_data = "360p"
                    )],
                    [
                        InlineKeyboardButton(  
                        "240p",
                        callback_data = "240p"
                    ),
                        InlineKeyboardButton(  
                        "144p",
                        callback_data = "144p"
                    )]]))
    except:
        message.reply_text(text = "Invalid URL")

@app.on_callback_query()
def send_the_video(client, callback_query):
    if callback_query.data == '720p':
        try:
            app.send_document(chat_id = callback_query.message.chat.id, document = stream720.download())
            callback_query.answer("Downloading..", cache_time = 3)
        except:
            callback_query.answer("Failed :(", cache_time = 3)
            app.send_message(chat_id = callback_query.message.chat.id, text = 'Unavailable')
    elif callback_query.data == '480p':
        try:
            app.send_document(chat_id = callback_query.message.chat.id, document = stream480.download())
            callback_query.answer("Downloading..", cache_time = 3)
        except:
            callback_query.answer("Failed :(", cache_time = 3)
            app.send_message(chat_id = callback_query.message.chat.id, text = 'Unavailable')
    elif callback_query.data == '360p':
        try:
            app.send_document(chat_id = callback_query.message.chat.id, document = stream360.download())
            callback_query.answer("Downloading..", cache_time = 3)
        except:
            callback_query.answer("Failed :(", cache_time = 3)
            app.send_message(chat_id = callback_query.message.chat.id, text = 'Unavailable')
    elif callback_query.data == '240p':
        try:
            app.send_document(chat_id = callback_query.message.chat.id, document = stream240.download())
            callback_query.answer("Downloading..", cache_time = 3)
        except:
            callback_query.answer("Failed :(", cache_time = 3)
            app.send_message(chat_id = callback_query.message.chat.id, text = 'Unavailable')
    elif callback_query.data == '144p':
        try:
            app.send_document(chat_id = callback_query.message.chat.id, document = stream144.download())
            callback_query.answer("Downloading..", cache_time = 3)
        except:
            callback_query.answer("Failed :(", cache_time = 3)
            app.send_message(chat_id = callback_query.message.chat.id, text = 'Unavailable')

app.run()
