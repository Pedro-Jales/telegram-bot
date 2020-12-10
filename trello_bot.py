import requests
import json
import os

import keyboard_bot as inline

class Trello_api:
    def __init__(self):
        self.url_base = f'https://api.trello.com/1/members/me/'

    def start(self):
        print("\n[Setup] - Trello connection is Online!")

    def getAllBoards(self):
        # -- My attemp who kinda worked

        #link = f'{self.url_base}boards?key={key}&token={token}'
        #result = requests.get(link)
        #print(result.text)

        # -- Tuto on boards doc who worked but i don't feel confident

        #headers = { "Accept": "application/json" }
        #query = { 'key': key, 'token': token}

        #result = requests.request("GET", self.url_base, headers=headers, params=query)
        #print(json.dumps(json.loads(result.text), sort_keys=True, indent=4, separators=(",", ": ")))

        # -- Tuto on api introduction

        #curl https://api.trello.com/1/members/me/boards?fields=name,url&key={apiKey}&token={apiToken}

        link = f'{self.url_base}boards?fields=name,url&key={key}&token={token}'
        result = requests.get(link)

        #print(json.dumps(json.loads(boards.text), sort_keys=True, indent=4, separators=(",", ": ")))

        boards = json.loads(result.text)
        boardsNames = []

        print('\n[Trello] - Boards:')

        #for board in boards:
        #    if first:
        #        first = False
        #        pass
        #
        #    print (board['name'])
        #    boardsNames.append(board['name'])

        #keyboard = {
        #        "inline_keyboard": [
        #            [{
        #                "text": "Budget",
        #                "callback_data": "budget"
        #            }],
        #            [{
        #                "text": "Expenses",
        #                "callback_data": "expenses"
        #            }],
        #            [{
        #                "text": "Savings",
        #                "callback_data": "savings"
        #            }]
        #        ]
        #    }

        first = True
        
        inline.initial()

        for board in boards:
            if first == False:
                inline.addComma()

            else:
                first = False

            print (board['name'])
            inline.addButton("board", board['name'], board['id'])
            boardsNames.append(board['name'])

        inline.finish()

        boards = json.dumps(boardsNames)

        print()

        return boardsNames

    def show_board(self, card_id):

        #link = f'{self.url_base}boards/{card_id}/cards?fields=name,url&key={key}&token={token}'
        link = f'https://api.trello.com/1/boards/{card_id}/cards?fields=name'

        query = {
            'key': key,
            'token': token
        }

        result = requests.request("GET", link, params=query)

        cards = json.loads(result.text)
        cardsNames = []

        print('\n[Trello] - Cards:')

        #first = True
        #inline.initial()

        for card in cards:
            #if first == False:
            #    inline.addComma()

            #else:
            #    first = False

            print (card['name'])
            #inline.addButton(board['name'], board['id'])
            cardsNames.append(card['name'])

        #inline.finish()

        #cards = json.dumps(cardsNames)

        print()

        return cardsNames

        pass

    #check the board weekly, look for current day
    def weekly(self):
        pass

#-----------------------------------------------

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    token = os.environ.get('trello_token', None)
    key = os.environ.get('trello_key', None)

else:
    with open("config_bot.json") as f:
        config = json.load(f)

    token = config['trello_token']
    key = config['trello_key']

bot = Trello_api()
bot.start()