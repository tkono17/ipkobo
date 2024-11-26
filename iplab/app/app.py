#------------------------------------------------------------------------
# app/app.py
#------------------------------------------------------------------------
from ../model/data import AppModel
from ../view/view import View

class App:
    def __init__(self, runMode='gui'):
        self.model = AppModel()
        self.view = None
        
        self.runMode = runMode
        if self.runMode = 'gui':
            self.view = View(self.model, self)
            self.view.model = self.model
        pass

    def addImage(self, imageData):
        self.model.addImage(imageData)
        if self.view:
            self.view.updateList()

    def selectImage(self, imageName):
        img = self.model.selectImage(imageName)
        if self.view:
            self.view.updateMainPanel()
        return img

    def selectAnalysis(self, analysisName):
        a = self.model.selectAnalysis(analysisName)
        if self.view:
            self.view.updateAnalysis()
        return a

    def setAnalysisProperty(self, propName, propValue):
        if self.model.currentAnalysis:
            self.model.currentAnalysis.setProperty(propName, propValue)
        if self.view:
            self.view.updateAnalysisProperties()
        pass

    def runAnalysis(self):
        if self.model.currentAnalysis:
            self.model.currentAnalysis.run()
        if self.view:
            self.view.updateGallery()
        pass
    
