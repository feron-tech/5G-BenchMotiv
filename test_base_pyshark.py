from monitor import Monitor
mon = Monitor()

mydf = mon.get_pyshark_kpis(display_filter=None, max_packs=5)
print(str(mydf))