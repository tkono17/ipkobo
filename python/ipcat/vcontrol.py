#------------------------------------------------------------------------
# ipcat: vcontrol.py
#------------------------------------------------------------------------

import tkinter as tk
import tkinter.filedialog
from   tkinter import ttk
import logging

from .gui import *
from .vmodel import ViewModel
from .common import cdata

log = logging.getLogger(__name__)

class ViewController:
    def __init__(self, mainWindow):
        self.app = mainWindow
        self.vmodel = ViewModel()
        self.treeInitialized = False
        pass

    def openFile(self, dname, ftypes):
        fn = tkinter.filedialog.askopenfilename(filetypes=ftypes, initialdir=dname)
        print('File opened: %s' % fn)
        return fn

    def addImage(self, img):
        self.addImageToTree(img)
        #self.update()

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
        n = len(tree.get_children())
        names = []
        for i in range(n):
            x = tree.get_children()[i]
            item = tree.item(x)
            names.append(item['values'][0])
        for img in self.vmodel.imageList:
            if not img.name in names:
                tree.insert('', 'end', values=(img.name, img.path))
            
    def setInputImage(self):
        tabName = cdata.app().tabs.select()
        print(tabName)

    def update(self):
        print('ViewController.update()')
        tabs = cdata.app().userControlPanel.tabs
        #x = tabs.select()
        #i = tabs.index(x)
        n = len(tabs.children)
        for i in range(n):
            p = list(tabs.children.values())[i]
            self.updateImageAnalysisPanel(p)
        
    #--------------------------------------------------------------------
    # Actions to ImageAnalysisPanel
    #--------------------------------------------------------------------
    def updateImageAnalysisPanel(self, p):
        log.debug('Update image analysis panel combo')
        for cb in p.comboEntries:
            keys = list(map(lambda x: x.name, cdata.controller.imageList()))
            log.debug('Combo keys: %s', str(keys))
            cb.comboBox['values'] = keys
            if not cb.entry in keys:
                cb.entry.textvariable = 'ABC'
            cb.entry['textvariable'] = 'ABC'
            
