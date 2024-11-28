#------------------------------------------------------------------------
# app/app.py
#------------------------------------------------------------------------
import logging

from ..model import AppModel
from ..view import View

logger = logging.getLogger(__name__)

class App:
    kGui = 'gui'
    kBatch = 'batch'
    def __init__(self, runMode='gui'):
        self.model = AppModel()
        self.view = None
        
        self.runMode = runMode
        if self.runMode == App.kBatch:
            self.view = View(self.model, self)
            self.view.model = self.model
        pass

    def initialize(self):
        self.model.initialize()
        if self.view:
            self.view.initialize()
        
    def addImage(self, imageData):
        self.model.addImage(imageData)
        if self.view:
            self.view.updateImageList()

    def readImagesFromJson(self, jsonFile):
        self.model.addImagesFromJson(jsonFile)
        if self.view:
            self.view.updateImageList()
    
    def selectImages(self, imageNames):
        img = self.model.selectImages(imageNames)
        if self.view:
            self.view.updateMainPanel()
        return img

    def selectAnalysis(self, analysisName):
        a = self.model.selectAnalysis(analysisName)
        if self.view:
            self.view.updateAnalysisPanel()
        return a

    def setAnalysisProperty(self, propName, propValue):
        if self.model.currentAnalysis:
            self.model.currentAnalysis.setProperty(propName, propValue)
        if self.view:
            self.view.updateAnalysisProperties()
        pass

    def runAnalysis(self):
        logger.info('Run analysis')
        if self.view:
            self.view.updateAnalysisParameters()
        self.model.runAnalysis()
        if self.model.currentAnalysis:
            logger.info(f'  N outputs: {len(self.model.currentAnalysis.outputImages)}')
            for img in self.model.currentAnalysis.outputImages:
                self.addImage(img)
        if self.view:
            self.view.updateGallery()
        pass
    
