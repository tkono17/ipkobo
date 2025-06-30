# ------------------------------------------------------------------------
# model/analysis/edgeAnalysis.py
# ------------------------------------------------------------------------
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

<<<<<<< HEAD

=======
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
class GapAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
<<<<<<< HEAD
            "scanDirection": Parameter(
                "scanDirection", value="Col", dtype=str, choices=("Col", "Row")
            ),
            "gapType": Parameter(
                "gapType", "Falling", dtype=str, choices=("Rising", "Falling")
            ),
            "crPosition": Parameter("crPosition", 0, dtype=int),
            "halfWindowSize": Parameter("halfWindowSize", 50, dtype=int),
            "bandSize": Parameter("bandSize", 10, dtype=int),
            "threshold": Parameter("threshold", 20, dtype=int),
        }

    def bandResize(self, img, bandSize, scanAxis):
        nrows, ncols = img.shape
        nrows2, ncols2 = nrows, ncols
        rebinAxis = 1 - scanAxis
        match rebinAxis:
            case 0:
                nrows2 = int(nrows / bandSize)
            case 1:
                ncols2 = int(ncols / bandSize)
        img1 = cv2.resize(img, (ncols2, nrows2))
        return img1

    def findLocalMinima(self, img, scanAxis, threshold):
        logger.info("findLocalMinima")
        # threshold = 15
        img1 = cv2.threshold(-img, threshold, 255, cv2.THRESH_TOZERO)[1]
        # strengths = np.zeros(len(x))
        logger.info(f"  scanAxis: {scanAxis}")
        x = np.sum(img1, axis=1 - scanAxis)
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(0, len(x)), x)
        self.addFig(fig, "_thrGap")
        #
        img1a = img1.astype(np.uint8)
        self.addImage(img1a, "_thr")
        #
        x = signal.argrelmax(img1, axis=scanAxis, order=5)
        return x  # np.vstack( [x, strengths] )

    def findLocalMaxima(self, img, scanAxis, threshold):
=======
            'scanDirection': Parameter('scanDirection', value='Col',
                                       dtype=str, choices=('Col', 'Row') ),
            'gapType': Parameter('gapType', 'Falling',
                                  dtype=str, choices=('Rising', 'Falling') ),
            'gapLocationAlongScan': Parameter('gapLocationAlongScan', 'First',
                                  dtype=str, choices=('First', 'Last') ),
            'crPosition': Parameter('crPosition', 0, dtype=int),
            'halfWindowSize': Parameter('halfWindowSize', 50, dtype=int),
            'nPixelsInCell': Parameter('nPixelsInCell', 10, dtype=int),
            'threshold': Parameter('threshold', 20, dtype=int),
            'useMaxGap': Parameter('useMaxGap', False, dtype=bool),
            }
        self.setParameters(kwargs)
        
    def resizeCell(self, img, scanDirection, nPixelsInCell):
        nrows, ncols = img.shape
        nrows2, ncols2 = nrows, ncols
        match scanDirection:
            case 'Row': ncols2 = int(ncols/nPixelsInCell)
            case 'Col': nrows2 = int(nrows/nPixelsInCell)
        img1 = cv2.resize(img, (ncols2, nrows2) )
        logger.info(f'  resize cell to {img1.shape}')
        return img1

    def findLocalMinima(self, img, scanAxis, threshold, useMaxGap=False):
        logger.info('findLocalMinima')
        return self.findLocalMaxima(-img, scanAxis, threshold, useMaxGap)
    
    def findLocalMaxima(self, img, scanAxis, threshold, useMaxGap=False):
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        img1 = cv2.threshold(img, threshold, 255, cv2.THRESH_TOZERO)[1]
        img1a = img1.astype(np.uint8)
        self.addImage(img1a, "_thr")
        #
        x = np.sum(img1, axis=1 - scanAxis)
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(0, len(x)), x)
        self.addFig(fig, "_thrGap")
        #
