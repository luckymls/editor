from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog

import os
import sys
import time
import random


root = Tk()
root.geometry('800x500')
root.title('Untitled - TindyEditor')

root.resizable(width=1,height=1)

##################

'''Checking S.O.'''

if sys.platform[:5].lower() == 'linux':
    isLinux = 1
else:
    isLinux = 0

##################


'''Serve per salvare valori da riutilizzare anche dopo la chiusura del programma'''

class config:

    '''Uso: config.get(nome_variabile)
    config.set(nome_variabile, valore_variabile)'''

    def get(variabile=None):

        var_path = '.config/'+variabile

        if os.path.exists(var_path):
            return open(var_path).read(os.path.getsize(var_path))
        else:
            return None


    def set(*args):
        try:
            os.mkdir('.config')
            if isLinux is 0:
                folderPath = os.getcwd()+'/.config'
                os.popen('attrib +S +H '+folderPath)
        except Exception as e:
            print(e)

        variabile = args[0]
        value = args[1]
        try:
            overwrite = args[2]
        except:
            overwrite = False
        '''Mode -> w = Sovrascrivo Mode -> a = Sposta puntatore a fine file e scrive'''
        mode = 'w'
        if overwrite: mode = 'a'
        var_path = '.config/'+variabile
        f = open(var_path, mode)
        f.write(value)
        f.close()


##################

def popup(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)

'''Scelta tema'''
def theme(x=None):
        global bgc,fgc


        if config.get('theme') and x is None:
            val = config.get('theme')
        else:
            val = themechoice.get()
            config.set('theme', val)


        clrs = clrschms.get(val) #000000.FFFFFF

        fgc, bgc = clrs.split('.')
        fgc, bgc = '#'+fgc, '#'+bgc

        textPad.config(bg=bgc, fg=fgc)
        config.set('theme', val)

def night_mode(event=None):
    current_theme = themechoice.get()
    black = '#515151'
    black2 = '#282C34'
    black3 = '#31363F'
    black4 = '#444447'
    white = '#F0F0F0'
    white2 = '#F7F7F7'
    grey = '#B3B3B3'
    grey2 = '#ABB2BF'
    grey3 = '#9DA5B4'
    blue = "#729FCF"
    objects=((menubar, filemenu, viewmenu, editmenu, aboutmenu, themesmenu, recentFiles, settingsMenu))
    if nightmodeln.get():
        nightmodeln.set(0)
        themechoice.set(current_theme)
        theme(1)
        textPad.config(insertbackground="#000000")

        lnlabel.config(bg='antique white', fg='#000000')
        infobar.config(fg=black, bg=white)
        scroll_x.config(bg=white, activebackground=white, troughcolor=grey,highlightbackground=white2)
        scroll_y.config(bg=white, activebackground=white, troughcolor=grey,highlightbackground=white2)
        shortcutbar.config(bg=white)
        root.config(bg=white)
        for i in objects:
            i.config(fg=black, bg=white, activebackground=blue, activeforeground=black)
    else:
        nightmodeln.set(1)
        textPad.config(fg=grey2, bg=black2, insertbackground="#5386E9")
        lnlabel.config(fg=grey2, bg=black2)
        infobar.config(fg=grey3, bg=black3)
        scroll_x.config(bg=black3, activebackground=black3, troughcolor=black2,highlightbackground=black2)
        scroll_y.config(bg=black3, activebackground=black3, troughcolor=black2,highlightbackground=black2)
        shortcutbar.config(bg=black3)
        root.config(bg=black3)
        for i in objects:
            i.config(fg=grey3, bg=black3, activebackground=black4, activeforeground=grey3)

def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO, fill=None, side=BOTTOM, anchor='c')
        scroll_x.pack_forget()
        scroll_x.pack(side=BOTTOM, fill=X)
    elif not val:
        infobar.pack_forget()


