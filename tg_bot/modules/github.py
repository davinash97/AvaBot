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
    msg = update.effective_message
    query = " ".join(args)
    if not query:
        msg.reply_text("Try /git {owner}/{repo}")
        return
    else:
        link = API.format(query)
        get_link = get(link).json()
        asset = get_link.get('assets')
        name = get_link.get('name')
        changelog = get_link.get('body')
        authorname = get_link.get('author').get('login')
        html_url = get_link.get('author').get('html_url')
        tag_name = get_link.get('tag_name')
        output = f"<b><u>Author</u> : <a href='{html_url}'> <u>{authorname.upper()}</u></a></b>\n\n"
        output += f"<b><u><a href='https://github.com/{query}'>{name} {tag_name}</a></u></b>\n\n"
        output += f"<b>Changelog :</b>\n<i>{changelog}</i>\n\n"
        for downloads in asset:
            assetname = downloads.get('name')
            login = downloads.get('uploader').get('login')
            download_url = downloads.get('browser_download_url')
            asset_size = (downloads.get('size')/1024)/1024
            calculation = f"{'{0:.2f}'.format(asset_size)}"
            download_count = downloads.get('download_count')
            created_at = downloads.get('created_at')
            output += f"<b>Name :</b> <a href='{download_url}'>{assetname}</a>\n"
            output += f"<b>Download Count: {download_count}</b>\n"
            output += f"<b>Size :</b> {calculation}MB\n"
            output += f"<b>Created at:</b> {created_at}\n\n"
        msg.reply_text(text=output,
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
