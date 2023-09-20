#------------------------------------------------------------------------
# ipcat: test.py
# -------------
# Tests
#------------------------------------------------------------------------
import logging
from .app import App
from .model import ImageData
from .io import InputData

logger = logging.getLogger(__name__)

class Test:
    def __init__(self, name, app):
        self.name = name
        self.app = app
        self.passed = False
    def run(self):
        pass
    def isPassed(self):
        return self.passed

class BatchTest1(Test):
    def __init__(self, name, app):
        super().__init__(name, app)

    def run(self):
        logger.info(f'Running BathTest1 {self.name}')
        imageName = 'test1'
        fn = ''
        w, h = 6000, 4000
        xy = (0, 0)
        analysisName = 'ColorToGray'
        self.app.addImageToList(ImageData(imageName,
                                          fn,
                                          width=w, height=h, offset=xy) )
        self.app.selectImage(imageName)
        self.app.selectAnalysis(analysisName)
        self.app.setAnalysisParameters({
            'name': 'analsys1'
        })
        self.app.runAnalysis()
        outputs = self.app.analysisOutputs()
        self.passed = True
        
class BasicTest(Test):
    def __init__(self, name, app):
        super().__init__(name, app)

    def run(self):
        indata = InputData('./a.json')
        v = indata.getImages()
        for x in v:
            self.app.addImage(x)
        
class BasicGuiTest(Test):
    def __init__(self, name, app):
        super().__init__(name, app)

    def run(self):
        logger.info(f'Running BasicGuiTest {self.name}')
        imageName = 'test1'
        fn = ''
        fn1 = '/home/tkono/work/ImageProcessing/work/Img43808.jpg'
        w, h = 6000, 4000
        xy = (0, 0)
        analysisName = 'ColorToGray'
        self.app.addImageToList(ImageData(imageName,
                                          fn1,
                                          width=w, height=h, offset=xy) )
        self.app.addImageToList(ImageData('test2',
                                          fn,
                                          width=w, height=h, offset=xy) )
        for i in range(50):
            self.app.addImageToList(ImageData(f'test{i}',
                                              fn,
                                              width=w, height=h, offset=xy) )
