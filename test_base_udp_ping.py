from monitor import Monitor
import gparams
server_ip='192.168.200.117'
import sys
from io import StringIO

mon = Monitor()

out=mon.get_udpping_stats(server_ip=server_ip,packet_size=1250,num_packets=2)
print(str(out))
my_strs=(str(out)).split('(all times in ns)')
print('all========='+str(my_strs))
geo=my_strs[1].split('out of')
print('geo========='+str(geo))
final=geo[0]
final=final.replace('\\n','$')
final=final.replace('\n','$')
final=final.replace('$','\n')
print('FINAL========='+str(final))
ola=StringIO(final)

import pandas as pd
df = pd.read_table(ola, sep=";",header=None)
df.columns=gparams._DB_FILE_FIELDS_INPUT_UDP_PING.split(gparams._DELIMITER)
print(str(df))