from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font
import os
import sys
import time
import random
import re
import ast
import json
import pygments
from pygments import lexers

##################

from iconDownload import *
from themeDownload import *

##################

'''Serve per salvare valori da riutilizzare anche dopo la chiusura del programma'''


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

#####################


root = Tk()
root.geometry('900x560')
root.title('Untitled - TindyEditor')
root.resizable(width=1, height=1)

language = StringVar(root)
language.set('python3')
language.trace('w', lambda *args: Syntaxhl.extract_text(open_mode=True))

fontSize = StringVar(root)

if config.get('font'): fontSize.set(config.get('font'))
else:                  fontSize.set('Medium')

##################

'''Checking S.O.'''

if sys.platform[:5].lower() == 'linux':
    isLinux = 1
else:
    isLinux = 0


##################

def getEncoding(filePath=None):
    encodes = ['utf-8', 'utf-16', 'iso-8859-15', 'cp437']

    for test in encodes:
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


####################

class Syntaxhl():
    colors = {
            'Token.Text': "#000000",
            'Token.Keyword': "#3060A6",
            'Token.Keyword.Constant': "#3060A6",
            'Token.Keyword.Declaration': "#3060A6",
            'Token.Keyword.Namespace': "#3060A6",
            'Token.Keyword.Pseudo': "#3060A6",
            'Token.Keyword.Reserved': "#3060A6",
            'Token.Keyword.Type': "#3060A6",
            'Token.Name': "#000000",
            'Token.Name.Attribute': "#4E9A06",
            'Token.Name.Builtin': "#4E9A06",
            'Token.Name.Builtin.Pseudo': "#4E9A06",
            'Token.Name.Class': "#4E9A06",
            'Token.Name.Constant': "#4E9A06",
            'Token.Name.Decorator': "#4E9A06",
            'Token.Name.Entity': "#4E9A06",
            'Token.Name.Exception': "#4E9A06",
            'Token.Name.Function': "#4E9A06",
            'Token.Name.Function.Magic': "#4E9A06",
            'Token.Name.Label': "#4E9A06",
            'Token.Name.Namespace': "#4E9A06",
            'Token.Name.Other': "#4E9A06",
            'Token.Name.Tag': "#4E9A06",
            'Token.Name.Variable': "#4E9A06",
            'Token.Name.Variable.Class': "#4E9A06",
            'Token.Name.Variable.Global': "#4E9A06",
            'Token.Name.Variable.Instance': "#4E9A06",
            'Token.Name.Variable.Magic': "#4E9A06",
            'Token.Literal': "#3CBBDD",
            'Token.Literal.Date': "#3CBBDD",
            'Token.Literal.String': "#3CBBDD",
            'Token.Literal.String.Affix': "#3CBBDD",
            'Token.Literal.String.Backtick': "#3CBBDD",
            'Token.Literal.String.Char': "#3CBBDD",
            'Token.Literal.String.Delimiter': "#3CBBDD",
            'Token.Literal.String.Doc': "#3CBBDD",
            'Token.Literal.String.Double': "#3CBBDD",
            'Token.Literal.String.Escape': "#3CBBDD",
            'Token.Literal.String.Heredoc': "#3CBBDD",
            'Token.Literal.String.Interpol': "#3CBBDD",
            'Token.Literal.String.Other': "#3CBBDD",
            'Token.Literal.String.Regex': "#3CBBDD",
            'Token.Literal.String.Single': "#3CBBDD",
            'Token.Literal.String.Symbol': "#3CBBDD",
            'Token.Operator': "#C10E18",
            'Token.Operator.Word': "#C10E18",
            'Token.Punctuation': "#494141",
            'Token.Comment': "#AD7FA8",
            'Token.Comment.Hashbang': "#AD7FA8",
            'Token.Comment.Multiline': "#AD7FA8",
            'Token.Comment.Preproc': "#AD7FA8",
            'Token.Comment.Single': "#AD7FA8",
            'Token.Comment.Special': "#AD7FA8",
            'Token.Literal.Number': "#04137A",
            'Token.Literal.Number.Bin': "#04137A",
            'Token.Literal.Number.Float': "#04137A",
            'Token.Literal.Number.Hex': "#04137A",
            'Token.Literal.Number.Integer': "#04137A",
            'Token.Literal.Number.Integer.Long': "#04137A",
            'Token.Literal.Number.Oct': "#04137A",
            'Token.Declaration': "#F53200",
    }
    lexers = {'css': pygments.lexers.CssLexer(),
    'html': pygments.lexers.HtmlLexer(),
    'javascript': pygments.lexers.JavascriptLexer(),
    'json': pygments.lexers.JsonLexer(),
    'python3': pygments.lexers.Python3Lexer(),
            'php': pygments.lexers.PhpLexer(startinline=True),
    'mysql': pygments.lexers.MySqlLexer(),
    'sql': pygments.lexers.SqlLexer(),
    'XML': pygments.lexers.XmlLexer()

    }

    def extract_text(event=None, return_mode=False, open_mode=False):
        if open_mode is False:

            if return_mode is False:
                linestart = textPad.index('insert linestart')
                lineend = textPad.index('insert lineend')
                text = textPad.get(linestart, lineend)
                Syntaxhl.find_syntax(text, linestart, lineend)

            else:
                linestart = str(int(textPad.index('insert linestart').split('.')[0]) - 1) + '.' + textPad.index('insert linestart').split('.')[1]
                lineend = str(int(textPad.index('insert lineend').split('.')[0]) - 1) + '.' + textPad.index('insert lineend-1c').split('.')[1]
                text = textPad.get(linestart, lineend)

                Syntaxhl.find_syntax(text, linestart, lineend)
        else:
            text = textPad.get('1.0', 'end')
