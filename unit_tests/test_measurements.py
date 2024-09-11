import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

root='C:\\Pycharm\\Projects\\golden_unit\\ericsson_tests\\'
folder_list_mmwave=[
             'id01_day1_exp_2',
             'id02_day1_exp_3',
             'id03_day1_exp_4',
             'id04_day1_exp_5',
             'id05_day1_exp_6',
             'id06_day2_exp1',
             'id07_day2_exp2_baseline'
]

folder_list_midband=[
    'id08_day2_mid_exp2',
    'id09_day2_mid_exp6_512',
    'id10_day2_mid_exp7_60kpackets',
    'id11_day2_mid_exp4_small_pack',
    'id12_day2_mid_exp5_fast',
    'id13_day2_mid_exp3_slow',
    'id14_day2_mid_exp1'
]

folder_list=folder_list_mmwave
folder_list.extend(folder_list_midband)

db_base_name='db_output_base.csv'
db_app_name='db_output_app.csv'
db_phy_name='db_output_phy.csv'

def get_thru_test():
    cnt=0
    merged_df=None
    for exp_name in folder_list:
        print('New=' + str(exp_name))
        myfolder = os.path.join(root, exp_name)
        db_base = os.path.join(myfolder, db_base_name)
        db_app = os.path.join(myfolder, db_app_name)
        db_phy = os.path.join(myfolder, db_phy_name)

        df_app = pd.read_csv(db_app, delimiter=';')

        df_app=df_app.loc[df_app['app'] == 'video_stream']

        df_app['id']=str(exp_name)
        df_app['throughput_Gbps'] = df_app['throughput_bps'].apply(lambda x: x * 1e-9)

        df_temp = df_app[['id', 'app','throughput_Gbps']]

        if cnt<1:
            merged_df=df_temp
        else:
            merged_df = pd.concat([merged_df, df_temp])
        cnt=cnt+1
    print(str(merged_df))
    merged_df.to_csv('thru_test.csv')

def get_stats_per_exp(_phy=True,_app=True,_base=True):
    for exp_name in folder_list:
        print('New='+str(exp_name))
        myfolder=os.path.join(root,exp_name)
        db_base=os.path.join(myfolder,db_base_name)
        db_app = os.path.join(myfolder, db_app_name)
        db_phy = os.path.join(myfolder, db_phy_name)

        df_base=pd.read_csv(db_base,delimiter=';')
        df_app = pd.read_csv(db_app,delimiter=';')
        df_phy = pd.read_csv(db_phy,delimiter=';')

        if _base:
            res=df_base['ping_rtt_avg'].mean()
            print('ping_rtt_avg_ms'+'='+str(res))

            res=df_base['ping_packet_loss_perc'].mean()
            print('ping_packet_loss_perc'+'='+str(res))

            res=df_base['ping_jitter'].mean()
            print('ping_jitter'+'='+str(res))

            res=df_base['iperf_tcp_dl_sent_bps'].mean()
            res=res*1e-6
            print('iperf_tcp_dl_sent_Mbps'+'='+str(res))

            res=df_base['iperf_tcp_dl_received_bps'].mean()
            res=res*1e-6
            print('iperf_tcp_dl_received_Mbps'+'='+str(res))

            res=df_base['iperf_tcp_ul_sent_bps'].mean()
            res=res*1e-6
            print('iperf_tcp_ul_sent_Mbps'+'='+str(res))

            res=df_base['iperf_tcp_ul_received_bps'].mean()
            res=res*1e-6
            print('iperf_tcp_ul_received_Mbps'+'='+str(res))

            res=df_base['iperf_udp_dl_bps'].mean()
            res=res*1e-6
            print('iperf_udp_dl_Mbps'+'='+str(res))

            res=df_base['iperf_udp_ul_bps'].mean()
            res=res*1e-6
            print('iperf_udp_ul_Mbps'+'='+str(res))

        if _app:
            print('app-level---------------')
            for  myapp in ['video_stream','mqtt']:
                print('----'+str(myapp))
                df_temp=df_app.loc[df_app['app'] == myapp]

                res = df_temp['mean_rtt'].mean()
                res=res*1e3
                print('mean_rtt_MS' + '=' + str(res))

                res = df_temp['sd_rtt_jitter'].mean()
                res=res*1e3
                print('sd_rtt_jitter_MS' + '=' + str(res))

                res = df_temp['throughput_bps'].mean()
                res=res*1e-9
                print('throughput_Gbps' + '=' + str(res))

                res = df_temp['drop_perc'].mean()
                print('drop_perc' + '=' + str(res))

                print('samples='+str(len(df_temp.index)))

        if _phy:
            print('phy---------------')

            res = df_phy['rssi'].mean()
            print('rssi' + '=' + str(res))

            res = df_phy['ber'].mean()
            print('ber' + '=' + str(res))

            res = df_phy['sinr_prx'].mean()
            print('sinr_prx' + '=' + str(res))

            res = df_phy['sinr_drx'].mean()
            print('sinr_drx' + '=' + str(res))

            res = df_phy['qrsrp_prx'].mean()
            print('qrsrp_prx' + '=' + str(res))

            res = df_phy['qrsrp_drx'].mean()
            print('qrsrp_drx' + '=' + str(res))

        print('----------------------------')

