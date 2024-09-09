import json
import subprocess
import re
#from influxdb_client import InfluxDBClient, Point, WritePrecision
#from influxdb_client.client.write_api import SYNCHRONOUS
import time

# Target server IP
host = "192.168.200.117"
count=5
#config_file = 'configfile_tcp.json'

command = ["owping", "-c", str(count), host]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(result.stdout)
print('------------------------')
command = ["owping", "-R", "-c", str(count), host]
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(result.stdout)









