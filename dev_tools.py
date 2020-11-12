import datetime

def getTime():
    return datetime.datetime.now().strftime("%H:%M:%S")

def system(msg):
    print(getTime(), msg)