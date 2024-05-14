#------------------------------------------------------------------------
# ipcat: view.py
# --------------------
# View logic (operations)
#------------------------------------------------------------------------
import os
import tkinter as tk
import logging
import cv2
from PIL import Image, ImageTk

from .model import ImageData, ImageFrame
from .gui   import MainWindow
from .guiComponents   import FieldEntry
from .analysis import AnalysisStore
import .callbacks as cb

logger = logging.getLogger(__name__)

class View:
    def __init__(self, model, app=None):
        self.model = model
        self.app = app
        # View model
        self.openFileDir = '.'
        #
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
        self.mainWindow.menuBar.File.entryconfig('Open', command=self.openInputs)
        self.mainWindow.menuBar.Test.entryconfig('Test1', command=self.test1)

        # ListPanel
        tree = self.mainWindow.listPanel
        tree['columns'] = ('Name', 'File')
        tree.column('#0', width=0, stretch='no')
        tree.column('Name', anchor=tk.W, width=100)
        tree.column('File', anchor=tk.W, width=100)
        tree.heading('#0', text='Label', anchor=tk.W)
        tree.heading('Name', text='Name', anchor=tk.W)
        tree.heading('File', text='File', anchor=tk.W)

        # ImagePanel
        self.mainWindow.imagePanel.config(text='Image under test')
        self.mainWindow.showButton.config(text='Show')
        self.mainWindow.showButton.bind('<Button-1>', self.onShowImagesClicked)

        # AnalysisPanel
        self.mainWindow.analysisPanel.config(text='Analysis panel')
        self.mainWindow.showButton.config(text='Show')
        self.updateAnalysisList()
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
    def openInputs(self):
        ftypes = [('JSON file', '*.json')]
        indir = self.openFileDir
        fn = tk.filedialog.askopenfilename(filetypes=ftypes,
                                           initialdir=indir)
        self.openFileDir = os.path.dirname(fn)
        self.app.readImagesFromJson(fn)
        self.model.printSummary()

    def onShowImagesClicked(self, e):
        print('Show images button clicked')
        tree = self.mainWindow.listPanel
        items = tree.selection()
        names = []
        for item in items:
            values = tree.item(item)['values']
            names.append(values[0])
        images = self.app.selectImages(names)
        self.showImages()

    def onAnalysisSelected(self, e):
        print(f'Analysis selected {e.widget.get()}')
        analysisName = e.widget.get()
        logger.info(f'Analysis selected ==> {analysisName}')
        self.app.selectAnalysis(analysisName)
        self.updateAnalysisPanel()

    def onRunAnalysisClicked(self):
        self.app.runAnalysis()

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

    def updateAnalysisList(self):
        if not self.mainWindow:
            return
        store = AnalysisStore.get()
        logger.info(f'Store n analysis: {len(store.analysisTypes)}')
        v = []
        for k in store.analysisTypes:
            v.append(k)
        self.mainWindow.selection.configure(values=v)

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
        fn = tk.filedialog.askopenfilename(filetypes=ftypes,
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
        fn = tk.filedialog.askopenfilename(filetypes=ftypes, initialdir=indir)
        self.openFileDir = os.path.dirname(fn)
        #
        self.app.readImagesFromJson(fn)
            
    def onFieldUpdated(self, field):
        pass
    
