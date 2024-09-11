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

def get_app_video():
	helper=Helper()
	db_in_user=helper.read_json2dict(loc=gparams._DB_FILE_LOC_INPUT_USER)

	try:
		_enable = db_in_user['Experiment']['Application']['Video']['enable']
		_fps = int(db_in_user['Experiment']['Application']['Video']['fps'])
		_width = float(db_in_user['Experiment']['Application']['Video']['width'])
		_height = float(db_in_user['Experiment']['Application']['Video']['height'])
		_shark_captime_sec = float(db_in_user['Experiment']['Application']['Wireshark']['capture time (sec)'])
		_shark_max_packs = int(db_in_user['Experiment']['Application']['Wireshark']['max packets'])
		_camp_name = db_in_user['Measurement']['Campaign name']

		if _enable == 'False':
			print('(Backend) DBG: Video test deactivated')
			return None
		else:
			print('(Backend) DBG: Init Video test ................')
	except Exception as ex:
		print('(Backend) ERROR: Init Video: ' + str(ex))
		return None

	config_dict = {
		'app_name': 'video',
		'client_app_image_name': 'client_stream',
		'camp_name': _camp_name,
		'ports_dict': {
			gparams._PORT_SERVER_OPENCV: gparams._PORT_SERVER_OPENCV
		},
		'env': {
			'ENV_STREAM_PORT': gparams._PORT_SERVER_OPENCV,
			'ENV_FPS': _fps,
			'ENV_FRAME_WIDTH': _width,
			'ENV_FRAME_HEIGHT': _height
		},
		'shark_captime_sec': _shark_captime_sec,
		'shark_max_packs': _shark_max_packs,
	}

	res = activate_app(config_dict=config_dict)

get_app_video()