def update_line_number(load=False, event=None):
    update_info_bar()
    if showln.get():
        if load == False:
            if int(lnlabel.index('end').split('.')[0]) < int(textPad.index('end').split('.')[0]):
                lnlabel.config(state='normal')
                line = int(textPad.index('end').split('.')[0]) - 1
                lnlabel.insert('end', "\n" + str(line))

                lnlabel.config(state='disabled')
                if textPad.index('insert').split('.')[0] == textPad.index('end-1c').split('.')[0]:
                    lnlabel.see(textPad.index('end'))
            else:
                lnlabel.config(state = 'normal')
                if int(lnlabel.index('end').split('.')[0]) > int(textPad.index('end').split('.')[0]):
                    lnlabel.delete(textPad.index('end'), 'end')
                lnlabel.config(state= 'disabled')
                lnlabel.yview_moveto(textPad.yview()[0])
        else:
            lnlabel.config(state = 'normal')
            lines = int(textPad.index('end').split('.')[0])
            lnlabel.delete('end')
            for i in range (2, lines):
                lnlabel.insert('end', '\n' + str(i))
            lnlabel.config(state= 'disabled')

def highlight_line(interval=100):
    textPad.tag_remove("active_line", 1.0, "end")
    textPad.tag_add("active_line", "insert linestart", "insert lineend+1c")
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
    #screen_w = root.winfo_screenwidth()
    #screen_h = root.winfo_screenheight()

    root.attributes('-fullscreen', state)

def anykey(event=None):
    update_file()
    update_line_number()
    update_info_bar()
    highlight_word()
    update_info_bar()
####################

def about(event=None):

    showinfo("About", "Developed by @Luckymls & Francesco, penso dovrei scrivere altro forse")

def help_box(event=None):

    showinfo("Help", "For help email to melis.luca2014@gmail.com", icon='question')

def exit_editor():

    if askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()
root.protocol('WM_DELETE_WINDOW',exit_editor)

#####################



'''Index e tags'''
def select_all(event=None):
	textPad.tag_add('sel', '1.0', 'end')

def on_find(event=None):
	t2 = Toplevel(root)
	t2.title('Find')
	t2.geometry('300x65+200+250')
	t2.resizable(width=0,height=0)
	t2.transient(root)
	Label(t2,text="Find All:").grid(row=0, column=0, pady=4, sticky='e')
	v=StringVar()
	e = Entry(t2, width=25, textvariable=v)
	e.grid(row=0, column=1, padx=2, pady=4, sticky='we')
	c=IntVar()
	Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
	Button(t2, text='Find All', underline=0, command=lambda:search_for(v.get(), c.get(), textPad, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=4)
	def close_search():
		textPad.tag_remove('match', '1.0', END)
		t2.destroy()
	t2.protocol('WM_DELETE_WINDOW', close_search)

def search_for(needle,cssnstv, textPad, t2,e) :
        textPad.tag_remove('match', '1.0', END)
        count =0
        if needle:
                pos = '1.0'
                while True:
                    pos = textPad.search(needle, pos, nocase=cssnstv, stopindex=END)
                    if not pos: break
                    lastpos = '%s+%dc' % (pos, len(needle))
                    textPad.tag_add('match', pos, lastpos)
                    count += 1
                    pos = lastpos
                textPad.tag_config('match', foreground='white', background='blue')
        e.focus_set()
        t2.title('%d matches found' %count)

#Nuova funzione per rimarcare parti di codice, introdotta 26/10/17
#Qualcosa non mi convince riguardo al ciclo while e tag_config

def highlight_word(search=None, event=None):
    if highlight_wordln.get():
        textPad.tag_remove('code', '1.0', END)
        pos = '1.0'
        count = 0
        code = {'if':'green', '{':'red', '}':'red', 'true': 'orange', 'echo': 'purple', 'print': 'purple'}
        for search in code:
            pos = '1.0'
            count = 0
            while True:

                pos = textPad.search(search, pos, nocase=True, stopindex=END)
                if not pos: break
                lastpos = '%s+%dc' % (pos, len(search))
                textPad.tag_add('code'+search, pos, lastpos)
                count +=1
                pos = lastpos
                textPad.tag_config('code'+search, foreground=code[search])
    else:
        textPad.tag_remove('code', '1.0', END)

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


def paste():
    textPad.event_generate("<<Paste>>")
    update_line_number(load=True)


######################################################################

def wSetting():

    t3 = Toplevel(root)
    t3.title('Settings')
    t3.geometry('500x300')
    t3.resizable(width=0,height=0)
    t3.transient(root)

    '''Menu'''

    menuBar = Menu(t3)
    t3.config(menu=menuBar)

    nightMenu = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Help", menu=nightMenu)
    nightMenu.add_command(label="About", compound=LEFT, command=about)
    menuBar.add_command(label="Close", compound=LEFT, command=t3.destroy)


######################################################################
def new_file(event=None):
    global filename
    filename = None
    root.title("Untitled - TindyEditor")
    textPad.delete(1.0, END)
    update_line_number()


def open_file(event=None):
    global filename

    filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("Text Documents","*.txt")]) #("All Files","*.*"), Da aggiungere dopo che aggiungiamo i vari tipi di codifica
    if filename == "":
        filename = None
    else:

        pathAlreadyExists = 0
        checkConf = config.get('recent files')
        if checkConf: checkConf = checkConf.split('\n')
        else: checkConf = []
        for testPath in checkConf:
            if testPath == filename:
                pathAlreadyExists = 1
        if pathAlreadyExists is 0:
            config.set('recent files', '\n'+filename, 1)

        '''Ritorna il nome del file senza estensione'''
        root.title(os.path.basename(filename) + " - Tkeditor")
        textPad.delete(1.0,END)
        fh = open(filename,"r")
        textPad.insert(1.0,fh.read())
        fh.close()
    update_line_number(load=True)

