class Download:

    import os
    import json
    import socket
    import urllib
    from urllib import request
    import shutil
        
        

    def is_connected():
        
        try:
            socket.create_connection(("www.google.com", 80))
            return 1
        except OSError:
            pass
            return 0

    


    def icon(self, isLinux=0):

        



        base_url = 'http://hydrogenicon.altervista.org/'

        

        realPath = os.getcwd()+'/icons/'


        if not os.path.exists(realPath):
            os.makedirs(realPath)
            
        os.popen('attrib +S +H ' + realPath[:-1])
        
        toDownload = ['about.png','copy.png', 'cut.png', 'new_file.png', 'on_find.png', 'open_file.png', 'paste.png', 'pypad.ico', 'redo.png', 'save.png', 'undo.png']

        for file in toDownload:


            if not os.path.exists(realPath+file):
                try:
                    getPath, headers = urllib.request.urlretrieve(base_url+file)
                except:
                    return 400
                
                try:
                    shutil.copy(getPath,realPath)

                    if not isLinux:
                        last = getPath.split('\\')[-1]
                    else:
                        last = getPath.split('/')[-1]
                    os.rename(realPath+last, realPath+file)  
                except:
                    
                    pass

    


    
    def themes(nowTheme = {}):

        
        if is_connected():
        
            url = 'http://hydrogenicon.altervista.org/theme.php'

            response = urllib.request.urlopen(url).read()
            newTheme = json.loads(response)

            if nowTheme !=  newTheme:

                return newTheme
            else:
                return 0
        else:
            return 0
        
    def downloadTheme(self):
        
        global clrschms
        
        result = self.themes(clrschms)
        if result:
            config.set('themeList', json.dumps(result))
         

    
                
