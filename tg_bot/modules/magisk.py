# Inspired from RaphaelGang's android.py
# By DAvinash97
from requests import get
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler
from telegram.ext import run_async
from tg_bot import dispatcher

@run_async
def magisk(bot: Bot, update: Update):
    msg = update.effective_message
    link = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    magisk_dict = {
            "*Stable*": "master/stable.json", "\n"
            "*Beta*": "master/beta.json",
        }.items()
    releases = '*Latest Magisk Releases:*\n\n'
    for magisk_type, release_url in magisk_dict:
        data = get(link + release_url).json()
        releases += f'{magisk_type}:\n' \
                f'》 *Manager* - [App v{data["app"]["version"]}]({data["app"]["link"]}) \n' \
                f'》 *Uninstaller* - [Uninstaller v{data["magisk"]["version"]}]({data["uninstaller"]["link"]}) \n'
    msg.reply_text(text=releases,
                   parse_mode=ParseMode.MARKDOWN,
                   disable_web_page_preview=True)

__help__ = """
*Available commands:*\n
*Magisk:* 
• `/magisk`, `/su`, `/root`: fetches latest magisk
"""
magisk_handler = CommandHandler(['magisk', 'root', 'su'], magisk)

dispatcher.add_handler(magisk_handler)

__mod_name__ = "Android"
__command_list__ = ["magisk", "root", "su"]
__handlers__ = [
    magisk_handler,
]
