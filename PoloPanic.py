#!/usr/bin/python
from poloniex import Poloniex
from time import sleep
import Tkinter as tk
import threading
import math
import datetime

"""
PoloPanic Scanner
Detect panic sells in all Poloniex markets
Built for Python 2.7

Requirements:
pip install https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.6.zip
apt-get install python-tk
"""

class CursorAnimation(threading.Thread):
	def __init__(self, timeframe):
		self.flag = True
		self.timeframe = timeframe
		threading.Thread.__init__(self)

	def run(self):
		timer = self.timeframe
		while self.flag:
			print "[Time Left: " + str(math.ceil(timer)) + " sec]",
			print "\r",
			sleep(0.01)
			timer -= 0.01

	def stop(self):
		self.flag = False

def alert(markets):	
	root = tk.Tk()
	root.title("PoloPanic!")
	label = tk.Label(root, text="Potential panic " + str(markets))
	label.pack(side="top", fill="both", expand=True, padx=20, pady=20)
	button = tk.Button(root, text="OK", command=lambda: root.destroy())
	button.pack(side="bottom", fill="none", expand=True)
	root.mainloop()
	

def detect_panic(drop, timeframe):
	spin = CursorAnimation(timeframe)
	spin.start()
	alert_list = []
	polo = Poloniex()
	ticker1 = polo.returnTicker()
	sleep(timeframe)
	ticker2 = polo.returnTicker()	

	for market in ticker1:
		delta = (float(ticker1[market]['last']) - float(ticker2[market]['last'])) / float(ticker1[market]['last'])
		if (delta < drop):
			alert_list.append(market)

	if (len(alert_list) > 0):
		alert(alert_list)
		print "----------------------------------------------------------------------------------------------------"
		print "[" + str(datetime.datetime.now()) + "] " + str(alert_list)
	
	spin.stop()
if __name__ == "__main__":
	drop = -0.04
	timeframe = 30 * 60 #minutes
	
	try:
		print "[+] Starting PoloPanic Scanner..."	
		print "[+] Time frame: " + str(timeframe / 60) + " min"
		print "[+] Drop: " + str(drop * 100) + "%"	
		while(True):
			detect_panic(drop, timeframe)
	except Exception, e:
		print "[-] Error: " + str(e.message)
