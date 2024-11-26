#------------------------------------------------------------------------
# ipcat: view.py
# --------------------
# View logic (operations)
#------------------------------------------------------------------------
import os
import tkinter as tk
from tkinter import filedialog
import logging

import cv2
from PIL import Image, ImageTk

from .gui    import MainWindow
from .guiComponents import FieldEntry
from .callbacks import *

from ..model    import ImageData, ImageFrame

logger = logging.getLogger(__name__)

class View:
    def __init__(self, model, app=None):
        self.model = model
        self.mainWindow = None
        self.app = app
        # View model
        self.openFileDir = '.'
        #
        self.selectedImages = []
        self.currentAnalysis = ''
        self.analysisProperties = []
        self.analysisOutImages = []
        self.analysisOutputs = []
        #
        self.messages = []
        # Initialize the main window after all variables are defined
        self.root = tk.Tk()
        self.root.title("Ipcat application")
        self.root.geometry("1000x700")
        self.mainWindow = MainWindow(self.root)
        self.initialize()

    def setApp(self, app):
        self.app = app

    def initialize(self):
        # Menu
        menu = self.mainWindow.menuBar
        menu.File.entryconfig('Open', command=self.onFileOpen)
        menu.Test.entryconfig('Test1', command=self.test1)

        # ListPanel
        tree = self.mainWindow.listPanel
        tree['columns'] = ('Name', 'File')
        tree.column('#0', width=0, stretch='no')
        tree.column('Name', anchor=tk.W, width=100)
        tree.column('File', anchor=tk.W, width=100)
        tree.heading('#0', text='Label', anchor=tk.W)
        tree.heading('Name', text='Name', anchor=tk.W)
        tree.heading('File', text='File', anchor=tk.W)
        tree.bind('<<TreeviewSelect>>', self.onTreeSelect)

        # ImagePanel
        self.mainWindow.imagePanel.config(text='Image under test')
        self.mainWindow.showButton.config(text='Show')
        self.mainWindow.showButton.bind('<Button-1>', self.onShowImagesClicked)

        # AnalysisPanel
        v = self.model.allAnalysisTypes()
        self.mainWindow.selection.configure(values=v)
        self.mainWindow.analysisPanel.config(text='Analysis panel')
        self.mainWindow.showButton.config(text='Show')
        self.mainWindow.selection.bind('<<ComboboxSelected>>', self.onAnalysisSelected)
        self.mainWindow.runButton.config(text='Run', command=self.onRunAnalysisClicked)

        # Gallery
        
        pass
    
    def mainloop(self):
        if self.mainWindow:
            self.mainWindow.mainloop()
        else:
            logger.error('Mainloop failed since mainWindow is null')
        
    # Actions on the GUI
    def onFileOpen(self):
        ftypes = [('JSON file', '*.json')]
        indir = self.openFileDir
        fn = filedialog.askopenfilename(filetypes=ftypes,
                                           initialdir=indir)
        self.openFileDir = os.path.dirname(fn)
        self.app.readImagesFromJson(fn)
        self.model.printSummary()

    def onTreeSelect(self, event):
        logger.debug('onTreeSelect')
        tree = self.mainWindow.listPanel
        ids = tree.selection()
        logger.info(f'{len(ids)} images selected')
        names = []
        for values in [tree.item(x)['values'] for x in ids]:
            names.append(values[0])
        self.selectedImages = names
        
    def onShowImagesClicked(self, e):
        print('Show images button clicked')
        if len(self.selectedImages)>0:
            self.model.setImagesToAnalyze(self.selectedImages)
            self.showImages()
        else:
            logger.warning('No images were selected')

    def onAnalysisSelected(self, e):
        print(f'Analysis selected {e.widget.get()}')
        analysisName = e.widget.get()
        logger.info(f'Analysis selected ==> {analysisName}')
        self.app.selectAnalysis(analysisName)

    def onRunAnalysisClicked(self):
        self.app.runAnalysis()

    # Needs to be tested
    def test1(self):
        self.app.readImagesFromJson('./images.json')
        self.app.selectAnalysis('ColorAnalysis')
        self.app.selectImages(['A'])
        self.model.printSummary()
        
    # Functions to update the GUI appearance (called by the application logic)
    def updateImageList(self):
        if not self.mainWindow:
            logger.error('No GUI')
            return
        tree = self.mainWindow.listPanel
        widgets = tree.get_children()
        tree.delete(*widgets)
        logger.info(f'Update imageList on {tree}')
        for img in self.model.imageList:
            values = (img.name, os.path.basename(img.path),
                      img.width, img.height, img.offset[0], img.offset[1])
            logger.info(f'  Add image {img.name} {values}')
            tree.insert('', tk.END, values=values)
        self.model.printSummary()
        pass
    
    def showImages(self):
        logger.info('Display images on the canvas')
        wframe = self.model.currentImageFrame
        wframe.drawOnCanvas(self.mainWindow.imageCanvas)

    def updateAnalysisPanel(self):
        analysis = self.model.currentAnalysis
        logger.info(f'Analysis {analysis.name} -> {analysis}')
        if analysis:
            pframe = self.mainWindow.propertiesFrame
            pframe.clear()
            logger.info(f'  Analysis parameters {len(analysis.parameters)}')
            fields = []
            for pn, pv in analysis.parameters.items():
                drange, choices = None, None
                if pv.drange != None:
                    drange = pv.drange
                elif pv.choices != None:
                    choices = pv.choices
                fields.append(FieldEntry(pv) )
            pframe.setFields(fields)
        pass
    
    # Obsolete functions
    def updateParamters(self):
        pass
    
    def addImageToGallery(self, img):
        pass
    
    def outputText(self, msg):
        pass
    
    def openImage(self, dname):
        ftypes = [('Image file', '*.jpg'), ('all', '*')]
        fn = filedialog.askopenfilename(filetypes=ftypes,
                                           initialdir=dname)
        img = None
        if fn != '' and os.path.exists(fn):
            name = 'input%d' % len(self.model.imageList)
            img = ImageData(name, fn)
        if img:
            self.model.addImage(img)

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
                self.mainWindow.gallery.addImageFrame(imageTk, imageData.name)
        pass

    def clearGallery(self):
        logger.info(f'Clear gallery')
        self.mainWindow.gallery.clear()
        pass

    # Action handlers
    def onOpenImageList(self):
        ftypes = [('JSON file', '*.json')]
        indir = self.openFileDir
        fn = filedialog.askopenfilename(filetypes=ftypes, initialdir=indir)
        self.openFileDir = os.path.dirname(fn)
        #
        self.app.readImagesFromJson(fn)
            
    def onFieldUpdated(self, field):
        pass
    
