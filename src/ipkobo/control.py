#------------------------------------------------------------------------
# ipcat: control.py
#------------------------------------------------------------------------
import os
from PIL import Image, ImageTk

from .model    import AppModel, ImageData
from .vcontrol import ViewController
from .common   import cdata

class Controller:
    def __init__(self):
        self.appData = AppModel()
        self.analysisList = []
        self.currentAnalysis = None
        pass

    def imageList(self):
        return self.appData.imageList
    
    #--------------------------------------------
    # Application actions
    #--------------------------------------------
    def openImage(self):
        dn = self.appData.openFileDir
        fn = cdata.vcontroller.openFile(dn, [('Image file', '*.jpg'), ('all', '*')])
        img = None
        if fn != '' and os.path.exists(fn):
            name = 'input%d' % len(self.appData.inputImageList)
            img = ImageData(name, fn)
            self.appData.addInputImage(img)
        return img

    def readImage(self, fn):
        if os.path.exists(fn):
            img1 = Image.open(fn)
            img1 = img1.resize( (600, 400) )
            img2 = ImageTk.PhotoImage(img1)
            return img2
        return 0
    
    def setInputImage(self, imageData):
        if self.currentAnalysis:
            self.currentAnalysis.setInputImage(imageData)
            cdata.vcontroller.setInputImage()

    pass
