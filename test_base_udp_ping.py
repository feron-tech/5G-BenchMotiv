from monitor import Monitor
import gparams
server_ip='192.168.200.117'


mon = Monitor()

out=mon.get_udpping_stats(server_ip=server_ip,packet_size=1250,num_packets=2)
print(str(out))