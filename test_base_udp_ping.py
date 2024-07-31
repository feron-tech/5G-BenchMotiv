from monitor import Monitor
import gparams
server_ip='192.168.200.117'


mon = Monitor()

out=mon.get_udpping_stats(server_ip=server_ip,packet_size=1250,num_packets=2)
print(str(out))

my_strs=out.split('(all times in ns)')
print(my_strs)
geo=my_strs[1].split('out of')
print(geo)
final=geo[0]
print(final)
import pandas as pd
df = pd.read_csv(TESTDATA, sep=";",escapechar='\n')
print(str(df))