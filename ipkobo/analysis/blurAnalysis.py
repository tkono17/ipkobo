#------------------------------------------------------------------------
# ipcat: analysis/simpleAnalysis.py
#------------------------------------------------------------------------
import logging
import numpy as np

import cv2

from .base import Parameter, SingleImageAnalysis

logger = logging.getLogger(__name__)

class GaussianBlurAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'ksizeX': Parameter('ksizeX', 3, dtype=int),
            'ksizeY': Parameter('ksizeY', 3, dtype=int),
            'sigma': Parameter('sigma', 0, dtype=int),
            }
    def run(self):
        ksize = (self.parameters['ksizeX'].value,
                 self.parameters['ksizeY'].value)
        sigma = self.parameters['sigma'].value
        img0 = self.inputImage0().image
        img1 = cv2.GaussianBlur(img0, ksize, sigma)
        name = self.makeImageName('_blur')
        self.outputImages.append(self.makeImageData(name, f'{name}.jpg', img1))
        self.saveOutputs()
