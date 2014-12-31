# -*- coding: utf8 -*-
'''
Created on 2014-12-22

@author: zhanghl
'''
from Tkinter import Frame, Button
import subprocess

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self, width=400,height=550)

        self.grid_propagate(True)
        self.grid()
        self.column = 0
        self.row = 0
#         self.propagate(False)
#         self.pack()
        
#         button = Button(self,text="hello",command=lambda:self.calback(name='zzzz'))
#         button.grid(row=0,column=0,padx=15,pady=15)
        
    def calback(self,name = 'name'):
#         tkMessageBox.showinfo("message", "hello world " + name)
        if name.endswith(".exe"):
            self.runExeCommand(name)

    def addButton(self,text='',exeMsg = ''):
        text = self.subName(text)
        button = Button(self,text=text,command=lambda:self.calback(name = exeMsg),wraplength=100)
        if self.column==0 & self.row==0:
            button.focus_set()
            
        self.column = self.column+1
        button.grid(row=self.row,column = self.column,padx=15,pady=15)
        if self.column==4:
            self.row = self.row + 1
            self.column = 0
        
    def subName(self,name):
        '''
            截取长度，如果长度大于5 截取，这里统一截取了，没有判断中英文
            中文应该 是一个占3位，后期完善
        '''
        if len(name)>5:
            name  = name.decode('utf-8')[0:5].encode('utf-8') + " ..."
        return name
        
    def runExeCommand(self,commandStr):
        if commandStr:
            subprocess.Popen([commandStr])
        self.quit()
        
    def main(self):
#         frame.addButton("213", "adsfdafdd")
        self.addButton("Sublime Text", "D:/Program Files/Sublime Text/SublimeText.exe")
        self.addButton("Sublime Text", "D:/Program Files/Sublime Text/SublimeText.exe")
        self.addButton("Sublime Text", "D:/Program Files/Sublime Text/SublimeText.exe")
        self.addButton("Sublime Text", "D:/Program Files/Sublime Text/SublimeText.exe")
        self.addButton("Sublime Text", "D:/Program Files/Sublime Text/SublimeText.exe")
        self.addButton("Sublime Text", "D:/Program Files/Sublime Text/SublimeText.exe")
        self.addButton("Sublime Text", "D:/Program Files/Sublime Text/SublimeText.exe")
        
        def focusout(*argus):
            self.runExeCommand("")
#         self.bind(sequence = "<Expose>", func = test,add= "+")
#         self.bind(sequence = "<FocusOut>", func = test,add= "+")
#         self.bind(sequence = "<Unmap>", func = test,add= "+")
#         
#         self.bind("<Leave>", self.test)
        self.bind("<FocusOut>", focusout)
        self.mainloop()
        
frame = MyFrame()
frame.main() 
