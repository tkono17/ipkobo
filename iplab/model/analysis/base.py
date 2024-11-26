#------------------------------------------------------------------------
# ipcat: analysis/base.py
#------------------------------------------------------------------------
import logging
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import io

import cv2

logger = logging.getLogger(__name__)

class Parameter:
    def __init__(self, name, value, dtype, **kwargs):
        self.name = name
        self.dtype = dtype
        self.value = value
        self.drange = None
        self.choices = None
        keys = kwargs.keys()
        if 'drange' in keys:
            self.drange = kwargs['drange']
        if 'choices' in keys:
            self.choices = kwargs['choices']

    def setValue(self, value):
        self.value = value

    def itemSelected(self, e):
        value = e.widget.get()
        print(f'Set value from item selected {value}')
        self.value = self.dtype(value)

    def scaleSet(self, value):
        fvalue = float(value)
        self.value = self.dtype(fvalue)
        pass
    
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

