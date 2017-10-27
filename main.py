from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
import os


root = Tk()
root.geometry('800x500')
root.title('Untitled - TindyEditor')
root.iconbitmap('icons/pypad.ico')
root.resizable(width=1,height=1)


##################

def popup(event):
    cmenu.tk_popup(event.x_root, event.y_root, 0)

'''Scelta tema'''
def theme():
        global bgc,fgc
        val = themechoice.get()
        clrs = clrschms.get(val)
        fgc, bgc = clrs.split('.')
        fgc, bgc = '#'+fgc, '#'+bgc
        textPad.config(bg=bgc, fg=fgc)

def show_info_bar():
    val = showinbar.get()
    if val:
        infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
    elif not val:
        infobar.pack_forget()

def update_line_number(event=None):
    txt = ''
    
    if showln.get(): 
        endline, endcolumn = textPad.index('end-1c').split('.')
        txt = '\n'.join(map(str, range(1, int(endline))))
        if int(endline) <= 30:
        
            anchor = 'nw'
        else:
            anchor = 'sw'
        lnlabel.config(text=txt, anchor=anchor)
    currline, curcolumn = textPad.index("insert").split('.')
    infobar.config(text='Line: %s | Column: %s'  %(currline,curcolumn) )

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
    
    if fullscreenln.get() == 0:
        state = 1
        fullscreenln.set(1)
    else:
        state = 0
        fullscreenln.set(0)
    #screen_w = root.winfo_screenwidth()
    #screen_h = root.winfo_screenheight()
    
    root.attributes('-fullscreen', state)
    
def anykey(event=None):
    update_line_number()
    update_file()
    highlight_word()

####################
    
def about(event=None):
    
    showinfo("About", "Developed by @Luckymls, penso dovrei scrivere altro forse")

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
    update_line_number()
    
def redo():
    textPad.event_generate("<<Redo>>")
    update_line_number()

def cut():
    textPad.event_generate("<<Cut>>")
    update_line_number()
    
def copy():
    textPad.event_generate("<<Copy>>")
    update_line_number()

def paste():
    textPad.event_generate("<<Paste>>")
    update_line_number()


######################################################################
    
def new_file(event=None):
    global filename
    filename = None
    root.title("Untitled - TindyEditor")
    textPad.delete(1.0, END)
    update_line_number()


def open_file(event=None):
    global filename
    
    filename = filedialog.askopenfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
    if filename == "":
        filename = None
    else:
        '''Ritorna il nome del file senza estensione'''
        root.title(os.path.basename(filename) + " - Tkeditor") 
        textPad.delete(1.0,END)         
        fh = open(filename,"r")        
        textPad.insert(1.0,fh.read()) 
        fh.close()
    update_line_number()

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
        f = filedialog.asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        fh = open(f, 'w')           
        global filename
        filename = f
        textoutput = textPad.get(1.0, END)
        fh.write(textoutput)              
        fh.close()
        '''Imposto il titolo della finestra principale'''
        root.title(os.path.basename(f) + " - Tkeditor") 
    except:
        pass

def update_file(event=None):

    try:
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
    update_line_number()
######################################################################
'''Icone del menù'''

'''Spiegazione rapida: label = testo, accelerator= testo per scorciatoia combinazione tasti, compund=posizione, command=comando da richiamare se si spunta/clicca l'opzione'''

newicon = PhotoImage(file='icons/new_file.gif')
openicon = PhotoImage(file='icons/open_file.gif')
saveicon = PhotoImage(file='icons/Save.gif')
cuticon = PhotoImage(file='icons/Cut.gif')
copyicon = PhotoImage(file='icons/Copy.gif')
pasteicon = PhotoImage(file='icons/Paste.gif')
undoicon = PhotoImage(file='icons/Undo.gif')
redoicon = PhotoImage(file='icons/Redo.gif')
on_findicon = PhotoImage(file='icons/on_find.gif')

'''Menù'''
menubar = Menu(root)

