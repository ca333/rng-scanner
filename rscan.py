#!/usr/bin/python3


#################################################################################
#                                                                               #
#.______               _______.  ______     ___      .__   __.                  #
#|   _  \             /       | /      |   /   \     |  \ |  |                  # 
#|  |_)  |    ______ |   (----`|  ,----'  /  ^  \    |   \|  |                  #
#|      /    |______| \   \    |  |      /  /_\  \   |  . `  |                  #
#|  |\  \----.    .----)   |   |  `----./  _____  \  |  |\   |                  #
#| _| `._____|    |_______/     \______/__/     \__\ |__| \__|  v0.1.4          #
#                                                                               #
#GNU PL - 2015 - ca333                                                          # 
#                                                                               #         
#USE AT OWN RISK!                                                               #
#################################################################################

import json
import urllib
import time
import sys
from urllib3 import Retry, PoolManager

print("WELCOME TO R-scan v0.1.4!")

print("ADDRESS-R-SCAN: ")
addr = input("type address:  ")
urladdr = "https://api-r.bitcoinchain.com/v1/address/txs/" + str(addr)
countaddr = "https://blockchain.info/de/rawaddr/" + str(addr)
#control api-url
print(urladdr)

retries = Retry(connect=5, read=2, redirect=5, backoff_factor=4)
http = PoolManager(retries=retries)


#https://stackoverflow.com/a/63112319
def request_source(urll):
	return http.request('GET', urll).data.decode('utf-8')

#print(request_source(countaddr))

countdata = json.loads(request_source(countaddr))
print("Data for pubkey: " + str(addr))
print("number of txs: " + str(countdata['n_tx']))
#tx-details:
y = 0
inputs = []

while y < countdata['n_tx']:
	print("#################################################################################")
	print("TX nr :" + str(y+1))
	if (y%100==0):
		time.sleep(3.0)
		while True:
			try:
				addrdata = json.loads(request_source(urladdr + "?offset=" + str(y)))
				break
			except ValueError:
				time.sleep(7.0)
	
	print("hash: " + str(addrdata[0][y%100]['tx']['self_hash']))
	print("number of inputs: " + str(len(addrdata[0][y%100]['tx']['inputs'])))
	zy = 0
	if (addrdata[0][y%100]['tx']['inputs'][0] is not None):
		while zy < len(addrdata[0][y%100]['tx']['inputs']):
			print("Input-ScriptNR " + str(zy+1) + " :" + str(addrdata[0][y%100]['tx']['inputs'][zy]['in_script']['hex']))
			inputs.append(addrdata[0][y%100]['tx']['inputs'][zy]['in_script']['hex'])
			zy += 1
	
	y += 1
	
print("compare: ")

xi = 0
zi = 1
lenx = len(inputs)
alert = 0

#compare the sig values in each input script
while xi < lenx-1:
	x = 0
	while x < lenx-zi: 
		if inputs[xi][10:74] == inputs[x+zi][10:74]:
			print("In Input NR: " + str(xi) + "[global increment] " + str(inputs[xi]))
			print('\a')
			print("Reused R-Value: ")
			print(inputs[x+zi][10:74])
			alert += 1

		x += 1
		
	zi += 1
	xi += 1

#check duplicates
#alert when everything ok

if alert < 1:
	print("Good pubKey. No problems.")


sys.exit()
