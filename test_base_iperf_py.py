from monitor import Monitor

server_ip='192.168.200.118'


mon = Monitor()

print('UDP-UL --------------------------------')
res_dict = mon.get_iperf_stats(server_ip=server_ip, protocol='udp', direction_dl=False)
print(str(res_dict))
print('TCP-UL --------------------------------')
res_dict = mon.get_iperf_stats(server_ip=server_ip, protocol='tcp', direction_dl=False)
print(str(res_dict))
print('UDP-DL --------------------------------')
res_dict = mon.get_iperf_stats(server_ip=server_ip, protocol='udp', direction_dl=True)
print(str(res_dict))
print('TCP-DL --------------------------------')
res_dict = mon.get_iperf_stats(server_ip=server_ip, protocol='tcp', direction_dl=True)
print(str(res_dict))