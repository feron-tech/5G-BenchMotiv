import docker
import socket
from helper import Helper
import gparams
from orchestrator import Orchestrator

_server_ip='192.168.200.117'
orch = Orchestrator()
env = {
	'ENV_SERVER_IP': _server_ip,
	'ENV_SERVER_PORT': int(gparams._PORT_SERVER_OPENCV)
}
iface = orch.activate(image='client_opencv', detach=True, env=env)
import time
time.sleep(5)
# deactivate app
orch.deactivate(image='client_opencv')



