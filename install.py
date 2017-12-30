import shutil
import os
import sys

if sys.platform[:5].lower() == 'linux':
	isLinux = 1
else:
	isLinux = 0

program_dir = os.getcwd()

def reAssemble(arg=None):
    global isLinux
    res = ''
    for Dir in arg:
        if not isLinux:
            res += Dir+'\\'
        else:
            res += Dir+'/'
    if isLinux:
        return res+'.editorX_Z'
    else:
        return res+'editorX_Z'

if isLinux:
	path = reAssemble(program_dir.split('/')[:-1])
else:
	path = reAssemble(program_dir.split('\\')[:-1])
    
    
if not isLinux and not os.path.exists(path):
    
    shutil.copytree(f'{program_dir}', path)
    os.popen('attrib +S +H ' + path)
    # https://msdn.microsoft.com/en-us/library/windows/desktop/aa381058(v=vs.85).aspx Aggiungere questo file

elif not os.path.exists(path) and isLinux:
    shutil.copytree(f'{program_dir}', path)
    try:
        os.system('gksudo ln -s main.py hydrogen')
        os.system('gksudo chmod +x main.py')
        os.system('gksudo mv hydrogen /usr/bin/')
        os.system('gksudo mv hydrogen.desktop /usr/share/applications/hydrogen.desktop')
    except:
        try:
            os.system('gksu ln -s main.py hydrogen')
            os.system('gksudo chmod +x main.py')
            os.system('gksudo mv hydrogen /usr/bin/')
            os.system('gksudo mv hydrogen.desktop /usr/share/applications/hydrogen.desktop') except:
        except:
            pass
	# Aggiungere apri con, la copia viene già effettuata e il file viene nascosto anteponendo il punto
	# Creare un file .desktop in /usr/share/applications che definisca le estensioni lette dal programma
	# Creare un link in /usr/bin all'eseguibile
	

