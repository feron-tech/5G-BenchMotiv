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

class Monitor:
	def __init__(self):
		self.helper=Helper()

	def get_ping_stats(self,server_ip,packs=50,interval=1):
		print('(Monitor) DBG: Entered Ping at:' + str(self.helper.get_str_timestamp()))
		print('(Monitor) DBG: Settings: server_ip=' + str(server_ip) + ',num_packets=' + str(packs) +
			  ',interval=' + str(interval) + '...')

		try:

			# ping has a max packet len around 1500 bytes
			res = ping(server_ip, count=packs, interval=interval,privileged=False,timeout=0.5)
			print('(Monitor) DBG: Ping res=' + str(res))
			#first_row=True
			#mydf=None

			if res.is_alive:
				my_row_dict={
					'ping_rtt_avg':[float(res.avg_rtt)],
					'ping_rtt_max': [float(res.max_rtt)],
					'ping_rtt_min': [float(res.min_rtt)],
					'ping_packet_loss_perc': [float(res.packet_loss)],
					'ping_packets_lost': [int(res.packets_sent-res.packets_received)],
					'ping_jitter':[float(res.jitter)]
				}
			else:
				my_row_dict={
					'ping_rtt_avg':[None],
					'ping_rtt_max': [None],
					'ping_rtt_min': [None],
					'ping_packet_loss_perc': [100],
					'ping_packets_lost': [int(packs)],
					'ping_jitter': [None]
				}

			return my_row_dict
		except Exception as ex:
			print('(Monitor) ERROR: Ping failed=' + str(ex))
			return None

		if False:
			new_row=pd.DataFrame(my_row_dict)

			if first_row:
				mydf=new_row
				first_row=False
			else:
				mydf = pd.concat([mydf, new_row], axis=0, ignore_index=True, join='outer')

			ping_avg=mydf['ping_rtt_avg'].mean()
			print('ping_avg='+str(ping_avg))

			ping_std_jitter=mydf['ping_rtt_avg'].std()
			print('ping_std_jitter='+str(ping_std_jitter))

			ping_max=mydf['ping_rtt_max'].min()
			print('ping_max='+str(ping_max))

			ping_min=mydf['ping_rtt_min'].max()
			print('ping_min='+str(ping_min))

			ping_avg_packet_loss_perc=mydf['ping_packet_loss_perc'].mean()
			print('ping_avg_packet_loss_perc='+str(ping_avg_packet_loss_perc))

	def get_iperf_stats_py(self,server_ip,port=5201,duration=10,protocol='tcp',direction_dl=False):
		print('(Monitor) DBG: Get iperf with protocol='+str(protocol)+',DL='+str(direction_dl)+',ip='+str(server_ip),'port='+str(port))
		try:
			client = iperf3.Client()
			client.duration = duration
			client.server_hostname = server_ip
			client.port = port
			client.protocol=protocol

			if direction_dl:
				client.reverse=False
			else:
				client.reverse=True

			result = client.run()

			mydict={}
			if protocol=='tcp':
				if direction_dl:
					try:
						mydict['iperf_tcp_dl_retransmits']=[result.retransmits]
					except:
						mydict['iperf_tcp_dl_retransmits'] = [None]
					try:
						mydict['iperf_tcp_dl_sent_bps']=[result.sent_bps]
					except:
						mydict['iperf_tcp_dl_sent_bps'] = [None]
					try:
						mydict['iperf_tcp_dl_sent_bytes']=[result.sent_bytes]
					except:
						mydict['iperf_tcp_dl_sent_bytes'] = [None]
					try:
						mydict['iperf_tcp_dl_received_bps']=[result.received_bps]
						print('(Monitor) DBG: Iperf received_bps=' + str(result.received_bps))
					except Exception as ex:
						mydict['iperf_tcp_dl_received_bps'] = [None]
						print('(Monitor) ERROR: No Iperf received_bps=' + str(ex))
					try:
						mydict['iperf_tcp_dl_received_bytes']=[result.received_bytes]
					except:
						mydict['iperf_tcp_dl_received_bytes'] = [None]
				else:
					try:
						mydict['iperf_tcp_ul_retransmits'] = [result.retransmits]
					except:
						mydict['iperf_tcp_ul_retransmits'] = [None]
					try:
						mydict['iperf_tcp_ul_sent_bps'] = [result.sent_bps]
					except:
						mydict['iperf_tcp_ul_sent_bps'] = [None]
					try:
						mydict['iperf_tcp_ul_sent_bytes'] = [result.sent_bytes]
					except:
						mydict['iperf_tcp_ul_sent_bytes'] = [None]
					try:
						mydict['iperf_tcp_ul_received_bps'] = [result.received_bps]
					except:
						mydict['iperf_tcp_ul_received_bps'] = [None]
					try:
						mydict['iperf_tcp_ul_received_bytes'] = [result.received_bytes]
					except:
						mydict['iperf_tcp_ul_received_bytes'] = [None]
			elif protocol=='udp':
				if direction_dl:
					try:
						mydict['iperf_udp_dl_bytes']=[result.bytes]
					except:
						mydict['iperf_udp_dl_bytes'] = [None]
					try:
						mydict['iperf_udp_dl_bps']=[result.bps]
					except:
						mydict['iperf_udp_dl_bps'] = [None]
					try:
						mydict['iperf_udp_dl_jitter_ms']=[result.jitter_ms]
					except:
						mydict['iperf_udp_dl_jitter_ms'] = [None]
					try:
						mydict['iperf_udp_dl_lost_percent']=[result.lost_percent]
					except:
						mydict['iperf_udp_dl_lost_percent'] = [None]
				else:
					try:
						mydict['iperf_udp_ul_bytes']=[result.bytes]
					except:
						mydict['iperf_udp_ul_bytes'] = [None]
					try:
						mydict['iperf_udp_ul_bps']=[result.bps]
					except:
						mydict['iperf_udp_ul_bps'] = [None]
					try:
						mydict['iperf_udp_ul_jitter_ms']=[result.jitter_ms]
					except:
						mydict['iperf_udp_ul_jitter_ms'] = [None]
					try:
						mydict['iperf_udp_ul_lost_percent']=[result.lost_percent]
					except:
						mydict['iperf_udp_ul_lost_percent'] = [None]
			return mydict
		except Exception as ex:
			print('(Monitor) ERROR: Iperf failed=' + str(ex))
			return None

	def get_iperf_stats(self,server_ip,port=5201,flag_udp=False,flag_downlink=False,duration=10,bitrate=None,mss=None):
		print('(Monitor) DBG: Entered iperf3 at:'+str(self.helper.get_str_timestamp()))
		print('(Monitor) DBG: Settings: UDP='+str(flag_udp)+',Downlink='+str(flag_downlink)+'...')
		# init iperf3
		cmd=['iperf3']

		# add server IP
		cmd.append('--client')
		cmd.append(str(server_ip))

		# add server port
		cmd.append('--cport')
		cmd.append(str(port))

		# duration in sec
		cmd.append('--time')
		cmd.append(str(duration))

		# bitrate in bps
		if bitrate is not None:
			cmd.append('--bitrate')
			cmd.append(str(bitrate))

		# check if reverse (uplink if the default in iperf, from client to server)
		if flag_downlink:
			cmd.append('--reverse')

		# check if udp, default is tcp
		if flag_udp:
			cmd.append('--udp')

		if mss is not None:
			cmd.append('--length')
			cmd.append(str(mss))

		cmd.append('--json')

		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		output= result.stdout

		try:
			data = json.loads(output)
		except Exception as ex:
			print('(Monitor) ERROR in iperf3 output json='+str(ex))

		mydict = {}
		if not flag_udp:
			if flag_downlink:
				try:
					mydict['iperf_tcp_dl_retransmits'] = [data['end']['sum_sent']['retransmits']]
				except:
					mydict['iperf_tcp_dl_retransmits'] = [None]
				try:
					mydict['iperf_tcp_dl_sent_bps'] = [data['end']['sum_sent']['bits_per_second']]
				except:
					mydict['iperf_tcp_dl_sent_bps'] = [None]
				try:
					mydict['iperf_tcp_dl_sent_bytes'] = [data['end']['sum_sent']['bytes']]
				except:
					mydict['iperf_tcp_dl_sent_bytes'] = [None]
				try:
					mydict['iperf_tcp_dl_received_bps'] = [data['end']['sum_received']['bits_per_second']]
					print('(Monitor) DBG: iperf_tcp_dl_received_bps=' + str(mydict['iperf_tcp_dl_received_bps']))
				except Exception as ex:
					mydict['iperf_tcp_dl_received_bps'] = [None]
					print('(Monitor) ERROR: iperf_tcp_dl_received_bps=' + str(ex))
				try:
					mydict['iperf_tcp_dl_received_bytes'] = [data['end']['sum_received']['bytes']]
				except:
					mydict['iperf_tcp_dl_received_bytes'] = [None]
			else:
				try:
					mydict['iperf_tcp_ul_retransmits'] = [data['end']['sum_sent']['retransmits']]
				except:
					mydict['iperf_tcp_ul_retransmits'] = [None]
				try:
					mydict['iperf_tcp_ul_sent_bps'] = [data['end']['sum_sent']['bits_per_second']]
				except:
					mydict['iperf_tcp_ul_sent_bps'] = [None]
				try:
					mydict['iperf_tcp_ul_sent_bytes'] = [data['end']['sum_sent']['bytes']]
					print('(Monitor) DBG: iperf_tcp_ul_sent_bytes=' + str(mydict['iperf_tcp_ul_sent_bytes']))
				except Exception as ex:
					mydict['iperf_tcp_ul_sent_bytes'] = [None]
					print('(Monitor) ERROR: iperf_tcp_ul_sent_bytes=' + str(ex))
				try:
					mydict['iperf_tcp_ul_received_bps'] = [data['end']['sum_received']['bits_per_second']]
				except:
					mydict['iperf_tcp_ul_received_bps'] = [None]
				try:
					mydict['iperf_tcp_ul_received_bytes'] = [data['end']['sum_received']['bytes']]
				except:
					mydict['iperf_tcp_ul_received_bytes'] = [None]
		else:
			if flag_downlink:
				try:
					mydict['iperf_udp_dl_bytes'] = [data['end']['sum']['bytes']]
				except:
					mydict['iperf_udp_dl_bytes'] = [None]
				try:
					mydict['iperf_udp_dl_bps'] = [data['end']['sum']['bits_per_second']]
					print('(Monitor) DBG: iperf_udp_dl_bps=' + str(mydict['iperf_udp_dl_bps']))
				except Exception as ex:
					mydict['iperf_udp_dl_bps'] = [None]
					print('(Monitor) ERROR: iperf_udp_dl_bps=' + str(ex))
				try:
					mydict['iperf_udp_dl_jitter_ms'] = [data['end']['sum']['jitter_ms']]
				except:
					mydict['iperf_udp_dl_jitter_ms'] = [None]
				try:
					mydict['iperf_udp_dl_lost_percent'] = [data['end']['sum']['lost_percent']]
				except:
					mydict['iperf_udp_dl_lost_percent'] = [None]
			else:
				try:
					mydict['iperf_udp_ul_bytes'] = [data['end']['sum']['bytes']]
				except:
					mydict['iperf_udp_ul_bytes'] = [None]
				try:
					mydict['iperf_udp_ul_bps'] = [data['end']['sum']['bits_per_second']]
					print('(Monitor) DBG: iperf_udp_ul_bps=' + str(mydict['iperf_udp_ul_bps']))
				except Exception as ex:
					mydict['iperf_udp_ul_bps'] = [None]
					print('(Monitor) ERROR: iperf_udp_ul_bps=' + str(ex))
				try:
					mydict['iperf_udp_ul_jitter_ms'] = [data['end']['sum']['jitter_ms']]
				except:
					mydict['iperf_udp_ul_jitter_ms'] = [None]
				try:
					mydict['iperf_udp_ul_lost_percent'] = [data['end']['sum']['lost_percent']]
				except:
					mydict['iperf_udp_ul_lost_percent'] = [None]
		return mydict


	def get_udpping_stats(self,server_ip,packet_size=1250,num_packets=5000,interval_ms=20,port=1234):
		print('(Monitor) DBG: Entered udpPing at:'+str(self.helper.get_str_timestamp()))
		print('(Monitor) DBG: Settings: packet_size='+str(packet_size)+',num_packets='+str(num_packets)+
			  ',interval_ms='+str(interval_ms)+'...')
		# get loc
		try:
			mypath=os.path.join(gparams._ROOT_DIR,'client')
			mypath = os.path.join(mypath, 'udp-ping')
			cmd=[]
			#cmd.append(str(mypath))
			#cmd.append('&&')
			cmd.append('./udpClient')

			# add server IP
			cmd.append('-a')
			cmd.append(str(server_ip))

			# add packet size
			cmd.append('-s')
			cmd.append(str(packet_size))

			# num_packets
			cmd.append('-n')
			cmd.append(str(num_packets))

			# interval_ms
			cmd.append('-i')
			cmd.append(str(interval_ms))

			out = subprocess.check_output(cmd,cwd=mypath)

			my_strs = (str(out)).split('(all times in ns)')
			temp_str = my_strs[1].split('out of')
			final_str = temp_str[0]
			final_str = final_str.replace('\\n', '$')
			final_str = final_str.replace('\n', '$')
			final_str = final_str.replace('$', '\n')
			df_str = StringIO(final_str)

			df = pd.read_table(df_str, sep=gparams._DELIMITER, header=None)
			df.columns = gparams._DB_FILE_FIELDS_INPUT_UDP_PING.split(gparams._DELIMITER)
			udpping_cl2server_ns = df['client2server_ns'].mean()
			udpping_server2cl_ns = df['server2client_ns'].mean()
			udpping_rtt_ns = df['rtt_ns'].mean()
			print('(Monitor) DBG UdpPing RTT='+str(udpping_rtt_ns))
		except Exception as ex:
			print('(Monitor) ERROR cannot process udpPing='+str(ex))

		mydict={}

		try:
			mydict['udpping_cl2server_ns']=[udpping_cl2server_ns]
		except:
			mydict['udpping_cl2server_ns']=[None]

		try:
			mydict['udpping_server2cl_ns']=[udpping_server2cl_ns]
		except:
			mydict['udpping_server2cl_ns']=[None]

		try:
			mydict['udpping_rtt_ns']=[udpping_rtt_ns]
		except:
			mydict['udpping_rtt_ns']=[None]

		return mydict

	def get_owamp_stats(self,host,packs,interval,packet_size=1200):
		print('(Monitor) DBG: Entered OWAMP at:' + str(self.helper.get_str_timestamp()))
		print('(Monitor) DBG: packs=' + str(packs)+',packetSize='+str(packet_size)+',interval='+str(interval)+'...')
		try:
			command = ["owping", "-c", str(packs), "-s", str(packet_size) , "-i",str(interval),host]
			result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
			output= result.stdout

			measurements = []
			sections = output.strip().split('\n\n')
			for section in sections:
				lines = section.split('\n')
				if len(lines) < 9:
					continue
				x = 0
				if re.search(r'owping', lines[0]) is None:
					x = 1
				# src_dst = re.search(r'from \[(.*)\]:\d+ to \[(.*)\]:\d+', lines[0])
				# sid = re.search(r'SID:\s+(\w+)', lines[1]).group(1)
				# first = re.search(r'first:\s+([^\s]+)', lines[2]).group(1)
				# last = re.search(r'last:\s+([^\s]+)', lines[3]).group(1)
				packets = re.search(r'(\d+) sent, (\d+) lost \(([^)]+)\), (\d+) duplicates', lines[4 + x])
				delay = re.search(r'one-way delay min/median/max = ([^/]+)/([^/]+)/([^ ]+) ms', lines[5 + x])
				jitter = re.search(r'jitter = ([^ ]+) ms', lines[6 + x]).group(1)
				hops = re.search(r'hops = (\d+)', lines[7 + x]).group(1)
				reordering = re.search(r'no reordering', lines[8 + x]) is not None

				measurement = {
					"packets_sent": int(packets.group(1)),
					"packets_lost": int(packets.group(2)),
					"loss_percentage": float(packets.group(3).replace('%', '')),
					"duplicates": int(packets.group(4)),
					"delay_min": float(delay.group(1)),
					"delay_median": float(delay.group(2)),
					"delay_max": float(delay.group(3)),
					"jitter": float(jitter),
					"hops": int(hops),
					"reordering": reordering
				}
				# write_to_influxdb(config, measurement, config['influxdb']['owamp_bucket'])
				measurements.append(measurement)
				print('(Monitor) DBG: OWAMP=' + str(measurements))
		except Exception as ex:
			print('(Monitor) ERROR: Error in owamp proc=' + str(ex))


		mydict={}

		try:
			mydict['owamp_ul_packets_sent']=[measurements[0]['packets_sent']]
		except:
			mydict['owamp_ul_packets_sent']=[None]

		try:
			mydict['owamp_ul_packets_lost'] = [measurements[0]['packets_lost']]
		except:
			mydict['owamp_ul_packets_lost'] = [None]

		try:
			mydict['owamp_ul_loss_percentage'] = [measurements[0]['loss_percentage']]
		except:
			mydict['owamp_ul_loss_percentage'] = [None]

		try:
			mydict['owamp_ul_duplicates'] = [measurements[0]['duplicates']]
		except:
			mydict['owamp_ul_duplicates'] = [None]

		try:
			mydict['owamp_ul_delay_min'] = [measurements[0]['delay_min']]
		except:
			mydict['owamp_ul_delay_min'] = [None]

		try:
			mydict['owamp_ul_delay_median'] = [measurements[0]['delay_median']]
		except:
			mydict['owamp_ul_delay_median'] = [None]

		try:
			mydict['owamp_ul_delay_max'] = [measurements[0]['delay_max']]
		except:
			mydict['owamp_ul_delay_max'] = [None]

		try:
			mydict['owamp_ul_jitter'] = [measurements[0]['jitter']]
		except:
			mydict['owamp_ul_jitter'] = [None]

		try:
			mydict['owamp_ul_hops'] = [measurements[0]['hops']]
		except:
			mydict['owamp_ul_hops'] = [None]

		try:
			mydict['owamp_ul_reordering'] = [measurements[0]['reordering']]
		except:
			mydict['owamp_ul_reordering'] = [None]

		try:
			mydict['owamp_dl_packets_sent'] = [measurements[1]['packets_sent']]
		except:
			mydict['owamp_dl_packets_sent'] = [None]

		try:
			mydict['owamp_dl_packets_lost'] = [measurements[1]['packets_lost']]
		except:
			mydict['owamp_dl_packets_lost'] = [None]

		try:
			mydict['owamp_dl_loss_percentage'] = [measurements[1]['loss_percentage']]
		except:
			mydict['owamp_dl_loss_percentage'] = [None]

		try:
			mydict['owamp_dl_duplicates'] = [measurements[1]['duplicates']]
		except:
			mydict['owamp_dl_duplicates'] = [None]

		try:
			mydict['owamp_dl_delay_min'] = [measurements[1]['delay_min']]
		except:
			mydict['owamp_dl_delay_min'] = [None]

		try:
			mydict['owamp_dl_delay_median'] = [measurements[1]['delay_median']]
		except:
			mydict['owamp_dl_delay_median'] = [None]

		try:
			mydict['owamp_dl_delay_max'] = [measurements[1]['delay_max']]
		except:
			mydict['owamp_dl_delay_max'] = [None]

		try:
			mydict['owamp_dl_jitter'] = [measurements[1]['jitter']]
		except:
			mydict['owamp_dl_jitter'] = [None]

		try:
			mydict['owamp_dl_hops'] = [measurements[1]['hops']]
		except:
			mydict['owamp_dl_hops'] = [None]

		try:
			mydict['owamp_dl_reordering'] = [measurements[1]['reordering']]
		except:
			mydict['owamp_dl_reordering'] = [None]

		return mydict

	def get_twamp_stats(self,host,packs,interval,packet_size=1200):
		print('(Monitor) DBG: Entered TWAMP at:' + str(self.helper.get_str_timestamp()))
		print('(Monitor) DBG: packs=' + str(packs)+',packetSize='+str(packet_size)+',interval='+str(interval)+'...')

		cmd = ["twping", "-c", str(packs), "-s", str(packet_size), "-i", str(interval), host]
		result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		if result.returncode != 0:
			print(f"Error running twping: {result.stderr}")
			output=None
		else:
			output=result.stdout

		data = {}
		lines = output.split('\n')
		print(output)
		for line in lines:
			if "sent, " in line:
				match = re.search(r"(\d+) sent, (\d+) lost \(([\d\.]+)%\)", line)
				if match:
					data["sent"] = int(match.group(1))
					data["lost"] = int(match.group(2))
					data["loss_percentage"] = float(match.group(3))
			elif "round-trip time min/median/max" in line:
				match = re.search(r"([\d\.]+)/([\d\.]+)/([\d\.]+) ms", line)
				if match:
					data["rtt_min"] = float(match.group(1))
					data["rtt_median"] = float(match.group(2))
					data["rtt_max"] = float(match.group(3))
			elif "send time min/median/max" in line:
				match = re.search(r"([\d\.]+)/([\d\.]+)/([\d\.]+) ms", line)
				if match:
					data["send_min"] = float(match.group(1))
					data["send_median"] = float(match.group(2))
					data["send_max"] = float(match.group(3))
			elif "reflect time min/median/max" in line:
				match = re.search(r"([\d\.-]+)/([\d\.-]+)/([\d\.-]+) ms", line)
				if match:
					data["reflect_min"] = float(match.group(1))
					data["reflect_median"] = float(match.group(2))
					data["reflect_max"] = float(match.group(3))
			elif "reflector processing time min/max" in line:
				match = re.search(r"([\d\.]+)/([\d\.]+) ms", line)
				if match:
					data["reflector_min"] = float(match.group(1))
					data["reflector_max"] = float(match.group(2))
			elif "two-way jitter" in line:
				match = re.search(r"([\d\.]+) ms", line)
				if match:
					data["two_way_jitter"] = float(match.group(1))
			elif "send jitter" in line:
				match = re.search(r"([\d\.]+) ms", line)
				if match:
					data["send_jitter"] = float(match.group(1))
			elif "reflect jitter" in line:
				match = re.search(r"([\d\.]+) ms", line)
				if match:
					data["reflect_jitter"] = float(match.group(1))
		mydict={}
		try:
			mydict['twamp_sent']=[data['sent']]
		except:
			mydict['twamp_sent']=[None]

		try:
			mydict['twamp_lost']=[data['lost']]
		except:
			mydict['twamp_lost']=[None]

		try:
			mydict['twamp_loss_percentage']=[data['loss_percentage']]
		except:
			mydict['twamp_loss_percentage']=[None]

		try:
			mydict['twamp_rtt_min']=[data['rtt_min']]
		except:
			mydict['twamp_rtt_min']=[None]

		try:
			mydict['twamp_rtt_median']=[data['rtt_median']]
		except:
			mydict['twamp_rtt_median']=[None]

		try:
			mydict['twamp_rtt_max']=[data['rtt_max']]
		except:
			mydict['twamp_rtt_max']=[None]

		try:
			mydict['twamp_send_min']=[data['send_min']]
		except:
			mydict['twamp_send_min']=[None]

		try:
			mydict['twamp_send_median']=[data['send_median']]
		except:
			mydict['twamp_send_median']=[None]

		try:
			mydict['twamp_send_max']=[data['send_max']]
		except:
			mydict['twamp_send_max']=[None]

		try:
			mydict['twamp_reflect_min']=[data['reflect_min']]
		except:
			mydict['twamp_reflect_min']=[None]

		try:
			mydict['twamp_reflect_median']=[data['reflect_median']]
		except:
			mydict['twamp_reflect_median']=[None]

		try:
			mydict['twamp_reflect_max']=[data['reflect_max']]
		except:
			mydict['twamp_reflect_max']=[None]

		try:
			mydict['twamp_reflector_min'] = [data['reflector_min']]
		except:
			mydict['twamp_reflector_min'] = [None]

		try:
			mydict['twamp_reflector_max'] = [data['reflector_max']]
		except:
			mydict['twamp_reflector_max'] = [None]

		try:
			mydict['twamp_two_way_jitter'] = [data['two_way_jitter']]
		except:
			mydict['twamp_two_way_jitter'] = [None]

		try:
			mydict['twamp_send_jitter'] = [data['send_jitter']]
		except:
			mydict['twamp_send_jitter'] = [None]

		try:
			mydict['twamp_reflect_jitter'] = [data['reflect_jitter']]
		except:
			mydict['twamp_reflect_jitter'] = [None]

		return mydict

	def get_pyshark_kpis(self,my_iface='Ethernet',display_filter=None,max_packs=5000):
		print('(Monitor) DBG: Initiate pyshark kpis ...')

		# hack to get all available veth-xxx interfaces (not supported by Pyshark)
		#my_iface=None
		#try:
		#	# expect this to fail and raise an exception with all available interfaces
		#	cap=pyshark.LiveCapture(interface='this_is_not_an_interface_100_percent!!', display_filter=display_filter)
		#	cap.sniff(timeout=1)
		#except Exception as ex:
		#	print('(Monitor) DBG: Getting available veth interfaces in the system...')
		#	# get all words of the exception str
		#	word_list=str(ex).split()
		#	for el in word_list:
		#		if 'veth' in el:
		#			my_iface=el
		#			break

		#if my_iface is None:
		#	print('(Monitor) ERROR: No veth ifaces found')
		#	return None

		try:
			attempt=1
			res=None
			while (res is None):
				try:
					print('(Monitor) DBG: Initiate capture for veth='+str(my_iface)+' (attempt=' + str(attempt) + ')...')
					if attempt > 1:
						self.helper.wait(gparams._WAIT_SEC_BACKEND_READ_INPUT_SOURCES)
					attempt = attempt + 1

					cap = pyshark.LiveCapture(interface=my_iface, display_filter=display_filter)
					cap.sniff(timeout=1)
					res=200
				except:
					if attempt >= 5:
						print('(Monitor) ERROR: Cannot find iface in Pyshark!')
						res = 500
			if res!=200:
				print('(Monitor) ERROR: Exiting...')
				exit()
			df=None

			found_first_correct_pack=False
			pack_cnt=0

			for pack in cap:
				if pack_cnt>max_packs:
					break
				pack_cnt = pack_cnt + 1

				mydict={}

				try:
					mydict['id']=[pack_cnt]
				except:
					pass

				try:
					mydict['time']=[pack.sniff_time]
				except:
					mydict['time']=[None]

				try:
					mydict['timestamp']=[float(pack.sniff_timestamp)]
				except:
					mydict['timestamp'] = [None]

				try:
					mydict['protocol']=[pack.highest_layer]
				except:
					mydict['protocol'] = [None]

				try:
					mydict['len_bytes']=[float(pack.length)]
				except:
					mydict['len_bytes'] = [None]

				try:
					mydict['addr_src']=[pack.ip.src]
				except:
					mydict['addr_src'] = [None]

				try:
					mydict['port_src']=[pack[pack.transport_layer].srcport]
				except:
					mydict['port_src'] = [None]

				try:
					mydict['addr_dest']=[pack.ip.dst]
				except:
					mydict['addr_dest'] = [None]

				try:
					mydict['port_dest']=[pack[pack.transport_layer].dstport]
				except:
					mydict['port_dest'] = [None]

				try:
					mydict['rtt']=[float(pack.tcp.analysis_ack_rtt)]
				except:
					mydict['rtt'] = [None]

				try:
					str_p=str(pack)
					if (
						"TCP Dup ACK" in str_p
						or "TCP Previous" in str_p
						or "TCP Retransmission" in str_p
						or "TCP Fast Retransmission" in str_p
						or "Out-Of-Order" in str_p
						or "TCP Spurious Retransmission" in str_p):
						res=True
					else:
						res=False

					mydict['drop']=[res]
				except:
					mydict['drop'] = [None]

				new_row = pd.DataFrame(mydict)
				if found_first_correct_pack:
					df = pd.concat([df, new_row], axis=0, ignore_index=True, join='outer')
				else:
					df=new_row
					found_first_correct_pack=True


			#print(df[df.isnull().any(axis=1)])
			#print(df[df.isna().any(axis=1)])

			res_dict={}

			try:
				total_packs = len(df.index)
				res_dict['total_packs'] = [total_packs]
			except:
				res_dict['total_packs'] = [None]

			try:
				total_bytes = df['len_bytes'].sum()
				res_dict['total_bytes'] = [total_bytes]
			except:
				res_dict['total_bytes'] = [None]

			try:
				total_time = df['time'].max() - df['time'].min()
				res_dict['total_time'] = [total_time]
			except:
				res_dict['total_time'] = [None]

			try:
				total_timestamp = df['timestamp'].max() - df['timestamp'].min()
				res_dict['total_timestamp'] = [total_timestamp]
			except:
				res_dict['total_timestamp'] = [None]


			try:
				mean_rtt = df['rtt'].mean()
				res_dict['mean_rtt'] = [mean_rtt]
			except:
				res_dict['mean_rtt'] = [None]

			try:
				sd_rtt_jitter = df['rtt'].std()
				res_dict['sd_rtt_jitter'] = [sd_rtt_jitter]
			except:
				res_dict['sd_rtt_jitter'] = [None]

			try:
				throughput_bps = (8 * total_bytes) / total_timestamp
				res_dict['throughput_bps'] = [throughput_bps]
			except:
				res_dict['throughput_bps'] = [None]

			try:
				drop_perc = (df[df['drop'] == True].shape[0]) / df.shape[0]
				res_dict['drop_perc'] = [drop_perc]
			except:
				res_dict['drop_perc'] = [None]

			try:
				arrive_perc = (df[df['drop'] == False].shape[0]) / df.shape[0]
				res_dict['arrive_perc'] = [arrive_perc]
			except:
				res_dict['arrive_perc'] = [None]

			res_df=pd.DataFrame(res_dict)
			return res_df,res_dict

		except Exception as ex:
			print('(Monitor) ERROR: Pyshark kpis fail=' + str(ex))
			return None

