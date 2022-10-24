#------------------------------------------------------------------------
# ipcat: gui.py
#------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

#------------------------------------------------------------------------
# MainWindow
#------------------------------------------------------------------------
class MainWindow(ttk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Image Processing Square')
        self.root.geometry('1000x600')
        self.root.minsize(width=500, height=400)
        #
        super().__init__(self.root, width=1000, height=600, style='main.TFrame')
        self.pack(expand=True, fill=tk.BOTH)
        self.setup()
        
    def setup(self):
        #
        #
        self.initialized = True
        pass

    def clear(self):
        pass

#------------------------------------------------------------------------
# FieldEntryPanel
#------------------------------------------------------------------------
class FieldEntryPanel(ttk.Frame):
    def __init__(self, fieldName):
        self.fieldName = fieldName

    pass
#------------------------------------------------------------------------
# EntryButtonPanel
#------------------------------------------------------------------------
class EntryButtonPanel(ttk.Frame):
    def __init__(self, parent, buttonText):
        super().__init__(parent)
        self.buttonText = buttonText
        self.build()
        
    def build(self, parent):
        entry = ttk.Entry(self)
        button = ttk.Button(self, self.buttonText)
        entry.pack()
        button.pack()
        pass
    pass

#------------------------------------------------------------------------
# UserInputPanel
#------------------------------------------------------------------------
class UserInputPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build()
        
    def build(self):
        openFile = ttk.Button(self, text='Open file')
        treeView = ttk.Treeview(self)
        openFile.pack(anchor=tk.NW)
        treeView.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
        pass
    pass

#------------------------------------------------------------------------
# UserControlPanel
#------------------------------------------------------------------------
class UserControlPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build()
        
    def build(self):
        notebook = ttk.Notebook(self, width=400)
        notebook.pack(expand=True, fill=tk.BOTH)
        frame1 = ttk.Frame(notebook)
        frame1.pack(expand=True, fill=tk.BOTH)
        notebook.add(frame1, text='Image analysis')
        pass
    pass

#------------------------------------------------------------------------
# MessagePanel
#------------------------------------------------------------------------
class MessagePanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def build(self):
        pass
    pass

#------------------------------------------------------------------------
# DisplayPanel
#------------------------------------------------------------------------
class DisplayPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH)
        frame = ttk.Frame(notebook, style='Blue.TFrame', width=200)
        frame.pack(expand=True, fill=tk.BOTH)
        notebook.add(frame, text='Default display')


