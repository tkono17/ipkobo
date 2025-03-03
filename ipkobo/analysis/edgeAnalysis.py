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

class GapTarget:
    def __init__(self, direction, edgeType, cr_position=None):
        self.direction = direction
        self.edgeType = edgeType
        self.crPosition = cr_position
        pass
    
class GapAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'scanDirection': Parameter('scanDirection', value='Col',
                                       dtype=str, choices=('Col', 'Row') ),
            'gapType': Parameter('gapType', 'Falling',
                                  dtype=str, choices=('Rising', 'Falling') ),
            'crPosition': Parameter('crPosition', 0, dtype=int),
            'halfWindowSize': Parameter('halfWindowSize', 50, dtype=int),
            'bandSize': Parameter('bandSize', 10, dtype=int),
            'threshold': Parameter('threshold', 20, dtype=int),
            }

    def bandResize(self, img, bandSize, scanAxis):
        nrows, ncols = img.shape
        nrows2, ncols2 = nrows, ncols
        rebinAxis = 1 - scanAxis
        match rebinAxis:
            case 0: nrows2 = int(nrows/bandSize)
            case 1: ncols2 = int(ncols/bandSize)
        img1 = cv2.resize(img, (ncols2, nrows2) )
        return img1

    def findLocalMinima(self, img, scanAxis, threshold):
        logger.info('findLocalMinima')
        #threshold = 15
        img1 = cv2.threshold(-img, threshold, 255, cv2.THRESH_TOZERO)[1]
        #strengths = np.zeros(len(x))
        logger.info(f'  scanAxis: {scanAxis}')
        x = np.sum(img1, axis=1-scanAxis)
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(0, len(x)), x)
        self.addFig(fig, '_thrGap')
        #
        img1a = img1.astype(np.uint8)
        self.addImage(img1a, '_thr')
        #
        x = signal.argrelmax(img1, axis=scanAxis, order=5)
        return x #np.vstack( [x, strengths] )
    
    def findLocalMaxima(self, img, scanAxis, threshold):
        img1 = cv2.threshold(img, threshold, 255, cv2.THRESH_TOZERO)[1]
        img1a = img1.astype(np.uint8)
        self.addImage(img1a, '_thr')
        #
        x = np.sum(img1, axis=1-scanAxis)
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(0, len(x)), x)
        self.addFig(fig, '_thrGap')
        #
        x = signal.argrelmax(img1, axis=scanAxis)
        #strengths = np.zeros(len(x))
        return x #np.vstack( [x, strengths] )

    def cnvToOriginalCoordinates(self, rcv, bandSize, halfWindowSize, scanAxis):
        dw = halfWindowSize * 2 + 1
        match scanAxis:
            case 0:
                v = ( [ r + dw for r in rcv[0] ],
                      [ int( (c+0.5)*bandSize) for c in rcv[1] ])
            case 1:
                v = ( [ int( (r+0.5)*bandSize) for r in rcv[0] ],
                      [ c + dw for c in rcv[1] ])
        return v

    def overlayPoints(self, img, rcv):
        img2 = img.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        radius = 50
        color = (0, 0, 150)
        thickness=1
        for rc in zip(rcv[0], rcv[1]):
            cv2.circle(img2, (rc[1], rc[0]), radius, color, thickness)
        return img2
    
    def overlayLine(self, img, gapPosition):
        img2 = img.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        thickness=10
        c = gapPosition[0]
        cv2.line(img2, (c, 0), (c, 4000), (0, 255, 0), thickness)
        return img2
    
    def scanRow(self, img, col, w):
        img1 = img[:, col:col+w]
        img1b = np.average(img1, axis=1)
        fig, ax = plt.subplots(1, 1)
        nrows = img1b.shape[0]
        ax.plot(range(0, ncols), img1b)
        return img1b, fig
        
    def scanCol(self, img, row, w):
        nrows, ncols = img.shape
        bw = int(nrows/w)
        logger.info(f'scanCol resize {bw}, {ncols}')
        img1b = cv2.resize(img, (ncols, bw) )
        img1b = cv2.threshold(img1b, 50, 255, cv2.THRESH_TOZERO)[1].astype(np.uint8)
        data = signal.argrelmax(img1b, axis=1)
        x = [ x for x in data[0][:10] ]
        y = [ y for y in data[1][:10] ]
        xy = zip(x, y)
        for a in xy:
            print(a)
        logger.info(f'  argrelmin data: {xy}')
        img1 = img[row:row+w, :]
        img1b = np.average(img1, axis=0)
        logger.info(f'  scanCol band-averaged shape: {img1b.shape}')
        fig, ax = plt.subplots(1, 1)
        ncols = img1b.shape[0]
        ax.plot(range(0, ncols), img1b)
        return img1b, fig

    def gapPlots(self, vgaps):
        r, c = vgaps
        fig, axes = plt.subplots(2, 2)
        nr, nc = len(r), len(c)
        axes[0][0].plot(np.arange(0, nr), r)
        axes[0][1].plot(np.arange(0, nc), c)
        nr, nc = 4000, 6000
        axes[1][0].hist(r, bins=nr, range=(0, nr))
        axes[1][1].hist(c, bins=nc, range=(0, nc))
        figname = self.makeImageName('_gaps')
        self.addFig(fig, '_gaps')

    def gapPositions(self, vgaps):
        positions = []
        rows, columns = vgaps
        nr, nc = 4000, 6000
        hist_r = np.histogram(rows, bins=nr, range=(0, nr) )[0]
        hist_c = np.histogram(columns, bins=nc, range=(0, nc) )[0]
        w= 10
        wfunc = np.ones(w)
        y = np.convolve(hist_c, wfunc, mode='same')# + w
        logger.info(f'  y shape: {y.shape}')
        
        fig, axes = plt.subplots(2, 2)
        axes[0][0].plot(range(0, nc), hist_c)
        axes[0][0].set_xlabel('column')
        axes[0][1].plot(range(0, nc), y)
        axes[0][1].set_xlabel('column')

        logger.info(f'  y shape: {y.shape} max={np.max(y)}')
        ymax = np.max(y)
        ythr = int(ymax * 0.5)
        y2 = np.where(y < ythr, 0, y)
        axes[1][0].plot(range(0, nc), y2)
        axes[1][0].set_xlabel('column')

        self.addFig(fig, '_merged')

        positions = signal.argrelmax(y2)
        logger.info(f'  all gaps: {positions}')
        for i in range(1820, 1830):
            print(f'   {i}: {y[i]}')
        return positions
    
    def scan(self, img0):
        nrows, ncols = img0.shape
        scanDirection = self.parameters['scanDirection'].value
        bandSize = self.parameters['bandSize'].value
        gapType = self.parameters['gapType'].value
        halfWindowSize = self.parameters['halfWindowSize'].value
        thr = self.parameters['threshold'].value
        scanAxis = 0
        match scanDirection:
            case 'Row': scanAxis = 0
            case 'Col': scanAxis = 1
        # Band resize
        img1 = self.bandResize(img0, bandSize, scanAxis)
        # Convolution with the kernel
        w = self.createKernel(halfWindowSize, bandSize, scanDirection)
        img2 = signal.convolve2d(img1, w, mode='same')
        img2a = (img2+255)/2
        img2b = img2a.astype(np.uint8)
        data1 = self.addImage(img2b, '_conv2d')
        # Gap projection
        axis1 = 1-scanAxis
        fig, ax = plt.subplots(1, 1)
        n = img2.shape[scanAxis]
        ax.plot(range(0, n), np.sum(img2, axis=axis1))
        self.addFig(fig, '_gapProj')
        # Find peaks
        thr = 20
        logger.info(f'GapType: {gapType}')
        match gapType:
            case 'Rising': vgaps = self.findLocalMaxima(img2, scanAxis, thr)
            case 'Falling': vgaps = self.findLocalMinima(img2, scanAxis, thr)
        #vgaps = self.cnvToOriginalCoordinates(vgaps, bandSize, halfWindowSize, scanAxis)
        self.gapPlots(vgaps)
        img4 = self.overlayPoints(img0, vgaps)
        data1 = self.addImage(img4, '_gapPoints')

        positions = self.gapPositions(vgaps)
        img5 = self.overlayLine(img0, positions[0])
        data1 = self.addImage(img5, '_gapLine')
        
        self.outputData['gapPoints'] = vgaps
        pass
    
    def run(self):
        self.clearOutputs()
        self.scan(self.inputImage0().image)
        self.saveOutputs()

    def createKernel(self, halfWindowSize, bandSize, scandir):
        wn = np.ones(halfWindowSize, dtype=np.float32)/halfWindowSize
        wp = -np.ones(halfWindowSize+1, dtype=np.float32)/(halfWindowSize+1)
        w = np.concat( (wn, wp) )
        bsize = 1 # bandSize
        if scandir == 'Col':
            w = np.vstack([w]*bsize)
            pass
        elif scandir == 'Row':
            w = np.hstack([w]*bsize)
            w = np.transpose(w)
        else:
            w = np.ones( (1, 1) )
        return w
    
    pass
    
class EdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'edgeType': Parameter('edgeType', value='L',
                                  choices=('T', 'B', 'L', 'R') ),
            'darkBg': Parameter('darkBg', value=True,
                                dtype=bool, choices=(True, False) ),
            'scanHwSize': Parameter('scanHwSize', 20, dtype=int),
            'scanBandSize': Parameter('scanBandSize', 1, dtype=int),
            'scanThreshold': Parameter('scanThreshold', 50, dtype=int),
        }
        self.gapAnalysis = None

    def projectPoints(self, x, axis):
        x2 = np.sum(x, axis=axis)
        return x2

    def sumNeighbors(self, x, width):
        k = np.ones(width)
        x2 = np.convolve(x, k)
        return x2

    def findLocalMaxima(self, x):
        ix = signal.argrelax(x)
        strengths = np.array([ x[i] for i in ix ])
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(0, len(x)), x)
        self.addFig(fig, '_thrGap')
        return np.vstack(ix, strengths)

    def selectPoints(self, points, ix, width):
        points = []
        line = None
        return points, line
    
    def analyzeGapImage(self, img, darkBg, edgeType):
        scanThreshold = abs(self.parameters['scanThreshold'])
        pdata = None
        match edgeType:
            case 'T' | 'B':
                pdata = np.sum(img, axis=0)
                logger.info(f'  gap image in horizontal direction {len(pdata)}')
            case 'L' | 'R':
                pdata = np.sum(img, axis=0)
                logger.info(f'  gap image in vertical direction {len(pdata)}')
        if pdata is None:
            logger.warning(f'  edgeType is not one of T|B|L|R')
            return None
        
            
    def run(self):
        edgeType = self.parameters['edgeType']
        darkBg = self.parameters['darkBg']
        scanHwSize = self.parameters['scanHwSize']
        scanBandSize = self.parameters['scanBandSize']
        #
        if edgeType in ('L', 'R'):
            gapDirection = 'Col'
        elif edgeType in ('T', 'B'):
            gapDirection = 'Row'
        else:
            logger.warning(f'EdgeAnalysis: Unknown edgeType "{edgeType}"')
            return None
        #
        gapType = 'Rising'
        match (darkBg, edgeType):
            case (True, 'L'): gapType = 'Rising'
            case (True, 'R'): gapType = 'Falling'
            case (True, 'T'): gapType = 'Rising'
            case (True, 'B'): gapType = 'Falling'
            case (False, 'L'): gapType = 'Falling'
            case (False, 'R'): gapType = 'Rising'
            case (False, 'T'): gapType = 'Falling'
            case (False, 'B'): gapType = 'Rising'
        self.gapAnalysis = GapAnalysis('', {
            'scanDirection': scanDirection,
            'gapType': gapType,
            'halfWindowSize': scanHwSize,
            'bandSize': scanBandSize,
            })
        #
        self.gapAnalysis.run()
        self.outputImages += self.gapAnalysis.outputImages
        idata1 = self.gapAnalysis.findImage('_gap')
        self.analyzeGapImage(idata1, darkBg, edgeType)

    
class CannyEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'threshold1': Parameter('threshold1', 30, dtype=int),
            'threshold2': Parameter('threshold2', 20, dtype=int),
            }

    def run(self):
        self.clearOutputs()
        img0 = self.inputImage0().image
        threshold1 = self.parameters['threshold1'].value
        threshold2 = self.parameters['threshold2'].value
        img1 = cv2.Canny(img0, threshold1, threshold2)
        name = self.makeImageName('_edge')
        self.outputImages.append(self.makeImageData(name, f'{name}.jpg', img1))
        self.saveOutputs()

class GfbaEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            'edgeDirection': Parameter('edgeDirection', 'Row', dtype=str,
                                       choices=('Col', 'Row')),
            'halfWindowSize': Parameter('halfWindowSize', 50, dtype=int),
            'gapThreshold': Parameter('gapThreshold', 50, dtype=int),
            }
    def run(self):
        self.clearOutputs()
        ga = GapAnalysis(self.name)
        for p in ('halfWindowSize'):
            ga.setParameter(key, self.parameters[key].value)
        match self.parameters['edgeDirection'].value:
            case 'Col': ga.setParameter('gapDirection', 'Row')
            case 'Row': ga.setParameter('gapDirection', 'Col')
        ga.run()
        self.outputImages += ga.outputImages()
        #
        img1 = self.outputImages[0]
        fig, ax = plt.subplots(1, 1, 1)
        nrows, ncols = img1.shape
        nbins = ncols
        ax.hist(img1, bins=nbins, range=(0, nrows))
        name = self.makeImageName('_hist')
        img2 = self.makeImageDataFromFig(name, f'{name}.png', fig=fig)
        self.outputImages.append(img2)
        self.saveOutputs()

