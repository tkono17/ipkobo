#------------------------------------------------------------------------
# ipcat: control.py
#------------------------------------------------------------------------
import os
from PIL import Image, ImageTk

from .model    import AppData, ImageNP
from .vcontrol import ViewController

class Controller:
    def __init__(self):
        self.appData = AppData()
        self.vc = None
        pass

    def setViewController(self, vc):
        self.vc = vc

    #--------------------------------------------
    # Application actions
    #--------------------------------------------
    def openImage(self):
        dn = self.appData.openFileDir
        fn = self.vc.openFile(dn, [('Image file', '*.jpg'), ('all', '*')])
        print(fn)
        if fn != '' and os.path.exists(fn):
            name = 'input%d' % len(self.appData.imageList)
            img = ImageNP(name, fn)
            self.appData.addImage(img)
            self.vc.addImageToTree(img)

    def readImage(self, fn):
        if os.path.exists(fn):
            img1 = Image.open(fn)
            img1 = img1.resize( (600, 400) )
            img2 = ImageTk.PhotoImage(img1)
            return img2
        return 0

    
