import pandas as pd
from helper import Helper

a=Helper()

#b='{"a":1,"b":2}\n{"a":3,"b":4}'

#json_file='{"camp_name": "Test01","repeat_id": "0"}{"camp_name": "Test01","repeat_id": "0"}'
json_file='C:\\Users\\giorgos.drainakis\\Downloads\\app.json'
a.write_dict2json(loc=json_file,mydict={'a':1,'be':2},clean=True)
a.write_dict2json(loc=json_file,mydict={'a':3,'be':3},clean=False)

df=pd.read_json(json_file, lines=True)

print(str(df.describe()))