#           Syntaxhl.lexer = pygments.lexers.guess_lexer(text)  # Non riconosce molto bene

            for tag in textPad.tag_names():
                textPad.tag_remove(tag, '1.0', 'end')
                lines = text.split('\n')
            for i in range(len(lines)):
                linestart = f'{str(i + 1)}.0'
                lineend = f'{str(i + 1)}.{len(lines[i])}'
                text = textPad.get(linestart, lineend)
                Syntaxhl.find_syntax(text, linestart, lineend)
        for wordtype in Syntaxhl.colors.keys():
            textPad.tag_config(wordtype, foreground=Syntaxhl.colors[wordtype])

    def analyze_language(text):

        pass

    def find_syntax(text, linestart, lineend):
        count = 0
        lexer = Syntaxhl.lexers[language.get()]
        for tag in textPad.tag_names():  # Esiste un modo più veloce?
            textPad.tag_remove(tag, linestart, lineend)
        for pair in pygments.lex(text, lexer):

            wordtype = str(pair[0])
            word = pair[1]
            if word == "\n":
                return
            #index = textPad.search(word, linestart, stopindex=lineend)

            chars = len(word)
            count += chars
            column = int(linestart.split('.')[1])
            line = int(linestart.split('.')[0])
            index = f'{line}.{count}'
            column = int(index.split('.')[1])
            textPad.tag_add(wordtype, f'{line}.{str(column - chars)}', index)

##################

def downloadTheme():
    global clrschms
    result = getThemes(clrschms)
    if result:
        config.set('themeList', json.dumps(result))
        
        





##################

def popup(event):
    cmenu.config(bg=Colors.pop_bg, fg=Colors.pop_fg, activebackground=Colors.pop_bg_active)
    cmenu.tk_popup(event.x_root, event.y_root)


'''Scelta tema'''


def theme(x=None):
        global bgc, fgc, clrschms

        if config.get('theme') and x is None:
            val = config.get('theme')
        else:
            val = themechoice.get()
            config.set('theme', val)

        clrs = clrschms[val]  # 000000.FFFFFF

        fgc, bgc = clrs.split('.')
        fgc, bgc = '#' + fgc, '#' + bgc

        textPad.config(bg=bgc, fg=fgc)
        config.set('theme', val)

def setFontSize(font=None):

    config.set('font', str(font))
    font = font.lower()

    if font == 'small':
        font = 9
    elif font == 'medium':
        font = 11
    elif font == 'large':
        font = 13

    lnlabel.config(font = f'Helvetica {font}')
    textPad.config(font = f'Helvetica {font}')


def getFontSize():
    font = fontSize.get().lower()
    if font == 'small':
        font = 9
    elif font == 'medium':
        font = 11
    elif font == 'large':
        font = 13
    return font


class Colors:
    mblack = '#171717'
    black = '#171E28' #prima #515151
    black2 = '#282C34'
    black3 = '#31363F'
    black4 = '#444447'
    white = '#F0F0F0'
    white2 = '#F7F7F7'
    grey = '#B3B3B3'
    grey2 = '#ABB2BF'
    grey3 = '#9DA5B4'
    blue = "#729FCF"
    pop_bg = white
    pop_fg = black
    pop_bg_active = white2
    pop_bg_list = 'white'
    active_line_highlight = '#E4FFD5'


def night_mode(event=None):  # Bug: creazione dei bookmark in nightmode: aggiungere colore globale per fg e bg, che venga preso sul momento dalla funzione draw - Aggiungere nightmode per tutte le finestre secondarie, menu contestuale compreso
    current_theme = themechoice.get()  # Potrei utilizzare il tag 'sel' per modificare il colore della selezione

    objects = ((menubar, filemenu, viewmenu, editmenu, aboutmenu, themesmenu, recentFiles, settingsMenu))
    if nightmodeln.get():
        nightmodeln.set(0)
        Colors.pop_bg = Colors.white
        Colors.pop_fg = Colors.black
        Colors.pop_bg_active = Colors.white2
        Colors.pop_bg_list = 'white'
        Colors.active_line_highlight = '#E4FFD5'

        themechoice.set(current_theme)
        theme(1)
        textPad.config(insertbackground="#000000")

        lnlabel.config(bg='#DDFFDC', fg='#650909')
        infobar.config(fg=Colors.black, bg=Colors.white)
        scroll_x.config(bg=Colors.white, activebackground=Colors.white, troughcolor=Colors.grey, highlightbackground=Colors.white2)
        scroll_y.config(bg=Colors.white, activebackground=Colors.white, troughcolor=Colors.grey, highlightbackground=Colors.white2)
        shortcutbar.config(bg=Colors.white)
        bookmarkbar.config(bg=Colors.white)
        root.config(bg=Colors.white)
        selector.config(bg=Colors.white, fg=Colors.black, activebackground=Colors.white2, activeforeground=Colors.black)
        selector["menu"].config(bg=Colors.white, fg=Colors.black, activebackground=Colors.white2, activeforeground=Colors.black)
        fontSelector.config(bg=Colors.white, fg=Colors.black, activebackground=Colors.white2, activeforeground=Colors.black)
        fontSelector["menu"].config(bg=Colors.white, fg=Colors.black, activebackground=Colors.white2, activeforeground=Colors.black)
        fr.config(bg=Colors.white)
        for i in objects:
            i.config(fg=Colors.black, bg=Colors.white, activebackground=Colors.blue, activeforeground=Colors.black)
        for i in bookmarkbar.winfo_children():
            i.config(bg=Colors.white, fg=Colors.black, activebackground=Colors.white2, activeforeground=Colors.black)
        for i in shortcutbar.winfo_children():
            i.config(bg=Colors.white, fg=Colors.black, activebackground=Colors.white2, activeforeground=Colors.black)

    else:
        nightmodeln.set(1)
        Colors.pop_bg = Colors.black2
        Colors.pop_fg = Colors.grey
        Colors.pop_bg_active = Colors.mblack
        Colors.pop_bg_list = Colors.black2
        Colors.active_line_highlight = '#082E58'
        textPad.config(fg=Colors.grey2, bg=Colors.black2, insertbackground="#5386E9")
        lnlabel.config(fg=Colors.grey2, bg=Colors.black2)
        infobar.config(fg=Colors.grey3, bg=Colors.black3)
        scroll_x.config(bg=Colors.black3, activebackground=Colors.black3, troughcolor=Colors.black2, highlightbackground=Colors.black2)
        scroll_y.config(bg=Colors.black3, activebackground=Colors.black3, troughcolor=Colors.black2, highlightbackground=Colors.black2)
        shortcutbar.config(bg=Colors.black3)
        root.config(bg=Colors.black3)
        bookmarkbar.config(bg=Colors.black3)
        selector.config(bg=Colors.black3, fg=Colors.grey3, activebackground=Colors.mblack, activeforeground=Colors.grey3)
        selector["menu"].config(bg=Colors.black3, fg=Colors.grey3, activebackground=Colors.mblack, activeforeground=Colors.grey3)
        fontSelector.config(bg=Colors.black3, fg=Colors.grey3, activebackground=Colors.mblack, activeforeground=Colors.grey3)
        fontSelector["menu"].config(bg=Colors.black3, fg=Colors.grey3, activebackground=Colors.mblack, activeforeground=Colors.grey3)
        fr.config(bg=Colors.black3)
        for i in objects:
            i.config(fg=Colors.grey3, bg=Colors.black3, activebackground=Colors.black4, activeforeground=Colors.grey3)
        for i in bookmarkbar.winfo_children():
            i.config(bg=Colors.black2, fg=Colors.grey3, activebackground=Colors.mblack, activeforeground=Colors.grey3)
        for i in shortcutbar.winfo_children():
            i.config(bg=Colors.black2, fg=Colors.grey3, activebackground=Colors.mblack, activeforeground=Colors.grey3)

