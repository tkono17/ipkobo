#------------------------------------------------------------------------
# ipcat: vmodel.py
#------------------------------------------------------------------------

class ViewModel:
    def __init__(self, model):
        self.model = model
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
        
    pass
    
