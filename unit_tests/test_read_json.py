import gparams
import helper
mmy=helper.Helper()
dictt=mmy.read_json2dict(loc=gparams._DB_FILE_LOC_IN_USER)
res=dictt['Network']['Server IP']
print(str(res))
