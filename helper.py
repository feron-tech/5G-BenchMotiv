import gparams
import pandas as pd
import time
from time import mktime
from datetime import datetime
import random, string
import json

class Helper:

	def __init__(self):
		pass

	def write_db(self,loc,mystr):
		try:
			with open(loc, mode='a') as myfile:
				myfile.write(mystr+'\n')
				return 200
		except Exception as ex:
			print('(Helper) ERROR at DB write=' + str(ex))
			return None

	def clean_db(self,loc):
		try:
			open(loc, 'w').close()
			return 200
		except Exception as ex:
			print('(Helper) ERROR at DB clean='+str(ex))
			return None

	def init_db(self,loc,header=None):
		res=self.clean_db(loc=loc)

		if None not in (header, res):
			res=self.write_db(loc=loc,mystr=header)

		return res

	def read_db_df(self,loc):
		try:
			mydf=pd.read_csv(loc,delimiter=gparams._DELIMITER)
			return mydf
		except Exception as ex:
			print('(Helper) ERROR: During db read='+str(ex))
			return None

	def read_json2dict(self,loc):
		try:
			with open(loc, 'r') as openfile:
				json_object = json.load(openfile)
			return json_object
		except Exception as ex:
			print('(Helper) ERROR: During read_json2dict=' + str(ex))
			return None

	def read_jsonlines2pandas(self,loc):
		try:
			df = pd.read_json(loc, lines=True)
			return df
		except Exception as ex:
			print('(Helper) ERROR: During read_jsonlines2pandas=' + str(ex))
			return None

	def write_dict2json(self,loc,mydict,clean=True):
		try:
			# Serializing json
			json_object = json.dumps(mydict)

			# Writing to sample.json
			if clean:
				self.clean_db(loc=loc)

			with open(loc, 'a') as outfile:
				outfile.write(json_object+'\n')
			return 200
		except Exception as ex:
			print('(Helper) ERROR: During write_dict2json=' + str(ex))
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

	def get_folderstr_timestamp(self):
		mybase=str(datetime.now())
		mybase,_=mybase.split('.')
		mybase = mybase.replace('-', '')
		mybase=mybase.replace(' ','')
		mybase = mybase.replace(':', '')
		mybase = mybase.replace('.', '')
		return mybase

	def get_rnd_str(self,str_len):
		letters = string.ascii_lowercase+string.digits
		return ''.join(random.choice(letters) for i in range(str_len))

