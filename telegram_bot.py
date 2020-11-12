import requests
import json
import datetime

import dev_tools

import keyboard_bot as inline
import trello_bot as trello

#All queries to the Telegram Bot API must be served over HTTPS and need to be presented in this form: 
# https://api.telegram.org/bot<token>/METHOD_NAME. 

# Like this for example:
#https://api.telegram.org/bot123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11/getMe

class RobotoJr_bot:
    def __init__(self):
        self.url_base = f'https://api.telegram.org/bot{token}/'
        self.inline = False

    #Turn bot online:
    def start(self):
        dev_tools.system("[Main] - Roboto is Online!\n")
        update_id = None

        while True:
            update = self.getMessages(update_id)
            messages = update['result']

            if messages:
                for message in messages:
                    dev_tools.system('[Telegram] - message receveid')
                    update_id = message['update_id']

                    # Check if the message is a callback
                    if('callback_query' in message and message['callback_query']['message']['from']['id'] == bot_id):
                        self.getCallback_query(message['callback_query']['data'])
                    
                    # Check if the message was sent by a verified user
                    elif(message['message']['from']['id'] != user):   
                        self.sentResponse("Access denied", message['message']['from']['id'])

                    # Process the message
                    else:
                        chat_id = message['message']['from']['id']
                        isFirstMessage = message['message']['message_id'] == 1 

                        # Create a response 
                        response = self.createResponse(message['message']['text'], isFirstMessage)

                        # Sent the response if there's a response
                        if(response != None):
                            self.sentResponse(response, chat_id)            
                            
                    #TODO: check wherever it should be
                    self.inline = False 
                        
                    dev_tools.system('[Telegram] - command processed\n')

    #Long polling
    def getMessages(self, update_id):
        source = f'{self.url_base}getUpdates?timeout={timer}'

        if update_id:
            source = f'{source}&offset={update_id + 1}'

        result = requests.get(source)
        return json.loads(result.content)

    #Create response
    def createResponse(self, message, isFirstMessage):
        dev_tools.system('[Telegram] - creating response')

        if(isFirstMessage): 
            return 'Hero Worudo'

        elif(message == 'boards'):
            boards = trello.bot.getAllBoards()
            response = 'All your boards:\n\n'

            for board in boards:
                response = response + board + '\n'

            self.inline = True

            return response

        elif(message == 'login'):
            response = "Login in Trello:"

            inline.initial()
            inline.addUrl('Login', 'https://trello.com/login')
            inline.finish()

            self.inline = True
            return response
        
        return 'Hero Worudooo'

    #Sent response
    def sentResponse(self, response, chat_id):
        dev_tools.system( '[Telegram] - sending response')
        
        link_sent = f'{self.url_base}sendMessage?chat_id={chat_id}&text={response}'

        if self.inline:
            with open('keyboard.json') as file:
                keyboard = json.dumps(json.load(file))

                link_sent = f'{self.url_base}sendMessage?chat_id={chat_id}&text={response}&reply_markup={keyboard}'

        if debug:
            print("[Telegram] -",requests.get(link_sent))

    #get type of callback_query
    def getCallback_query(self, call):
        result = call.split(' ')

        prefix = result[0]
        obj = result[1]

        commands = [
            ["board", trello.bot.show_board(obj)]
        ]

        for command in commands:
            if prefix == command[0]:
                command[1]

        #if(result[0] == "board"):
        #    trello.bot.show_board(result[1])


# ----------------------------------------------------

with open("config_bot.json") as f:
    config = json.load(f)

token = config['telegram_token']
timer = config['timer_dev']
debug = config['debug']

user  = config['telegram_user_id']
bot_id = config['telegram_bot_id']

print("[Setup] - Roboto is initializing...\n")
bot = RobotoJr_bot()
bot.start()