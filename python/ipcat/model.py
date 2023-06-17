#------------------------------------------------------------------------
# ipcat: model.py
#------------------------------------------------------------------------
import numpy as np

class ImageNP:
    def __init__(self, name, path=''):
        self.name = name
        self.path = path
        self.offset = np.array([0.0, 0.0])
        self.width = 0.0
        self.height = 0.0
        self.image = None

    def open(self):
        pass

    def save(self, fpath):
        pass

class AppData:
    def __init__(self):
        self.openFileDir = '.'
        self.inputImageList = []
        self.imageList = []
        self.analysisList = []
        self.originalImage = None
        #
        #self.viewModel = ViewModel(app)
        pass

    def addImage(self, img):
        self.imageList.append(img)

    def addInputImage(self, img):
        self.inputImageList.append(img)
        self.addImage(img)

    def changeImageName(self, name1, name2):
        pass
    
    def deleteImage(self, name):
        pass
    
