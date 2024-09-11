import docker
import socket
from helper import Helper
import gparams
from orchestrator import Orchestrator


orch = Orchestrator()


config_dict = {
	'app_name': 'video',
	'client_app_image_name': 'client_stream',
	'camp_name': 'test',
	'ports_dict': {
		gparams._PORT_SERVER_OPENCV: gparams._PORT_SERVER_OPENCV
	},
	'env': {
		'ENV_STREAM_PORT': gparams._PORT_SERVER_OPENCV,
		'ENV_FPS': 30,
		'ENV_FRAME_WIDTH': 400,
		'ENV_FRAME_HEIGHT': 400
	}
}

_client_app_image_name=config_dict['client_app_image_name']
_env=config_dict['env']
_ports_dict=config_dict['ports_dict']

iface = orch.activate(image=_client_app_image_name, detach=True, env=_env,port_dict=_ports_dict)