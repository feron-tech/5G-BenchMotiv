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
out=result.stdout

import gparams
from io import StringIO
import pandas as pd

cols=[
    'SEQ',
    'STIME',
    'SS',
    'SERR',
    'RTIME',
    'RS',
    'RERR',
    'TTL'
]

out = out.replace(' ', ';')
out = out.replace('\n', '$')
out = out.replace('$', '\n')
df_str = StringIO(out)

df = pd.read_table(df_str, sep=';', header=None)
df.columns = cols
print(str(df))

df['is_previous_larger'] = (df['SEQ'].shift(1) > df['SEQ']).astype(int)
mylist=df.index[df['is_previous_larger'] == 1].tolist()
a=mylist[0]

first_ten = df[:a]
rest = df[a:]

print(str(first_ten))
print(str(rest))









