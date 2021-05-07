# Common imports for eval
import os, io, traceback, textwrap
from contextlib import redirect_stdout
from tg_bot import LOGGER, dispatcher
from tg_bot.modules.helper_funcs.chat_status import is_user_ban_protected
from telegram import ParseMode, Update, Bot
from telegram.ext import CommandHandler, run_async
from tg_bot.modules.helper_funcs.filters import CustomFilters
from subprocess import Popen, PIPE
from tg_bot.modules.helper_funcs.misc import sendMessage

namespaces = {}

def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            '__builtins__': globals()['__builtins__'],
            'bot': bot,
            'effective_message': update.effective_message,
            'effective_user': update.effective_user,
            'effective_chat': update.effective_chat,
            'update': update
        }

    return namespaces[chat]

def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(
        f"IN: {update.effective_message.text} (user={user}, chat={chat})")

def send(msg, bot, update):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            bot.send_document(
                chat_id=update.effective_chat.id, document=out_file)
    else:
        LOGGER.info(f"OUT: '{msg}'")
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{msg}",
            parse_mode=ParseMode.MARKDOWN)

def shell(command):
    process = Popen(command,stdout=PIPE,shell=True,stderr=PIPE)
    stdout,stderr = process.communicate()
    return (stdout,stderr)

@run_async
def evaluate(bot: Bot, update: Update):
    send(do(eval, bot, update), bot, update)

@run_async
def execute(bot: Bot, update: Update):
    send(do(exec, bot, update), bot, update)

def cleanup_code(code):
    if code.startswith('```') and code.endswith('```'):
        return '\n'.join(code.split('\n')[1:-1])
    return code.strip('` \n')

def do(func, bot, update):
    log_input(update)
    content = update.message.text.split(' ', 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

    os.chdir(os.getcwd())
    with open(
            os.path.join(os.getcwd(),
                         'tg_bot/modules/helper_funcs/temp.txt'),
            'w') as temp:
        temp.write(body)

    stdout = io.StringIO()

    to_compile = f'def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return f'{e.__class__.__name__}: {e}'

    func = env['func']

    try:
        with redirect_stdout(stdout):
            func_return = func()
    except Exception as e:
        value = stdout.getvalue()
        return f'{value}{traceback.format_exc()}'
    else:
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = f'{value}'
            else:
                try:
                    result = f'{repr(eval(body, env))}'
                except:
                    pass
        else:
            result = f'{value}{func_return}'
        if result:
            return result

@run_async
def shellExecute(bot: Bot, update: Update):
    cmd = update.message.text.split(' ',maxsplit=1)
    if len(cmd) == 1:
        sendMessage("No command provided!", bot, update)
        return
    LOGGER.info(cmd)
    output = shell(cmd[1])
    if output[1].decode():
        LOGGER.error(f"Shell: {output[1].decode()}")
    if len(output[0].decode()) > 4000:
        with open("shell.txt",'w') as f:
            f.write(f"Output\n-----------\n{output[0].decode()}\n")
            if output[1]:
                f.write(f"STDError\n-----------\n{output[1].decode()}\n")
        with open("shell.txt",'rb') as f:
            bot.send_document(document=f, filename=f.name,
                                  reply_to_message_id=update.message.message_id,
                                  chat_id=update.message.chat_id)  
    else:
        if output[1].decode():
            sendMessage(f"<code>{output[1].decode()}</code>", bot, update)
            return
        else:
            sendMessage(f"<code>{output[0].decode()}</code>", bot, update)

@run_async
def clear(bot: Bot, update: Update):
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)

EVAL_HANDLER = CommandHandler(('e', 'ev', 'eva', 'eval'), evaluate, filters=CustomFilters.sudo_filter)
EXEC_HANDLER = CommandHandler(('x', 'ex', 'exe', 'exec', 'py'), execute, filters=CustomFilters.sudo_filter)
CLEAR_HANDLER = CommandHandler(('clearlocals'), clear, filters=CustomFilters.sudo_filter)
SHELL_HANDLER = CommandHandler(('sh','shell'), shellExecute, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(EVAL_HANDLER)
dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(CLEAR_HANDLER)
dispatcher.add_handler(SHELL_HANDLER)
