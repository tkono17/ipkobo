#------------------------------------------------------------------------
# ipcat: gui.py
#------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from .handlers import Handlers, openImage
from .guiComponents import *
from .analysis import *

def initTk():
    root = tk.Tk()
    root.title('Image Processing Square')
    root.geometry('1000x600')
    root.minsize(width=500, height=400)
    return root

#------------------------------------------------------------------------
# MainWindow
#------------------------------------------------------------------------
class MainWindow(ttk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1000, height=600, style='main.TFrame')
        self.pack(expand=True, fill=tk.BOTH)
        self.handlers = Handlers()
        #
        self.setStyle()
        self.setup()
        
    def setup(self):
        frame = ttk.Frame(self, width=1000, height=800, 
                          style='Red.TFrame')
        frame.pack(anchor=tk.NW, expand=True, fill=tk.BOTH)
        lr = ttk.Panedwindow(frame, orient=tk.HORIZONTAL)
        lr.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        x1 = self.buildLeftPanel(lr)
        x2 = self.buildDisplayPanel(lr)
        lr.add(x1)
        lr.add(x2)
        #
        self.setupHandlers()
        #
        self.initialized = True
        pass

    def setupHandlers(self):
        #self.userInputPanel.openFile['command'] = self.handlers.openImage
        self.userInputPanel.imageTree.bind('<Double-1>', self.handlers.selectImage)
        #self.userControlPanel.singleDisplaySet['command'] = self.handlers.singleDisplaySet

    def setStyle(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Main.TFrame', background='yellow')
        style.configure('Blue.TFrame', foreground='yellow', background='blue')
        style.configure('Red.TFrame', background='red')
        style.configure('Green.TFrame', background='green')
        style.configure('P1.TFrame', background='#abcdef' )

    # Functions to build subcomponents
    def buildLeftPanel(self, parent):
        frame = ttk.Panedwindow(parent, orient=tk.VERTICAL)
        frame.pack(expand=True, fill=tk.BOTH)
        x1 = self.buildUserPanel(frame)
        x2 = self.buildMessagePanel(frame)
        frame.add(x1)
        frame.add(x2)
        self.messagePanel = x2
        return frame
        
    def buildUserPanel(self, parent):
        frame = ttk.Panedwindow(parent, orient=tk.HORIZONTAL, height=400)
        frame.pack(expand=True, fill=tk.BOTH)
        frame.pack()
        x1 = self.buildUserInputPanel(frame)
        x2 = self.buildUserControlPanel(frame)
        frame.add(x1)
        frame.add(x2)
        self.userInputPanel = x1
        self.userControlPanel = x2
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
        self.displayPanel = x
        return x

    def addAnalysisPanel(self, name):
        self.userControlPanel.addAnalysisPanel(name)
        pass
    
    def addDisplayPanel(self, name):
        self.displayPanel.addDisplayPanel(name)
        pass

    def clear(self):
        self.userControlPanel.clear()
        self.displayPanel.clear()
        pass

#------------------------------------------------------------------------
# UserInputPanel
#------------------------------------------------------------------------
class UserInputPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=400)
        self.build()
        
    def build(self):
        columns = ('Name', 'Path')
        openFile = ttk.Button(self, text='Open file')
        treeView = ttk.Treeview(self, columns=columns)
        treeView.column('#0', anchor='w', width=0, stretch='no')
        treeView.column('Name', anchor='w', width=20)
        treeView.column('Path', anchor='w', width=60)
        #
        openFile.pack(anchor=tk.NW)
        treeView.pack(anchor=tk.W, fill=tk.BOTH, expand=True)
        #
        openFile['command'] = openImage
        self.openFile = openFile
        self.imageTree = treeView
        pass
    pass

#------------------------------------------------------------------------
# Control panels
#------------------------------------------------------------------------
class SingleDisplayPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='Red.TFrame')
        button = ttk.Button(self, text='Set')
        button.pack(anchor=tk.NW)
        self.setButton = button
        c = tk.Canvas(self, bg='cyan')
        c.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas = c
        
#------------------------------------------------------------------------
# UserControlPanel
#------------------------------------------------------------------------
class UserControlPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build()
        
    def build(self):
        notebook = ttk.Notebook(self, width=400)
        notebook.pack(expand=True, fill=tk.BOTH)
        self.tabs = notebook
        self.addAnalysisPanel('SingleImageAnalysis')
        self.addAnalysisPanel('ColorAnalysis')
        self.addAnalysisPanel('CannyEdgeAnalysis')
        pass

    def addAnalysisPanel(self, name):
        if name in analysisClassMap.keys():
            cls1 = analysisClassMap[name]
            analysis = cls1(name)
            x = ImageControlPanel(self.tabs, analysis)
            x.pack(expand=True, fill=tk.BOTH)
            self.tabs.add(x, text=name)
            self.singleDisplay = x
            #self.singleDisplaySet = x.setButton
        else:
            pass
    def clear(self):
        pass
    pass

#------------------------------------------------------------------------
# MessagePanel
#------------------------------------------------------------------------
class MessagePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def build(self):
        pass
    pass

#------------------------------------------------------------------------
# DisplayPanel
#------------------------------------------------------------------------
class DisplayPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH)
        self.tabs = notebook
        self.addDisplayPanel('Gallery')
        
    def addDisplayPanel(self, name):
        frame = ttk.Frame(self.tabs, style='Blue.TFrame', width=600)
        frame.pack(expand=True, fill=tk.BOTH)
        self.tabs.add(frame, text=name)
        