def show_line_bar():
    val = showln.get()
    if val:
        
        lnlabel.pack(side=LEFT, fill=Y, before=textPad)
    else:
        lnlabel.pack_forget()

def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO, fill=None, side=BOTTOM, anchor='c')
        scroll_x.pack_forget()
        scroll_x.pack(side=BOTTOM, fill=X)
    elif not val:
        infobar.pack_forget()


def update_line_number(load=False, event=None, paste=False, new=False):
    global filename
    update_info_bar()

    if showln.get():
        if load is False:
            if int(lnlabel.index('end').split('.')[0]) < int(textPad.index('end').split('.')[0]):
                lnlabel.config(state='normal')
                line = int(textPad.index('end').split('.')[0]) - 1
                lnlabel.insert('end', "\n" + str(line))

                lnlabel.config(state='disabled')
                if textPad.index('insert').split('.')[0] == textPad.index('end-1c').split('.')[0]:
                    lnlabel.see(textPad.index('end'))
            else:
                lnlabel.config(state='normal')
                if int(lnlabel.index('end').split('.')[0]) > int(textPad.index('end').split('.')[0]):
                    lnlabel.delete(textPad.index('end'), 'end')
                lnlabel.config(state='disabled')
                lnlabel.yview_moveto(textPad.yview()[0])
        else:
            Syntaxhl.extract_text(open_mode=True)
            lnlabel.config(state='normal')

            lines = int(textPad.index('end').split('.')[0])
            lnlabel.delete(2.0, 'end')

            for i in range(2, lines):
                lnlabel.insert('end', '\n' + str(i))
            lnlabel.config(state='disabled')
            if paste is False and new is False:

                try:
                    bookmarks_list = config.get('bookmarks').split('\n')
                except:
                    pass
                else:
                    for i in bookmarks_list:
                        if i.split(';')[0] == filename:
                            Bookmark.bookmarks = ast.literal_eval(i.split(';')[1])
                            Bookmark.draw(delete=True)
                            return
                        elif bookmarks_list.index(i) == len(bookmarks_list):
                            Bookmark.bookmarks = {}
                            Bookmark.draw(delete=True)


selected_text = BooleanVar()


def highlight_line(interval=1):
    textPad.tag_remove("active_line", 1.0, "end")  # si può sfruttare questo meccanismo per aggiornare in tempo reale la barra mentre si seleziona
    if selected_text.get() == False:
        textPad.tag_add("active_line", "insert linestart", "insert lineend+1c")
        textPad.tag_config("active_line", background=Colors.active_line_highlight)
    textPad.after(interval, toggle_highlight)


def undo_highlight():
    textPad.tag_remove("active_line", 1.0, "end")


def toggle_highlight(event=None):
    val = hltln.get()
    undo_highlight() if not val else highlight_line()


def fullscreen(event=None):

    if fullscreenln.get():
        state = 0
        fullscreenln.set(0)
    else:
        state = 1
        fullscreenln.set(1)
    # screen_w = root.winfo_screenwidth()
    # screen_h = root.winfo_screenheight()

    root.attributes('-fullscreen', state)


def anykey(event=None):
    update_file()
    update_line_number()
    update_info_bar()

    update_info_bar()
    selected_text.set(False)
####################


def about(event=None):

    showinfo("About", "Developed by @Luckymls & Francesco")


def help_box(event=None):

    showinfo("Help", "For help email to melis.luca2014@gmail.com", icon='question')


def exit_editor():

    if askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', exit_editor)

#####################


'''Index e tags'''


def select_all(event=None):
    textPad.tag_add('sel', '1.0', 'end')


def on_find(event=None):
    t2 = Toplevel(root, bg=Colors.pop_bg)
    t2.title('Find')
    t2.geometry('350x65+200+250')
    t2.resizable(width=0, height=0)
    t2.transient(root)
    Label(t2, text="Find All:", bg=Colors.pop_bg, fg=Colors.pop_fg).grid(row=0, column=0, pady=4, sticky='e')
    v = StringVar()
    e = Entry(t2, width=25, textvariable=v, bg=Colors.pop_bg, fg=Colors.pop_fg)
    e.grid(row=0, column=1, padx=2, pady=4, sticky='we')
    c = IntVar()
    Checkbutton(t2, text='Ignore Case', variable=c, bg=Colors.pop_bg, fg=Colors.pop_fg).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(t2, text='Find All', underline=0, bg=Colors.pop_bg, fg=Colors.pop_fg, command=lambda: search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=4)
    def close_search():
        textPad.tag_remove('match', '1.0', END)
        t2.destroy()
    t2.protocol('WM_DELETE_WINDOW', close_search)


def search_for(needle, cssnstv, textPad, t2, e):
        textPad.tag_remove('match', '1.0', END)
        count = 0
        if needle:
                pos = '1.0'
                while True:
                    pos = textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
                    if not pos:
                        break
                    lastpos = '%s+%dc' % (pos, len(needle))
                    textPad.tag_add('match', pos, lastpos)
                    count += 1
                    pos = lastpos
                textPad.tag_config('match', foreground='white', background='blue')
        e.focus_set()
        t2.title('%d matches found' % count)


