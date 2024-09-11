import os
import gparams
for file in os.listdir(gparams._DB_DIR):
	filename = os.fsdecode(file)
	print(str(filename))