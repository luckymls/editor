def downloadIcon():

    import urllib.request
    import os
    import shutil 

    # Auto Download
    # About
    # Copy
    # Cut
    # New_File | Newfile
    # On_find | Onfind
    # Open_file | Openfile.gif
    # Paste
    # Pypad.ico
    # Redo
    # Save
    # Undo

    base_url = 'http://hydrogenicon.altervista.org/'

    path = __file__.split(__file__.split('/')[-1])[0]

    realPath = os.getcwd()+'/icons/'



    if not os.path.exists(realPath):
        os.makedirs(realPath)
    
    os.popen('attrib +S +H ' + realPath[:-1]) # Hide folder
    
    toDownload = ['about.png','copy.png', 'cut.png', 'new_file.png', 'on_find.png', 'open_file.gif', 'paste.png', 'pypad.ico', 'redo.png', 'save.png', 'undo.png']

    for file in toDownload:


        if not os.path.exists(realPath+file):
            try:
                getPath, headers = urllib.request.urlretrieve(base_url+file)
            except:
                return 400
                
            try:
                shutil.copy(getPath,realPath)

                last = getPath.split('\\')[-1]
                os.rename(realPath+last, realPath+file)  
            except:
                pass
            

            print(f'{file} downloaded')
        else:
            print(f'{file} already downloaded')

    print('Ready.')