def get_cdf_plotter(sample_list,bins=50):
    count, bins_count = np.histogram(sample_list, bins=bins)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    return bins_count[1:],cdf

def get_ping_cdfs(_draw='mmWave',_include_ping=True):


    if _draw=='mmWave':
        my_folder_list=folder_list_mmwave
    else:
        my_folder_list = folder_list_midband

    cnt=0
    for exp_name in my_folder_list:
        print('New=' + str(exp_name))
        myfolder = os.path.join(root, exp_name)
        db_base = os.path.join(myfolder, db_base_name)

        new_df = pd.read_csv(db_base, delimiter=';')

        if cnt<1:
            merged_df=new_df
        else:
            merged_df = pd.concat([merged_df, new_df])
        cnt=cnt+1

    merged_df['owamp_ulNdl_delay_median']=merged_df['owamp_ul_delay_median']+merged_df['owamp_dl_delay_median']

    ping_rtt_avg_list = merged_df['ping_rtt_avg'].tolist()
    owamp_ulNdl_delay_median_list = merged_df['owamp_ulNdl_delay_median'].tolist()
    twamp_rtt_median_list = merged_df['twamp_rtt_median'].tolist()

    ping_rtt_avg_list = [x for x in ping_rtt_avg_list if str(x) != 'nan']
    owamp_ulNdl_delay_median_list = [x for x in owamp_ulNdl_delay_median_list if str(x) != 'nan']
    twamp_rtt_median_list = [x for x in twamp_rtt_median_list if str(x) != 'nan']

    print(str(ping_rtt_avg_list))
    print(str(owamp_ulNdl_delay_median_list))
    print(str(twamp_rtt_median_list))

    ping_x,ping_y=get_cdf_plotter(ping_rtt_avg_list)
    ow_x,ow_y=get_cdf_plotter(owamp_ulNdl_delay_median_list)
    tw_x,tw_y=get_cdf_plotter(twamp_rtt_median_list)

    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    fig, ax1 = plt.subplots(constrained_layout=True)
    _LINEWIDTH=8
    _LABEL_SIZE=35
    _LEGEND_SIZE=30
    _TICK_PARAMS=35
    _TITLE_SIZE=30
    #ax1.set_xscale('log')
    if _include_ping:
        ax1.plot(ping_x, ping_y, 'k', label="Ping", linewidth=_LINEWIDTH + 1, linestyle='solid')
    ax1.plot(ow_x, ow_y, 'r', label="OWAMP", linewidth=_LINEWIDTH + 1, linestyle='solid')
    ax1.plot(tw_x, tw_y, 'b', label="TWAMP", linewidth=_LINEWIDTH + 1, linestyle='solid')

    ax1.set_title('Latency measurements: '+str(_draw) + str(' 5G'), fontdict={'fontsize': _TITLE_SIZE})
    ax1.set_xlabel('RTT (ms)', fontsize=_LABEL_SIZE)
    ax1.set_ylabel('CDF', fontsize=_LABEL_SIZE)
    #ax1.set_xlim(-0.001, 0.4)
    # ax1.set_ylim(_y_lim_begin, _y_lim_end)
    ax1.legend(loc='best', fontsize=_LEGEND_SIZE)
    ax1.grid(True, which='major', axis='both')
    ax1.tick_params(axis='both', which='major', labelsize=_TICK_PARAMS)
    ax1.tick_params(axis='both', which='minor', labelsize=_TICK_PARAMS)
    plt.show()

get_ping_cdfs(_draw='mmWave',_include_ping=False)
get_ping_cdfs(_draw='mid-band',_include_ping=False)