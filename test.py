from icmplib import ping, multiping, traceroute, resolve
def get_icmp_stats( server_ip, packs=50, interval_sec=1, payload_bytes=64):
	print('(Monitor) DBG: Settings: server_ip=' + str(server_ip) + ',num_packets=' + str(packs) +
	      ',interval_sec=' + str(interval_sec) + ',payload_bytes=' + str(payload_bytes) + ' ...')


# ping has a max packet len around 1500 bytes
res = ping(address='127.0.0.1', count=5, interval=0.01, payload_size=12, privileged=False, timeout=0.5)
print('(Monitor) DBG: Ping res=' + str(res))

if res.is_alive:
	print('(Monitor) DBG: Ping alive!')

else:
	print('(Monitor) DBG: Ping NOT alive!')

