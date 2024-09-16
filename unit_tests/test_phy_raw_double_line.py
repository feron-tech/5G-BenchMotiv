import re
import logging
import serial
import time
from helper import Helper
import gparams
import os
import helper

def get_qrsrq():
	helper = Helper()
	## log cmd in log file
	try:
		helper.write_db(loc=gparams._RES_FILE_LOC_PHY_RAW, mystr="AT+QRSRQ")
	except:
		pass

	#response = self.send_at_command("AT+QRSRQ")

	with open('C:\\Pycharm\\Projects\\golden_unit\\single_test.txt', 'r') as file:
		response = file.read()

	## log res in log file
	try:
		helper.write_db(loc=gparams._RES_FILE_LOC_PHY_RAW, mystr=str(response))
	except:
		pass

	# Define the regular expression to match the QRSRP response
	pattern = r'\+QRSRQ: (-?\d+),(-?\d+),(-?\d+),(-?\d+),(\w+)'

	# Search for the pattern in the response
	for line in response.splitlines():
		match = re.search(pattern, line)
		print(str(match))
		if match:
			rsrq_prx = match.group(1)
			rsrq_drx = match.group(2)
			rsrq_rx2 = match.group(3)
			rsrq_rx3 = match.group(4)
			rsrq_sysmode = match.group(5)
			print(rsrq_prx, rsrq_drx, rsrq_rx2, rsrq_rx3, rsrq_sysmode)
		else:
			pass

get_qrsrq()