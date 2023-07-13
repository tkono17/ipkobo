#------------------------------------------------------------------------
# ipcat: app.py
# -------------
# Application logic (operations)
#------------------------------------------------------------------------
from .view import View
from .analysis import AnalysisStore

class App:
    def __init__(self, model, gui=None):
        self.model = model
        self.gui = gui
        self.view = None
        if self.gui:
            self.view = View(self.gui)
            self.gui.handlers.setApp(self)
        self.analysisStore = AnalysisStore()
        self.view.updateAnalysisList()
        pass
    
    # Actions on the model
    def readImagesFromDirectory(self, dname):
        pass
    
    def readImageFromFile(self, fname):
        img2 = None
        if os.path.exists(fname):
            img1 = Image.open(fname)
            #img1 = img1.resize( (600, 400) )
            img2 = ImageTk.PhotoImage(img1)
        return img2

    def addImageToList(self, imageData):
        self.model.addImageToList(imageData)
        if self.view:
            self.view.updateImageList()
        pass

    def allImageNames(self):
        v = self.model.allImageNames()
        return v
    
    def allAnalysisNames(self):
        v = self.model.allAnalysisNames()
        return v
    
    def selectImages(self, imageNames):
        images = []
        for imageName in imageNames:
            img = self.model.findImage(imageName)
            if img:
                images.append(img)
                print(img.name, img.path, img.width, img.offset)
            else:
                logger.warning(f'Cannot find image {imageName}')
        self.model.selectImages(images)
        if self.view:
            self.view.showImages(images)
        pass
    
    def selectAnalysis(self, analysisName):
        a = self.model.findAnalysis(analysisName)
        self.model.selectImage(a)
        pass

    def setAnalysisParameters(self, pars):
        if self.model.currentAnalysis:
            self.model.currentAnalysis.setParameters(pars)
        pass
    
    def runAnalysis(self):
        if self.model.currentAnalysis:
            self.model.currentAnalysis.run()
        pass
    def analysisOutputs(self):
        pass
    
    def clearImageList(self):
        pass

