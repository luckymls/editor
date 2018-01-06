class Font:

    font = {'small': 9, 'medium': 11, 'large': 13}

    def setFontSize(self, char=None):

    
        font = self.font[char.lower()]

        config.set('font', str(char))
        lnlabel.config(font = f'Helvetica {font}')
        textPad.config(font = f'Helvetica {font}')
        


    def getFontSize(self):
        
        char = fontSize.get().lower()
        return self.font[char]

