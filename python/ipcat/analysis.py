#------------------------------------------------------------------------
# ipcat: analysis.py
#------------------------------------------------------------------------
import logging
from tkinter import ttk

from .model import *

logger = logging.getLogger(__name__)

class ImageAnalysis:
    def __init__(self, name):
        self.name = name
        self.nInputImages = 0
        self.parameters = {}
        self.inputImages = []
        self.parameterChoiceMap = {}
        self.outputImages = []
        self.outputValues = {}
        pass

    def addParameters(self, pars):
        self.parameters.extend(pars)

    def setParameter(self, key, value):
        self.parameters[key] = value

    def setInputImage(self, imageData):
        name, path, img = '', '', None
        if len(imageData)>0: name = imageData[0]
        if len(imageData)>1: path = imageData[1]
        if len(imageData)>2: img = imageData[2]
        x = ImageData(name, path, img)
        self.inputImages.clear()
        self.inputImages.append(x)
        
    def setInputImages(self, imageData):
        self.inputImages.clear()
        for data in imageData:
            name, path, img = '', '', None
            if len(imageData)>0: name = data[0]
            if len(imageData)>1: path = data[1]
            if len(imageData)>2: img = data[2]
            x = ImageData(name, path, img)
            self.inputImages.append(x)
        
    def run(self):
        logger.debug('ImageAnalysis.run()')
        pass
    
class SingleImageAnalysis:
    def __init__(self, name):
        self.name = name
        self.nInputImages = 1
        self.parameters = {}
        self.inputImages = []

    def run(self):
        super().run()

class ColorAnalysis(SingleImageAnalysis):
    def __init__(self, name):
        super().__init__(name)
        self.parameters = {
            'ColorConversion': 'COLOR_BGR2GRAY', 
            }
    def run(self):
        super().__init__()

class CannyEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name):
        super().__init__(name)
        self.parameters = {
            'Threshold1': 100, 
            'Threshold2': 50, 
            }
    def run(self):
        super().__init__()

class GfbaEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name):
        super().__init__(name)
        self.parameters = {
            'wsum': 30, 
            'tgap': 100,
            'direction': 'XY', 
            }
    def run(self):
        super().__init__()

class AnalysisStore:
    sInstance = None
    
    @staticmethod
    def get():
        if AnalysisStore.sInstance == None:
            AnalysisStore.sInstance = AnalysisStore()
        return AnalysisStore.sInstance
    
    def __init__(self):
        self.analysisTypes = []
        self.analysisClasses = {}
        self.initialize()
        pass

    def initialize(self):
        logger.info('AnalysisStore initialize')
        self.addAnalysis('ColorAnalysis', ColorAnalysis)
        self.addAnalysis('CannyEdgeAnalysis', CannyEdgeAnalysis)
        
    def addAnalysis(self, name, analysisClass):
        if name in self.analysisTypes:
            print(f'Analysis {name} already exists')
        else:
            self.analysisTypes.append(name)
            self.analysisClasses[name] = analysisClass

    def find(self, name):
        x = None
        if name in self.analysisClasses.keys():
            x = self.analysisClasses[name]
        return x

    def create(self, clsName, name=''):
        x = None
        cls = self.find(clsName)
        if cls:
            x = cls(name)
        return x
    
