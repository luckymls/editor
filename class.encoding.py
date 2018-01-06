# Classe utilizzata per l'apertura file nella funzione open_file

class Encoding:


    encodes = ['utf-8', 'utf-16', 'iso-8859-15', 'cp437']
    
    def getEncoding(self, filePath=None):
    
    
    for test in self.encodes:
        try:
            open(filePath, 'r', encoding=test)
        except:
            pass
        else:
            encoding = test
            break

    if encoding:
        return encoding
    else:
        return 0
