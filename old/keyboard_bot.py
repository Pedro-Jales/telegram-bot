import json

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

def initial():
    content = '{ "inline_keyboard": ['

    with open("keyboard.json", "w") as file:
        file.write(content)

def addButton(call, content, id):
    with open("keyboard.json", "a") as file:
        file.write('\n\t[{\n\t\t')

        line = str('"text": "' + str(content) +'",\n\t\t')
        file.write(line)

        line = str('"callback_data": "' + str(call) + ' ' + str(id) +'"')
        file.write(line)

        file.write('\n\t}]')

def addUrl(content, url):
    with open("keyboard.json", "a") as file:
        file.write('\n\t[{\n\t\t')

        line = str('"text": "' + str(content) +'",\n\t\t')
        file.write(line)

        line = str('"login_url": "' + str(url) +'"')
        file.write(line)

        file.write('\n\t}]')

def addComma():
    with open("keyboard.json", "a") as file:
        file.write(',')

def finish():
    content = '\n]}'

    with open("keyboard.json", "a") as file:
        file.write(content)