from monitor import Monitor
import gparams
server_ip='192.168.200.117'


mon = Monitor()

out=mon.get_udpping_stats(server_ip=server_ip)
print(str(out))