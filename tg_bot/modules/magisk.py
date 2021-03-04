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
    magisk = {
        "<b>Stable</b>\n": "master/stable.json",
        "<b>Beta</b>\n": "master/beta.json",
            }.items()
    link = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    output = "<a href='https://topjohnwu.github.io/Magisk/install.html'><b>Guide for New Magisk</b></a>\n"
    output += "<a href='https://topjohnwu.github.io/Magisk/install.html#custom-recovery'>How to Install New Magisk?</a> \n"
    output += "\n<b><u>Latest Magisk Releases:</u></b>\n"
    for types, jsons in magisk:
        json_links = get(link + jsons).json()
        output += f"\n{types}" \
        f"<i>App: <a href='{json_links.get('magisk').get('link')}'>{json_links.get('magisk').get('version')}</a></i> \n" \
        f"<i>Uninstaller: <a href='{json_links.get('uninstaller').get('link')}'> Zip v{json_links.get('magisk').get('version')}</a></i> \n"
    
    msg.reply_text(text=output,
                   parse_mode=ParseMode.HTML,
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
