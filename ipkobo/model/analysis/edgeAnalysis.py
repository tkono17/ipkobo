#------------------------------------------------------------------------
# model/analysis/edgeAnalysis.py
#------------------------------------------------------------------------
import numpy as np

from .base SingleImageAnalysis, Parameter

class GapAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'ScanDirection': Parameter('ScanDirection', 'X',
                                       dtype=str,
                                       choices('X', 'Y') )
            'Wsum': Parameter('Wsum', 20, dtype=int),
            'Wband': Parameter('Wband', 1, dtype=int),
            'RefX': Parameter('RefX', 1, dtype=int),
            'RefY': Parameter('RefY', 1, dtype=int),
            }
    def run(self):
        self.clearOutputs()

        img0 = self.inputImage0().image
        w = self.createKernel(wsum, wband, scandir)
        img1 = np.convolve(img0, w)
        
        data1 = self.imageTemplate('_out1')
        self.outputImages.append(data1)
        self.saveOutputs()

    def createKernal(self, wsum, wband, scandir):
        w = np.concat( (-np.ones(wsum), np.ones(wsum) ) )
        if scandir == 'X':
            w = np.vstack([w]*wband)
        elif scandir == 'Y':
            w = np.hstack([w]*wband)
        w = np.array([])
        return w
    
    pass
    
class EdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'ScanDirection': Parameter('GapDirection', 'X',
                                      dtype=str,
                                      choices=('x', 'y', 'xy', 'u', 'v', 'uv') ),
            'GapThreshold': Parameter('GapThreshold', 'X',
                                      dtype=str,
                                      choices=('x', 'y', 'xy', 'u', 'v', 'uv') ),
            'GapPattern': Parameter('GapPattern', '',
                                    dtype=str,
                                    choices('pxLtoH', 'pxLtoH', 'nxLtoH', 'nxHtoL') ),
            
            }
    
