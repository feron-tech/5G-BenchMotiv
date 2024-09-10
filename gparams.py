import os

#########################  input params  ########################
if os.name == 'nt':
    # windows OS
    _ROOT_DIR='C:\\Pycharm\\Projects\\golden_unit'
else:
    # linux OS
    _ROOT_DIR='/home/simu5g/git/golden_unit'
################################################################

# folder settings
_DB_DIR=os.path.join(_ROOT_DIR,'db')
_RES_DIR=os.path.join(_ROOT_DIR,'results')
_UDPPING_ROOT=os.path.join(os.path.join(_ROOT_DIR,'client'),'udp-ping')
_UDPPING_DELIMITER=';'
_OWAMP_DELIMITER=';'
_TWAMP_DELIMITER=';'
_DELIMITER=';'

_DB_FILE_LOC_OUTPUT_BASE=os.path.join(_DB_DIR,'db_output_base.json')
_DB_FILE_FIELDS_OUTPUT_BASE=('camp_name;camp_id;exp_id;timestamp;'
                             'ping_rtt_avg;ping_rtt_max;ping_rtt_min;ping_packet_loss_perc;' 
                            'ping_packets_lost;ping_jitter;' 
                            'iperf_tcp_dl_retransmits;iperf_tcp_dl_sent_bps;iperf_tcp_dl_sent_bytes;' 
                            'iperf_tcp_dl_received_bps;iperf_tcp_dl_received_bytes;iperf_tcp_ul_retransmits;' 
                            'iperf_tcp_ul_sent_bps;iperf_tcp_ul_sent_bytes;iperf_tcp_ul_received_bps;' 
                            'iperf_tcp_ul_received_bytes;iperf_udp_dl_bytes;iperf_udp_dl_bps;' 
                            'iperf_udp_dl_jitter_ms;iperf_udp_dl_lost_percent;iperf_udp_ul_bytes;' 
                            'iperf_udp_ul_bps;iperf_udp_ul_jitter_ms;iperf_udp_ul_lost_percent;'
                             'owamp_ul_packets_sent;'
                             'owamp_ul_packets_lost;'
                             'owamp_ul_loss_percentage;'
                             'owamp_ul_duplicates;'
                             'owamp_ul_delay_min;'
                             'owamp_ul_delay_median;'
                             'owamp_ul_delay_max;'
                             'owamp_ul_jitter;'
                             'owamp_ul_hops;'
                             'owamp_ul_reordering;'
                             'owamp_dl_packets_sent;'
                             'owamp_dl_packets_lost;'
                             'owamp_dl_loss_percentage;'
                             'owamp_dl_duplicates;'
                             'owamp_dl_delay_min;'
                             'owamp_dl_delay_median;'
                             'owamp_dl_delay_max;'
                             'owamp_dl_jitter;'
                             'owamp_dl_hops;'
                             'owamp_dl_reordering;'
                             'twamp_sent;twamp_lost;twamp_loss_percentage;twamp_rtt_min;'
                             'twamp_rtt_median;twamp_rtt_max;twamp_send_min;twamp_send_median;twamp_send_max;'
                             'twamp_reflect_min;twamp_reflect_median;twamp_reflect_max;twamp_reflector_min;'
                             'twamp_reflector_max;twamp_two_way_jitter;twamp_send_jitter;twamp_reflect_jitter;'
                             'udpping_cl2server_ns;udpping_server2cl_ns;udpping_rtt_ns'
                             )

_DB_FILE_LOC_OUTPUT_APP=os.path.join(_DB_DIR,'db_output_app.json')
_DB_FILE_FIELDS_OUTPUT_APP='camp_name;camp_id;exp_id;timestamp;app;total_packs;total_bytes;total_time;total_timestamp;' \
                           'mean_rtt;sd_rtt_jitter;throughput_bps;drop_perc;arrive_perc'