def open_recent_file(filename=None):

    root.title(os.path.basename(filename) + " - Tkeditor")
    textPad.delete(1.0,END)
    fh = open(filename,"r")
    textPad.insert(1.0,fh.read())
    fh.close()
    update_line_number(load=True)

def save(event=None):
    global filename
    try:
        f = open(filename, 'w')
        letter = textPad.get(1.0, 'end')
        f.write(letter)
        f.close()
    except:
        save_as()

def save_as():
    try:
        '''Apro finestra wn per salvare file con nome'''
        f = filedialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("Text Documents","*.txt")]) #("All Files","*.*"),
        fh = open(f, 'w')
        global filename
        filename = f
        textoutput = textPad.get(1.0, END)
        fh.write(textoutput)
        fh.close()
        '''Imposto il titolo della finestra principale'''
        root.title(os.path.basename(f) + " - Tkeditor")
    except Exception as e:
        print('Exception: '+ str(e))

def update_file(event=None):
    update_line_number()
    if autoSave.get():
        try:
            rand = random.randint(1, 3)
            if rand is 3:

                f = 'Unsaved.txt'
                fh = open(f, 'w')
                global filename
                filename = f
                textoutput = textPad.get(1.0, END)
                fh.write(textoutput)
                fh.close()
                '''Imposto il titolo della finestra principale'''
                root.title(os.path.basename(f) + " - TindyEditor")
        except:
         pass
def update_info_bar(event=None):
    line = int(textPad.index('insert').split('.')[0])
    total = int(textPad.index('end').split('.')[0]) - 1
    column = int(textPad.index('insert').split('.')[1]) + 1
    infobar.config(text=f'Line {line}/{total} | Column {column}')

######################################################################
'''Icone del menù'''

'''Spiegazione rapida: label = testo, accelerator= testo per scorciatoia combinazione tasti, compund=posizione, command=comando da richiamare se si spunta/clicca l'opzione'''

if isLinux:
    completePath = os.getcwd()+'/'
else:
    completePath = ''
    root.iconbitmap('icons/pypad.ico')


new_fileicon = PhotoImage(file=completePath+'icons/new_file.gif')
open_fileicon = PhotoImage(file=completePath+'icons/open_file.gif')
saveicon = PhotoImage(file=completePath+'icons/save.gif')
cuticon = PhotoImage(file=completePath+'icons/cut.gif')
copyicon = PhotoImage(file=completePath+'icons/copy.gif')
pasteicon = PhotoImage(file=completePath+'icons/paste.gif')
undoicon = PhotoImage(file=completePath+'icons/undo.gif')
redoicon = PhotoImage(file=completePath+'icons/redo.gif')
on_findicon = PhotoImage(file=completePath+'icons/on_find.gif')
abouticon = PhotoImage(file=completePath+'icons/about.gif')

