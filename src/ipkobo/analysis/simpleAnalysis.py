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
        idata_bw = self.makeImageData(name, f'{name}.jpg', img2)
        self.outputImages.append(idata_bw)
        self.saveOutputs()

class IntensityAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'normalize': Parameter('normalize', value=False,
                                   dtype=Parameter.toBool,
                                   choices=(False, True) ),
            'invert': Parameter('invert', value=False,
                                dtype=Parameter.toBool,
                                choices=(False, True) ),
        }
    def createIntensityPlot(self, img1, nrows, ncols, ncolors):
        logger.info('  Prepare plt')
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        #
        img_bw = img1
        logger.info(f'  ncolors = {ncolors}')
        n = nrows * ncols
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
        figname = f'{self.inputName}_hist'
        fname = f'{figname}.png'
        idata_hist = self.makeImageDataFromFig(figname, fname, fig)
        return idata_hist

    def checkShape(self, img1):
        print(f'shape: {img1.shape}')
        nrows, ncols, ncolors = 1, 1, 1
        if len(img1.shape) == 2:
            nrows, ncols = img1.shape
        elif len(img1.shape) == 3:
            nrows, ncols, ncolors = img1.shape
        else:
            logger.warning(f'Unexpected shape of the image {img1.shape}. Should be (nr, nc) or (nr, nc, 3)')
            return False
        return (nrows, ncols, ncolors)

    def createNormalized(self, img):
        nrows, ncols = img.shape
        nrows2, ncols2 = int(nrows/2), int(ncols/2)
        img2 = img.copy()
        img2.resize(nrows2, ncols2)
        y1, y2 = np.min(img2), np.max(img2)
        s = 1
        if y2 > y1:
            s = 255.0/(y2 - y1)
            img3 = ( (img - y1) * s).astype(np.uint8)
        else:
            img3 = img
        logger.debug(f'  y1, y2, scale = {y1}, {y2}, {s}, {img3.shape}')
        name = self.makeImageName('_norm')
        return self.makeImageData(name, f'{name}.jpg', img3)
    
    def run(self):
        logger.info('IntensityAnalysis')
        self.clearOutputs()
        img1 = self.inputImage0().image
        #
        nrows, ncols, ncolors = self.checkShape(img1)
        img = self.createIntensityPlot(img1, nrows, ncols, ncolors)
        self.outputImages.append(img)
        if self.parameters['normalize'].value or True:
            img = self.createNormalized(img1)
            self.outputImages.append(img)
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
            }
    def run(self):
        self.clearOutputs()
        img1 = self.inputImage0().image
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
        
