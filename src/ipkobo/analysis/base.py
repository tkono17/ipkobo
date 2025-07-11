#------------------------------------------------------------------------
# ipcat: analysis/base.py
#------------------------------------------------------------------------
import logging
from tkinter import ttk
import io
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

logger = logging.getLogger(__name__)

class Parameter:
    @staticmethod
    def toBool(s):
        x = None
        s1 = s.lower()
        if s1 == "false":
            x = False
        elif s1 == "true":
            x = True
        return x
    
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
        if self.dtype == bool and type(value) == str:
            match value.lower():
                case 'true': value = True
                case 'false': value = False
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
    outputArea = os.path.join(os.environ['ProjectDir'], 'outputs')
    def __init__(self, name, **kwargs):
        self.name = name
        self.inputName = ''
        self.parameters = {}
        self.combinedImageFrame = None
        self.inputImages = []
        self.nInputImages = 0
        self.outputImages = []
        self.outputData = {}
        logging.getLogger('matplotlib.font_manager').setLevel(logging.INFO)
        logging.getLogger('matplotlib.pyplot').setLevel(logging.INFO)
        logging.getLogger('PIL.PngImagePlugin').setLevel(logging.INFO)
        self.setInputImages(self.readKwarg(kwargs, 'inputImages', []) )
        pass

    def readKwarg(self, kwargs, key, defaultValue):
        x = defaultValue
        if key in kwargs.keys():
            x = kwargs[key]
        logger.info(f'kwargs: {kwargs}')
        logger.info(f'Return {x} for the kwarg {key}')
        return x

    def setParameters(self, options):
        keys = self.parameters.keys()
        for k, v in options.items():
            if k in keys:
                self.setParameter(k, v)
        
    def setName(self, name):
        self.name = name
        
    def setParameter(self, key, value):
        if key in self.parameters:
            logger.info(f'  set parameter {key} for {self.__class__.__name__} to {value}')
            self.parameters[key].setValue(value)
        else:
            logger.warning(f'  {self.name} has no parameter {key}')

    def showSettings(self):
        logger.info(f'{self.__class__.__name__} {self.name}')
        logger.info(f'  parameters:')
        for k, p in self.parameters.items():
            logger.info(f'    {k}: {p.value}')
        
    def inputImage0(self):
        x = None
        if len(self.inputImages)>0:
            print(f'inputImages0: {self.inputImages}')
            x = self.inputImages[0]
        return x
    
    def setInputImage(self, image, name=''):
        self.setInputImages([image], name)

    def setInputImages(self, images, name=''):
        self.inputImages.clear()
        for x in images:
            self.inputImages.append(x)
        self.deduceInputName(name)

    def deduceInputName(self, name=''):
        if name == '':
            logger.info(f'Analysis {self.name} compose inputName (suggestion: {name})')
            if len(self.inputImages)==0:
                self.inputName = 'noImage'
            else:
                self.inputName = self.inputImage0().name
                n = self.inputName.rfind('.')
                if n > 0:
                    self.inputName = self.inputName[0:n]
        else:
            self.inputName = name
        logger.info(f'  InputName is set to {self.inputName}')

    def makeImageName(self, suffix='_'):
        x = f'{self.inputName}_{self.name}{suffix}'
        if self.name == '':
            x = f'{self.inputName}{suffix}'
        return x

    def makeImageData(self, name, fname='', img=None):
        x = self.inputImage0().makeCopy()
        x.name = name
        x.path = ''
        x.setImage(img)
        return x

    def makeImageDataFromFig(self, name, fname, fig):
        x = self.makeImageData(name, fname)
        tmpname = os.path.join('/tmp', os.path.basename(fname) )
        fig.savefig(tmpname)
        img = None
        try:
            img = cv2.imread(tmpname, cv2.IMREAD_COLOR)
        except:
            logger.warning(f'Cannot read image {tmpname}')
        if x is None:
            x.setInputImage(None)
        else:
            x.setInputImage(img)
        return x
    
    def imageTemplate(self, suffix, fig=None, image=None):
        name = self.makeImageName(suffix)
        fname = f'{name}.jpg'
        x = None
        if fig is None:
            x = self.makeImageData(name, fname, image)
        else:
            fname = f'{name}.png'
            x = self.makeImageDataFromFig(name, fname, fig)
        return x

    def addImage(self, image, suffix):
        name = self.makeImageName(suffix)
        figname = f'{name}.jpg'
        data = self.makeImageData(name, figname, image)
        self.outputImages.append(data)
        return data
    
    def addFig(self, fig, suffix):
        name = self.makeImageName(suffix)
        figname = f'{name}.png'
        data = self.makeImageDataFromFig(name, figname, fig)
        self.outputImages.append(data)
        return data

    def findImage(self, suffix):
        x = None
        if suffix.startswith('_'):
            candidates = filter(lambda img: img.name.endswith(suffix),
                                self.outputImages)
            if len(candidates)>0:
                x = candidates[0]
        return x
    
    def clearOutputs(self):
        self.outputImages = []
        self.outputData = {}

    def saveOutputs(self):
        workarea = ImageAnalysis.workArea
        for img in self.outputImages:
            if img.imageOk:
                if img.path == '':
                    img.path = os.path.join(ImageAnalysis.outputArea, f'{img.name}.jpg')
                logger.info(f'Writing image {img.name} to file {img.path}')
                cv2.imwrite(img.path, img.image)
    
    def run(self):
        logger.debug('ImageAnalysis.run()')
        pass
    
class SingleImageAnalysis(ImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.name = name
        self.parameters = {}
        inputImage = self.readKwarg(kwargs, 'inputImage', None)
        if inputImage != None:
            self.nInputImages = 1
            self.inputImages = [inputImage]
            
    def run(self):
        super().run()

