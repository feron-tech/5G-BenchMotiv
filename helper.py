import gparams
import pandas as pd
import time
from time import mktime
from datetime import datetime
import random, string

class Helper:

	def __init__(self):
		pass

	def init_db(self,loc,header=None):
		with open(loc, mode='w+') as myfile:
			if header is not None:
				myfile.write(header+'\n')

	def write_db(self,loc,mystr):
		with open(loc, mode='a') as myfile:
			myfile.write(mystr+'\n')

	def clean_db(self,loc):
		try:
			open(loc, 'w').close()
		except Exception as ex:
			print('(Helper) WARNING: Didnt find a db to clean='+str(ex))

	def read_db_df(self,loc):
		try:
			mydf=pd.read_csv(loc,delimiter=gparams._DELIMITER)
			return mydf
		except Exception as ex:
			print('(Helper) ERROR: During db read='+str(ex))
			return None

	def write_df2db(self,loc,df,header=False):
		try:
			df.to_csv(loc, sep=gparams._DELIMITER, encoding='utf-8',index=False,header=header,mode='a')
			return 200
		except Exception as ex:
			print('(Helper) ERROR: During db write='+str(ex))
			return None

	def create_csv_line(self,list_of_str):
		final_str=''
		for mystr in list_of_str:
			final_str=final_str+str(mystr)+gparams._DELIMITER
		final_str = final_str[:-1]
		return final_str

	def wait(self,time_sec):
		time.sleep(time_sec)

	def get_curr_time(self):
		return time.asctime(time.localtime(time.time()))

	def diff_betw_times(self,t1,t2):
		t1 = time.strptime(t1)
		t1 = mktime(t1)
		t2 = time.strptime(t2)
		t2 = mktime(t2)
		return t2-t1

	def get_str_timestamp(self):
		return str(datetime.now())

	def get_rnd_str(self,str_len):
		letters = string.ascii_lowercase+string.digits
		return ''.join(random.choice(letters) for i in range(str_len))

