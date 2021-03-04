# Feel free to use it, but don't forget to mention credits
# Will add db later, Currently WIP
# By DAvinash97
from requests import get
from typing import List
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler
from telegram.ext import run_async
from tg_bot import dispatcher

API = "https://api.github.com/repos/{}/releases/latest"

@run_async
def github(bot, update, args: List[str]):
    query = " ".join(args)
    if not query:
        msg.reply_text("Try /git {owner}/{repo}")
        return
    else:
        link = API.format(query)
        get_link = get(link).json()
        asset = get_link.get('assets')
        name = get_link.get('name')
        authorname = get_link.get('author').get('login')
        output = f"<b><u>Author: {authorname.upper()}</u></b>\n"
        output += f"<b><u>{name}</u></b>\n\n"
        for downloads in asset:
            assetname = downloads.get('name')
            login = downloads.get('uploader').get('login')
            download_url = downloads.get('browser_download_url')
            output += f"<a href='{download_url}'>{assetname}</a>\n"
        msg.reply_text(chat_id=update.effective_chat.id,
                        text=output,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True)
                    
__help__ = """
*Available commands:*\n
*Github:* 
• `/git`: fetches latest releases.
"""
git_handler = CommandHandler('git', github, pass_args=True)

dispatcher.add_handler(git_handler)

__mod_name__ = "Github"
__command_list__ = ["git"]
__handlers__ = [git_handler]