<<<<<<< HEAD
        x = signal.argrelmax(img1, axis=scanAxis)
        # strengths = np.zeros(len(x))
        return x  # np.vstack( [x, strengths] )

    def cnvToOriginalCoordinates(self, rcv, bandSize, halfWindowSize, scanAxis):
        dw = halfWindowSize * 2 + 1
        match scanAxis:
            case 0:
                v = (
                    [r + dw for r in rcv[0]],
                    [int((c + 0.5) * bandSize) for c in rcv[1]],
                )
            case 1:
                v = (
                    [int((r + 0.5) * bandSize) for r in rcv[0]],
                    [c + dw for c in rcv[1]],
                )
=======
        if useMaxGap:
            ymax = np.max(img1)
            ythr = ymax*0.9
            img2 = np.where(img1 < ythr, 0, img1)
            rows, cols = np.nonzero(img2)
            x = (rows, cols)
            logger.info(f'  found local maximum {x}')
        else:
            x = signal.argrelmax(img1, axis=scanAxis, order=5)
        return x

    def cnvToOriginalCoordinates(self, rcv, scanDirection, nPixelsInCell, halfWindowSize):
        dw = halfWindowSize
        vrows, vcols = rcv
        match scanDirection:
            case 'Row':
                v = ( [ r + dw for r in vrows ],
                      [ int( (c+0.5)*nPixelsInCell) for c in vcols ])
            case 'Col':
                v = ( [ int( (r+0.5)*nPixelsInCell) for r in vrows ],
                      [ c + dw for c in vcols ])
        logger.info(f'  coordinate: {v}')
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        return v

    def overlayPoints(self, img, rcv):
        img2 = img.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        radius = 10
        color = (0, 0, 150)
        thickness = 1
        for rc in zip(rcv[0], rcv[1]):
            cv2.circle(img2, (int(rc[1]), int(rc[0])), radius, color, thickness)
        return img2
<<<<<<< HEAD

    def overlayLine(self, img, gapPosition):
        img2 = img.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        thickness = 10
        c = gapPosition[0]
        cv2.line(img2, (c, 0), (c, 4000), (0, 255, 0), thickness)
        return img2

    def scanRow(self, img, col, w):
        img1 = img[:, col : col + w]
        img1b = np.average(img1, axis=1)
        fig, ax = plt.subplots(1, 1)
        nrows = img1b.shape[0]
        ax.plot(range(0, ncols), img1b)
        return img1b, fig

    def scanCol(self, img, row, w):
        nrows, ncols = img.shape
        bw = int(nrows / w)
        logger.info(f"scanCol resize {bw}, {ncols}")
        img1b = cv2.resize(img, (ncols, bw))
        img1b = cv2.threshold(img1b, 50, 255, cv2.THRESH_TOZERO)[1].astype(np.uint8)
        data = signal.argrelmax(img1b, axis=1)
        x = [x for x in data[0][:10]]
        y = [y for y in data[1][:10]]
        xy = zip(x, y)
        for a in xy:
            print(a)
        logger.info(f"  argrelmin data: {xy}")
        img1 = img[row : row + w, :]
        img1b = np.average(img1, axis=0)
        logger.info(f"  scanCol band-averaged shape: {img1b.shape}")
        fig, ax = plt.subplots(1, 1)
        ncols = img1b.shape[0]
        ax.plot(range(0, ncols), img1b)
        return img1b, fig

=======
    
    def overlayLine(self, img, gapPosition, scanDirection):
        img2 = img.copy()
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        thickness=10
        nrows, ncols, _ = img2.shape
        cmin, cmax, rmin, rmax = 0, ncols, 0, nrows
        gp = int(gapPosition)
        match scanDirection:
            case 'Row':
                rmin, rmax = gp, gp
            case 'Col':
                cmin, cmax = gp, gp
        cv2.line(img2, (cmin, rmin), (cmax, rmax), (0, 255, 0), thickness)
        return img2
    
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
    def gapPlots(self, vgaps):
        r, c = vgaps
        fig, axes = plt.subplots(2, 2)
        nr, nc = len(r), len(c)
        axes[0][0].plot(np.arange(0, nr), r)
        axes[0][1].plot(np.arange(0, nc), c)
        nr, nc = 4000, 6000
        axes[1][0].hist(r, bins=nr, range=(0, nr))
        axes[1][1].hist(c, bins=nc, range=(0, nc))
        figname = self.makeImageName("_gaps")
        self.addFig(fig, "_gaps")

    def gapPositions(self, shape, vgaps, scanDirection):
        positions = []
        rows, columns = vgaps
