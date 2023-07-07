#------------------------------------------------------------------------
# ipcat: handlers.py
#------------------------------------------------------------------------
import tkinter as tk

from .control  import *
from .common import cdata

class Handlers:
    def __init__(self):
        self.app = None
        self.vcontrol = None
        
    def setApp(self, app):
        self.app = app
        self.guiControl = app.guiControl
        
    def openImage(self):
        print('openImage called')
        dn = self.app.model.openFileDir
        img = self.guiControl.openImage(dn)
        self.app.addImageFromFile(img)

    def singleDisplaySet(self):
        print('singleDisplaySet')
        tree = self.app.userInputPanel.imageTree
        v = tree.selection()
        print('Images selected %d' % len(v))
        self.image = None
        if len(v) == 1:
            entry = tree.item(v[0])
            values = entry['values']
            iname = values[0]
            path = values[1]
            vc = self.controller.vc
            img = self.controller.readImage(path)
            print('Open file path: %s' % path)
            print('w,h = {},{}'.format(img.width(), img.height()) )
            canvas = self.app.userControlPanel.singleDisplay.canvas
            canvas.create_image(0, 0, image=img, anchor=tk.NW)
            self.image = img
            canvas.update()
            
    def selectImage(self, e):
        print('selectImage from Treeview called')
        tree = e.widget
        selected = tree.selection()
        if len(selected) == 1:
            print(selected[0])
            values = tree.item(selected[0])['values']
            print(values)

def openImage():
    img = cdata.controller.openImage()
    cdata.vcontroller.addImage(img)

def selectImage():
    tree = cdata.app().userInputPanel.imageTree
    v = tree.selection()
    print('Images selected %d' % len(v))
    self.image = None
    if len(v) == 1:
        entry = tree.item(v[0])
        values = entry['values']
        name = values[0]
        path = values[1]
        
        cdata.contorller.setInputImage( (name, path) )
        #
        img = cdata.controller.readImage(path)
        print('Open file path: %s' % path)
        print('w,h = {},{}'.format(img.width(), img.height()) )
        #canvas = self.app.userControlPanel.singleDisplay.canvas
        #canvas.create_image(0, 0, image=img, anchor=tk.NW)
        #self.image = img
        #canvas.update()


#    # Actions
#    def addImagesFromDirectory(self, dname):
#        pass
#    def addImageToList(self, image):
#        pass
#    def clearImageList(self):
#        pass
#    def selectImage(self, imageName):
#        pass
#    def showImage(self, image):
#        pass
#    def selectAnalysis(self, analysisName):
#        pass
#    def addAnalysisProperty(self, prop):
#        pass
#    def clearAnalysisProperties(self):
#        pass
#    def clearGallery(self):
#        pass
#    def showImageInGallery(self, image):
#        pass
    
