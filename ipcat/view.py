#------------------------------------------------------------------------
# ipcat: guiControl.py
# --------------------
# GUI logic (operations)
#------------------------------------------------------------------------
import os
import tkinter as tk
import logging
import cv2
from PIL import Image, ImageTk

from .model import ImageData, ImageFrame
from .gui   import MainWindow
from .handlers import Handlers
from .analysis import AnalysisStore

logger = logging.getLogger(__name__)

class View:
    def __init__(self, model):
        self.model = model
        self.handlers = Handlers()
        self.mainWindow = MainWindow(model, self.handlers)
        #
        self.currentImageFrame = None
        
    def mainloop(self):
        if self.mainWindow:
            self.mainWindow.mainloop()
        else:
            logger.error('Mainloop failed since mainWindow is null')
        
    # Actions on the GUI
    def addImageToList(self):
        pass
    
    def setInputImages(self):
        pass
    
    def updateParamters(self):
        pass
    
    def clearGallery(self):
        pass
    
    def addImageToGallery(self):
        pass
    
    def outputText(self):
        pass
    
    # Actions on the GUI
    def openImage(self, dname):
        ftypes = [('Image file', '*.jpg'), ('all', '*')]
        fn = tk.filedialog.askopenfilename(filetypes=ftypes,
                                                initialdir=dname)
        img = None
        if fn != '' and os.path.exists(fn):
            name = 'input%d' % len(self.appData.inputImageList)
            img = ImageData(name, fn)
        return img

    def updateAnalysisList(self):
        if not self.mainWindow:
            return
        store = AnalysisStore.get()
        logger.info(f'Store n analysis: {len(store.analysisTypes)}')
        for k in store.analysisTypes:
            #self.vmodel.addAnalysis(k)
            pass
        self.mainWindow.analysisPanel.selection.configure()#values=self.vmodel.analysisList)

    def updateAnalysisPanel(self, analysisName):
        #self.vmodel.currentAnalysis = analysisName
        store = AnalysisStore.get()
        analysis = store.create(analysisName, f'{analysisName}1')
        self.model.selectAnalysis(analysis)
        logger.info(f'Analysis {analysisName} -> {analysis}')
        if analysis:
            pframe = self.mainWindow.analysisPanel.propertiesFrame
            pframe.clear()
            logger.info(f'  Analysis parameters {len(analysis.parameters)}')
            for pn, pv in analysis.parameters.items():
                values = (pn, pv)
                #self.vmodel.analysisProperties.append(pv)
                pframe.addParameter(pv)
                pframe.build()
        pass
    
    def updateImageList(self):
        if not self.mainWindow:
            logger.info('No GUI is empty')
            return
        widgets = self.mainWindow.imageList.get_children()
        self.mainWindow.imageList.delete(*widgets)
        logger.info('Update imageList')
        logger.info(f'{self.mainWindow.imageList}')
        tree = self.mainWindow.imageList
        for img in self.model.imageList:
            values = (img.name, os.path.basename(img.path),
                      img.width, img.height, img.offset[0], img.offset[1])
            logger.info(f'  Add image {img.name} {values}')
            self.mainWindow.imageList.insert('', tk.END, values=values)
        pass
    
    def showImages(self, images):
        logger.info(f'View.showImages called Nimages={len(images)}')
        #
        wframe = ImageFrame(images)
        self.currentImageFrame = wframe
        wframe.drawOnCanvas(self.mainWindow.canvas)
        logger.info('Display images on the canvas')

    def clearImage(self):
        pass

    def addAnalysisProperty(self, prop):
        pass

    def updateAnalysisProperties(self):
        pass

    def clearAnalysisProperties(self):
        pass

    def showImageInGallery(self, image):
        pass

    def addImageToFrame(self, imageData, frame):
        pass
    
    def updateGallery(self):
        self.clearGallery()
        analysis = self.model.currentAnalysis
        width = 500
        cr = (width, width)
        if analysis:
            logger.info(f'Update gallery with {len(analysis.outputImages)} images')
            for imageData in analysis.outputImages:
                r = imageData.heightToWidthRatio()
                cr = (int(width), int(width*r) )
                imageTk = imageData.resize(cr)
                logger.info(f'{imageTk}')
                self.mainWindow.galleryPanel.addImageFrame(imageTk, imageData.name)
        pass

    def clearGallery(self):
        self.mainWindow.galleryPanel.clear()
        pass

