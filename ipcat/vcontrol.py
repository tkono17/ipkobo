#------------------------------------------------------------------------
# ipcat: vcontrol.py
#------------------------------------------------------------------------

import tkinter as tk
import tkinter.filedialog
from   tkinter import ttk

from .gui import *
from .vmodel import ViewModel

class ViewController:
    def __init__(self, mainWindow):
        self.app = mainWindow
        self.vmodel = ViewModel(mainWindow)
        self.treeInitialized = False
        pass

    def openFile(self, dname, ftypes):
        fn = tkinter.filedialog.askopenfilename(filetypes=ftypes, initialdir=dname)
        print('File opened: %s' % fn)
        return fn
        
    def addImageToTree(self, img):
        self.vmodel.imageList.append(img)
        self.updateImageTree()

    def initImageTree(self):
        columns = ('Name', 'Path')
        tree = self.app.userInputPanel.imageTree
        tree.heading('#0', text='level', anchor='w')
        for c in columns:
            tree.heading(c, text=c, anchor='w')

    def updateImageTree(self):
        print('updateImageTree')
        tree = self.app.userInputPanel.imageTree
        if not self.treeInitialized:
            self.initImageTree()
        for img in self.vmodel.imageList:
            tree.insert('', 'end', values=(img.name, img.path))
            

