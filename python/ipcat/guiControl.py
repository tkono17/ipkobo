#------------------------------------------------------------------------
# ipcat: guiControl.py
# --------------------
# GUI logic (operations)
#------------------------------------------------------------------------
import os
import tkinter as tk

from .model import ImageData

def GuiControl:
    def __init__(self, gui):
        self.gui = gui
        pass
    
    # Actions on the GUI
    def openImage(self, dname):
        ftypes = [('Image file', '*.jpg'), ('all', '*')]
        fn = tk.filedialog.askopenfilename(filetypes=ftypes,
                                                initialdir=dname)
        img = None
        if fn != '' and os.path.exists(fn):
            name = 'input%d' % len(self.appData.inputImageList)
            img = ImageData(name, fn)
        return img
        pass
    
    def updateImageList(self):
        pass
    
    def showImage(self, imageData):
        pass

    def clearImage(self):
        pass

    def addAnalysisProperty(self, prop):
        pass

    def updateAnalysisProperties(self):
        pass

    def clearAnalysisProperties(self):
        pass

    def showImageInGallery(self, image):
        pass
    
    def updateGallery(self):
        pass

    def clearGallery(self):
        pass

