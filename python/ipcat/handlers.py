#------------------------------------------------------------------------
# ipcat: handlers.py
#------------------------------------------------------------------------
import logging
import tkinter as tk

from .control  import *
from .common   import cdata
from .test     import *

logger = logging.getLogger(__name__)

class Handlers:
    def __init__(self):
        self.app = None
        self.view = None
        
    def setApp(self, app):
        self.app = app
        self.view = app.view
        
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
            
    def runTest(self, testName):
        test = None
        if testName == 'BasicGuiTest':
            test = BasicGuiTest('test1', self.app)
        if test:
            test.run()
            
    def showImages(self, e):
        print('showImages called')
        tree = self.view.gui.imageList
        items = tree.selection()
        names = []
        for item in items:
            values = tree.item(item)['values']
            names.append(values[0])
        self.app.selectImages(names)

    def runAnalysis(self, e):
        logger.info('Run analysis')

    def analysisSelected(self, e):
        analysisName = e.widget.get()
        logger.info(f'Analysis selected ==> {analysisName}')
        self.view.analysisSelected(analysisName)
        
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
    