<<<<<<< HEAD
        nr, nc = 4000, 6000
        hist_r = np.histogram(rows, bins=nr, range=(0, nr))[0]
        hist_c = np.histogram(columns, bins=nc, range=(0, nc))[0]
        w = 10
        wfunc = np.ones(w)
        y = np.convolve(hist_c, wfunc, mode="same")  # + w
        logger.info(f"  y shape: {y.shape}")

        fig, axes = plt.subplots(2, 2)
        axes[0][0].plot(range(0, nc), hist_c)
        axes[0][0].set_xlabel("column")
        axes[0][1].plot(range(0, nc), y)
        axes[0][1].set_xlabel("column")
=======
        nr, nc = shape
        w= 10
        wfunc = np.ones(w)

        hist = None
        xlabel = ''
        nbins = 1
        match scanDirection:
            case 'Row':
                hist = np.histogram(rows, bins=nr, range=(0, nr) )[0]
                xlabel = 'Row'
                nbins = nr
            case 'Col':
                hist = np.histogram(columns, bins=nc, range=(0, nc) )[0]
                xlabel = 'Column'
                nbins = nc
        y = np.convolve(hist, wfunc, mode='same')# + w
        logger.info(f'  y shape: {y.shape}')
        
        fig, axes = plt.subplots(2, 2)
        axes[0][0].plot(range(0, nbins), hist)
        axes[0][0].set_xlabel(xlabel)
        axes[0][0].set_ylabel('N pixels on gaps')
        axes[0][1].plot(range(0, nbins), y)
        axes[0][1].set_xlabel(xlabel)
        axes[0][1].set_ylabel('N pixels on gap band')
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7

        logger.info(f"  y shape: {y.shape} max={np.max(y)}")
        ymax = np.max(y)
        ythr = int(ymax * 0.5)
        y2 = np.where(y < ythr, 0, y)
<<<<<<< HEAD
        axes[1][0].plot(range(0, nc), y2)
        axes[1][0].set_xlabel("column")
=======
        axes[1][0].plot(range(0, nbins), y2)
        axes[1][0].set_xlabel(xlabel)
        axes[1][0].set_ylabel('N pixels on gap band (thr)')
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7

        self.addFig(fig, "_merged")

        positions = signal.argrelmax(y2)
<<<<<<< HEAD
        logger.info(f"  all gaps: {positions}")
        for i in range(1820, 1830):
            print(f"   {i}: {y[i]}")
=======
        logger.info(f'  all gaps: {positions}')
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        return positions

    def scan(self, img0):
        nrows, ncols = img0.shape
<<<<<<< HEAD
        scanDirection = self.parameters["scanDirection"].value
        bandSize = self.parameters["bandSize"].value
        gapType = self.parameters["gapType"].value
        halfWindowSize = self.parameters["halfWindowSize"].value
        thr = self.parameters["threshold"].value
        scanAxis = 0
        match scanDirection:
            case "Row":
                scanAxis = 0
            case "Col":
                scanAxis = 1
=======
        scanDirection = self.parameters['scanDirection'].value
        nPixelsInCell = self.parameters['nPixelsInCell'].value
        gapType = self.parameters['gapType'].value
        gapLocationAlongScan = self.parameters['gapLocationAlongScan'].value
        halfWindowSize = self.parameters['halfWindowSize'].value
        thr = self.parameters['threshold'].value
        useMaxGap = self.parameters['useMaxGap'].value
        
        scanAxis = 0
        match scanDirection:
            case 'Row': scanAxis = 0
            case 'Col': scanAxis = 1

