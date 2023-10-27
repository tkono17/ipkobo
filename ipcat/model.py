#------------------------------------------------------------------------
# ipcat: model.py
#------------------------------------------------------------------------
import os
import logging

from PIL import Image, ImageTk

import numpy as np
import cv2

from .analysis import AnalysisStore

logger = logging.getLogger(__name__)

class ImageData:
    def __init__(self, name, path, width, height, offset=[0.0, 0.0]):
        self.name = name
        self.path = path
        self.width = width
        self.height = height
        self.offset = np.array(offset)
        self.imageOk = False
        self.image = None
        self.imageResized = None
        self.imageTk = None

    def makeCopy(self):
        x = ImageData(name=self.name, path='',
                      width=self.width, height=self.height, offset=self.offset)
        return x

    def widthToHeightRatio(self):
        r = self.width/self.height
        return r
    
    def heightToWidthRatio(self):
        r = self.height/self.width
        return r
    
    def createImageTk(self, img=None):
        if type(img)==type(None):
            img = self.image
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

    def setImage(self, image):
        self.image = image
        self.imageOk = True
        
    def resize(self, cr):
        if self.imageOk:
            logger.info(f'Try to resize {cr} <-- {self.image.shape}')
            self.imageResized = cv2.resize(self.image, cr)
            self.createImageTk(self.imageResized)
        else:
            logging.warning(f'Cannot resize as the base image is empty')
        return self.imageTk
    
    def clearImage(self):
        self.image = None
        self.imageOk = False
        
    def save(self, fpath):
        pass

class ImageFrame:
    def __init__(self, images, width=0.0, height=0.0, offset=[0.0, 0.0]):
        self.images = images
        self.width = width
        self.height = height
        self.offset = np.array(offset)
        self.rows = 5000
        self.columns = 5000
        self.combinedImage = None
        self.setImages(images)
        
    def positionBL(self):
        x = self.offset[0] - self.width/2.0
        y = self.offset[1] - self.height/2.0
        return np.array( (x, y) )
    
    def positionTR(self):
        x = self.offset[0] + self.width/2.0
        y = self.offset[1] + self.height/2.0
        return np.array( (x, y) )
    
    def setImages(self, images):
        if len(images)==1 and images[0].imageOk:
            img0 = images[0]
            image0 = img0.image.copy()
            self.combinedImage = ImageData(name='combinedImage', path='',
                                           width=img0.width,
                                           height=img0.height, 
                                           offset=img0.offset)
            self.combinedImage.setImage(image0)
            return
        xmin = min(map(lambda x: x.offset[0]-x.width/2.0, images) )
        xmax = max(map(lambda x: x.offset[0]+x.width/2.0, images) )
        ymin = min(map(lambda x: x.offset[1]-x.height/2.0, images) )
        ymax = max(map(lambda x: x.offset[1]+x.height/2.0, images) )
        self.width = xmax - xmin
        self.height = ymax - ymin
        self.offset = np.array([ (xmin+xmax)/2.0, (ymin+ymax)/2.0 ])
        self.combinedImage = ImageData(name='combinedImage', path='',
                                width=self.width, height=self.height, 
                                offset=self.offset)
        if len(images)==1 and images[0].imageOk:
            img = images[0].image
            self.rows = img.shape[0]
            self.columns = img.shape[1]
        else:
            if self.width > self.height:
                self.rows = self.columns * int(self.width/self.height)
            elif self.width > self.height:
                self.columns = self.rows * int(self.height/self.width)
        image0 = np.ones( (self.rows, self.columns, 3), np.uint8)*255
        self.combinedImage.setImage(image0)
        logger.info(f'End of setImages, combine Images: {self.combinedImage}')
        self.combineImages()
        pass

    def xyToCR(self, xy):
        xmin, xmax = -self.width/2.0, self.width/2.0
        ymin, ymax = -self.height/2.0, self.height/2.0
        dx = (xmax - xmin)/self.columns
        dy = (ymax - ymin)/self.rows
        x, y = xy
        c = int( (x-xmin)/dx)
        r = int(self.rows - (y-ymin)/dy)
        return (c, r)
        
    def combineImages(self):
        logger.info(f'Start, combine Images: {self.combinedImage}')
        for idata in self.images:
            scales = idata.width/self.width, idata.height/self.height
            ncols = int(scales[0]*self.columns)
            nrows = int(scales[1]*self.rows)
            w = idata.width
            h = idata.height
            idata.resize( (ncols, nrows) )
            offset1 = idata.offset - self.offset
            xmin = offset1[0] - w/2.0
            xmax = offset1[0] + w/2.0
            ymin = offset1[1] - h/2.0
            ymax = offset1[1] + h/2.0
            #logger.info(f'({xmin},{ymin}) - ({xmax},{ymax})')
            c1, r1 = self.xyToCR( (xmin, ymax) )
            #c2, r2 = self.xyToCR( (xmax, ymin) )
            r2 = r1 + idata.imageResized.shape[0]
            c2 = c1 + idata.imageResized.shape[1]
            logger.info(f'  Insert at [{c1}:{c2}, {r1}:{r2}] w/h={w},{h}')
            self.combinedImage.image[r1:r2,c1:c2,:] = idata.imageResized
        #
        logger.info(f'Combined image: w,h={self.width},{self.height}, offset={self.offset}')
        return self.combinedImage

    def drawOnCanvas(self, canvas):
        cw, ch = canvas.winfo_width(), canvas.winfo_height()
        w = self.columns
        h = self.rows
        scale = min(cw/w, ch/h)
        imgTk = self.combinedImage.resize( (int(scale*w), int(scale*h)) )
        cr = (int(scale*w/2), int(scale*h/2))
        cr = (int(cw/2), int(ch/2))
        logger.info(f'drawOnCanvas {canvas} cr={cr}, img={imgTk}')
        logger.info(f'{type(imgTk)}')
        canvas.create_image(cr[0], cr[1], image=imgTk)
        pass
    
class AppModel:
    def __init__(self):
        self.workDir = '.'
        self.analysisList = []
        self.imageList = []
        self.currentImageFrame = None
        self.currentImages = []
        self.combinedImage = None
        self.currentAnalysis = None
        #
        pass

    def addImage(self, img):
        self.imageList.append(img)

    def addImagesFromJson(self, jsonFile):
        pass
    
    def selectImages(self, imageNames):
        logger.info(f'Model.selectImages called n={len(imageNames)}')
        for image in self.currentImages:
            image.clearImage()
        self.currentImages.clear()
        #
        for iname in imageNames:
            img = self.findImage(iname)
            self.currentImages.append(img)
        for image in self.currentImages:
            logger.info(f'Open image file {image.path}')
            image.open()
        logger.info(f'{len(imageNames)} images selected. Creating the combined frame')
        #
        wframe = ImageFrame(self.currentImages)
        self.currentImageFrame = wframe
        return self.currentImages

    def selectAnalysis(self, analysisName):
        store = AnalysisStore.get()
        analysis = store.create(analysisName, f'{analysisName}1')
        self.currentAnalysis = analysis
        return self.currentAnalysis

    def getAnalysis(self):
        return self.currentAnalysis
    
    def allAnalysisNames(self):
        v = list(map(lambda x: x.name, self.analysisList))
        return v
            
    def allImageNames(self):
        v = list(map(lambda x: x.name, self.imageList))
        return v
            
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
    
    def runAnalysis(self):
        self.currentAnalysis.run()
        pass
    
    def changeImageName(self, name1, name2):
        pass
    
    def deleteImage(self, name):
        pass
    
