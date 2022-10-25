#------------------------------------------------------------------------
# ipcat: vcontrol.py
#------------------------------------------------------------------------

import tkinter as tk
import tkinter.filedialog

from .gui import *

class ViewController:
    def __init__(self):
        pass

    def openFile(self, dname, ftypes):
        fn = tkinter.filedialog.askopenfilename(filetypes=ftypes, initialdir=dname)
        print('File opened: %s' % fn)
        
        
    

