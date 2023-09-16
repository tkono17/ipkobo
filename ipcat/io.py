#------------------------------------------------------------------------
# ipcat: io.py
#------------------------------------------------------------------------
import os
import json
import yaml
import urllib.request
from .model import ImageData

class InputData:
    def __init__(self, fn):
        self.filePath = fn
        self.data = None
        self.imageData = []
        self.readData(fn)

    def readData(self, fn):
        if os.path.exists(fn):
            with open(fn, 'r') as fin:
                self.data = json.load(fin)
        elif fn.beginswith('http'):
            res = urllib.urlopen(fn)
            if res.status == 200:
                self.data = res.read()
                
    def setProp(self, props, key, section):
        x = None
        if key in section.keys():
            x = section[key]
            props[key] = x
    
    def getImage(self, section):
        props = {}
        self.setProp(props, 'name', section)
        self.setProp(props, 'path', section)
        self.setProp(props, 'width', section)
        self.setProp(props, 'height', section)
        self.setProp(props, 'offset', section)
        x = ImageData(**props)
        return x

    def getImages(self):
        v = []
        for image in self.data['images']:
            v.append(self.getImage(image))
        return v
    pass

    
    
