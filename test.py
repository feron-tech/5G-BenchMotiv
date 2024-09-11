import os
import gparams
import helper

helper=helper.Helper()

df_app = helper.read_jsonlines2pandas(loc=gparams._RES_FILE_LOC_APP)

list_of_repeat_id=df_app['repeat_id'].unique()
list_of_exp_id=df_app['exp_id'].unique()
list_of_apps = df_app['app_name'].unique()

final_list_of_dicts=[]

for _app in list_of_apps:
	for _repeat_id in list_of_repeat_id:
		for _exp_id in list_of_exp_id:
			curr_df=df_app.loc[ (df_app['app_name'] == _app) & (df_app['exp_id'] == _exp_id) & (df_app['repeat_id'] == _repeat_id)]


			min_time= curr_df['sniff_timestamp'].min()
			max_time= curr_df['sniff_timestamp'].max()
			total_bytes= curr_df['pack_len_bytes'].sum()
			mean_rtt_sec=curr_df['rtt'].mean()
			time_diff= max_time - min_time
			thru_bps= float((total_bytes * 8) / time_diff),

			mydict={
				'mean_rtt_msec':mean_rtt_sec*1e3,
				'app_name':_app,
				'thru_mbps':float(thru_bps*1e-6),
				'max_timestamp':curr_df['timestamp'].max()
			}
			final_list_of_dicts.append(mydict)