#######################################################################


insertln = IntVar()
gTL = StringVar()


def goToLine(event=None):
    
    global gTL

    t4 = Toplevel(root, bg=Colors.pop_bg)
    t4.focus_set()
    t4.title('Go to...')
    t4.geometry('300x65')
    t4.resizable(width=0, height=0)
    t4.transient(root)
    Label(t4, text="Line:", bg=Colors.pop_bg, fg=Colors.pop_fg).grid(row=0, column=0, pady=4, sticky='e')

    pos = gTL.get() + '.0'
    gTL.set('')
    e = Entry(t4, width=25, textvariable=gTL, takefocus='active', bg=Colors.pop_bg, fg=Colors.pop_fg)
    e.grid(row=0, column=1, padx=2, pady=4, sticky='we')
    e.focus_set()
    b = Button(t4, text='Go!', command=lineSearch, default='active', bg=Colors.pop_bg, fg=Colors.pop_fg, activebackground=Colors.pop_bg_active)
    b.grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=4)

    # def check_content():
    #     accepted_characters = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # Da implementare
    #     if i in accepted_characters:
    #         return True
    #     else:
    #         return False
    #
    # e. config(validate='key', validatecommand=check_content)

    def close_goto(event=None):
        textPad.tag_remove('lineSearch', 1.0, "end")

        t4.destroy()
    pos = gTL.get() + '.1'
    t4.protocol("WM_DELETE_WINDOW", close_goto)
    t4.bind('<Return>', lineSearch)
    e.bind('<FocusOut>', close_goto)


def lineSearch(event=None):

    textPad.tag_remove('lineSearch', 1.0, "end")
    pos = gTL.get() + '.0'
    lastpos = int(gTL.get()) + 1
    lastpos = str(lastpos) + '.0'
    textPad.tag_add('lineSearch', pos, lastpos)
    textPad.tag_config('lineSearch', foreground='white', background='blue')
    textPad.see([pos])
    lnlabel.yview_moveto(textPad.yview()[0])


########################################################################


'''Funzioni preesistenti di tkinter'''


def undo():
    textPad.event_generate("<<Undo>>")
    
def redo():
    textPad.event_generate("<<Redo>>")


def cut():
    textPad.event_generate("<<Cut>>")


def copy():
    textPad.event_generate("<<Copy>>")


def paste(event=None):
    textPad.event_generate("<<Paste>>")
    
def on_paste(event=None):
    textPad.delete('sel.first', 'sel.last')
    
previous_event = StringVar()  
previous_event.set('Control')

def key_release(event=None):
    
    
    if previous_event.get()[:-2] == 'Control':
        if event.keysym.lower() == 'z' or event.keysym.lower() == "v" or event.char == '\x1a' or event.char == '\x16':
            update_line_number(load=True, paste=True)
            Syntaxhl.extract_text(open_mode=True)
    previous_event.set(event.keysym)
def on_tab_key(event=None):
    textPad.delete('insert-1c')
    textPad.insert('insert', '    ') 

######################################################################


def wSetting():

    t3 = Toplevel(root, bg=Colors.pop_bg)
    t3.title('Settings')
    t3.geometry('500x300')
    t3.resizable(width=0, height=0)
    t3.transient(root)

    '''Menu'''

    menuBar = Menu(t3)
    t3.config(menu=menuBar)

    nightMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Help", menu=nightMenu)
    nightMenu.add_command(label="About", compound=LEFT, command=about)
    menuBar.add_command(label="Close", compound=LEFT, command=t3.destroy)


############################################

def new_file(event=None):
    global filename
    
    filename = None
    root.title("Untitled - Hydrogen")
    textPad.delete(1.0, END)
    update_line_number(load=True, new=True)
    

def open_file(event=None, file_name=None):
    global filename
    
    filename = file_name
    if filename is None:
        filename = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt"), ("All Files", "*.*")])  # ("All Files","*.*"), Da aggiungere dopo che aggiungiamo i vari tipi di codifica

    if filename == "":
        filename = None
    else:
        filename = str(filename)
        if os.path.isfile(filename + ".backup"):
            if os.path.getmtime(filename) < os.path.getmtime(filename + ".backup"):
                if askokcancel("Yes", "Backup file has more recent changes, do you want to open the backup file instead?"):
                    root.title(os.path.basename(filename) + " - Hydrogen")
                    textPad.delete(1.0, END)
                    fh = open(filename + ".backup", "r")
                    textPad.insert(1.0, fh.read())
                    fh.close()
                    update_line_number(load=True)
                    Syntaxhl.extract_text(open_mode=True)
                    return
                else: pass
        '''Ritorna il nome del file senza estensione'''
        root.title(os.path.basename(filename) + " - Hydrogen")
        textPad.delete(1.0, END)
        fh = open(filename, "r")
        textPad.insert(1.0, fh.read())
        fh.close()
    update_line_number(load=True)
    Syntaxhl.extract_text(open_mode=True)

def open_recent_file(file_name=None):  # Aggiungere funzione backup anche qui
    global filename
    nBase = os.path.basename(file_name)
    filename = file_name
    try:
        fh = open(file_name, "r")
    except:
        messagebox.showerror("Error", "File not found")

        checkConf = config.get('recent files').split('\n')
        
        for file in checkConf:
            exists = os.path.exists(file)
            if not exists:
                checkConf.remove(file)
        toAdd = ''
        for file in checkConf:
            toAdd+= file+'\n'
        config.set('recent files', toAdd)
            
        
    else:
        if os.path.isfile(filename + ".backup"):
            if os.path.getmtime(filename) < os.path.getmtime(filename + ".backup"):
                if askokcancel("Yes", "Backup file has more recent changes, do you want to open the backup file instead?"):
                    root.title(os.path.basename(filename) + " - Hydrogen")
                    textPad.delete(1.0, END)
                    fh = open(filename + ".backup", "r")
                    textPad.insert(1.0, fh.read())
                    fh.close()
                    update_line_number(load=True)
                    Syntaxhl.extract_text(open_mode=True)
                    return
                else: pass
        root.title(nBase + " - Hydrogen")
        textPad.delete(1.0, END)
        textPad.insert(1.0, fh.read())
        fh.close()
        update_line_number(load=True)
        Syntaxhl.extract_text(open_mode=True)

