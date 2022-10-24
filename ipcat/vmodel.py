#------------------------------------------------------------------------
# ipcat: vmodel.py
#------------------------------------------------------------------------

from tkinter import ttk

from .gui import *

class ViewModel:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.setStyle()
        pass

    def setStyle(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Main.TFrame', background='yellow')
        style.configure('Blue.TFrame', foreground='yellow', background='blue')
        style.configure('Red.TFrame', background='red')
        
    def initialize(self):
        frame = ttk.Frame(self.mainWindow, width=1000, height=800, 
                          style='Red.TFrame')
        frame.pack(anchor=tk.NW, expand=True, fill=tk.BOTH)
        lr = ttk.Panedwindow(frame, orient=tk.HORIZONTAL)
        lr.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        x1 = self.buildLeftPanel(lr)
        x2 = self.buildDisplayPanel(lr)
        lr.add(x1)
        lr.add(x2)
        
    def buildLeftPanel(self, parent):
        frame = ttk.Panedwindow(parent, orient=tk.VERTICAL)
        frame.pack(expand=True, fill=tk.BOTH)
        x1 = self.buildUserPanel(frame)
        x2 = self.buildMessagePanel(frame)
        frame.add(x1)
        frame.add(x2)
        return frame
        
    def buildUserPanel(self, parent):
        frame = ttk.Panedwindow(parent, orient=tk.HORIZONTAL, height=400)
        frame.pack(expand=True, fill=tk.BOTH)
        frame.pack()
        x1 = self.buildUserInputPanel(frame)
        x2 = self.buildUserControlPanel(frame)
        frame.add(x1)
        frame.add(x2)
        return frame
        
    def buildUserInputPanel(self, parent):
        x = UserInputPanel(parent)
        x.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        return x
    
    def buildUserControlPanel(self, parent):
        x = UserControlPanel(parent)
        x.pack(expand=True, fill=tk.BOTH)
        return x

    def buildMessagePanel(self, parent):
        x = tk.Text(parent, width=40, height=10)
        x.pack(expand=True, fill=tk.BOTH)
        return x

    def buildDisplayPanel(self, parent):
        x = DisplayPanel(parent)
        x.pack(fill=tk.BOTH, expand=True)
        return x
    

