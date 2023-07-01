#------------------------------------------------------------------------
# ipcat: model.py
#------------------------------------------------------------------------
import numpy as np
import cv2

class ImageData:
    def __init__(self, name, path, width, height, offset=[0.0, 0.0]):
        self.name = name
        self.path = path
        self.offset = offset
        self.width = width
        self.height = height
        self.image = None
        if os.path.exists(self.path):
            self.open()

    def open(self):
        if os.path.exists(self.path):
            self.image = cv2.imread(self.path, cv2.IMREAD_COLOR)

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
        #self.viewModel = ViewModel(app)
        pass

    def allAnalysisNames(self):
        v = list(map(lambda x: x.name, self.analysisList))
        return v
            
    def allImageNames(self):
        v = list(map(lambda x: x.name, self.imageList))
        return v
            
    def addImageToList(self, img):
        self.imageList.append(img)

    def setImage(self, img):
        self.currentImage = img

    def setAnalysis(self, analysis):
        self.currentAnalysis = analysis
        
    def changeImageName(self, name1, name2):
        pass
    
    def deleteImage(self, name):
        pass
    