def save(event=None):
    global filename
    try:
        config.set('bookmarks', Bookmark.save(filename))
        pathAlreadyExists = 0
        checkConf = config.get('recent files')
        if checkConf:
            checkConf = checkConf.split('\n')
        else:
            checkConf = []

        for testPath in checkConf:
            if testPath == filename:
                pathAlreadyExists = 1

        if pathAlreadyExists is 0:
            if len(checkConf) < 5:

                config.set('recent files', filename + '\n', 1)

            else:

                config.set('recent files', filename + '\n', 1, 1)

        f = open(filename, 'w')
        letter = textPad.get(1.0, 'end')
        f.write(letter)
        f.close()
        return filename
    except:
        return save_as()


def save_as():
    global filename

    '''Apro finestra wn per salvare file con nome'''
    f = filedialog.asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("Text Documents", "*.txt")])  # ("All Files","*.*"),

    fh = open(f, 'w')
    filename = f

    config.set('bookmarks', Bookmark.save(filename))
    pathAlreadyExists = 0
    checkConf = config.get('recent files')

    if checkConf:
        checkConf = checkConf.split('\n')
    else:
        checkConf = []

    for testPath in checkConf:
        if testPath == filename:
            pathAlreadyExists = 1

    if pathAlreadyExists is 0:
        if len(checkConf) < 5:

            config.set('recent files', filename + '\n', 1)

        else:
            config.set('recent files', filename + '\n', 1, 1)

    textoutput = textPad.get(1.0, END)
    fh.write(textoutput)
    fh.close()
    root.title(os.path.basename(f) + " - TindyEditor")
    return filename

def update_file(event=None):
    update_line_number()
    global filename
    if autoSave.get():
        try:
            rand = random.randint(1, 3)
            if rand is 3:
                baseName = os.path.basename(filename)
                f = filename.replace('/'+baseName, '')+f'/.{baseName}.backup'
                
                
                
                fh = open(f, 'w')
                
                if not isLinux:
                    os.popen('attrib +S +H ' + f)
                    
                textoutput = textPad.get(1.0, END)
                fh.write(textoutput)
                fh.close()

        except:
            pass


def update_info_bar(event=None):
    linecount = IntVar()
    line = int(textPad.index('insert').split('.')[0])
    total = int(textPad.index('end').split('.')[0]) - 1
    column = int(textPad.index('insert').split('.')[1]) + 1
    infobar.config(text=f'Line {line}/{total} | Column {column}')


def on_return_key(event=None):
    if textPad.get('insert-2c') == ":" and (language.get() == 'python3' or language.get() == 'python2'):

        textPad.insert('insert', '    ')
    if textPad.get('insert-1l linestart') == ' ':
        line = textPad.get('insert-1l linestart', 'insert-1l lineend')
        for i in range(0, len(line), 4):
            spaces = line[i:i+4]
            if spaces == '    ':
                textPad.insert('insert', '    ')
            else:
                break

    Syntaxhl.extract_text(return_mode=True)

def dedent():
       print(textPad.tag_get('sel'))

def printSheet():
    #Only work on Windows
    filePath = save()
    os.startfile(filePath, "print")
    messagebox.showinfo("Title", 'Printing...')

######################################################################


'''Icone del menù'''

'''Spiegazione rapida: label = testo, accelerator= testo per scorciatoia combinazione tasti, compund=posizione, command=comando da richiamare se si spunta/clicca l'opzione'''


if not os.path.exists(os.getcwd()+'/icons/') or len(os.listdir(os.getcwd()+'/icons/')) < 11:
    print('Icons not found, downloading...')
    rDownload = downloadIcon(isLinux=isLinux)

    if rDownload == 400:
        input('Internet connection trouble. Please enable your internet connection and try again. Press any key to exit')
        exit()




if isLinux:
    completePath = os.getcwd() + '/'
else:
    completePath = ''
    root.iconbitmap('icons/pypad.ico')


new_fileicon = PhotoImage(file=completePath + 'icons/new_file.png')
open_fileicon = PhotoImage(file=completePath + 'icons/open_file.gif')
saveicon = PhotoImage(file=completePath + 'icons/save.png')
cuticon = PhotoImage(file=completePath + 'icons/cut.png')
copyicon = PhotoImage(file=completePath + 'icons/copy.png')
pasteicon = PhotoImage(file=completePath + 'icons/paste.png')
undoicon = PhotoImage(file=completePath + 'icons/undo.png')
redoicon = PhotoImage(file=completePath + 'icons/redo.png')
on_findicon = PhotoImage(file=completePath + 'icons/on_find.png')
abouticon = PhotoImage(file=completePath + 'icons/about.png')



'''Menù'''
menubar = Menu(root, relief='ridge', bd=1, activebackground="#729FCF")

'''File menù'''
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=new_fileicon, underline=0, command=new_file)
filemenu.add_separator()
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=open_fileicon, underline=0, command=open_file)
recentFiles = Menu(filemenu, tearoff=0)
filemenu.add_cascade(label="Recent Files", menu=recentFiles)
themechoice = IntVar()
filemenu.config(bg=Colors.white, fg=Colors.black, activebackground="#729FCF", activeforeground="#FFFFFF")

'''Add Recent Files'''
if config.get('recent files'):
    recentOpen = config.get('recent files').split('\n')
    i = 0
    for filePaths in recentOpen:
        if len(filePaths) > 3:
            i += 1
            fileName = os.path.basename(filePaths)[0].upper() + os.path.basename(filePaths)[1:]
            recentFiles.add_command(label=str(i) + '. ' + fileName, compound=LEFT, underline=0, command=lambda x=filePaths: open_recent_file(x))


filemenu.add_separator()
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT, image=saveicon, underline=0, command=save)
filemenu.add_command(label="Save as", accelerator='Shift+Ctrl+S', command=save_as)
autoSave = IntVar()
autoSave.set(1)
filemenu.add_checkbutton(label="Save Automatically", variable=autoSave, command=update_file)
if not isLinux:  # Print Function

    filemenu.add_separator()

    filemenu.add_command(label="Print", command=printSheet)
