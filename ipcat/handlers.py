#------------------------------------------------------------------------
# ipcat: handlers.py
#------------------------------------------------------------------------
from .control  import *
from .vcontrol import *


controller = Controller()
vcontroller = ViewController()

class Handlers:

    @classmethod
    def openImage(e):
        print('openImage called')
        dn = controller.openFileDir()
        vcontroller.openFile(dn, [('Image file', '*.jpg;*.png')])

    def selectImage():
        print('selectImage called')


        
