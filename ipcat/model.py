#------------------------------------------------------------------------
# ipcat: model.py
#------------------------------------------------------------------------

from .vmodel import ViewModel

class ImageNP:
    def __init__(self, name, path=''):
        self.name = name
        self.path = path
        self.image = ''

    def open(self):
        pass

    def save(self):
        pass

class AppData:
    def __init__(self):
        self.openFileDir = '.'
        self.imageList = []
        self.originalImage = None
        #
        #self.viewModel = ViewModel(app)
        pass

    def addImage(self, img):
        self.imageList.append(img)

    def deleteImage(self, name):
        pass
    