filemenu.add_separator()
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=exit_editor)
menubar.add_cascade(label="File", menu=filemenu)
recentFiles.config(activebackground="#729FCF", activeforeground="#FFFFFF")
'''Edit menù'''
editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", compound=LEFT, image=undoicon, accelerator='Ctrl+Z', command=undo)
editmenu.add_command(label="Redo", compound=LEFT, image=redoicon, accelerator='Ctrl+Y', command=redo)
editmenu.add_separator()
editmenu.add_command(label="Cut", compound=LEFT, image=cuticon, accelerator='Ctrl+X', command=cut)
editmenu.add_command(label="Copy", compound=LEFT, image=copyicon, accelerator='Ctrl+C', command=copy)
editmenu.add_command(label="Paste", compound=LEFT, image=pasteicon, accelerator='Ctrl+V', command=paste)
editmenu.add_separator()
editmenu.add_command(label="Find", compound=LEFT, image=on_findicon, accelerator='Ctrl+F', command=on_find)
editmenu.add_separator()
editmenu.add_command(label="Select All", compound=LEFT, accelerator='Ctrl+A', underline=7, command=select_all)
editmenu.config(bg=Colors.white, fg=Colors.black, activebackground="#729FCF", activeforeground="#FFFFFF")
'''View menu'''

viewmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label="Show Line Number", variable=showln, command=show_line_bar)
showinbar = IntVar()
showinbar.set(1)
viewmenu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar, command=show_info_bar)
hltln = IntVar()
viewmenu.add_checkbutton(label="Highlight Current Line", variable=hltln, command=toggle_highlight)

viewmenu.add_command(label='Go to...', accelerator='Ctrl+G', command=goToLine)
viewmenu.add_separator()
themesmenu = Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label="Themes", menu=themesmenu)
viewmenu.add_separator()
fullscreenln = IntVar()
nightmodeln = IntVar()
viewmenu.add_checkbutton(label="Night Mode", variable=nightmodeln.get(), accelerator='F9', command=night_mode)
viewmenu.add_checkbutton(label="Full Screen", variable=fullscreenln.get(), accelerator='F11', command=fullscreen)
viewmenu.config(bg=Colors.white, fg=Colors.black, activebackground="#729FCF", activeforeground="#FFFFFF")

'''Dizionario con: nome: esadecimale carattere.esadecimale sfondo'''

####################



if config.get('themeList'):
    
    clrschms = json.loads(config.get('themeList'))
    downloadTheme()
else:
    
    clrschms = {
        '1. Default White': '000000.FFFFFF',
        '2. Greygarious Grey': '83406A.D1D4D1',
        '3. Lovely Lavender': '202B4B.E1E1FF',
        '4. Aquamarine': '5B8340.D1E7E0',
        '5. Bold Beige': '4B4620.FFF0E1',
        '6. Cobalt Blue': 'ffffBB.3333aa',
        '7. Olive Green': 'D1E7E0.5B8340',
    }
    config.set('themeList', json.dumps(clrschms))
    

    
###################

themechoice = StringVar()

'''Imposto tema se salvato altrimenti default'''

if config.get('theme'):

    themechoice.set(config.get('theme'))

else:
    themechoice.set('1. Default White')


for k in sorted(clrschms):
    themesmenu.add_radiobutton(label=k, variable=themechoice, command=lambda: theme(1))
themesmenu.config(bg=Colors.white, fg=Colors.black, activebackground="#729FCF", activeforeground="#FFFFFF")


'''Settings menu'''

settingsMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Settings', menu=settingsMenu)
settingsMenu.add_command(label='Settings', compound=LEFT, command=wSetting)
settingsMenu.config(bg=Colors.white, fg=Colors.black, activebackground="#729FCF", activeforeground="#FFFFFF")

'''About menu'''
aboutmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=aboutmenu)
aboutmenu.add_command(label="About", compound=LEFT, command=about)
aboutmenu.add_command(label="Help", command=help_box)
aboutmenu.config(bg=Colors.white, fg=Colors.black, activebackground="#729FCF", activeforeground="#FFFFFF")
root.config(menu=menubar)

'''Exit menu'''
menubar.add_command(label='Exit', command=exit_editor)


'''Menù Scorciatoie e numero linea'''
shortcutbar = Frame(root, height=25, relief='ridge', bd=1)


icons = ['new_fileicon', 'open_fileicon', 'saveicon', 'cuticon', 'copyicon', 'pasteicon', 'undoicon', 'redoicon', 'on_findicon', 'abouticon']
for i, icon in enumerate(icons):
    tbicon = eval(icon)
    cmd = eval(icon[:-4])
    toolbar = Button(shortcutbar, image=tbicon, command=cmd)
    toolbar.image = tbicon
    toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)

''' Bottom Frame '''
fr = Frame(root, bg=Colors.white)
fr.pack(side=BOTTOM, fill=X)

''' Language Selector'''

selector = OptionMenu(fr, language, 'css', 'html', 'javascript', 'json', 'python3', 'php', 'sql', 'XML')  # Inserire in un menu sotto forma di cascade
selector.config(bg=Colors.white, fg=Colors.black)
selector.pack(side=LEFT, anchor=S)

''' Font Size Selector'''
fontSelector = OptionMenu(fr, fontSize, 'Small', 'Medium', 'Large', command=lambda x=fontSize.get(): setFontSize(x))
fontSelector.config(bg=Colors.white, fg=Colors.black)
fontSelector.pack(side=RIGHT, anchor=S)


'''Info Bar''' 

infobar = Label(fr, text=f'Line:1 | Column:0', relief='groove', bd=1)
infobar.pack(fill=X, side=BOTTOM, anchor=S)
 
'''Scrollbars drawing''' 
scroll_y = Scrollbar(root, bd=1, relief='groove')
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x = Scrollbar(fr, orient=HORIZONTAL, bd=1, relief='flat')
scroll_x.pack(side=BOTTOM, fill=X)

