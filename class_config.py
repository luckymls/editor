import os


class config:

    '''Uso: config.get(nome_variabile)
    config.set(nome_variabile, valore_variabile)'''

    def get(variabile=None):

        var_path = '.config/' + variabile

        if os.path.exists(var_path):
            return open(var_path).read(os.path.getsize(var_path))
        else:
            return None

    def set(*args):

        try:
            os.mkdir('.config')
            if isLinux is 0:
                folderPath = os.getcwd() + '/.config'
                os.popen('attrib +S +H ' + folderPath)
        except:
            pass

        variabile = args[0]
        var_path = '.config/' + variabile
        value = args[1]
        try:
            overwrite = args[2]
        except:
            overwrite = False
        '''Mode -> w = Sovrascrivo Mode -> a = Sposta puntatore a fine file e scrive'''
        mode = 'w'
        if overwrite:
            mode = 'a'

        try:
            overWriteFirst = args[3]
        except:
            overWriteFirst = 0
        isOverWriteFirst = 0
        if overWriteFirst and os.path.exists(var_path):
            toRead = str(open(var_path, 'r').read(os.path.getsize(var_path)))
            list1 = toRead.split('\n')

            list2 = []
            for element in list1:
                if len(element) > 3:
                    list2.append(str(element))
            list3 = []

            list3.append(str(list2[1]))
            list3.append(str(list2[2]))
            list3.append(str(list2[3]))
            list3.append(str(list2[4]))
            list3.append(str(value))


            txt = ''
            for element in list3:
                txt += str(element) + '\n'
            txt = txt[:-2]
            isOverWriteFirst = 1
            value = txt
            mode = 'w'

        f = open(var_path, mode)
        f.write(value)
        f.close()