>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        # Band resize
        img1 = self.resizeCell(img0, scanDirection, nPixelsInCell)

        # Convolution with the kernel
<<<<<<< HEAD
        w = self.createKernel(halfWindowSize, bandSize, scanDirection)
        img2 = signal.convolve2d(img1, w, mode="same")
        img2a = (img2 + 255) / 2
        img2b = img2a.astype(np.uint8)
        data1 = self.addImage(img2b, "_conv2d")
=======
        w = self.createKernel(scanDirection, halfWindowSize)
        img2 = signal.convolve2d(img1, w, mode='valid')
        img2a = (img2+255)/2
        img2b = img2a.astype(np.uint8)
        data1 = self.addImage(img2b, '_conv2d')

>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        # Gap projection
        axis1 = 1 - scanAxis
        fig, ax = plt.subplots(1, 1)
        n = img2.shape[scanAxis]
<<<<<<< HEAD
        ax.plot(range(0, n), np.sum(img2, axis=axis1))
        self.addFig(fig, "_gapProj")
        # Find peaks
        thr = 20
        logger.info(f"GapType: {gapType}")
        match gapType:
            case "Rising":
                vgaps = self.findLocalMaxima(img2, scanAxis, thr)
            case "Falling":
                vgaps = self.findLocalMinima(img2, scanAxis, thr)
        # vgaps = self.cnvToOriginalCoordinates(vgaps, bandSize, halfWindowSize, scanAxis)
=======
        ax.plot(range(0, n), np.average(img2, axis=axis1))
        self.addFig(fig, '_gapProj')

        # Find peaks
        logger.info(f'GapType: {gapType}')
        match gapType:
            case 'Rising':
                vgaps = self.findLocalMaxima(img2, scanAxis, thr, useMaxGap)
            case 'Falling':
                vgaps = self.findLocalMinima(img2, scanAxis, thr, useMaxGap)
        vgaps = self.cnvToOriginalCoordinates(vgaps, scanDirection, nPixelsInCell, halfWindowSize)
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        self.gapPlots(vgaps)
        img4 = self.overlayPoints(img0, vgaps)
        data1 = self.addImage(img4, "_gapPoints")

<<<<<<< HEAD
        positions = self.gapPositions(vgaps)
        img5 = self.overlayLine(img0, positions[0])
        data1 = self.addImage(img5, "_gapLine")

        self.outputData["gapPoints"] = vgaps
=======
        rc_positions = self.gapPositions(img0.shape, vgaps, scanDirection)
        gposition = None
        logger.info(f'  rc_positions size: {len(rc_positions)} axis={scanAxis}')
        positions = rc_positions[0]
        logger.info(f'  positions: {positions}')
        if len(positions)>0:
            posIndex = 0
            if gapLocationAlongScan == 'Last': posIndex = -1
            logger.info(f'  position index: {posIndex}')
            gposition = positions[posIndex]
            img5 = self.overlayLine(img0, gposition, scanDirection)
            data1 = self.addImage(img5, '_gapLine')
        
        #self.outputData['gapPoints'] = vgaps
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        pass

    def run(self):
        self.showSettings()
        self.clearOutputs()
        self.scan(self.inputImage0().image)
        self.saveOutputs()

<<<<<<< HEAD
    def createKernel(self, halfWindowSize, bandSize, scandir):
        wn = np.ones(halfWindowSize, dtype=np.float32) / halfWindowSize
        wp = -np.ones(halfWindowSize + 1, dtype=np.float32) / (halfWindowSize + 1)
        w = np.concat((wn, wp))
        bsize = 1  # bandSize
        if scandir == "Col":
            w = np.vstack([w] * bsize)
            pass
        elif scandir == "Row":
            w = np.hstack([w] * bsize)
            w = np.transpose(w)
        else:
            w = np.ones((1, 1))
        return w