'''Row Bar'''
rowSize = getFontSize()
lnlabel = Text(root, width=6, bg='#DDFFDC', bd=1, relief='solid', fg='#650909', spacing3=2, font=f'Helvetica {rowSize}')
lnlabel.pack(side=LEFT, fill=Y)

'''Text widget'''
textSize = getFontSize()
tabS = '0.5c'
if isLinux:
    tabS = '1c'
textPad = Text(root, undo=True, takefocus=True, wrap=NONE, spacing3=2, relief='flat', bd=1, font=f'Helvetica {textSize}', tabs=tabS)  # Inserire la possibilità di scegliere il tab e l'utilizzo degli spazi e la conversione da uno all'altro
textPad.pack(expand=YES, fill=BOTH)


'''Scrollbar function'''


def yscroll(*args):
    textPad.yview(*args)
    lnlabel.yview(*args)


def mousewheel(event):

    if event.num == 4:
        lnlabel.yview_scroll(-1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])
    elif event.num == 5:
        lnlabel.yview_scroll(1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])
    elif event.delta > 1:
        lnlabel.yview_scroll(-1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])
    elif event.delta < 1:
        lnlabel.yview_scroll(1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])


def select(event=None, state='not_active'):

    if state == 'active':
        selected_text.set(True)
    elif state == 'not_active':
        selected_text.set(False)
    if insertln.get() == 1:
        textPad.mark_set('insert', gTL.get() + '.0 lineend')
        textPad.mark_gravity('insert', RIGHT)
        insertln.set(0)
    lnlabel.yview_moveto(textPad.yview()[0])
    update_info_bar()


textPad.configure(yscrollcommand=scroll_y.set)
lnlabel.config(yscrollcommand=scroll_y.set)
scroll_y.config(command=yscroll)


textPad.configure(xscrollcommand=scroll_x.set)
scroll_x.config(command=textPad.xview)

bm_list = Variable(root)
bm_list.set([])


''' Bookmark Bar '''  # ctrl b per impostare alla riga corrente, ctrl shift b per aprire pannello, doppio click sulla barra per impostare, doppio click sui segnalibri per configurare, ctrl numero per selezionare un segnalibro, ctrl freccia per andare avanti e indietro (funzione search)


class Bookmark:  # Per poter agire direttamente sui pulsanti, ad esempio con un menu contestuale, utilizzare il winfo_children() e poi fare in modo che il dizionario salvato dal programma venga direttamente dai parametri dei tasti (nome, linea)

    bookmarks = {}
    bm_name = str()
    nline = str()
    b_list = []
    lock = bool()
    bookmarks_to_draw = list(bookmarks.keys())
    slide_current = -1  # Da correggere: se parto andando all'indietro, mi verrà mostrato il penultimo e non l'ultimo bookmark
    slide = []

    def draw(delete=True):

        bookmarks_keys = Bookmark.bookmarks.keys()
        index = 0
        button_list = list()
        if delete is False:
            button_list = []
            for i in bookmarks_keys:
                button = i
                bm_txt = Bookmark.bookmarks[i].split('.')[0]
                bm_line = i
                button = Button(bookmarkbar, text=bm_txt, command=lambda: Bookmark.go(bm_line), bd=1, relief='solid', bg=Colors.pop_bg, fg=Colors.pop_fg, activebackground=Colors.pop_bg_active)
                index += 1

                if index == len(Bookmark.bookmarks) and button:
                    button.pack(side=LEFT)
                    button_list.append(button)
        elif delete is True:

            for i in bookmarkbar.winfo_children():
                i.destroy()
            Bookmark.bookmarks_to_draw = list(bookmarks_keys)
            Bookmark.draw(delete='recursive drawing')
        else:

            if Bookmark.bookmarks_to_draw:
                i = Bookmark.bookmarks_to_draw[0]
                bm_txt = Bookmark.bookmarks[i]
                bm_line = i

                button = Button(bookmarkbar, text=bm_txt, command=lambda: Bookmark.go(bm_line), bd=1, relief='solid', bg=Colors.pop_bg, fg=Colors.pop_fg, activebackground=Colors.pop_bg_active)
                Bookmark.bookmarks_to_draw.pop(0)
                button.pack(side=LEFT)
            if not len(Bookmark.bookmarks_to_draw) == 0:
                Bookmark.draw('recursive drawing')
            return

    def go(line):
        endline = str(int(line.split('.')[0]) + 1) + '.0'
        textPad.tag_add('bookmark', line, endline)
        textPad.tag_config('bookmark', background='yellow')
        textPad.mark_set('insert', line + ' lineend')
        textPad.see('insert')
        textPad.bind('<Any-KeyPress>', Bookmark.highlight_stop)
        textPad.bind('<Button-1>', Bookmark.highlight_stop)

    def highlight_stop(event=None):
        textPad.tag_remove('bookmark', '1.0', 'end')

    def add(line):
        if Bookmark.lock is True:
            return
        Bookmark.lock = True
        Bookmark.nline = line + '.0'
        if Bookmark.nline not in Bookmark.bookmarks:

            Bookmark.select_name()

            textPad.mark_set('bookmark', Bookmark.nline)
            textPad.mark_gravity('bookmark', direction='left')

    def select_name():

        t5 = Toplevel(root, bg=Colors.pop_bg)
        t5.focus_set()
        t5.title('Bookmark...')
        t5.geometry('320x65')
        t5.resizable(width=0, height=0)
        t5.transient(root)
        Label(t5, text="Name:", bg=Colors.pop_bg, fg=Colors.pop_fg).grid(row=0, column=0, pady=4, sticky='e')

        bname = Entry(t5, width=25, takefocus='active', bg=Colors.pop_bg, fg=Colors.pop_fg)
        bname.grid(row=0, column=1, padx=2, pady=4, sticky='we')
        bname.focus_set()

        def close_select(event=None):
            if event == "wm_del_window":
                Bookmark.lock = False
                t5.destroy()
                return
            a = str(bname.get())
            Bookmark.bm_name = a
            Bookmark.bookmarks[Bookmark.nline] = Bookmark.bm_name
            t5.destroy()
            Bookmark.lock = False
            Bookmark.draw()

        closeb = Button(t5, bg=Colors.pop_bg, fg=Colors.pop_fg, text='Ok', command=close_select, default='active')
        closeb.grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=4)
        t5.protocol("WM_DELETE_WINDOW", lambda: close_select("wm_del_window"))
        t5.bind('<Return>', close_select)

    def delete(selection):
        bookmark_to_del = selection.split(':')[0] + '.0'
        del Bookmark.bookmarks[bookmark_to_del]

        Bookmark.b_list.pop(Bookmark.b_list.index(selection))
        bm_list.set(Bookmark.b_list)
        Bookmark.draw(delete=True)

    def settings(update=False):

        Bookmark.b_list = []
        for i in Bookmark.bookmarks.keys():
            line = i.split('.')[0]
            Bookmark.b_list.append(line + ':' + Bookmark.bookmarks[i])
        bm_list.set(Bookmark.b_list)
        t6 = Toplevel(root, bg=Colors.pop_bg)
        t6.geometry('600x450')
        t6.focus_set()
        t6.title('Bookmarks...')
        t6.transient()
        bmListBox = Listbox(t6, height=350, width=300, listvariable=bm_list, bg=Colors.pop_bg_list, fg=Colors.pop_fg)
        label = Label(t6, text='Choose a bookmark:', bg=Colors.pop_bg, fg=Colors.pop_fg)
        label.pack(side=TOP, fill=X)
        delButton = Button(t6, text='Delete bookmark', command=lambda: Bookmark.delete(bmListBox.get('active')), bg=Colors.pop_bg, fg=Colors.pop_fg, activebackground=Colors.pop_bg_active)
        delButton.pack(side=BOTTOM)
        bmListBox.pack(fill=NONE, expand=NO, side=LEFT)

    def save(filename):
        if config.get('bookmarks') == None:
            bookmark_file = filename + ';' + str(Bookmark.bookmarks) + '\n'
            return bookmark_file
        else:
            file_list = config.get('bookmarks').split('\n')
            for i in file_list:
                if i.split(';')[0] == filename:
                    file_list.pop(file_list.index(i))
                    file_list.append(filename + ';' + str(Bookmark.bookmarks))
                    return ('\n').join(file_list)
                else:
                    if file_list.index(i) == len(file_list) - 1:
                        file_list.append(filename + ';' + str(Bookmark.bookmarks))
                        return ('\n').join(file_list)

    def slider(event=None):
        Bookmark.slide = [*Bookmark.bookmarks]
        index = Bookmark.slide_current

        if event == 'next':
            index += 1
            if index == len(Bookmark.slide):
                index = 0
            Bookmark.slide_current = index
            line = Bookmark.slide[index]
            Bookmark.go(line)
        else:
            index -= 1
            if index < -len(Bookmark.slide):
                index = (-1)
            Bookmark.slide_current = index
            line = Bookmark.slide[index]
            Bookmark.go(line)


