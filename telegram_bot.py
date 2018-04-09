from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import requests
import random
import time 

BOT_TOKEN = ''
USER_ID = ''
KOINEX_API = 'https://koinex.in/api/ticker'
ZEBPAY_API = 'https://www.zebapi.com/api/v1/market/ticker/btc/inr'


def getPrices():
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    request_koinex = requests.get(KOINEX_API, headers=headers)
    request_zebpay = requests.get(ZEBPAY_API, headers=headers)
    ethereum_price  = request_koinex.json()['prices']['ETH']
    bitcoin_price  = request_koinex.json()['prices']['BTC']
    golem_price = request_koinex.json()['prices']['GNT']
    zebpay_btc = request_zebpay.json()['buy']
    print "Ethereum last traded price on %s: %s" % (time.ctime(), ethereum_price)
    print "Bitcoin last traded price on %s: %s" % (time.ctime(), bitcoin_price)
    print "Buy price on Zebpay %s" % zebpay_btc
    return """
Time: %s\nEthereum: Rs.%s
Bitcoin: Rs.%s
GNT: Rs.%s
"""\
        % (time.ctime(), ethereum_price, bitcoin_price, golem_price)

def start(bot, update):
    bot.send_message(chat_id=USER_ID, text="I'm a bot, please talk to me!")

def prices(bot, update):
    bot.send_message(chat_id=USER_ID, text=getPrices())

def prices_minute(bot, job):
    bot.send_message(chat_id=USER_ID, text=getPrices())

if __name__ == '__main__':
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher 
    j = updater.job_queue
    job_minute = j.run_repeating(prices_minute, interval=60*60, first=0)
    start_handler = CommandHandler('start', start)
    prices_handler = CommandHandler('prices', prices)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(prices_handler)
    updater.start_polling()
