#------------------------------------------------------------------------
# ipcat: analysis/simpleAnalysis.py
#------------------------------------------------------------------------
import logging
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import io

import cv2

from .base import Parameter, SingleImageAnalysis

logger = logging.getLogger(__name__)

class ColorAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'ColorConversion': Parameter('ColorConversion', 'COLOR_BGR2GRAY',
                                         dtype=str, 
                                         choices=('COLOR_BGR2GRAY') )
            }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
        img2 = img1
        logger.info(f'{self.name} running, pars={self.parameters}')
        pvalue = self.parameters['ColorConversion'].value
        if pvalue == 'COLOR_BGR2GRAY':
            img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            logger.info(f'Conversion to Grayscale shape={img2.shape}')
        else:
            logger.warning(f'Unknown ColorConversion "{pvalue}"')
        idata = self.inputImage0().makeCopy()
        idata.name = f'{idata.name}_bw'
        idata.setImage(img2)
        self.outputImages.append(idata)

class IntensityAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, kwargs)
        self.parameters = {
            'normalize': Parameter('normalize', value=False,
                                   dtype=bool,
                                   choices=(False, True) ),
            'invert': Parameter('invert', value=False,
                                dtype=bool,
                                choices=(False, True) ),
        }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
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

class ThresholdAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, kwargs)
        self.parameters = {
            'threshold': Parameter('threshold', 128, dtype=int,
                                   drange=(0, 255) ), 
            'option': Parameter('option', 'THRESH_BINARY', dtype=str, 
                                choices=('THRESH_BINARY', 'THRESH_BINARY_INV',
                                         'THRESH_TRUNC',
                                         'THRESH_TOZERO', 'THRESH_TOZERO_INV') ), 
            }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
        
class ContourAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, kwargs)
        self.parameters = {
            }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
        
class BoundaryAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, kwargs)
        self.parameters = {
            }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
        
class CannyEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, kwargs)
        self.parameters = {
            'Threshold1': 100, 
            'Threshold2': 50, 
            }
    def run(self):
        self.clearOutputs()
        pass

class GfbaEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, kwargs)
        self.parameters = {
            'wsum': 30, 
            'tgap': 100,
            'direction': 'XY', 
            }
    def run(self):
        self.clearOutputs()

