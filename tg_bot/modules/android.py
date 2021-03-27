# Feel free to use it, but don't forget to mention credits
# By DAvinash97
from requests import get
from typing import List
from telegram import Bot, Update, ParseMode
from telegram.ext import Updater, CommandHandler
from telegram.ext import run_async
from tg_bot import dispatcher

@run_async
def magisk(bot, update):
    msg = update.effective_message
    magisk = {
        "<b>Stable</b>\n": "master/stable",
        "<b>Beta</b>\n": "master/beta"
            }.items()
    link = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    output = "<a href='https://topjohnwu.github.io/Magisk/install.html'><b>Guide for New Magisk</b></a>\n"
    output += "<a href='https://topjohnwu.github.io/Magisk/install.html#custom-recovery'>How to Install New Magisk?</a> \n"
    output += "\n<b><u>Latest Magisk Releases:</u></b>\n"
    for types, jsons in magisk:
        json_links = get(link + jsons + ".json").json()
        output += f"\n{types}" \
        f"<i>App: <a href='{json_links.get('magisk').get('link')}'>{json_links.get('magisk').get('version')}</a></i> \n" \
        f"<i>Uninstaller: <a href='{json_links.get('uninstaller').get('link')}'> Zip v{json_links.get('magisk').get('version')}</a></i> \n"
    
    msg.reply_text(text=output,
                   parse_mode=ParseMode.HTML,
                   disable_web_page_preview=True)

@run_async
def ofox(bot, update, args: List[str]):
    msg = update.effective_message
    link = 'https://api.orangefox.download/v2/device/{}/releases/'
    query = " ".join(args)
    if not query:
        msg.reply_text("Which Device You mean?")
        return
    else:
        mainlink = link.format(query)
        getlink = get(mainlink).json()
        output = f"\n<u><b>Ofox recovery for {query.upper()}</b></u>:\n\n"
        dllink = 'https://dl.orangefox.download/'
        stable = getlink.get('stable')
        for downid in stable:
            version = downid.get('version')
            downlinks = dllink + downid.get('_id')
            date = downid.get('date')
            output += f"{date}\n"
            output += f"Version : <i><a href='{downlinks}'>{version}</a></i>\n\n"
        msg.reply_text(text=output,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True)

def listofox(bot, update):
    msg = update.effective_message
    link = 'https://api.orangefox.download/v2/device'
    getlink = get(link).json()
    output = "<b>Ofox is currently available for these devices:</b>\n"
    for devices in getlink:
        codename = devices.get('codename')
        output += f"{codename}\n"
    bot.send_message(chat_id=update.effective_chat.id,
                text=output,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True)
    
__help__ = """
*Available commands:*\n
*Magisk:* 
• `/magisk`, `/su`, `/root`: fetches latest magisk
*Ofox:*
• `/ofox`, `/fox`, `/orangefox`: fetches latest stable ofox if available for your device.
• `/ofoxdevices` to check if your devices has ofox officially.
"""
magisk_handler = CommandHandler(['magisk', 'root', 'su'], magisk)
ofox_handler = CommandHandler(['ofox', 'fox', 'orangefox'], ofox, pass_args=True)
ofoxlist_handler = CommandHandler('ofoxdevices', listofox)

dispatcher.add_handler(magisk_handler)
dispatcher.add_handler(ofox_handler)
dispatcher.add_handler(ofoxlist_handler)

__mod_name__ = "Android"
__command_list__ = ["magisk", "root", "su", "ofox", "fox", "orangefox", "listdevices"]
__handlers__ = [
    magisk_handler, ofox_handler, ofoxlist_handler
]
