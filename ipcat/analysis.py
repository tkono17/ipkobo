#------------------------------------------------------------------------
# ipcat: analysis.py
#------------------------------------------------------------------------
import logging
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import io

import cv2

#from .model import *

logger = logging.getLogger(__name__)

class Parameter:
    def __init__(self, name, dtype, **kwargs):
        self.name = name
        self.dtype = dtype
        self.value = self.dtype()
        self.drange = None
        self.choices = None
        keys = kwargs.keys()
        if 'drange' in keys:
            self.drange = kwargs['drange']
        if 'choices' in keys:
            self.choices = kwargs['choices']

    def setValue(self, value):
        self.value = value

    def isValid(self, value):
        x = True
        if self.drange:
            if x > self.drange[0] and x < self.drange[1]:
                x = True
            else:
                x = False
        elif self.choices:
            if x in self.choices:
                x = True
            else:
                x = False
        return x
        
def figToArray(fig, dpi=180):
    logger.info('figToArray')
    buf = io.BytesIO()
    logger.info('Hello')
    fig.savefig(buf, format='png', dpi=dpi)
    logger.info('seek 0')
    buf.seek(0)
    logger.info('frombuffer')
    imgArray = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    logger.info('close buffer')
    buf.close()
    logger.info('imdecode')
    img = cv2.imdecode(imgArray, 1)
    logger.info('return img')
    return img

class ImageAnalysis:
    def __init__(self, name):
        self.name = name
        self.parameters = {}
        self.combinedImageFrame = None
        self.nInputImages = 0
        self.inputImages = []
        self.outputImages = []
        self.outputValues = {}
        logging.getLogger('matplotlib.font_manager').setLevel(logging.INFO)
        logging.getLogger('matplotlib.pyplot').setLevel(logging.INFO)
        logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)
        pass

    def addParameters(self, pars):
        self.parameters.extend(pars)

    def addParameter(self, par):
        self.parameters.append(pars)

    def setParameter(self, key, value):
        self.parameters[key].setValue(value)

    def setInputImages(self, imageFrame, images):
        self.combinedImageFrame = imageFrame
        self.inputImages.clear()
        for x in images:
            self.inputImages.append(x)
        
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

    def makeImageData(self, name):
        x = self.inputImages[0].makeCopy()
        x.name = name
        return x
    
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
        logger.info(f'{self.name} running, pars={self.parameters}')
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

class IntensityAnalysis(SingleImageAnalysis):
    def __init__(self, name):
        super().__init__(name)
        self.parameters = {
            }
    def run(self):
        img1 = self.inputImages[0].image
        #
        img_bw = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        idata_bw = self.makeImageData(f'{self.name}_bw')
        idata_bw.setImage(img_bw)
        self.outputImages.append(idata_bw)
        #
        n = img_bw.shape[0]*img_bw.shape[1]
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.hist(img_bw.reshape( (n) ), bins=255, range=(0, 255), color='k', histtype='step', fill=False)
        ax.hist(img1[:,:,0].reshape( (n) ), bins=255, range=(0, 255), histtype='step', color='b', fill=False)
        ax.hist(img1[:,:,1].reshape( (n) ), bins=255, range=(0, 255), histtype='step', color='g', fill=False)
        ax.hist(img1[:,:,2].reshape( (n) ), bins=255, range=(0, 255), histtype='step', color='r', fill=False)
        img_hist = figToArray(fig)
        idata_hist = self.makeImageData(f'{self.name}_hist')
        idata_hist.setImage(img_hist)
        self.outputImages.append(idata_hist)

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
        self.addAnalysis('IntensityAnalysis', IntensityAnalysis)
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
    
