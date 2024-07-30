import os

if os.name == 'nt':
    _ROOT_DIR='C:\\Pycharm\\Projects\\sniffer'
else:
    _ROOT_DIR='/home/simu5g/git/sniffer'

_DELIMITER=';'
_DB_DIR=os.path.join(_ROOT_DIR,'db')

_DB_FILE_LOC_INPUT_USER=os.path.join(_DB_DIR,'db_input_user.csv')
_DB_FILE_FIELDS_INPUT_USER='in_set_client_ip;in_set_server_ip;in_set_num_packets;in_set_exp_duration;in_stats_thru;' \
                           'in_stats_rtt;in_stats_e2e_delay;in_app_base;in_app_mqtt;' \
                           'in_app_video_stream;in_app_profinet'

_DB_FILE_LOC_OUTPUT_BASE=os.path.join(_DB_DIR,'db_output_base.csv')
_DB_FILE_FIELDS_OUTPUT_BASE='camp_name;camp_id;exp_id;timestamp;ping_rtt_avg;ping_rtt_max;ping_rtt_min;ping_packet_loss_perc;' \
                            'ping_packets_lost;ping_jitter;' \
                            'iperf_tcp_dl_retransmits;iperf_tcp_dl_sent_bps;iperf_tcp_dl_sent_bytes;' \
                            'iperf_tcp_dl_received_bps;iperf_tcp_dl_received_bytes;iperf_tcp_ul_retransmits;' \
                            'iperf_tcp_ul_sent_bps;iperf_tcp_ul_sent_bytes;iperf_tcp_ul_received_bps;' \
                            'iperf_tcp_ul_received_bytes;iperf_udp_dl_bytes;iperf_udp_dl_bps;' \
                            'iperf_udp_dl_jitter_ms;iperf_udp_dl_lost_percent;iperf_udp_ul_bytes;' \
                            'iperf_udp_ul_bps;iperf_udp_ul_jitter_ms;iperf_udp_ul_lost_percent'

_DB_FILE_LOC_OUTPUT_APP=os.path.join(_DB_DIR,'db_output_app.csv')
_DB_FILE_FIELDS_OUTPUT_APP='camp_name;camp_id;exp_id;timestamp;app;total_packs;total_bytes;total_time;total_timestamp;' \
                           'mean_rtt;sd_rtt_jitter;throughput_bps;drop_perc;arrive_perc'

_DB_FILE_LOC_OUTPUT_LOG=os.path.join(_DB_DIR,'db_output_log.csv')
_DB_FILE_FIELDS_OUTPUT_LOG='time;description'

_DB_FILE_LOC_OUTPUT_PHY=os.path.join(_DB_DIR,'db_output_phy.csv')
_DB_FILE_FIELDS_OUTPUT_PHY=('camp_name;camp_id;exp_id;timestamp;'
                            'mode_pref;oper;act;apn;resp1;rssi;ber;qrsrp_prx;qrsrp_drx;qrsrp_rx2;qrsrp_rx3'
                            ';qrsrp_sysmode;rsrq_prx;rsrq_drx;rsrq_rx2;rsrq_rx3;rsrq_sysmode;'
                            'sinr_prx;sinr_drx;sinr_rx2;sinr_rx3;sinr_sysmode')
## ports
_PORT_SERVER_IPERF=5201
_PORT_SERVER_MQTT1=1883
_PORT_SERVER_MQTT2=8883
_PORT_SERVER_OPENCV=8888

_PORT_CLIENT_GUI=8050

## timeouts
_ATTEMPTS_BACKEND_READ_INPUT_SOURCES=1e6
_WAIT_SEC_BACKEND_READ_INPUT_SOURCES=15

## app settings
_MQTT_MAX_PAYLOAD=300
_PHY_PORT='/dev/ttyUSB3'
_PHY_BAUD_RATE=115200
_PHY_CMD='AT'
_PHY_APN='internet.vodafone.gr'