bookmarkbar = Frame(shortcutbar, height=25, bd=0, relief='ridge')


if Bookmark.bookmarks:
    Bookmark.draw()
bookmarkbar.pack(expand='no', fill=X)

'''Bookmarks config'''
menubar.add_command(label="Bookmarks...", command=Bookmark.settings)

'''Context Menu (Quando faccio click destro sulla casella di testo)'''
cmenu = Menu(textPad, tearoff=0, bg=Colors.pop_bg, fg=Colors.pop_fg, activebackground=Colors.pop_bg_active)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    '''Aggiunto da poco, mette maiuscola nel menù cut => Cut'''
    i = i[0].upper() + i[1:]

    cmenu.add_command(label=i, compound=LEFT, command=cmd)
cmenu.add_separator()
cmenu.add_command(label='Select All', underline=7, command=select_all)
textPad.bind("<Button-3>", popup)


'''Imposto tema'''
theme(1)

#################################################
'''Rilevo evento tastiera, chiamo funzione'''


root.bind('<Any-KeyPress>', anykey)
root.bind('<Any-KeyRelease>', key_release)
root.bind('<Control-N>', new_file)
root.bind('<Control-n>', new_file)
root.bind('<Control-O>', open_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-S>', save)
root.bind('<Control-s>', save)
root.bind('<Button-1>', update_info_bar)
textPad.bind('<Control-A>', select_all)
textPad.bind('<Control-a>', select_all)
textPad.bind('<Control-f>', on_find)
textPad.bind('<Control-F>', on_find)

textPad.bind_all('<Control-g>', goToLine)
textPad.bind_all('<Control-G>', goToLine)
textPad.bind('<Alt-Left>', lambda event: Bookmark.slider('previous'))
textPad.bind('<Alt-Right>', lambda event: Bookmark.slider('next'))
textPad.bind('<Any-KeyRelease>', Syntaxhl.extract_text)
textPad.bind('<KeyRelease-Return>', on_return_key)
textPad.bind('<KeyRelease-Tab>', on_tab_key)
textPad.bind_all('<Alt-Tab>', dedent)  # Da fare
textPad.bind_all('<<Paste>>', on_paste)
textPad.bind_all('<Button-4>', mousewheel)
textPad.bind_all('<Button-5>', mousewheel)
textPad.bind_all('<MouseWheel>', mousewheel)
textPad.bind_all('<Button-1>', select)
textPad.bind_all('<B1-Motion>', lambda event: select(state='active'))
textPad.bind_all('<ButtonRelease-1>', lambda event: select(state='ok'))
lnlabel.bind('<Double-Button-1>', lambda event: Bookmark.add(lnlabel.index('current').split('.')[0]))
textPad.bind('<Control-b>', lambda event: Bookmark.add(textPad.index('insert').split('.')[0]))
root.bind('<KeyPress-F1>', help_box)
root.bind('<KeyPress-F2>', about)
root.bind('<KeyPress-F9>', night_mode)
root.bind('<KeyPress-F11>', fullscreen)


textPad.tag_configure("active_line", background="ivory2")

lnlabel.config(state='normal')
lnlabel.insert('current', '1')
lnlabel.config(state='disable')

''' Accept open with parameter '''
if len(sys.argv) > 1:
    path = ' '.join(sys.argv[1:len(sys.argv)])
    open_file(file_name=path)
    
root.mainloop()
