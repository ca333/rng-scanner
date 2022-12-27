import requests
import re

blockstart = 170399
blockstart += 59711

print("WELCOME TO R-scan Python3 Edition v0.1.2!")

addr_files = input("address list file path --> ")
addr_files = open(addr_files, "r")
tx_n = 0

tx_information = None 
tx_id = None	
tx_count = None
tx_n = None
x = None
while(True):
	found_reused_r = False
	addr = addr_files.readline()
	if not addr:
		break
	if(not addr.startswith("1")):
		continue
	addr = addr[:34]
	addr = addr.replace("\n", "")
	print(addr)
	if(addr == ""):
		continue
	urladdr = f"https://sochain.com/api/v2/address/BTC/{addr}"
	headers = {"content-type": "application/json"}
	try:
		tx_info = requests.get(urladdr).json()["data"]["txs"]
		tx_id = tx_info
		tx_n = 0
		x = 1
	except Exception:
		continue
	try:
		while not found_reused_r:
			urladdr = f"https://sochain.com/api/v2/tx/BTC/{tx_id[tx_n]['txid']}"
			rawdata_res = requests.get(urladdr, headers = headers).json()
			rawdata = rawdata_res["data"]["inputs"][0]["script_asm"]
			rawdata = rawdata.replace(" ", "")
			prev_r = rawdata[10:74]
			if(len(rawdata_res["data"]["inputs"]) == 1):
				tx_n += 1
				continue
			while x < len(rawdata_res["data"]["inputs"]): 
				print()
				print(f"compare : {prev_r} <=> {rawdata_res['data']['inputs'][x]['script_asm'][10:74]}")
				if prev_r == rawdata_res['data']['inputs'][x]['script_asm'][10:74]:
					message = ""
					message += "-----------------------------\n"
					message += f"Address : {addr}\n"
					message += f"TXID2 : {tx_id[tx_n]['txid']}\n"
					message += "Reused R-Value: \n"
					message += prev_r + "\n"
					message += "-----------------------------\n"
					print(message)
					reused = open("vulnList.txt", "a")
					print(message, file = reused)
					reused.close()
					found_reused_r = True
				x += 1
			tx_n += 1
			x = 1

	except Exception as e:
		pass

addr_files.close()