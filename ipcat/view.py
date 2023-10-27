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
from .guiComponents import FieldEntry
#from .handlers import Handlers
from .analysis import AnalysisStore

logger = logging.getLogger(__name__)

class View:
    def __init__(self, model):
        self.model = model
        self.app = None
        # View model
        self.openFileDir = '.'
        # Copied from the old ViewModel
        self.selectedImages = []
        self.inputImagePath = ''
        self.inputImageOffset = [0.0, 0.0]
        self.inputImageWidth = 0.0
        self.inputImageHeight = 0.0
        #
        self.analysisList = []
        #
        self.currentImage = ''
        self.combinedFrame = None
        #
        self.currentAnalysis = ''
        self.analysisProperties = []
        self.analysisOutImages = []
        self.analysisOutputs = []
        #
        self.messages = []
        # Initialize the main window after all variables are defined
        self.mainWindow = MainWindow(self)

    def setApp(self, app):
        self.app = app
        
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
        v = []
        for k in store.analysisTypes:
            v.append(k)
        self.mainWindow.analysisPanel.selection.configure(values=v)

    def updateAnalysisPanel(self):
        analysis = self.model.currentAnalysis
        logger.info(f'Analysis {analysis.name} -> {analysis}')
        if analysis:
            pframe = self.mainWindow.analysisPanel.propertiesFrame
            pframe.clear()
            logger.info(f'  Analysis parameters {len(analysis.parameters)}')
            fields = []
            for pn, pv in analysis.parameters.items():
                fields.append(FieldEntry(pn, pv))
            pframe.setFields(fields)
        pass
    
    def updateImageList(self):
        if not self.mainWindow:
            logger.info('No GUI')
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
    
    def showImages(self):
        logger.info('Display images on the canvas')
        wframe = self.model.currentImageFrame
        wframe.drawOnCanvas(self.mainWindow.canvas)

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
        logger.info(f'Update gallery from analysis={analysis}')
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
        logger.info(f'Clear gallery')
        self.mainWindow.galleryPanel.clear()
        pass

    # Action handlers
    def onOpenImageList(self):
        ftypes = [('JSON file', '*.json')]
        indir = self.openFileDir
        fn = tk.filedialog.askopenfilename(filetypes=ftypes, initialdir=indir)
        self.openFileDir = os.path.dirname(fn)
        #
        self.app.readImagesFromJson(fn)
            
    def onShowImagesClicked(self, e):
        print('Show images button clicked')
        tree = self.mainWindow.imageList
        items = tree.selection()
        names = []
        for item in items:
            values = tree.item(item)['values']
            names.append(values[0])
        images = self.app.selectImages(names)
        self.showImages()

    def onAnalysisSelected(self):
        analysisName = e.widget.get()
        logger.info(f'Analysis selected ==> {analysisName}')
        self.app.selectAnalysis(analysisName)
        self.view.updateAnalysisPanel()
        pass

    def onRunClicked(self):
        logger.info('Run analysis')
        self.app.runAnalysis()
        pass

    def onFieldUpdated(self, field):
        pass
    
