#------------------------------------------------------------------------
# ipcat: model.py
#------------------------------------------------------------------------
import os
import logging
import numpy as np
import cv2
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)

class ImageData:
    def __init__(self, name, path, width, height, offset=[0.0, 0.0]):
        self.name = name
        self.path = path
        self.width = width
        self.height = height
        self.offset = offset
        self.imageOk = False
        self.image = None
        self.imageResized = None
        self.imageTk = None

    def createImageTk(self, img):
        self.imageTk = None
        if self.imageOk:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(img)
            self.imageTk = ImageTk.PhotoImage(img1)
        return self.imageTk
    
    def open(self):
        if not self.imageOk and os.path.exists(self.path):
            self.image = cv2.imread(self.path, cv2.IMREAD_COLOR)
            self.imageOk = True
            self.createImageTk(self.image)
        else:
            logger.warning(f'Tried to open non-existing file {self.path}')

    def resize(self, cr):
        if self.imageOk:
            self.imageResized = cv2.resize(self.image, cr)
            self.createImageTk(self.imageResized)
        return self.imageTk
    
    def clearImage(self):
        self.image = None
        self.imageOk = False
        
    def save(self, fpath):
        pass

class AppData:
    def __init__(self):
        self.openFileDir = '.'
        self.workDir = '.'
        self.analysisList = []
        self.imageList = []
        self.currentImage = None
        self.currentAnalysis = None
        #
        pass

    def allAnalysisNames(self):
        v = list(map(lambda x: x.name, self.analysisList))
        return v
            
    def allImageNames(self):
        v = list(map(lambda x: x.name, self.imageList))
        return v
            
    def addImageToList(self, img):
        self.imageList.append(img)

    def findImage(self, imageName):
        x = None
        for y in self.imageList:
            if y.name == imageName:
                x = y
                logger.info(f'Found match {imageName}, {x.path}')
                break
        return x
    
    def findAnalysis(self, analysisName):
        x = None
        for y in self.analysisList:
            if y.name == analysisName:
                x = y
        return x
    
    def selectImages(self, images):
        logger.info(f'Model.selectImages called n={len(images)}')
        if len(images) == 1:
            img = images[0]
            if self.currentImage:
                if self.currentImage != img:
                    self.currentImage.clearImage()
                    self.currentImage = img
            else:
                self.currentImage = img
            if self.currentImage:
                logger.info(f'Open image file {self.currentImage.path}')
                self.currentImage.open()
        else:
            logger.warning('Images analysis on multiple images is not implemented yet')

    def selectAnalysis(self, analysis):
        self.currentAnalysis = analysis

    def runAnalysis(self):
        self.currentAnalysis.run()
        pass
    
    def changeImageName(self, name1, name2):
        pass
    
    def deleteImage(self, name):
        pass
    