'''Menù'''
menubar = Menu(root)

'''File menù'''
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=new_fileicon, underline=0, command=new_file)
filemenu.add_separator()
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=open_fileicon, underline=0, command=open_file)
recentFiles = Menu(filemenu, tearoff=0)
filemenu.add_cascade(label="Recent Files", menu=recentFiles)
themechoice = IntVar()
filemenu.config(activebackground="#729FCF", activeforeground="#FFFFFF")

'''Add Recent Files'''

try:
    recentOpen = config.get('recent files').split('\n')
    for filePaths in recentOpen:
        if len(filePaths) > 3:
            fileName = os.path.basename(filePaths)[0].upper()+os.path.basename(filePaths)[1:]
            recentFiles.add_command(label=fileName, compound = LEFT, underline = 0, command= lambda: open_recent_file(filePaths))
except Exception as e:
    print('Exception: '+ str(e))

filemenu.add_separator()
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT, image=saveicon, underline=0, command=save)
filemenu.add_command(label="Save as", accelerator='Shift+Ctrl+S', command=save_as)
autoSave = IntVar()
autoSave.set(1)
filemenu.add_checkbutton(label="Save Automatically", variable=autoSave, command=update_file)
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
editmenu.add_command(labe="Paste", compound=LEFT, image=pasteicon, accelerator='Ctrl+V', command=paste)
editmenu.add_separator()
editmenu.add_command(label="Find", compound=LEFT, image=on_findicon, accelerator='Ctrl+F', command=on_find)
editmenu.add_separator()
editmenu.add_command(label="Select All", compound=LEFT, accelerator='Ctrl+A', underline=7, command=select_all)
editmenu.config(activebackground="#729FCF", activeforeground="#FFFFFF")
'''View menu'''

viewmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="View", menu=viewmenu)
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label="Show Line Number", variable=showln)
showinbar = IntVar()
showinbar.set(1)
viewmenu.add_checkbutton(label="Show Info Bar at Bottom", variable=showinbar, command=show_info_bar)
hltln = IntVar()
viewmenu.add_checkbutton(label="Highlight Current Line", variable=hltln, command=toggle_highlight)
highlight_wordln = IntVar()
viewmenu.add_checkbutton(label="Highlight Informatic Words", variable=highlight_wordln, command=highlight_word)
viewmenu.add_separator()
themesmenu = Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label="Themes", menu=themesmenu)
viewmenu.add_separator()
fullscreenln = IntVar()
nightmodeln = IntVar()
viewmenu.add_checkbutton(label="Night Mode", variable=nightmodeln.get(), accelerator='F9', command=night_mode)
viewmenu.add_checkbutton(label="Full Screen", variable=fullscreenln.get(),accelerator='F11', command=fullscreen)
viewmenu.config(activebackground="#729FCF", activeforeground="#FFFFFF")

'''Dizionario con: nome: esadecimale carattere.esadecimale sfondo'''
clrschms = {
'1. Default White': '000000.FFFFFF',
'2. Greygarious Grey':'83406A.D1D4D1',
'3. Lovely Lavender':'202B4B.E1E1FF' ,
'4. Aquamarine': '5B8340.D1E7E0',
'5. Bold Beige': '4B4620.FFF0E1',
'6. Cobalt Blue':'ffffBB.3333aa',
'7. Olive Green': 'D1E7E0.5B8340',
}
themechoice= StringVar()

'''Imposto tema se salvato altrimenti default'''
if config.get('theme'):


    themechoice.set(config.get('theme'))


else:
    themechoice.set('1. Default White')



for k in sorted(clrschms):
    themesmenu.add_radiobutton(label=k, variable=themechoice, command= lambda: theme(1))
themesmenu.config(activebackground="#729FCF", activeforeground="#FFFFFF")



'''Settings menu'''

settingsMenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Settings', menu=settingsMenu)
settingsMenu.add_command(label='Settings', compound=LEFT, command=wSetting)
settingsMenu.config(activebackground="#729FCF", activeforeground="#FFFFFF")

