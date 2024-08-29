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



cap = pyshark.LiveCapture(interface='Ethernet',output_file='path_to_save.pcap')
cap.sniff(timeout=1)

pack_cnt = 0
max_packs=100

for pack in cap:
	print(str(pack))
	print('--------------------------')
	if pack_cnt > max_packs:
		break
	pack_cnt = pack_cnt + 1
