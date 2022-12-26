import json
import requests
import time
import sys

blockstart = 170399
blockstart += 59711

print("WELCOME TO R-scan Python3 Edition v0.1.2!")

addr_files = input("address list file path --> ")
addr_files = open(addr_files, "r")
tx_n = 0
while(True):
	found_reused_r = False
	addr = addr_files.readline()
	if not addr:
		break
	addr = "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm"
	urladdr = f"https://sochain.com/api/v2/get_tx_spent/BTC/{str(addr)}"
	headers = {"content-type": "application/json"}

	tx_information= requests.get(urladdr).json()["data"]["txs"]
	tx_id = tx_information	
	tx_count = len(tx_information)
	tx_n = 0
	x = 1
	
	try:
		while not found_reused_r:
			urladdr = f"https://sochain.com/api/v2/tx/BTC/{tx_id[tx_n]['txid']}"
			rawdata_res = requests.get(urladdr, headers = headers).json()
			rawdata = rawdata_res["data"]["inputs"][0]["script_hex"]
			prev_r = rawdata[10:74]
			while not found_reused_r: 
				urladdr = f"https://sochain.com/api/v2/tx/BTC/{tx_id[tx_n + x]['txid']}"
				next_rawdata = requests.get(urladdr).json()["data"]["inputs"][0]["script_hex"]
				print(f"compare : {prev_r} <=> {next_rawdata[10:74]}")
				if prev_r == next_rawdata[10:74]:
					print('\a')
					print("-----------------------------")
					print(f"Address : {addr}")
					print(f"TXID : {tx_id[tx_n]['txid']}")
					print(f"Reused R TXID : {tx_id[tx_n + x]['txid']}")
					print("Resued R-Value: ")
					print(next_rawdata[10:74])
					print("-----------------------------")
					found_reused_r = True
				prev_r = next_rawdata[10:74]
					
				x += 1
			tx_n += 1
	except Exception:
		pass

addr_files.close()