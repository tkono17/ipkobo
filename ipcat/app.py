#------------------------------------------------------------------------
# ipcat: app.py
# -------------
# Application logic (operations)
#------------------------------------------------------------------------
import logging

from .analysis import AnalysisStore
from .io       import InputData
from .model    import AppModel
from .view     import View

logger = logging.getLogger(__name__)

# Static variable
sApp = None

class App:
    
    def __init__(self, useGUI=True):
        self.model = AppModel()
        self.view = View(self.model)
        self.view.setApp(self)
        self.mainWindow = self.view.mainWindow
        self.analysisStore = AnalysisStore.get()
        self.view.updateAnalysisList()
        pass

    # Static actions
    @staticmethod
    def get():
        return sApp

    def processCommand(self, cmd):
        words = cmd.split()
        cmdname = ''
        args = []
        if len(words)>=1:
            cmdname = words[0]
        args = words[1:]
        if cmdname == 'readImagesFromJson':
            pass
        elif cmdname == 'readImageFromFile':
            pass
        elif cmdname == 'selectImages':
            pass
        pass

    def mainloop(self):
        if self.view:
            self.view.mainloop()
            
    # Actions on the model
    def readImagesFromJson(self, fn):
        data = InputData(fn)
        v = data.getImages()
        for x in v:
            self.addImageToList(x)
    
    def readImageFromFile(self, fname):
        img2 = None
        if os.path.exists(fname):
            img1 = Image.open(fname)
            #img1 = img1.resize( (600, 400) )
            img2 = ImageTk.PhotoImage(img1)
        return img2

    def addImageToList(self, imageData):
        self.model.addImage(imageData)
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
        images = self.model.selectImages(imageNames)
        if self.view:
            self.view.showImages()
        pass
    
    def selectAnalysis(self, analysisName):
        #a = self.model.findAnalysis(analysisName)
        #self.model.selectImage(a)
        return self.model.selectAnalysis(analysisName)

    def setAnalysisParameters(self, pars):
        if self.model.currentAnalysis:
            self.model.currentAnalysis.setParameters(pars)
        pass
    
    def runAnalysis(self):
        image = self.model.currentImageFrame
        analysis = self.model.currentAnalysis
        logger.info(f'  runAnalysis {image}, {analysis}')
        if image and analysis:
            analysis.setInputImages(image, self.model.currentImages)
            analysis.run()
            self.view.updateGallery()
        pass
    def analysisOutputs(self):
        pass
    
    def clearImageList(self):
        pass

