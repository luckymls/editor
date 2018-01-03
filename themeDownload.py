import json
import socket
import urllib
from urllib import request


def is_connected():
    try:

        socket.create_connection(("www.google.com", 80))
        return 1
    except OSError:
        pass
    return 0


def getThemes(nowTheme = {}):

    if is_connected():
    
        url = 'http://hydrogenicon.altervista.org/theme.php'

        response = urllib.request.urlopen(url).read()
        newTheme = json.loads(response)

        if len(nowTheme) < len(newTheme):

            return newTheme
        else:
            return 0
    else:
        return 0
    
        
