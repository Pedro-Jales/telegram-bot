import logging
import json
import datetime
import os
import socket

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import InlineQueryHandler

from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent

#---- Custom ----

import dev_tools

import keyboard_bot as inline
import trello_bot as trello

#---- Initial ----

if(os.environ.get('IS_HEROKU', None)):
    print("[Setup] - Roboto is on heroku.")

    token = os.environ.get('telegram_token', None)
    timer = int(os.environ.get('timer_dev', None))
    debug = os.environ.get('debug', None)

    user  = int(os.environ.get('telegram_user_id', None))
    bot_id = int(os.environ.get('telegram_bot_id', None))

    #----

    host = '0.0.0.0'
    port = int(os.environ.get('PORT', None))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host, port))
    except socket.error as e:
        print(str(e))

    s.listen(5)

    conn, addr = s.accept()

    print('connected to: ' + addr[0] + ':' + str(addr[1]))
    print("port:" + (os.environ.get('PORT', None)))
    
    #----

else:
    print("[Setup] - Roboto is on local machine.")
    with open("config_bot.json") as f:
        config = json.load(f)

    token = config['telegram_token']
    timer = config['timer_default']
    debug = config['debug']

    user  = config['telegram_user_id']
    bot_id = config['telegram_bot_id']

#---- Default ----

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#---- Custom Functions ----

def verify(id):
    if (id == user):
        return True

    return False

def board(update, context):
    if(verify(update.effective_chat.id)):
        boards = trello.bot.getAllBoards()
        response = 'All your boards:\n\n'

        for board in boards:
            response = response + board + '\n'

        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

#---- Default Functions -----

def start(update, context):
    if(verify(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def unknown(update, context):
    if(verify(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

#---- Example Functions ----

def echo(update, context):
    if(verify(update.effective_chat.id)):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
    if(verify(update.effective_chat.id)):
        text_caps = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def inline_caps(update, context):
    if(verify(update.effective_chat.id)):
        query = update.inline_query.query
        if not query:
            return
        results = list()
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title='Caps',
                input_message_content=InputTextMessageContent(query.upper())
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results)

#---- Handlers ----

# /start
dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
dispatcher.add_handler(CommandHandler('caps', caps))
dispatcher.add_handler(InlineQueryHandler(inline_caps))

dispatcher.add_handler(CommandHandler('board', board))

# unknow
dispatcher.add_handler(MessageHandler(Filters.command, unknown))

#---- Final Config ----
if(os.environ.get('IS_HEROKU', None)):
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(
        listen="0.0.0.0", 
        port=PORT, 
        url_path=token)
    updater.bot.set_webhook("https://roboto-jr.herokuapp.com/" + token)

else:
    updater.start_polling()

updater.idle()