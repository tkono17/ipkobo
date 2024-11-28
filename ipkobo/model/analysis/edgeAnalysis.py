#------------------------------------------------------------------------
# model/analysis/edgeAnalysis.py
#------------------------------------------------------------------------
import logging
import numpy as np

from .base import SingleImageAnalysis, Parameter
from .tools import conv2d

logger = logging.getLogger(__name__)

class GapAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'ScanDirection': Parameter('ScanDirection', value='Col',
                                       dtype=str, choices=('Col', 'Row') ),
            'Wsum': Parameter('Wsum', 20, dtype=int),
            'Wband': Parameter('Wband', 1, dtype=int),
            'Row0': Parameter('Row0', 1, dtype=int),
            'Col0': Parameter('Col0', 1, dtype=int),
            }
        
    def run(self):
        self.clearOutputs()

        scandir = self.parameters['ScanDirection'].value
        r0 = self.parameters['Row0'].value
        c0 = self.parameters['Col0'].value
        suffix = f'_scan{scandir}'
        if scandir == 'Col':
            suffix += f'atRow{r0}'
        elif scandir == 'Row':
            suffix += f'atCol{c0}'
        wsum = self.parameters['Wsum'].value
        wband = self.parameters['Wband'].value
        logger.info(f'Run GapAnalysis with')
        logger.info(f'  ScanDirection: {scandir} at Row0={r0}, Col0={c0}')
        logger.info(f'  Convolution kernel: wsum={wsum}, wband={wband}')
        logger.info(f'  Input images: {len(self.inputImages)}')
        logger.info(f'  Input images: {self.inputImage0()}')
        logger.info(f'  Input images: {self.inputImage0().image}')
        #
        img0 = self.inputImage0().image
        w = self.createKernel(wsum, wband, scandir)
        img1 = conv2d(img0, w)
        logger.info(f'    Image returned from conv2d: {img1}')
        logger.info(f'    Image returned from conv2d shape: {img1.shape}')
        data1 = self.imageTemplate(suffix, img1)
        self.outputImages.append(data1)
        self.saveOutputs()

    def createKernel(self, wsum, wband, scandir):
        w1 = np.ones(wsum)
        w = np.concat( (-w1, w1) )
        if scandir == 'Col':
            w = np.vstack([w]*wband)
        elif scandir == 'Row':
            w = np.hstack([w]*wband)
        else:
            w = np.ones( (1, 1) )
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
                                    choices=('pxLtoH', 'pxLtoH', 'nxLtoH', 'nxHtoL') ),
            }
    
