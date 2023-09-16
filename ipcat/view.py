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
from .analysis import AnalysisStore

logger = logging.getLogger(__name__)

class View:
    def __init__(self, model):
        self.model = model
        self.handlers = Handlers()
        self.mainWindow = MainWindow(model, handlers)
        #
        self.buildGui(self.mainWindow)

    def mainloop(self):
        if self.mainWindow:
            self.mainWindow.mainloop()
        else:
            logger.error('Mainloop failed since mainWindow is null')
        
    # GUI building
    def buildGui(self):
        self.buildMenu(self.mainWindow)
        #
        columns = ttk.Panedwindow(self.mainWindow, orient=tk.HORIZONTAL)
        columns.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        listPanel = ttk.Frame(columns)
        workPanel = ttk.Panedwindow(columns, orient=tk.VERTICAL)
        outputPanel = ttk.Panedwindow(columns, orient=tk.VERTICAL)
        listPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        workPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        outputPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        columns.add(listPanel, weight=1)
        columns.add(workPanel, weight=2)
        columns.add(outputPanel, weight=2)
        #
        self.buildListPanel(listPanel)
        self.buildWorkPanel(workPanel)
        self.buildOutputPanel(outputPanel)
        
    def buildMenu(self, parent):
        menuBar = tk.Menu(parent)
        self.root.config(menu=menuBar)
        #
        file_menu = tk.Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label='File', menu=file_menu, underline=0)
        file_menu.add_command(label='Open', command=self.handlers.readInputs)
        file_menu.add_command(label='Quit', command=self.cleanup)
        #
        test_menu = tk.Menu(menuBar, tearoff=False)
        test_menu.add_command(label='BasicTest',
                              command=functools.partial(self.handlers.runTest, 'BasicTest') )
        menuBar.add_cascade(label='Test', menu=test_menu)#, underline=0)

    def buildGui(self, parent):
        pass

    def buildMenu(self, parent):
        pass
    
    def buildListPanel(self, parent):
        pass
    
    def buildAnalysisPanel(self, parent):
        pass
    
    def buildInputImageFrame(self, parent):
        pass
    
    def buildParametersPanel(self, parent):
        pass
    
    def buildOutputPanel(self, parent):
        pass

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
        if not self.gui:
            return
        store = AnalysisStore.get()
        logger.info(f'Store n analysis: {len(store.analysisTypes)}')
        for k in store.analysisTypes:
            self.vmodel.addAnalysis(k)
        self.gui.analysisPanel.selection.configure(values=self.vmodel.analysisList)

    def updateAnalysisPanel(self, analysisName):
        self.vmodel.currentAnalysis = analysisName
        store = AnalysisStore.get()
        analysis = store.create(analysisName, f'{analysisName}1')
        self.model.selectAnalysis(analysis)
        logger.info(f'Analysis {analysisName} -> {analysis}')
        if analysis:
            pframe = self.gui.analysisPanel.propertiesFrame
            pframe.clear()
            logger.info(f'  Analysis parameters {len(analysis.parameters)}')
            for pn, pv in analysis.parameters.items():
                values = (pn, pv)
                self.vmodel.analysisProperties.append(pv)
                pframe.addParameter(pv)
                pframe.build()
        pass
    
    def updateImageList(self):
        if not self.gui:
            return
        self.gui.imageList.delete(*self.gui.imageList.get_children())
        for img in self.model.imageList:
            values = (img.name, os.path.basename(img.path),
                      img.width, img.height, img.offset[0], img.offset[1])
            self.gui.imageList.insert('', tk.END, values=values)
        pass
    
    def showImages(self, images):
        logger.info(f'View.showImages called Nimages={len(images)}')
        self.vmodel.selectedImages.clear()
        #
        wframe = ImageFrame(images)
        self.vmodel.setCombinedFrame(wframe)
        wframe.combineImages()
        wframe.drawOnCanvas(self.gui.canvas)
        #self.gui.canvas.config('background')
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
                self.gui.galleryPanel.addImageFrame(imageTk, imageData.name)
        pass

    def clearGallery(self):
        self.gui.galleryPanel.clear()
        pass

