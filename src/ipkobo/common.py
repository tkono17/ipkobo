#------------------------------------------------------------------------
# ipcat: common.py
#------------------------------------------------------------------------

class CommonData:
    def __init__(self):
        self.application = None
        self.controller = None
        self.vcontroller = None
        
    def set(self, app, c, vc):
        self.application = app
        self.controller = c
        self.vcontroller = vc

    def app(self):
        return self.application
    
    def c(self):
        return self.controller

    def vc(self):
        return self.vcontroller
    
cdata = CommonData()
