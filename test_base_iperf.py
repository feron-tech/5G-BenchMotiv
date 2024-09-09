from monitor import Monitor
import gparams
server_ip='192.168.200.117'


mon = Monitor()

print('TCP DL------------')
df_iperf_tcp_dl = mon.get_iperf_stats(server_ip=server_ip, port=gparams._PORT_SERVER_IPERF, flag_udp=False,
                                      flag_downlink=True, duration=10, bitrate=None, pack_len=1200)
print('TCP UL------------')
df_iperf_tcp_ul = mon.get_iperf_stats(server_ip=server_ip, port=gparams._PORT_SERVER_IPERF, flag_udp=False,
                                      flag_downlink=False, duration=10, bitrate=None, pack_len=1200)
print('UDP DL------------')
df_iperf_udp_dl = mon.get_iperf_stats(server_ip=server_ip, port=gparams._PORT_SERVER_IPERF, flag_udp=True,
                                      flag_downlink=True, duration=10, bitrate=None, pack_len=1200)
print('UDP DL------------')
df_iperf_udp_ul = mon.get_iperf_stats(server_ip=server_ip, port=gparams._PORT_SERVER_IPERF, flag_udp=True,
                                      flag_downlink=False, duration=10, bitrate=None, pack_len=1200)