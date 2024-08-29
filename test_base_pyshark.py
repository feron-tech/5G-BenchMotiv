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

mymon=Monitor()

a,b=mymon.get_pyshark_kpis(my_iface='vethcc322d1',max_packs=50)
print(str(a))
print(str(b))
