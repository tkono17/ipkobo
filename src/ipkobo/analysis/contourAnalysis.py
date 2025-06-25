#------------------------------------------------------------------------
# model/analysis/edgeAnalysis.py
#------------------------------------------------------------------------
import logging
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
import cv2

from .base import SingleImageAnalysis, Parameter

logger = logging.getLogger(__name__)

class ContourAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            # 'threshold': Parameter('threshold', dtype=int, value=100), # ok for PCB Fmark
            'threshold': Parameter('threshold', dtype=int, value=200
),
            }

    def run(self):
        logger.info('Run Contour analysis')
        self.clearOutputs()
        img0 = self.inputImage0().image
        thr = self.parameters['threshold'].value
        _, img1 = cv2.threshold(img0, thr, 255, cv2.THRESH_BINARY)
        self.addImage(img1, '_thr')
        
        contours, hierarchy = cv2.findContours(img1,
                                               cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)
        logger.info(f'  number of contours: {len(contours)}')
        img2 = np.zeros(img1.shape, dtype=np.uint8)
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(img2, contours, -1, (0,255,0), -1)
        self.addImage(img2, '_cont')

        areas = [ cv2.contourArea(c) for c in contours ]
        fig, ax = plt.subplots(1, 1)
        ax.hist(areas, bins=100, range=(0, 1.0E+6) )
        ax.set_xlabel('Area')
        ax.set_ylabel('Entries')
        ax.set_yscale('log')
        self.addFig(fig, '_area')

        def targetSize(c):
            x, y, w, h = cv2.boundingRect(c)
            w0, h0, dw, dh = 250, 250, 50, 50
            if w > (w0-dw) and w < (w0+dw) and\
               h > (h0-dh) and h < (h0+dh):
                logger.info(f'   target size: {w}x{h}')
                return True
            else:
                return False
        contours1 = list(filter(lambda x: cv2.contourArea(x)>1.0E+4, contours))
        contours1 = list(filter(targetSize, contours1))
        if len(contours1)>0:
            ac = [ (cv2.contourArea(c), c) for c in contours1 ]
            ac.sort()
            area1, c1 = ac[-1]
            #contours2 = [c1]
            contours2 = contours1
            logger.info(f'  N contours with area>10^4: {len(contours1)}')
            logger.info(f'    max area: {area1}')
            xy, r = cv2.minEnclosingCircle(c1)
            center = ( int(xy[0]), int(xy[1]) )
            r = int(r)
            img3 = np.zeros(img1.shape, dtype=np.uint8)
            img3 = cv2.cvtColor(img3, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(img3, contours2, -1, (0,255,0), -1)
            cv2.circle(img3, center, r, (0, 0, 255), 3)
            self.addImage(img3, '_cont2')
        
        self.saveOutputs()
