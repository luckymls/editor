from dist_utils.dir_util import copy_tree
import os
import sys


if sys.platform[:5].lower() == 'linux':
	isLinux = 1
else:
	isLinux = 0
	
program_dir = os.getcwd()
if not isLinux:
	copy_tree(f'program_dir', 'C:\Program Files (x86)\hydrogen\')

else:
	pass
	# copy_tree(f'