_RES_FILE_LOC_PHY=os.path.join(_DB_DIR,'phy.json')
_RES_FILE_FIELDS_PHY={
    'timestamp':None,
    'mode_pref':None,
    'oper':None,
    'act':None,
    'apn':None,
    'resp1':None,
    'rssi':None,
    'ber':None,
    'qrsrp_prx':None,
    'qrsrp_drx':None,
    'qrsrp_rx2':None,
    'qrsrp_rx3':None,
    'qrsrp_sysmode':None,
    'rsrq_prx':None,
    'rsrq_drx':None,
    'rsrq_rx2':None,
    'rsrq_rx3':None,
    'rsrq_sysmode':None,
    'sinr_prx':None,
    'sinr_drx':None,
    'sinr_rx2':None,
    'sinr_rx3':None,
    'sinr_sysmode':None
}

_RES_FILE_LOC_IPERF=os.path.join(_DB_DIR,'iperf.json')
_RES_FILE_FIELDS_IPERF={
    'camp_name': None,
    'repeat_id': None,
    'exp_id': None,
    'timestamp': None,
    'tcp_dl_retransmits': None,
    'tcp_dl_sent_bps': None,
    'tcp_dl_sent_bytes': None,
    'tcp_dl_received_bps': None,
    'tcp_dl_received_bytes': None,
    'tcp_ul_retransmits': None,
    'tcp_ul_sent_bps': None,
    'tcp_ul_sent_bytes': None,
    'tcp_ul_received_bps': None,
    'tcp_ul_received_bytes': None,
    'udp_dl_bytes': None,
    'udp_dl_bps': None,
    'udp_dl_jitter_ms': None,
    'udp_dl_lost_percent': None,
    'udp_ul_bytes': None,
    'udp_ul_bps': None,
    'udp_ul_jitter_ms': None,
    'udp_ul_lost_percent': None
}

_RES_FILE_LOC_ICMP=os.path.join(_DB_DIR,'icmp.json')
_RES_FILE_FIELDS_ICMP={
    'camp_name': None,
    'repeat_id': None,
    'exp_id': None,
    'timestamp': None,
    'min_rtt_ms': None,
    'avg_rtt_ms': None,
    'max_rtt_ms': None,
    'rtts_ms': None,
    'packets_sent': None,
    'packets_received': None,
    'packet_loss_0to1': None,
    'jitter_ms': None
}

_RES_FILE_LOC_UDPPING=os.path.join(_DB_DIR,'udpping.json')
_RES_FILE_FIELDS_UDPPING=[
    'seq_nr',
    'send_time',
    'server_time',
    'receive_time',
    'client2server_ns',
    'server2client_ns',
    'rtt_ns'
]

_RES_FILE_LOC_OWAMP=os.path.join(_DB_DIR,'owamp.json')
_RES_FILE_FIELDS_OWAMP=[
    'seq_nr',
    'tx_time',
    'tx_sync',
    'tx_err_perc',
    'rx_time',
    'rx_sync',
    'rx_err_perc',
    'ttl'
]
_KEY_WORD_OWAMP='seq_nr'
_DBG_KEY_WORD_OWAMP='tx_sync'

_RES_FILE_LOC_TWAMP=os.path.join(_DB_DIR,'twamp.json')
_RES_FILE_FIELDS_TWAMP=[
'tx_seq_nr',
'tx_time',
'tx_sync',
'tx_err_perc',
'tx_rx_time',
'tx_rx_sync',
'tx_rx_err_perc',
'tx_ttl',
'reflect_seq_nr',
'reflect_tx_time',
'reflect_tx_sync',
'reflect_tx_err_perc',
'rx_time',
'rx_sync',
'rx_err_perc',
'reflect_ttl',
]
_DBG_KEY_WORD_TWAMP='tx_sync'

_DB_FILE_LOC_INPUT_USER=os.path.join(_DB_DIR,'db_input_user.json')

_DB_FILE_LOC_OUTPUT_LOG=os.path.join(_DB_DIR,'db_output_log.json')
_DB_FILE_FIELDS_OUTPUT_LOG='time;description'

## ports
_PORT_SERVER_IPERF=5201
_PORT_SERVER_MQTT1=1883
_PORT_SERVER_MQTT2=8883
_PORT_SERVER_OPENCV=8888
_PORT_SERVER_UDP_PING=1234

_PORT_CLIENT_GUI=8050
_PORT_CLIENT_UDP_PING=1234

## timeouts
_ATTEMPTS_BACKEND_READ_INPUT_SOURCES=1e6
_WAIT_SEC_BACKEND_READ_INPUT_SOURCES=15

## local test
_LOCAL_TEST=True
