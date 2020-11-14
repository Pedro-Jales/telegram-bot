import time

class timer:
    def __init__(self):
        self.counter = 300

    def start(self):
        print("[Timer] - Timer is online!")

        while True:
            self.wait()

    def wait(self):
        time.sleep(self.counter)
        print("[Timer] - 5 min has passed")

#----------------------------------------------

bot = timer()
bot.start()