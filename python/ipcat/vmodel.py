#------------------------------------------------------------------------
# ipcat: vmodel.py
#------------------------------------------------------------------------

class ViewModel:
    def __init__(self):
        #
        self.imageList = []
        self.inputImagePath = ''
        self.inputImageOffset = [0.0, 0.0]
        self.inputImageWidth = 0.0
        self.inputImageHeight = 0.0
        #
        self.currentImage = None
        self.currentAnalysis = None
        #
        self.analysisProperties = []
        self.analysisOutputs = []
        self.analysisOutImages = []
        #
        self.messages = []
        
    # Actions
    def addImagesFromDirectory(self, dname):
        pass
    
    def addImageToList(self, image):
        pass

    def clearImageList(self):
        pass
    
    def selectImage(self, imageName):
        pass
    
    def showImage(self, image):
        pass

    def selectAnalysis(self, analysisName):
        pass

    def addAnalysisProperty(self, prop):
        pass

    def clearAnalysisProperties(self):
        pass
    
    def clearGallery(self):
        pass
    
    def showImageInGallery(self, image):
        pass
    
    pass
    
