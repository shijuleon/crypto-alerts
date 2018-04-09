import requests
import time
import random
import subprocess

#just a quick script 

ETH_MIN = 50000
BTC_MIN = 1000000
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
KOINEX_API_ENDPOINT = "https://koinex.in/api/ticker"
ZEBPAY_API_ENDPOINT = "https://www.zebapi.com/api/v1/market/ticker/btc/inr"
ALERT_MP3 = "/home/shiju/alerts/beep.mp3"

def getprices():
	while(1):
		try:
			r = requests.get(KOINEX_API_ENDPOINT, headers=headers)
			r1 = requests.get(ZEBPAY_API_ENDPOINT, headers=headers)
			ethereum_price  = r.json()['prices']['ETH']
			bitcoin_price  = r.json()['prices']['BTC']
			zebpay_btc = r1.json()['buy']
			print("Ethereum last traded price on %s: %s" % (time.ctime(), ethereum_price))
			print("Bitcoin last traded price on %s: %s" % (time.ctime(), bitcoin_price))
			print("Buy price on Zebpay %s" % zebpay_btc)
			if float(zebpay_btc) < BTC_MIN:
				print ("Zebpay lower")
				subprocess.call(["mplayer", ALERT_MP3], shell=True)
			if float(ethereum_price) < ETH_MIN or float(bitcoin_price) < BTC_MIN:
				print("Ethereum lower than %s, now %s" % (ETH_MIN, ethereum_price))
				print("Bitcoin lower than %s, now %s" % (BTC_MIN, bitcoin_price))
				subprocess.call(["mplayer", ALERT_MP3], shell=True)
			sleep_time = random.randrange(90, 270)
			print("Sleeping for %d seconds" % sleep_time)
			time.sleep(sleep_time)
		except:
			#ignore everything, keep on trying
			pass

if __name__ == '__main__':
	getprices()