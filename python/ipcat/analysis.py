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
        self.parameters = {}
        self.nInputImages = 0
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
        self.inputImages.clear()
        self.inputImages.append(imageData)
        
    def setInputImages(self, imageData):
        self.inputImages.clear()
        for data in imageData:
            self.inputImages.append(data)
        
    def run(self):
        logger.debug('ImageAnalysis.run()')
        pass
    
class SingleImageAnalysis(ImageAnalysis):
    def __init__(self, name):
        super().__init__(name)
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
        img1 = self.inputImages[0].image
        img2 = img1
        if self.parameters['ColorConversion'] == 'COLOR_BGR2GRAY':
            img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            logger.info(f'Conversion to Grayscale shape={img2.shape}')
        else:
            cc = self.parameters['ColorConversion']
            logger.warning(f'Unknown ColorConversion "{cc}"')
        idata = self.inputImages[0].makeCopy()
        idata.name = f'{idata.name}_bw'
        idata.setImage(img2)
        self.outputImages.append(idata)

class CannyEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name):
        super().__init__(name)
        self.parameters = {
            'Threshold1': 100, 
            'Threshold2': 50, 
            }
    def run(self):
        super().run()
        pass

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
            logger.info(f'Create analysis of type {clsName} {cls}')
            x = cls(name)
        return x
    
