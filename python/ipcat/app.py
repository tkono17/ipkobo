#------------------------------------------------------------------------
# ipcat: app.py
# -------------
# Application logic (operations)
#------------------------------------------------------------------------
from .guiControl import GuiControl

class App:
    def __init__(self, model, gui=None):
        self.model = model
        self.gui = gui
        self.guiControl = None
        if self.gui:
            self.gui.handlers.setApp(self)
            self.guiControl = GuiControl(self.gui)
        pass
    
    # Actions on the model
    def addImagesFromDirectory(self, dname):
        pass
    
    def addImageFromFile(self, fname):
        if os.path.exists(fname):
            img1 = Image.open(fname)
            #img1 = img1.resize( (600, 400) )
            img2 = ImageTk.PhotoImage(img1)
            return img2
        return 0
        pass

    def addImageToList(self, imageData):
        pass

    def clearImageList(self):
        pass

    def setImage(self, imageName):
        pass

    def setAnalysis(self, analysisName):
        pass

    def runAnalysis(self, analysisName):
        pass

