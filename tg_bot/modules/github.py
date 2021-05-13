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
        data = get(link).json()
        nope = 'Not Found'
        if data.get('message') == nope:
            msg.reply_text(text=f"Umm... Sorry `{query}` {nope}", parse_mode=ParseMode.MARKDOWN)
            return
        else:
            message = f"<b>Fetched data for</b> <code>{args}</code>:\n\n"
            message += f"<b><u>{data.get('name')}: {data.get('tag_name')}</u></b>\n\n"
            message += "\t<b>Downloads:</b>\n\n"
            for assets in data.get('assets'):
                assetname = assets.get('name')
                extension = assetname[-3:]
                assetlink = assets.get('browser_download_url')
                assetdown = assets.get('download_count')
                assetsize = assets.get('size')
                uploaddate = assets.get('created_at')
                dateformat = uploaddate[:-10]
                downinmb = "{0:.2f}".format(assetsize/1048576)
                message += f"\t\t<b>Name:</b><a href='{assetlink}'>{assetname}</a>\n"
                message += f"\t\t<b>Created On:</b> {dateformat}\n"
                message += f"\t\t<b>Link:</b> <a href='{assetlink}'>{extension.upper()}\n"
                message += f"\t\t<b>Count</b>: {assetdown}\n"
                message += f"\t\t<b>Size</b>: {downinmb}MB\n\n"
        msg.reply_text(text=message,
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
