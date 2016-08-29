import tkinter
from tkinter import *
from tkinter.scrolledtext import *
from tkinter import filedialog as filedialog
from tkinter import messagebox as messagebox
import os
from re import *
from pygments import *
from pygments.lexers import PythonLexer
import subprocess as sub
import sys










#proc = sub.Popen(['python', 'test.py'], stdout=sub.PIPE, stderr=sub.STDOUT)
#proctext = proc.stdout.read()
#retcode = proc.wait()
#
#print (proctext)



#textPad = ScrolledText(root,width=100,height=80, bg = "black",fg = "white",font=('courier', 16, 'normal'),insertbackground= "green",bd=0, highlightthickness=0 )
#textPad.config(cursor = "boat blue blue")

#textPad.pack()
#textPad.insert(END, proctext)


            



         

 

    
#menu = Menu(root)
#root.config(menu=menu)
#filemenu = Menu(menu)
#menu.add_cascade(label="File", menu=filemenu)
#filemenu.add_command(label="New", command=code)
#filemenu.add_command(label="Open...", command=open_command)
#filemenu.add_command(label="Save", command=save_command)
#filemenu.add_separator()
#filemenu.add_command(label="Exit", command=exit_command)
#
#helpmenu = Menu(menu)
#menu.add_cascade(label="Help", menu=helpmenu)
#helpmenu.add_command(label="About", command = about_command)
#

#textPad.pack()
#root.mainloop()

