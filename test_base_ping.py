from monitor import Monitor
mon = Monitor()

mydict = mon.get_ping_stats(server_ip='192.168.200.117')
print(str(mydict))