'''File menù'''
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT, image=newicon, underline=0, command=new_file)
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT, image=openicon, underline=0, command=open_file)
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT, image=saveicon, underline=0, command=save)
filemenu.add_command(label="Save as", accelerator='Shift+Ctrl+S', command=save_as)
filemenu.add_command(label="Exit", accelerator='Alt+F4', command=exit_editor)
menubar.add_cascade(label="File", menu=filemenu) 

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
viewmenu.add_checkbutton(label="Full Screen", variable=fullscreenln.get(),accelerator='F11', command=fullscreen)


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
themechoice.set('1. Default White')
for k in sorted(clrschms):
    themesmenu.add_radiobutton(label=k, variable=themechoice, command=theme)

'''About menu'''
aboutmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=aboutmenu)
aboutmenu.add_command(label="About", compound=LEFT, command=about)
aboutmenu.add_command(label="Help", command=help_box)

root.config(menu=menubar)

'''Menù Scorciatoie e numero linea'''
shortcutbar = Frame(root, height=25)
icons = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'on_find', 'about']
for i, icon in enumerate(icons):
    tbicon = PhotoImage(file='icons/'+icon+'.gif')
    cmd = eval(icon)
    toolbar = Button(shortcutbar, image=tbicon,  command=cmd)
    toolbar.image = tbicon  
    toolbar.pack(side=LEFT)
shortcutbar.pack(expand=NO, fill=X)

lnlabel = Label(root,  width=2,  bg = 'antique white')
lnlabel.pack(side=LEFT, fill=Y)



'''Text widget and scrollbar widget'''
#####################################

#BUG da fixare: scrollbar numero riga difettosa, offset numero righe sbagliato
textPad = Text(root, undo=True, takefocus=True)
textPad.pack(expand=YES, fill=BOTH)
scroll=Scrollbar(textPad)
textPad.configure(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)

'''Info Bar'''
infobar = Label(textPad, text='Line: 1 | Column:0')
infobar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')


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

#################################################
'''Rilevo evento tastiera, chiamo funzione'''
#Non capisco perchè ma per qualche strano motivo non rileva F11

root.bind('<Any-KeyPress>', anykey)
root.bind('<Control-N>', new_file)
root.bind('<Control-n>', new_file)
root.bind('<Control-O>', open_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-S>', save)
root.bind('<Control-s>', save)
textPad.bind('<Control-A>', select_all)
textPad.bind('<Control-a>', select_all)
textPad.bind('<Control-f>', on_find)
textPad.bind('<Control-F>', on_find)
textPad.bind('<Control-E>', highlight_word)
textPad.bind('<Control-e>', highlight_word)
root.bind('<KeyPress-F1>', help_box)
root.bind('<KeyPress-F2>', about)
root.bind('<KeyPress-F11>', fullscreen)


textPad.tag_configure("active_line", background="ivory2")


root.mainloop() #luup#


'''

       '   /            .       `          '                \
  `       /__________________________________________________\   `
           |           `      |    Can you        Maybe.    |'
     `   . |  ___  '  ______  |  believe it?!  `   , _____  |      '
   '       | |   |   |      | |'   |   | `~..    OO |     | |   `
      .    | |  o| . |_||||_| |  . |  o|   >>   ((  |_____| |_      `
        ___|_|___|____________|____|___|__ |\ _ b b ________|_`._ '
       ----------------------------------------------------------
 ________
         \                 `   .
 _________\  '
         |     That's not          It is if you're
  _____  |      an answer.         ,  a skepticist.
 |     | | `             `~..    OO
 |_____| |     .    '      >>   ((
 ________|________________ |\ _ b b ___________


                Hold on.            I believe a certain amount
              "Skepticist"?         ,  of skepticism is healthy.
                         `~..     OO
                          .>>.   ((
                  ________ || __ b b _________


                    Really?         Maybe.
                          `         ,
                          ~..     OO
                          .>>.   .||.
                jg________ || ___ dd _________
'''