class PyPad: 
    
    def __init__(self):
        
        self.root = Tk()
        self.root.title("PyEditor")
        self.root.maxsize(width=1500, height= 1015)
        self.textPad = ScrolledText(self.root,width=100,height=80, bg = "black",fg = "white",font=('Menlo-Regular', 16, 'normal'),insertbackground= "green",bd=0, highlightthickness=0 )
        self.textPad.config(cursor = "boat blue blue")
        self.output = ScrolledText(self.root, width = 50, height = 80,bd=0, highlightthickness=0,font=('Menlo-Regular', 16, 'normal'))
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.dummy)
        self.filemenu.add_command(label="Open...", command=self.ope)
        self.filemenu.add_command(label="Save", command=self.save_command)
        self.filemenu.add_command(label="Save As", command=self.save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit)
        self.previousContent = 0
        self.projectmenu = Menu(self.menu)
        self.menu.add_cascade(label="Project", menu = self.projectmenu) 
        self.projectmenu.add_command(label = "Build", command= self.code_output)
        self.helpmenu = Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=self.helpmenu)
        self.helpmenu.add_command(label="About")
        self.name = False
        self.highlightWords = {'if': 'green',  
        'else': 'green', 
        'def': "pink", 
        ":": 'orange',
        "0": "red"
        
        }

    
        self.textPad.pack(side = "left")
        self.textPad.bind('<KeyRelease>', self.highlight)
        self.output.pack(side = "right")

        self.root.mainloop()
        
        

        

    def highlighter(self, event):
    
        for k,v in self.highlightWords.items(): # iterate over dict
            self.startIndex = '1.0'
            
            while True:
                self.startIndex = self.textPad.search(k, self.startIndex, END) # search for occurence of k
                if self.startIndex:
                    self.endIndex = self.textPad.index('%s+%dc' % (self.startIndex, (len(k)))) # find end of k
                    self.textPad.tag_add(k, self.startIndex, self.endIndex) # add tag to k
                    self.textPad.tag_config(k, foreground=v)      # and color it with v
                    self.startIndex = self.endIndex # reset startIndex to continue searching
                else:
                    break
          
    def dummy(self): 
        print("I am dummy")
 
    def code_output(self):
        
        
        self.save_command()            
        self.proc = sub.Popen(['python', self.name.name], stdout=sub.PIPE, stderr=sub.STDOUT)
        self.proctext = self.proc.stdout.read()
        self.retcode = self.proc.wait() 

            
        self.output.insert(END, self.proctext)
           
    def highlight(self, argument):
        self.content = self.textPad.get("0.0", END)

        if (self.previousContent != self.content):
            self.textPad.mark_set("range_start", "0.0")

            self.words = self.content.split(" ")
            self.lastWordLength = len(self.words[len(self.words) - 1])
            
            self.lastPos = self.textPad.index("end-1c")
            self.startRow = int(self.lastPos.split(".")[0])
            self.startCol = abs(int(self.lastPos.split(".")[1]) - self.lastWordLength)
            
            print(self.startRow, self.startCol) # Results in incorrect values

            data = self.textPad.get("0.0", END)
            for token, content in lex(data, PythonLexer()):
                self.textPad.tag_configure("Token.Keyword", foreground="pink")
                self.textPad.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
                self.textPad.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
                self.textPad.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
                self.textPad.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
                self.textPad.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
                self.textPad.tag_configure("Token.Keyword.Type", foreground="#CC7A00")
                
                self.textPad.tag_configure("Token.Name.Class", foreground="#003D99")
                self.textPad.tag_configure("Token.Name.Exception", foreground="#003D99")
                self.textPad.tag_configure("Token.Name.Function", foreground="#003D99")
                self.textPad.tag_configure("Token.Operator.Word", foreground="#CC7A00")
                self.textPad.tag_configure("Token.Comment", foreground="#B80000")
                self.textPad.tag_configure("Token.Literal.String", foreground="#248F24")

                self.textPad.mark_set("range_end", "range_start + %dc" % len(content))
                self.textPad.tag_add(str(token), "range_start", "range_end")
                self.textPad.mark_set("range_start", "range_end")
                

        self.previousContent = self.textPad.get("0.0", END)
                         
                        
    def ope(self):
        #file = filedialog.askopenfile()
        #self.name = file 
        
        if self.textPad.get(1.0,END) == "\n":
            file = filedialog.askopenfile()
            self.name = file 
            contents = file.read()
            self.textPad.insert('1.0',contents)
            file.close()
            
        else:
            self.save_command()
            file = filedialog.askopenfile()
            self.name = file 
            self.textPad.delete(1.0, END)
            contents = file.read()
            self.textPad.insert('1.0',contents)
            file.close()
        self.root.title("PyEditor: " + self.name.name )
    def readFile(self,filename):
        
        f = open(filename, "w")
        text = f.read()
        f.close()
        return text
    
    def save_command(self):
        print(self.name)
        if self.name == False : 
            
            file = filedialog.asksaveasfile(mode='w', defaultextension=".py", title = "Save As")
            self.name = file
            if file != None:
    # slice off the last character from get, as an extra return is added
                data = self.textPad.get('1.0', END+'-1c')
                f =  open(self.name.name, 'w')
                f.write(data)
                f.close()
                self.root.title("PyEditor: " + self.name.name )
        else:
            data = self.textPad.get('1.0', END+'-1c')
            f =  open(self.name.name, 'w')
            f.write(data)
            f.close()
 
    def save_as(self):
        if self.name == False:
            
            file = filedialog.asksaveasfile(mode='w', defaultextension=".py", title = "Save As")
            self.name = file
            if file != None:
    # slice off the last character from get, as an extra return is added
                data = self.textPad.get('1.0', END+'-1c')
                f =  open(self.name.name, 'w')
                f.write(data)
                f.close() 
        else:
            file = filedialog.asksaveasfile(mode='w', defaultextension=".py", title = "Save As", initialfile = self.name.name) #fix 
            self.name = file
            if file != None:
    # slice off the last character from get, as an extra return is added
                data = self.textPad.get('1.0', END+'-1c')
                f =  open(self.name.name, 'w')
                f.write(data)
                f.close() 
        self.root.title("PyEditor: " + self.name.name )  
    
    
    def exit(self):
        self.save_command()
        self.root.destroy()
    
        
        

        
        
        
        
        
        
       

       


        