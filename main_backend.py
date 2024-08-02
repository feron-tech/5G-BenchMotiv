import pandas as pd
from helper import Helper
import gparams
from monitor import Monitor
from orchestrator import Orchestrator
import socket
import time
import subprocess

class Backend:
	def __init__(self):
		self.df_out_monitor=None
		self.helper = Helper()
		self.helper.init_db(loc=gparams._DB_FILE_LOC_OUTPUT_APP, header=gparams._DB_FILE_FIELDS_OUTPUT_APP)
		self.helper.init_db(loc=gparams._DB_FILE_LOC_OUTPUT_BASE, header=gparams._DB_FILE_FIELDS_OUTPUT_BASE)
		self.helper.init_db(loc=gparams._DB_FILE_LOC_OUTPUT_LOG, header=gparams._DB_FILE_FIELDS_OUTPUT_LOG)
		self.helper.init_db(loc=gparams._DB_FILE_LOC_OUTPUT_PHY, header=gparams._DB_FILE_FIELDS_OUTPUT_PHY)

		
		self.counter_exp=0
		self.counter_camp=0
		# read user input
		self.df_in_user = self.read_input()

		if self.df_in_user is not None:
			self.run_campaign()

	def read_input(self):
		res_df=None
		attempt = 1
		while (res_df is None) or (res_df.empty):
			print('(Backend) DBG: Reading input sources (attempt='+str(attempt)+')...')

			if attempt>1:
				self.helper.wait(gparams._WAIT_SEC_BACKEND_READ_INPUT_SOURCES)

			res_df=self.helper.read_db_df(loc=gparams._DB_FILE_LOC_INPUT_USER)
			attempt=attempt+1

			if attempt>=gparams._ATTEMPTS_BACKEND_READ_INPUT_SOURCES:
				print('(Backend) ERROR: Cannot read input sources!')
				return None

		print('(Backend) DBG: Read input sources - Success')
		return res_df

	def run_campaign(self):
		try:
			_camp_repet=int(self.df_in_user['in_meas_repet'].iloc[0])
			_camp_gap = int(self.df_in_user['in_meas_gap'].iloc[0])
			_camp_name = self.df_in_user['in_meas_campaign_name'].iloc[0]
			_exp_num=int(self.df_in_user['in_meas_exps'].iloc[0])

			myline='Initiating campaign with name:'+ str(_camp_name)+',repet='+str(_camp_repet)+',gap='+str(_camp_gap)+',for exps='+str(_exp_num)
			print('(Backend) DBG:'+str(myline))
			mycsv_line = self.helper.get_str_timestamp()+gparams._DELIMITER+myline
			self.helper.write_db(loc=gparams._DB_FILE_LOC_OUTPUT_LOG, mystr=mycsv_line)

		except Exception as ex:
			print('(Backend) ERROR: At input settings=' + str(ex))
			return None

		self.counter_camp=0
		while (self.counter_camp<_camp_repet):
			# start new campaign repetition
			time_start=self.helper.get_curr_time()

			self.counter_exp=0
			for i in range(0,_exp_num):
				self.run_exp()
				self.counter_exp = self.counter_exp +1

				myline = 'Completed exp:' + str(self.counter_exp) + ',of campaign repetition:' + str(self.counter_camp)
				mycsv_line = self.helper.get_str_timestamp() + gparams._DELIMITER + myline
				self.helper.write_db(loc=gparams._DB_FILE_LOC_OUTPUT_LOG, mystr=mycsv_line)
				print('(Backend) DBG: ' + myline)
				print('---   ---   --- ---   ---   --- ---   ---   --- ')

			self.counter_camp=self.counter_camp+1

			curr_time=self.helper.get_curr_time()
			while (self.helper.diff_betw_times(time_start,curr_time)<3600*_camp_gap):
				curr_time = self.helper.get_curr_time()
				if (self.helper.diff_betw_times(time_start,curr_time) % 1200==0) or (self.helper.diff_betw_times(time_start,curr_time)<300):
					myline = 'Waiting for new campaign, remaining (sec):' + str(3600*_camp_gap-self.helper.diff_betw_times(time_start,curr_time))
					mycsv_line = self.helper.get_str_timestamp() + gparams._DELIMITER + myline
					self.helper.write_db(loc=gparams._DB_FILE_LOC_OUTPUT_LOG, mystr=mycsv_line)
					print('(Backend) DBG: ' + myline)
				self.helper.wait(300)

	def run_exp(self):
		try:
			_server_ip = self.df_in_user['in_set_server_ip'].iloc[0]
			print('(Backend) DBG: Initiating new experiment, target IP=' + str(_server_ip))
		except Exception as ex:
			print('(Backend) ERROR: Cannot init new experiment='+str(ex))

		if (self.df_in_user['in_app_base'].iloc[0]):

			try:
				subprocess.run(["/home/targetx/anaconda3/envs/golden_unit/bin/python", "physical.py"],
							   capture_output=True, text=True)
				print('(Backend) DBG: physical capture OK')
			except Exception as ex:
				print('(Backend) ERROR: At physical capture:'+str(ex))

			self.get_baseline_measurements()

		max_packs =int(self.df_in_user['in_set_num_packets'].iloc[0])

		# video stream
		if (self.df_in_user['in_app_video_stream'].iloc[0]):

			env = {
				'ENV_SERVER_IP': _server_ip,
				'ENV_SERVER_PORT': int(gparams._PORT_SERVER_OPENCV)
			}
			self.get_app_measurements(app_name='video_stream', app_image='client_opencv',
			                          env=env, max_packs=max_packs)

		# mqtt
		if (self.df_in_user['in_app_mqtt'].iloc[0]):
			env = {
				'ENV_SERVER_IP': _server_ip,
				'ENV_SERVER_PORT': int(gparams._PORT_SERVER_MQTT1),
				'MAX_PAYLOAD_SIZE':int(gparams._MQTT_MAX_PAYLOAD),
				'SLEEP_SEC':float(gparams._MQTT_SLEEP_SEC)
			}
			self.get_app_measurements(app_name='mqtt', app_image='client_mqtt',
			                          env=env, max_packs=max_packs)

	def get_app_measurements(self,app_name,app_image,env,max_packs):
		print('(Backend) DBG: Get measurements for app='+str(app_name)+'...')

		# activate app
		orch = Orchestrator()
		iface=orch.activate(image=app_image, detach=True, env=env)

		# monitor stats
		mon=Monitor()
		df_res,dict_res=mon.get_pyshark_kpis(my_iface=iface,max_packs=max_packs)

		# deactivate app
		orch.deactivate(image=app_image)

		# assign app name to output
		df_res['app'] = [app_name]
		df_res['timestamp'] = [self.helper.get_str_timestamp()]
		dict_res['app'] = [app_name]
		dict_res['timestamp'] = [self.helper.get_str_timestamp()]

		# write to db
		if df_res is not None:

			_DB_FILE_FIELDS_OUTPUT_APP = 'camp_name;camp_id;exp_id;timestamp;app;total_packs;total_bytes;total_time;total_timestamp;' \
			                             'mean_rtt;sd_rtt_jitter;throughput_bps;drop_perc;arrive_perc'

			mystr = self.df_in_user['in_meas_campaign_name'].iloc[0]+gparams._DELIMITER+\
				str(self.counter_camp)+gparams._DELIMITER+\
			        str(self.counter_exp)+gparams._DELIMITER+\
			        str(dict_res['timestamp'][0]) +gparams._DELIMITER+\
			        str(dict_res['app'][0]) +gparams._DELIMITER+\
			        str(dict_res['total_packs'][0]) +gparams._DELIMITER+\
			        str(dict_res['total_bytes'][0])+gparams._DELIMITER+\
			        str(dict_res['total_time'][0])+gparams._DELIMITER+\
			        str(dict_res['total_timestamp'][0]) +gparams._DELIMITER+\
			        str(dict_res['mean_rtt'][0]) +gparams._DELIMITER+\
			        str(dict_res['sd_rtt_jitter'][0]) +gparams._DELIMITER+\
			        str(dict_res['throughput_bps'][0]) +gparams._DELIMITER+\
			        str(dict_res['drop_perc'][0]) +gparams._DELIMITER+\
			        str(dict_res['arrive_perc'][0])

			self.helper.write_db(loc=gparams._DB_FILE_LOC_OUTPUT_APP, mystr=mystr)


			print('(Backend) DBG: Get measurements for app=' + str(app_name) + ' OK!')
		else:
			print('(Backend) ERROR: Get measurements for app=' + str(app_name) + ' failed!')

	def get_baseline_measurements(self):
		mon = Monitor()
		try:
			_server_ip = self.df_in_user['in_set_server_ip'].iloc[0]
			_iperf_duration=10
			_camp_name = 'day2_exp2_baseline'
			_ping_interval = 0.020
			_ping_packs = 2000
			_packet_size=1200
			print('(Backend) DBG: Get baseline measurements for ip='+str(_server_ip)+'...')

			base_dict={}
			base_dict['camp_name'] = [str(_camp_name)]
			base_dict['camp_id'] = [str(self.counter_camp)]
			base_dict['exp_id'] = [str(self.counter_exp)]
			base_dict['timestamp'] = [self.helper.get_str_timestamp()]

			try:

				df_ping=mon.get_ping_stats(server_ip=_server_ip,packs=_ping_packs,interval=_ping_interval)
			except:
				df_ping = mon.get_ping_stats(server_ip=_server_ip)
			base_dict.update(df_ping)

			df_iperf_tcp_dl=mon.get_iperf_stats(server_ip=_server_ip,port=gparams._PORT_SERVER_IPERF,flag_udp=False,
												flag_downlink=True,duration=_iperf_duration,bitrate=None,mss=_packet_size)
			df_iperf_tcp_ul=mon.get_iperf_stats(server_ip=_server_ip,port=gparams._PORT_SERVER_IPERF,flag_udp=False,
												flag_downlink=False,duration=_iperf_duration,bitrate=None,mss=_packet_size)
			df_iperf_udp_dl=mon.get_iperf_stats(server_ip=_server_ip,port=gparams._PORT_SERVER_IPERF,flag_udp=True,
												flag_downlink=True,duration=_iperf_duration,bitrate='2000M',mss=_packet_size)
			df_iperf_udp_ul=mon.get_iperf_stats(server_ip=_server_ip,port=gparams._PORT_SERVER_IPERF,flag_udp=True,
												flag_downlink=False,duration=_iperf_duration,bitrate='2000M',mss=_packet_size)
			base_dict.update(df_iperf_tcp_dl)
			base_dict.update(df_iperf_tcp_ul)
			base_dict.update(df_iperf_udp_dl)
			base_dict.update(df_iperf_udp_ul)

			dict_owamp=mon.get_owamp_stats(host=_server_ip,packs=_ping_packs,interval=_ping_interval,packet_size=_packet_size)
			dict_twamp=mon.get_twamp_stats(host=_server_ip,packs=_ping_packs,interval=_ping_interval,packet_size=_packet_size)
			base_dict.update(dict_owamp)
			base_dict.update(dict_twamp)

			dict_udp_ping=mon.get_udpping_stats(server_ip=_server_ip,packet_size=_packet_size,num_packets=_ping_packs,
												interval_ms=_ping_interval)
			base_dict.update(dict_udp_ping)

			mystr=''
			mylist=gparams._DB_FILE_FIELDS_OUTPUT_BASE.split(gparams._DELIMITER)
			for el in mylist:
				mystr=mystr+str(base_dict[el][0])+gparams._DELIMITER
			mystr = mystr[:-1]

			self.helper.write_db(loc=gparams._DB_FILE_LOC_OUTPUT_BASE,mystr=mystr)

			print('(Backend) DBG: Get baseline measurements OK!')
		except Exception as ex:
			print('(Backend) ERROR: Failed to get baseline measurements='+str(ex))
			return None

if __name__ == '__main__':
	print('(Backend) DBG: Backend initialized')
	pd.options.mode.chained_assignment = None  # default='warn'
	backend=Backend()