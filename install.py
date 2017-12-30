from dist_utils.dir_util import copy_tree
import os
import sys

operating_sys = sys.platform
program_dir = os.getcwd()
if not operating_sys == 'linux':
	copy_tree(f'program_dir', 'C:\Program Files (x86)\hydrogen\')

else:
	pass
	# copy_tree(f'
