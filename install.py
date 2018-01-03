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
    
    winPath = os.getcwd()+'\\'+'win.reg'
    os.popen(f'start {winPath}') #Imposto valore registro
    
    pathCommon = os.environ['COMMONPROGRAMFILES(X86)']
    pathCommon = '\\'.join(path.split('\\')[:-1]) #Spostare con copytree tutta la cartella in (X86)
    
    shutil.copytree(f'{program_dir}', pathCommon)
    
elif not os.path.exists(path) and isLinux:
    shutil.copytree(f'{program_dir}', path)
    try:
        os.system('gksudo ln -s main.py hydrogen || gksu ln -s main.py hydrogen')
        os.system('gksudo chmod +x main.py')
        os.system('gksudo mv hydrogen /usr/bin/')
        os.system('gksudo mv hydrogen.desktop /usr/share/applications/hydrogen.desktop')
    except:
        pass
	
	# Creare un file .desktop in /usr/share/applications che definisca le estensioni lette dal programma
	# Creare un link in /usr/bin all'eseguibile
	
