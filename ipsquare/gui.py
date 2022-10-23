#------------------------------------------------------------------------
# ImageProcessingSquare: gui.py
#------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

#------------------------------------------------------------------------
# MainWindow
#------------------------------------------------------------------------
class MainWindow(ttk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        super().__init__()
        self.initialized = False
        
    def setup(self):
        self.root.title('Image Processing Square')
        self.root.geometry('1200x800')
        self.initialized = True
        pass

    def startGui(self):
        if not self.initialized: self.setup()
        self.root.mainloop()
        
    def clear(self):
        pass

#------------------------------------------------------------------------
# TreeViewPanel
#------------------------------------------------------------------------
class TreeViewPanel:
    def __init__(self):
        self.data = []
        pass

    def setup(self):
        pass

    def clear(self):
        pass
    
#------------------------------------------------------------------------
# UserPanel
#------------------------------------------------------------------------

#------------------------------------------------------------------------
# MessagePanel
#------------------------------------------------------------------------

#------------------------------------------------------------------------
# DisplayPanel
#------------------------------------------------------------------------
