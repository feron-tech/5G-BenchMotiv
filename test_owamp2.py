import subprocess
import gparams
from io import StringIO
import pandas as pd

server_ip = "192.168.200.117"
packs=5
interval_sec=0.020
payload_bytes=120

cmd=['owping']

cmd.append('-c')
cmd.append(str(packs))

cmd.append('-s')
cmd.append(str(payload_bytes))

cmd.append('-i')
cmd.append(str(interval_sec))

cmd.append('-R')

cmd.append(str(server_ip))

result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output = result.stdout

cols=[
    'SEQ',
    'STIME',
    'SS',
    'SERR',
    'RTIME',
    'RS',
    'RERR',
    'TTL'
]

output = output.replace(' ', ';')
output = output.replace('\n', '$')
output = output.replace('$', '\n')
df_str = StringIO(output)

df = pd.read_table(df_str, sep=';', header=None)
df.columns = cols

df['is_previous_larger'] = (df['SEQ'].shift(1) > df['SEQ']).astype(int)
mylist=df.index[df['is_previous_larger'] == 1].tolist()
df = df.drop('is_previous_larger', axis=1)
sep_raw=mylist[0]

df.loc[:sep_raw, 'direction'] = 'ul'
df.loc[sep_raw:, 'direction'] = 'dl'

print(str(df))










