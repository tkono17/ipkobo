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
    def userInput_SelectFile(self):
        pass
    
    def userInput_AddImage(self):
        pass
    
    def imageList_Select(self):
        pass
    
    def analysis_Select(self):
        pass
    
    def analysis_SetProperties(self):
        pass
    
    pass
    
