from covid import Covid
from typing import List
from telegram import ParseMode, Update, Bot, Message, Chat
from telegram.ext import run_async
from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler

def covid_19(bot, update, args: List[str]):
    msg = update.effective_message
    covid = Covid(source="worldometers")
    query = " ".join(args)
    if not query:
        msg.reply_text("Which Country You mean?")
        return
    else:
        data = covid.get_status_by_country_name(query)
        if data:
            covid_data  = f"*Corona Virus Info  :*\n\n"
            covid_data += f"*Country*           : `{data['country']}`\n"
            covid_data += f"*Confirmed*         : `{data['confirmed']}`\n"
            covid_data += f"*Death*             : `{data['deaths']}`\n"
            covid_data += f"*Active*            : `{data['active']}`\n"
            covid_data += f"*Recovered*         : `{data['recovered']}`\n"
            covid_data += f"*Critical Stage*    : `{data['critical']}`\n\n"
            covid_data += f"*New Cases*         : `{data['new_cases']}`\n"
            covid_data += f"*New Deaths*        : `{data['new_deaths']}`\n\n"
            covid_data += f"*Total Population*  : `{data['population']}`\n\n"
            covid_data += f"Data Provided by [Worldometers](https://www.worldometers.info/coronavirus)"
            msg.reply_text(covid_data,
                           parse_mode=ParseMode.MARKDOWN,
                           disable_web_page_preview=True)
        else:
            msg.reply_text("Invalid Country, Try /covid pakistan")

__help__ = """
Need Covid-19 status? Try available commands below.

*Available Commands:*
-/covid <country name>: To get your country's covid-19 status
"""

__mod_name__ = "Covid"

COVID_HANDLER = DisableAbleCommandHandler("covid", covid_19, pass_args=True)
dispatcher.add_handler(COVID_HANDLER)
