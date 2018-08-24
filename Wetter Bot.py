from telegram.ext import Updater
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np
from pyowm import OWM
import json
import requests
import datetime




updater = Updater(token='614124459:AAFtKh67wdT6v2Mjagt21c17OucZxbRw_Yo')
dispatcher = updater.dispatcher

owmKey="0d33a1d7fd9b89fd54f1942c068f21bb"
apiRequest=requests.get('https://api.openweathermap.org/data/2.5/forecast?q=ravensburg&APPID=0d33a1d7fd9b89fd54f1942c068f21bb')
wetterList=apiRequest.json()
chat_id=""
bot=None


print((datetime.datetime.fromtimestamp(int(wetterList["list"][0]["dt"])))-(datetime.timedelta(days=23)))




def start(_bot,update):
    global chat_id
    global bot
    bot=_bot
    chat_id=update.message.chat_id
    bot.send_message(chat_id=chat_id, text=(("Wetter Bot gestartet\n")+("ID ist:\n")+str(chat_id)))



def todaysWeather():
    todaysDate = (datetime.datetime.today()).strftime('%Y-%m-%d %H:%M:%S')[:10]
    if (wetterList["list"][0]["rain"]):
        earlyTime = (
                    (datetime.datetime.fromtimestamp(int(wetterList["list"][0]["dt"]))) - (datetime.timedelta(hours=3)))
        lateTime = datetime.datetime.fromtimestamp(int(wetterList["list"][0]["dt"]))
        strEarly = str(earlyTime)
        strLate = str(lateTime)
        bot.send_message(chat_id=chat_id, text=(
                    "Von " + strEarly[10:13] + " Uhr bis " + strLate[10:13] + " Uhr hat es " + str(
                wetterList["list"][0]["rain"]["3h"]) + "mm Regen"))
    for x in range(len(wetterList["list"])):
        if (todaysDate == datetime.datetime.fromtimestamp(int(wetterList["list"][x]["dt"])).strftime(
                '%Y-%m-%d %H:%M:%S')[:10]):
            time = datetime.datetime.fromtimestamp(int(wetterList["list"][x]["dt"])).strftime('%Y-%m-%d %H:%M:%S')
            wetter = "\n" + wetterList["list"][x]["weather"][0]["main"]
            regenDict = wetterList["list"][x + 1]["rain"]

            if regenDict:
                regen = ": " + str(wetterList["list"][x + 1]["rain"]["3h"]) + " mm"
            else:
                regen = ""

            bot.send_message(chat_id=chat_id, text=time + wetter + regen)


def replyTodaysWeather(bot,update):
    todaysDate = (datetime.datetime.today()).strftime('%Y-%m-%d %H:%M:%S')[:10]
    if (wetterList["list"][0]["rain"]):
        earlyTime = ((datetime.datetime.fromtimestamp(int(wetterList["list"][0]["dt"]))) - (datetime.timedelta(hours=3)))
        lateTime = datetime.datetime.fromtimestamp(int(wetterList["list"][0]["dt"]))
        strEarly=str(earlyTime)
        strLate=str(lateTime)
        bot.send_message(chat_id=chat_id, text=("Von "+strEarly[10:13]+ " Uhr bis " + strLate[10:13] + " Uhr hat es " + str(wetterList["list"][0]["rain"]["3h"]) + "mm Regen"))
    for x in range(len(wetterList["list"])):
        if (todaysDate == datetime.datetime.fromtimestamp(int(wetterList["list"][x]["dt"])).strftime('%Y-%m-%d %H:%M:%S')[:10]):
            time = datetime.datetime.fromtimestamp(int(wetterList["list"][x]["dt"])).strftime('%Y-%m-%d %H:%M:%S')
            wetter = "\n" + wetterList["list"][x]["weather"][0]["main"]
            regenDict = wetterList["list"][x+1]["rain"]

            if regenDict:
                regen = ": " + str(wetterList["list"][x+1]["rain"]["3h"]) + " mm"
            else:
                regen = ""

            bot.send_message(chat_id=chat_id, text=time + wetter + regen)


from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
wetter_handler = CommandHandler('wetter', replyTodaysWeather)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(wetter_handler)

updater.start_polling()

scheduler = BlockingScheduler()
scheduler.add_job(todaysWeather, 'interval', hours=24)
scheduler.start()








