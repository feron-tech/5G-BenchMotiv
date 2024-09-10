from io import StringIO
import os.path
import re
import subprocess
import pyshark
import pandas as pd
import math
import docker
import json
import gparams
from helper import Helper
import iperf3
from icmplib import ping, multiping, traceroute, resolve
from icmplib import async_ping, async_multiping, async_resolve
from icmplib import ICMPv4Socket, ICMPv6Socket, AsyncSocket, ICMPRequest, ICMPReply
from icmplib import ICMPLibError, NameLookupError, ICMPSocketError
from icmplib import SocketAddressError, SocketPermissionError
from icmplib import SocketUnavailableError, SocketBroadcastError, TimeoutExceeded
from icmplib import ICMPError, DestinationUnreachable, TimeExceeded
from monitor import Monitor

cap = pyshark.LiveCapture(interface='Ethernet', display_filter=None,
                          output_file='path_to_save.pcap')
cap.sniff_continuously()

pack_cnt=0
max_packs=10
for pack in cap:
	pack_cnt=pack_cnt+1
	if pack_cnt > max_packs:
		break

cap=pyshark.FileCapture(input_file='path_to_save.pcap')

for pack in cap:
	if pack_cnt > max_packs:
		break
	pack_cnt = pack_cnt + 1

	mydict = {}

	try:
		mydict['id'] = [pack_cnt]
	except:
		pass

	try:
		mydict['time'] = [pack.sniff_time]
	except:
		mydict['time'] = [None]

	try:
		mydict['timestamp'] = [float(pack.sniff_timestamp)]
	except:
		mydict['timestamp'] = [None]

	try:
		mydict['protocol'] = [pack.highest_layer]
	except:
		mydict['protocol'] = [None]

	try:
		mydict['len_bytes'] = [float(pack.length)]
	except:
		mydict['len_bytes'] = [None]

	try:
		mydict['addr_src'] = [pack.ip.src]
	except:
		mydict['addr_src'] = [None]

	try:
		mydict['port_src'] = [pack[pack.transport_layer].srcport]
	except:
		mydict['port_src'] = [None]

	try:
		mydict['addr_dest'] = [pack.ip.dst]
	except:
		mydict['addr_dest'] = [None]

	try:
		mydict['port_dest'] = [pack[pack.transport_layer].dstport]
	except:
		mydict['port_dest'] = [None]

	try:
		mydict['rtt'] = [float(pack.tcp.analysis_ack_rtt)]
	except:
		mydict['rtt'] = [None]

	try:
		str_p = str(pack)
		if (
			"TCP Dup ACK" in str_p
			or "TCP Previous" in str_p
			or "TCP Retransmission" in str_p
			or "TCP Fast Retransmission" in str_p
			or "Out-Of-Order" in str_p
			or "TCP Spurious Retransmission" in str_p):
			res = True
		else:
			res = False

		mydict['drop_flag'] = [res]
	except:
		mydict['drop_flag'] = [None]