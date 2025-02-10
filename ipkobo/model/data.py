#------------------------------------------------------------------------
# ipcat: model.py
#------------------------------------------------------------------------
import json
import logging
import os

from urllib.request import urlopen
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
            img1 = Image.fromarray(imgRGB)
            self.imageTk = ImageTk.PhotoImage(img1)
        return self.imageTk
    
    def open(self):
        if not self.imageOk:
            if os.path.exists(self.path):
                self.image = cv2.imread(self.path, cv2.IMREAD_COLOR)
                self.imageOk = True
                self.createImageTk(self.image)
            elif self.path.startswith('http://') or self.path.startswith('https://'):
                response = urlopen(self.path)
                print(f'URL request status: {response.status}')
                if response.status == 200:
                    data = bytearray(response.read())
                    darray = np.asarray(data, np.uint8)
                    self.image = cv2.imdecode(darray, cv2.IMREAD_UNCHANGED)
                    self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
                    self.imageOk = True
                    self.createImageTk(self.image)
            else:
                logger.warning(f'Tried to open non-existing file {self.path}')
        pass

    def setImage(self, image):
        self.image = image
        if image is None:
            self.imageOk = False
        else:
            self.imageOk = True
        
    def resize(self, cr):
        if self.imageOk:
            logger.info(f'Try to resize {cr} <-- {self.image.shape}')
            self.imageResized = cv2.resize(self.image, cr)
            self.createImageTk(self.imageResized)
        else:
            logger.warning(f'Cannot resize as the base image is empty')
        return self.imageTk
    
    def clearImage(self):
        self.image = None
        self.imageOk = False
        
    def save(self, fpath):
        pass

    def dump(self):
        logger.info(f'ImageData name:{self.name}')
        logger.info(f'  image: {self.imageOk}')
        if self.imageOk:
            logger.info(f'  image shape: {self.image.shape}')

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
        print(f'Set {len(images)} images on the frame')
        for image in images:
            image.open()
        if len(images)==1 and images[0].imageOk:
            img0 = images[0]
            image0 = img0.image.copy()
            #self.combinedImage = ImageData(name='combinedImage', path='',
            #                               width=img0.width,
            #                               height=img0.height, 
            #                               offset=img0.offset)
            self.combinedImage = images[0]
            self.combinedImage.setImage(image0)
            print('just one image')
            return
        print('combine multiple images')
        xmin = min(map(lambda x: x.offset[0]-x.width/2.0, images) )
        xmax = max(map(lambda x: x.offset[0]+x.width/2.0, images) )
        ymin = min(map(lambda x: x.offset[1]-x.height/2.0, images) )
        ymax = max(map(lambda x: x.offset[1]+x.height/2.0, images) )
        self.width = xmax - xmin
        self.height = ymax - ymin
        self.offset = np.array([ (xmin+xmax)/2.0, (ymin+ymax)/2.0 ])
        self.combinedImage = self.images[0]
        return
        #
        self.combinedImage = ImageData(name='combinedImage', path='',
                                width=self.width, height=self.height, 
                                offset=self.offset)
        shape = (1, 1, 1)
        if len(images)==1 and images[0].imageOk:
            img = images[0].image
            self.rows = img.shape[0]
            self.columns = img.shape[1]
            shape = img.shape
        else:
            if self.width > self.height:
                self.rows = self.columns * int(self.width/self.height)
            elif self.width > self.height:
                self.columns = self.rows * int(self.height/self.width)
        image0 = np.ones(shape, np.uint8)*255
        #self.combinedImage.setImage(image0)
        #logger.info(f'End of setImages, combine Images: {self.combinedImage}')
        #self.combineImages()
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
        isShape2 = False
        if len(self.combinedImage.shape)==2:
            isShape2 = True
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
            if isShape2:
                self.combinedImage.image[r1:r2,c1:c2] = idata.imageResized
            else:
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
        self.currentImages = []
        self.currentImageFrame = None
        self.combinedImage = None
        self.currentAnalysis = None
        #
        pass

    def initialize(self):
        pass

    def allAnalysisTypes(self):
        store = AnalysisStore.get()
        logger.info(f'Store n analysis: {len(store.analysisTypes)}')
        v = []
        for k in store.analysisTypes:
            v.append(k)
        return v
    
    def printSummary(self):
        logger.info(f'Ipcat application data')
        logger.info(f'  Number of analyses: {len(self.analysisList)}')
        logger.info(f'  Number of images: {len(self.imageList)}')
        logger.info(f'  Current analysis: {self.currentAnalysis}')
        logger.info(f'  Current images: {self.currentImageNames()}')

    def currentImageNames(self):
        v = [ x.name for x in self.currentImages ]
        return v
    
    def addImage(self, img):
        for i, x in enumerate(self.imageList):
            if x.name == img.name:
                logger.warning(f'Image with the name {img.name} exists, overwrite it')
                del self.imageList[i:i+1]
        self.imageList.append(img)

    def addImagesFromJson(self, jsonFile):
        if os.path.exists(jsonFile):
            with open(jsonFile) as fin:
                data = json.load(fin)
                if 'images' in data.keys():
                    for data1 in data['images']:
                        img = ImageData(data1['name'], data1['path'],
                                        data1['width'], data1['height'])
                        self.addImage(img)
                else:
                    logger.warning(f'No images in the JSON file {jsonFile}')
        else:
            logger.warning(f'JSON file {jsonFile} does not exist')
        pass

    def clearCurrentImages(self):
        for image in self.currentImages:
            image.clearImage()
        self.currentImages.clear()

    def setImageToAnalyze(self, imageName):
        logger.info(f'Model.setImageToAnalyze called for {imageName}')
        self.clearCurrentImages()
        #
        img = self.findImage(imageName)
        img.open()
        self.currentImages.append(img)
        logger.info(f'Creating the combined frame for 1 image')
        #
        wframe = ImageFrame(self.currentImages)
        self.currentImageFrame = wframe

    def setImagesToAnalyze(self, imageNames):
        logger.info(f'Model.setImagesToAnalyze called n={len(imageNames)}')
        self.clearCurrentImages()
        #
        for iname in imageNames:
            img = self.findImage(iname)
            self.currentImages.append(img)
        for image in self.currentImages:
            logger.info(f'Open image file {image.path}')
            image.open()
        logger.info(f'{len(imageNames)} images selected. Creating the combined frame')
        self.currentImageFrame = ImageFrame(self.currentImages)

    def selectAnalysis(self, analysisName):
        store = AnalysisStore.get()
        analysis = store.create(analysisName, '', #f'{analysisName[0]}', 
                                inputImages=self.currentImages)
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
        logger.info(f'  {self.currentAnalysis.name}')
        self.currentAnalysis.setInputImages(self.currentImages)
        self.currentAnalysis.run()
        pass
    
    def changeImageName(self, name1, name2):
        pass
    
    def deleteImage(self, name):
        pass
    
