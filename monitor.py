import pyshark
import pandas as pd
import math
import docker
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
		try:
			print('(Monitor) DBG: Get ping for ip='+str(server_ip)+'...')

			res = ping(server_ip, count=packs, interval=interval,privileged=False)
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

	def get_iperf_stats(self,server_ip,port=5201,duration=10,protocol='tcp',direction_dl=False):
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

