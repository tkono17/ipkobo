#------------------------------------------------------------------------
# ipcat: vmodel.py
#------------------------------------------------------------------------

class ViewModel:
    def __init__(self, model):
        self.model = model
        #
        self.selectedImages = []
        self.inputImagePath = ''
        self.inputImageOffset = [0.0, 0.0]
        self.inputImageWidth = 0.0
        self.inputImageHeight = 0.0
        #
        self.analysisList = []
        #
        self.currentImage = ''
        #
        self.currentAnalysis = ''
        self.analysisProperties = []
        self.analysisOutImages = []
        self.analysisOutputs = []
        #
        self.messages = []

    def addAnalysis(self, key):
        self.analysisList.append(key)
        print(self.analysisList)
    pass
    
