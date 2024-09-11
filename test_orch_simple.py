import docker
import socket
from helper import Helper
import gparams
from orchestrator import Orchestrator


def activate_app(config_dict):
	try:
		_app_name = config_dict['app_name']
		_client_app_image_name = config_dict['client_app_image_name']
		_ports_dict = config_dict['ports_dict']
		_env = config_dict['env']
		_shark_captime_sec = config_dict['shark_captime_sec']
		_shark_max_packs = config_dict['shark_max_packs']
		_camp_name = config_dict['camp_name']
		print('(Backend) DBG: Activating app=' + str(_app_name) + '...')
	except Exception as ex:
		print('(Backend) ERROR: Activate app:' + str(ex) + '...')
		return None

	# activate app
	orch = Orchestrator()
	if _ports_dict is None:
		iface = orch.activate(image=_client_app_image_name, detach=True, env=_env)
	else:
		iface = orch.activate(image=_client_app_image_name, detach=True, env=_env, port_dict=_ports_dict)

	print(str('Done'))
	# deactivate app
	#orch.deactivate(image=_client_app_image_name)




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
	},
	'shark_captime_sec': 10,
	'shark_max_packs': 20,
}

res = activate_app(config_dict=config_dict)

orch = Orchestrator()
_ports_dict=config_dict['ports_dict']
_client_app_image_name=config_dict['client_app_image_name']
_env=config_dict['env']
if _ports_dict is None:
	iface = orch.activate(image=_client_app_image_name, detach=True, env=_env)
else:
	iface = orch.activate(image=_client_app_image_name, detach=True, env=_env, port_dict=_ports_dict)

print(str('Done'))