'''About menu'''
aboutmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=aboutmenu)
aboutmenu.add_command(label="About", compound=LEFT, command=about)
aboutmenu.add_command(label="Help", command=help_box)
aboutmenu.config(activebackground="#729FCF", activeforeground="#FFFFFF")
root.config(menu=menubar)

'''Exit menu'''
menubar.add_command(label='Exit', command=exit_editor)

'''Menù Scorciatoie e numero linea'''
shortcutbar = Frame(root, height=25)


icons = ['new_fileicon', 'open_fileicon', 'saveicon', 'cuticon', 'copyicon', 'pasteicon', 'undoicon', 'redoicon', 'on_findicon', 'abouticon']
for i, icon in enumerate(icons):
    tbicon = eval(icon)
    cmd = eval(icon[:-4])
    toolbar = Button(shortcutbar, image=tbicon,  command=cmd)
    toolbar.image = tbicon
    toolbar.pack(side=LEFT)

shortcutbar.pack(expand=NO, fill=X)




'''Info Bar'''

infobar = Label(root, text=f'Line:1 | Column:0')
infobar.pack(expand=NO, fill=None, side=BOTTOM, anchor='c')

'''Scrollbars drawing'''
scroll_y = Scrollbar(root)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x = Scrollbar(root, orient=HORIZONTAL)
scroll_x.pack(side=BOTTOM, fill=X)

'''Row Bar'''

lnlabel = Text(root,  width=4,  bg = 'antique white')
lnlabel.pack(side=LEFT, fill=Y)

'''Text widget'''

textPad = Text(root, undo=True, takefocus=True, wrap=NONE)
textPad.pack(expand=YES, fill=BOTH)


'''Scrollbar function'''
def yscroll(*args):
    textPad.yview(*args)
    lnlabel.yview(*args)


def mousewheel(event):
    #lnlabel.yview_moveto(textPad.yview()[0])
    if event.num == 4:
        lnlabel.yview_scroll(-1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])
    elif event.num == 5:
        lnlabel.yview_scroll(1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])
    elif event.delta >1:
        lnlabel.yview_scroll(-1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])
    elif event.delta < 1:
        lnlabel.yview_scroll(1, 'units')
        textPad.yview_moveto(lnlabel.yview()[0])

def select(event):
    lnlabel.yview_moveto(textPad.yview()[0])
    update_info_bar()
textPad.configure(yscrollcommand=scroll_y.set)
lnlabel.config(yscrollcommand=scroll_y.set)
scroll_y.config(command=yscroll)



textPad.configure(xscrollcommand=scroll_x.set)
scroll_x.config(command=textPad.xview)



'''Context Menu (Quando faccio click destro sulla casella di testo)'''
cmenu = Menu(textPad,tearoff=0)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    '''Aggiunto da poco, mette maiuscola nel menù cut => Cut'''
    i = i[0].upper()+i[1:]

    cmenu.add_command(label=i, compound=LEFT, command=cmd)
cmenu.add_separator()
cmenu.add_command(label='Select All', underline=7, command=select_all)
textPad.bind("<Button-3>", popup)


'''Imposto tema'''
theme(1)

#################################################
'''Rilevo evento tastiera, chiamo funzione'''


root.bind('<Any-KeyPress>', anykey)
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
textPad.bind('<Control-E>', highlight_word)
textPad.bind('<Control-e>', highlight_word)
textPad.bind_all('<Button-4>', mousewheel)
textPad.bind_all('<Button-5>', mousewheel)
textPad.bind_all('<MouseWheel>', mousewheel)
textPad.bind_all('<B1-Motion>', select)
root.bind('<KeyPress-F1>', help_box)
root.bind('<KeyPress-F2>', about)
root.bind('<KeyPress-F9>', night_mode)
root.bind('<KeyPress-F11>', fullscreen)


textPad.tag_configure("active_line", background="ivory2")

lnlabel.config(state='normal')
lnlabel.insert('current', '1')
lnlabel.config(state='disable')
root.mainloop() #luup#