=======
    def createKernel(self, scanDirection, halfWindowSize):
        n0 = halfWindowSize
        n1 = halfWindowSize + 1
        wn = np.ones(n1, dtype=np.float32)/n1
        wp = -np.ones(n0, dtype=np.float32)/n0
        w = np.concat( (wn, wp) )
        match scanDirection:
            case 'Row':
                w = w.reshape(len(w), 1)
            case 'Col':
                w = w.reshape(1, len(w))
        return w
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
    pass


class EdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
<<<<<<< HEAD
            "edgeType": Parameter(
                "edgeType", value="L", dtype=str, choices=("T", "B", "L", "R")
            ),
            "darkBg": Parameter(
                "darkBg", value=True, dtype=bool, choices=(True, False)
            ),
            "scanHwSize": Parameter("scanHwSize", 20, dtype=int),
            "scanBandSize": Parameter("scanBandSize", 1, dtype=int),
            "scanThreshold": Parameter("scanThreshold", 50, dtype=int),
=======
            'edgeType': Parameter('edgeType', value='L', dtype=str, 
                                  choices=('T', 'B', 'L', 'R') ),
            'darkBg': Parameter('darkBg', value=True,
                                dtype=bool, choices=(True, False) ),
            'scanHwSize': Parameter('scanHwSize', 20, dtype=int),
            'scanBandSize': Parameter('scanBandSize', 10, dtype=int),
            'scanThreshold': Parameter('scanThreshold', 50, dtype=int),
            'useMaxGap': Parameter('useMaxGap', False, dtype=bool),
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
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
<<<<<<< HEAD
        ix = signal.argrelax(x)
        strengths = np.array([x[i] for i in ix])
=======
        ix = signal.argrelmax(x)
        strengths = np.array([ x[i] for i in ix ])
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        fig, ax = plt.subplots(1, 1)
        ax.plot(range(0, len(x)), x)
        self.addFig(fig, "_thrGap")
        return np.vstack(ix, strengths)

    def selectPoints(self, points, ix, width):
        points = []
        line = None
        return points, line

    def analyzeGapImage(self, img, darkBg, edgeType):
        scanThreshold = abs(self.parameters["scanThreshold"])
        pdata = None
        match edgeType:
            case "T" | "B":
                pdata = np.sum(img, axis=0)
                logger.info(f"  gap image in horizontal direction {len(pdata)}")
            case "L" | "R":
                pdata = np.sum(img, axis=0)
                logger.info(f"  gap image in vertical direction {len(pdata)}")
        if pdata is None:
            logger.warning(f"  edgeType is not one of T|B|L|R")
            return None

    def run(self):
<<<<<<< HEAD
        edgeType = self.parameters["edgeType"]
        darkBg = self.parameters["darkBg"]
        scanHwSize = self.parameters["scanHwSize"]
        scanBandSize = self.parameters["scanBandSize"]
        #
        if edgeType.value in ("L", "R"):
            gapDirection = "Col"
        elif edgeType.value in ("T", "B"):
            gapDirection = "Row"
=======
        self.showSettings()
        edgeType = self.parameters['edgeType'].value
        darkBg = self.parameters['darkBg'].value
        scanHwSize = self.parameters['scanHwSize'].value
        scanBandSize = self.parameters['scanBandSize'].value
        useMaxGap = self.parameters['useMaxGap'].value
        #
        scanDirection = ''
        if edgeType in ('L', 'R'):
            scanDirection = 'Col'
        elif edgeType in ('T', 'B'):
            scanDirection = 'Row'
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7
        else:
            logger.warning(f'EdgeAnalysis: Unknown edgeType "{edgeType.value}"')
            return None
        #
