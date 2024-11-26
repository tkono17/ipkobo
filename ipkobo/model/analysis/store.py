#------------------------------------------------------------------------
# ipcat: analysis/base.py
#------------------------------------------------------------------------
import logging
from .base import *
from .simpleAnalysis import *

logger = logging.getLogger(__name__)

class AnalysisStore:
    sInstance = None
    
    @staticmethod
    def get():
        if AnalysisStore.sInstance == None:
            AnalysisStore.sInstance = AnalysisStore()
        return AnalysisStore.sInstance
    
    def __init__(self):
        self.analysisTypes = []
        self.analysisClasses = {}
        self.initialize()
        pass

    def initialize(self):
        logger.info('AnalysisStore initialize')
        self.addAnalysis('ColorAnalysis', ColorAnalysis)
        self.addAnalysis('IntensityAnalysis', IntensityAnalysis)
        self.addAnalysis('CannyEdgeAnalysis', CannyEdgeAnalysis)
        self.addAnalysis('ThresholdAnalysis', ThresholdAnalysis)
        self.addAnalysis('ContourAnalysis', ContourAnalysis)
        
    def addAnalysis(self, name, analysisClass):
        if name in self.analysisTypes:
            print(f'Analysis {name} already exists')
        else:
            self.analysisTypes.append(name)
            self.analysisClasses[name] = analysisClass

    def find(self, name):
        x = None
        if name in self.analysisClasses.keys():
            x = self.analysisClasses[name]
        return x

    def create(self, clsName, name, inputImages=[]):
        x = None
        cls = self.find(clsName)
        if cls:
            logger.info(f'Create analysis of type {clsName} {cls}')
            x = cls(name, inputImages=inputImages)
        return x
    
