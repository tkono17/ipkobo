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

        name = self.makeImageName('_bw')
        idata_bw = self.makeImageData(name, f'{name}.jpg')
        idata_bw.setImage(img2)
        self.outputImages.append(idata_bw)

class IntensityAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'normalize': Parameter('normalize', value=False,
                                   dtype=bool,
                                   choices=(False, True) ),
            'invert': Parameter('invert', value=False,
                                dtype=bool,
                                choices=(False, True) ),
        }
    def run(self):
        logger.info('IntensityAnalysis')
        self.clearOutputs()
        img1 = self.inputImage0().image
        print(f'shape: {img1.shape}')
        nrows, ncols, ncolors = 1, 1, 1
        if len(img1.shape) == 2:
            nrows, ncols = img1.shape
        elif len(img1.shape) == 3:
            nrows, ncols, ncolors = img1.shape
        else:
            logger.warning(f'Unexpected shape of the image {img1.shape}. Should be (nr, nc) or (nr, nc, 3)')
            return
        n = nrows*ncols
        #
        logger.info('  Prepare plt')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        #
        img_bw = img1
        logger.info(f'  ncolors = {ncolors}')
        if ncolors == 3:
            img_bw = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            name = self.makeImageName('_bw')
            idata_bw = self.makeImageData(name, f'{name}.jpg')
            idata_bw.setImage(img_bw)
            self.outputImages.append(idata_bw)
            
            ax.hist(img1[:,:,0].reshape( (n) ), bins=255, range=(0, 255), histtype='step', color='blue', fill=False)
            ax.hist(img1[:,:,1].reshape( (n) ), bins=255, range=(0, 255), histtype='step', color='green', fill=False)
            ax.hist(img1[:,:,2].reshape( (n) ), bins=255, range=(0, 255), histtype='step', color='red', fill=False)
        #
        logger.info(f'  make bw hist')
        ax.hist(img_bw[:,:].reshape( (n) ), bins=255, range=(0, 255), histtype='step', fill=False)

        logger.info('  Save figures')
        figname = f'{self.name}_hist'
        fname = f'{figname}.png'
        idata_hist = self.makeImageDataFromFig(figname, fname, fig)
        idata_hist.dump()
        self.outputImages.append(idata_hist)
        self.saveOutputs()

class ThresholdAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'threshold': Parameter('threshold', 128, dtype=int,
                                   drange=(0, 255) ), 
            'option': Parameter('option', 'THRESH_BINARY', dtype=str, 
                                choices=('THRESH_BINARY', 'THRESH_BINARY_INV',
                                         'THRESH_TRUNC',
                                         'THRESH_TOZERO', 'THRESH_TOZERO_INV') ),
            'maxVal': Parameter('maxVal', 255, dtype=int, drange=(0, 255)), 
            }
    def run(self):
        self.clearOutputs()
        img0 = self.inputImage0().image
        m = {
            'THRESH_BINARY': cv2.THRESH_BINARY,
            'THRESH_BINARY_INV': cv2.THRESH_BINARY_INV,
            'THRESH_TRUNC': cv2.THRESH_TRUNC,
            'THRESH_TOZERO': cv2.THRESH_TOZERO,
            'THRESH_TOZERO_INV': cv2.THRESH_TOZERO_INV
            }
        option = m[self.parameters['option'].value]
        img1 = cv2.threshold(img0,
                             self.parameters['threshold'].value,
                             self.parameters['maxVal'].value,
                             option)
        thr = self.parameters['threshold'].value
        self.outputImages.append(self.imageTemplate(f'_thr{thr}', image=img1) )
        self.saveOutputs()
        
class ContourAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
        self.saveOutputs()
        
class BoundaryAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
        self.saveOutputs()
        
class CannyEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'Threshold1': 100, 
            'Threshold2': 50, 
            }
    def run(self):
        self.clearOutputs()
        self.saveOutputs()
        pass

class GfbaEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'wsum': 30, 
            'tgap': 100,
            'direction': 'XY', 
            }
    def run(self):
        self.clearOutputs()
        self.saveOutputs()