<<<<<<< HEAD
        gapType = "Rising"
        match (darkBg.value, edgeType.value):
            case (True, "L"):
                gapType = "Rising"
            case (True, "R"):
                gapType = "Falling"
            case (True, "T"):
                gapType = "Rising"
            case (True, "B"):
                gapType = "Falling"
            case (False, "L"):
                gapType = "Falling"
            case (False, "R"):
                gapType = "Rising"
            case (False, "T"):
                gapType = "Falling"
            case (False, "B"):
                gapType = "Rising"
        self.gapAnalysis = GapAnalysis(
            "",
            **{
                "scanDirection": gapDirection,
                "gapType": gapType,
                "halfWindowSize": scanHwSize.value,
                "bandSize": scanBandSize.value,
            },
        )
        #
        self.gapAnalysis.run()
        self.outputImages += self.gapAnalysis.outputImages
        idata1 = self.gapAnalysis.findImage("_gap")
        self.analyzeGapImage(idata1, darkBg, edgeType)
=======
        gapType = 'Rising'
        gapLocationAlongScan = 'First'
        match (darkBg, edgeType):
            case (True, 'L') | (True, 'T') | (False, 'R') | (False, 'B'):
                gapType = 'Rising'
            case (True, 'R') | (True, 'B') | (False, 'L') | (False, 'T'):
                gapType = 'Falling'
        match edgeType:
            case 'T' | 'L':
                gapLocationAlongScan = 'First'
            case 'B' | 'R':
                gapLocationAlongScan = 'Last'
        options = {
            'scanDirection': scanDirection,
            'gapType': gapType,
            'gapLocationAlongScan': gapLocationAlongScan,
            'halfWindowSize': scanHwSize,
            'nPixelsInCell': scanBandSize,
            'useMaxGap': useMaxGap,
            }
        self.gapAnalysis = GapAnalysis('', **options)
        self.gapAnalysis.setInputImages(self.inputImages)
        #
        self.gapAnalysis.run()
        self.outputImages += self.gapAnalysis.outputImages
        keys = [ x.name for x in self.outputImages ]
        for k in keys:
            logger.info(f'    image names: {k}')
        #idata1 = self.gapAnalysis.findImage('_gap')
        #self.analyzeGapImage(idata1, darkBg, edgeType)
>>>>>>> 2a92f4e7e5926c103e95d651be1275b7ce3710e7


class CannyEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            "threshold1": Parameter("threshold1", 30, dtype=int),
            "threshold2": Parameter("threshold2", 20, dtype=int),
        }

    def run(self):
        self.clearOutputs()
        img0 = self.inputImage0().image
        threshold1 = self.parameters["threshold1"].value
        threshold2 = self.parameters["threshold2"].value
        img1 = cv2.Canny(img0, threshold1, threshold2)
        name = self.makeImageName("_edge")
        self.outputImages.append(self.makeImageData(name, f"{name}.jpg", img1))
        self.saveOutputs()


class GfbaEdgeAnalysis(SingleImageAnalysis):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.parameters = {
            "edgeDirection": Parameter(
                "edgeDirection", "Row", dtype=str, choices=("Col", "Row")
            ),
            "halfWindowSize": Parameter("halfWindowSize", 50, dtype=int),
            "gapThreshold": Parameter("gapThreshold", 50, dtype=int),
        }

    def run(self):
        self.clearOutputs()
        ga = GapAnalysis(self.name)
        for p in "halfWindowSize":
            ga.setParameter(key, self.parameters[key].value)
        match self.parameters["edgeDirection"].value:
            case "Col":
                ga.setParameter("gapDirection", "Row")
            case "Row":
                ga.setParameter("gapDirection", "Col")
        ga.run()
        self.outputImages += ga.outputImages()
        #
        img1 = self.outputImages[0]
        fig, ax = plt.subplots(1, 1, 1)
        nrows, ncols = img1.shape
        nbins = ncols
        ax.hist(img1, bins=nbins, range=(0, nrows))
        name = self.makeImageName("_hist")
        img2 = self.makeImageDataFromFig(name, f"{name}.png", fig=fig)
        self.outputImages.append(img2)
        self.saveOutputs()
