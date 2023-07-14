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

from .model import ImageData
from .analysis import AnalysisStore

logger = logging.getLogger(__name__)

class View:
    def __init__(self, gui):
        self.gui = gui
        self.vmodel = self.gui.vmodel
        self.model = self.gui.vmodel.model
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

    def analysisSelected(self, analysisName):
        self.vmodel.currentAnalysis = analysisName
        store = AnalysisStore.get()
        analysis = store.create(analysisName, f'{analysisName}1')
        self.model.selectAnalysis(analysis)
        logger.info(f'Analysis {analysisName} -> {analysis}')
        if analysis:
            table = self.gui.analysisPanel.table
            table.delete(*table.get_children())
            logger.info(f'  Analysis parameters {len(analysis.parameters)}')
            for pn, pv in analysis.parameters.items():
                values = (pn, pv)
                self.vmodel.analysisProperties.append( (pn, pv) )
                table.insert('', tk.END, values=values)
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
        if len(images) == 1:
            self.vmodel.selectedImages.append(images[0])
            imageData = images[0]
            if imageData.imageOk:
                img0 = imageData.image
                cw = self.gui.canvas.winfo_width()
                ch = self.gui.canvas.winfo_height()
                h, w = img0.shape[0], img0.shape[1]
                scale = min(cw/w, ch/h)
                imgTk = imageData.resize( (int(scale*w), int(scale*h)) )
                self.gui.canvas.create_image( (cw/2, ch/2), image=imgTk)
        else:
            logger.warning('Only one image can be selected')
        pass

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
        
        pass

    def clearGallery(self):
        pass

