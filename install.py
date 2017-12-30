import shutil
import os
import sys

if sys.platform[:5].lower() == 'linux':
	isLinux = 1
else:
	isLinux = 0operating_sys = sys.platform
	
program_dir = os.getcwd()
if not isLinux:
	if not os.path.exists('C:\Program Files (x86)\hydrogen'):
		os.makedirs('C:\Program Files (x86)\hydrogen')
	shutil.copytree(f'{program_dir}', 'C:\Program Files (x86)\hydrogen')
	os.system(f'pathman /au C:\Program Files (x86)\hydrogen')

else:
	pass
	# copy_tree(f'
