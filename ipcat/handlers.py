#------------------------------------------------------------------------
# ipcat: handlers.py
#------------------------------------------------------------------------
from .control  import *

class Handlers:
    def __init__(self, app=None, controller=None):
        self.init(app, controller)
        
    def init(self, app, controller):
        self.app = app
        self.controller = controller
        
    def openImage(self):
        print('openImage called')
        self.controller.openImage()

    def singleDisplaySet(self):
        print('singleDisplaySet')
        tree = self.app.userInputPanel.imageTree
        v = tree.selection()
        print('Images selected %d' % len(v))
        if len(v) == 1:
            print(tree.item(v[0]))
            
    def selectImage(self, e):
        print('selectImage from Treeview called')
        tree = e.widget
        selected = tree.selection()
        if len(selected) == 1:
            print(selected[0])
            values = tree.item(selected[0])['values']
            print(values)

