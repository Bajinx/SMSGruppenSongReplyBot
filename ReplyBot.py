from telegram.ext import Updater
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np



updater = Updater(token='655307721:AAFlbYE4tJLZwWT84CgSyn1zOnGW9hWe_Q8')
dispatcher = updater.dispatcher


moods=[" gut"," ULTRA MEGA TURBO GEIL", " sehr gut", " mega gut", " ganz ok", " richtig schlecht", " SCHEIßE", " PENIS", " nice", " nizze"]
moodsPrio=[10,1,3,20,5,6,7,8,18,10]
moodsPercent=[]

for x in moodsPrio:
    moodsPercent.append(x/sum(moodsPrio))


def settodaysMood():
    global todaysMood
    todaysMood = np.random.choice(moods, size=1, p=moodsPercent)

settodaysMood()
def echo(bot, update):
    message=update.message.text
    containsPhraseAndReplyBot=False
    att1=(("findest du" in message.lower()) | ("magst" in message.lower()) | ("hälts du" in message.lower()))
    att2=(("wetter" in message.lower()) | ("song" in message.lower()))
    att3=("bot" in message.lower())
    att4=(("niklas" in message.lower())|("heike" in message.lower()))


    print (att1)
    print(att2)
    print(att3)
    print(att4)

    if((att1)&(att2)&(att3)):
        print (todaysMood)
        bot.send_message(chat_id=update.message.chat_id, text="Ich sagte doch ich finde den song"+todaysMood[0])
    if (((att1))&(att3)&(att4)):
        print (message[0].upper)
        bot.send_message(chat_id=update.message.chat_id, text="Doof und Niklas sein Bot ist schlecht")

    #bot.send_message(chat_id=update.message.chat_id, text = "Test")

def penis(bot, update):
    update.message.reply_text("I'm a penis, Nice to meet you!")

from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler

echo_handler = MessageHandler(Filters.text, echo)
start_handler = CommandHandler('start', start)
penis_handler= CommandHandler('a',penis)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(penis_handler)

updater.start_polling()

scheduler = BlockingScheduler()
scheduler.add_job(settodaysMood, 'interval', hours=24)
scheduler.start()




