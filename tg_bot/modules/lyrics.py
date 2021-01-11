from tswift import Song
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
from tg_bot import dispatcher
from typing import List
from telegram.ext.dispatcher import run_async

@run_async
def lyrics(bot, update, args):
    lyric_for = " ".join(args)
    msg = update.effective_message
    song_lyric = Song.find_song
    if not lyric_for:
        msg.reply_text("Provide some argument with command")
        return
    else:
        result = song_lyric(lyric_for)
        if result == None:
            msg.reply_text("Sorry! Couldn't found Lyrics, try with Artist name May be?")
        else:
            msg.reply_text(result.format())

__help__ = """
*Available commands:*\n
*Magisk:* 
• `/lyrics`: fetches Song Lyrics for you
try /lyrics {song name}
"""
lyrics_handler = CommandHandler('lyrics', lyrics, pass_args=True)

dispatcher.add_handler(lyrics_handler)

__mod_name__ = "Lyrics"
__command_list__ = ["lyrics"]
__handlers__ = [lyrics_handler]
