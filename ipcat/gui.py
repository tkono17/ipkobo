#------------------------------------------------------------------------
# ipcat: gui.py
# -------------
# - menuBar: ttk.Menubar
# - columns: ttk.Panedwindow
#   - listPanel: ttk.Frame
#     - imageList: ttk.Treeview
#   - workPanel: ttk.Panedwindow
#     - imagePanel: ttk.Frame
#     - analysisPanel: AnalysisPanel
#       - title: ttk.Label
#       - selection: ttk.Combobox
#       - properties: ttk.Treeview
#         - table: ttk.Treeview
#   - outputPanel: ttk.Panedwindow
#     - galleryPanel: GalleryPanel
#     - messagePanel: ttk.Text
#------------------------------------------------------------------------
import functools
import logging
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from .guiComponents import *
from .analysis import *

logger = logging.getLogger(__name__)

def initTk():
    root = tk.Tk()
    root.title('Image Processing Square')
    root.geometry('1000x600')
    root.minsize(width=500, height=400)
    return root

#------------------------------------------------------------------------
# MainWindow
#------------------------------------------------------------------------
class MainWindow(ttk.Frame):
    def __init__(self, view):
        self.view = view
        self.model = view.model
        self.root = initTk()
        self.setStyle()
        super().__init__(self.root, width=1000, height=600, style='main.TFrame')
        #
        self.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        #
        self.menuBar = None
        # Left
        self.imageList = None
        # Middle
        self.imagePanel = None
        self.analysisPanel = None
        # Right
        self.galleryPanel = None
        self.messagePanel = None

        self.buildGui()

    def setStyle(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='darkgreen')
        style.configure('main.TFrame', background='blue')
        style.configure('panel.TFrame', background='lightgreen')#(32, 32, 190))
        style.configure('canvas.TFrame', background='yellow')
        #style.configure('TButton', background=(32, 32, 50))
        #style.configure('ImageList.Treeview', rowHeight=100)
        style.configure('TLabelframe', background='blue')
        pass
    
    # GUI building
    def buildGui(self):
        self.buildMenu(self)
        #
        columns = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        columns.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        listPanel = ttk.Frame(columns)
        workPanel = ttk.Panedwindow(columns, orient=tk.VERTICAL)
        outputPanel = ttk.Panedwindow(columns, orient=tk.VERTICAL)
        listPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        workPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        outputPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        columns.add(listPanel, weight=1)
        columns.add(workPanel, weight=2)
        columns.add(outputPanel, weight=2)
        #
        self.buildListPanel(listPanel)
        self.buildWorkPanel(workPanel)
        self.buildOutputPanel(outputPanel)
        
    def buildMenu(self, parent):
        menuBar = tk.Menu(parent)
        self.root.config(menu=menuBar)
        #
        file_menu = tk.Menu(menuBar, tearoff=False)
        menuBar.add_cascade(label='File', menu=file_menu, underline=0)
        file_menu.add_command(label='Open', command=self.view.onOpenImageList)
        file_menu.add_command(label='Quit', command=self.cleanup)
        #
        test_menu = tk.Menu(menuBar, tearoff=False)
        test_menu.add_command(label='BasicTest'
                              #command=functools.partial(self.handlers.runTest, 'BasicTest')
                              )
        menuBar.add_cascade(label='Test', menu=test_menu)#, underline=0)

    def buildInputImageFrame(self, parent):
        pass
    
    def buildParametersPanel(self, parent):
        pass
    
    def buildListPanel(self, parent):
        columns = ('name', 'path', 'width', 'height', 'xOffset', 'yOffset')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=100)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        tree.grid(row=0, column=0, sticky=tk.N+tk.EW)
        addScrollBars(tree, parent, True, True)
        tree.heading('name', text='Name')
        tree.heading('path', text='Path')
        tree.heading('width', text='W')
        tree.heading('height', text='H')
        tree.heading('xOffset', text='X offset')
        tree.heading('yOffset', text='Y offset')
        tree.column('name', minwidth=50, width=100)
        tree.column('path', minwidth=50, width=100)
        tree.column('width', minwidth=50, width=50)
        tree.column('height', minwidth=50, width=50)
        tree.column('xOffset', minwidth=50, width=50)
        tree.column('yOffset', minwidth=50, width=50)
        self.imageList = tree
        
    def buildWorkPanel(self, parent):
        imagePanel = ttk.LabelFrame(parent, text='Image to analyze')
        imagePanel.pack(anchor=tk.NW, fill=tk.BOTH, expand=True)
        showButton = ttk.Button(imagePanel, text='Show selected image(s)')
        showButton.pack(anchor=tk.NW)
        showButton.bind('<Button-1>', self.view.onShowImagesClicked)
        canvas = tk.Canvas(imagePanel, bg='orange')
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        analysisPanel = AnalysisPanel(parent, self.view.analysisList)
        analysisPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        parent.add(imagePanel)
        parent.add(analysisPanel)
        analysisPanel.selection.bind('<<ComboboxSelected>>', self.view.onAnalysisSelected)
        analysisPanel.runButton.bind('<Button-1>', self.view.onRunClicked)
        self.imagePanel = imagePanel
        self.analysisPanel = analysisPanel
        self.canvas = canvas
        
    def buildOutputPanel(self, parent):
        galleryPanel = GalleryPanel(parent)
        galleryPanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.galleryPanel = galleryPanel
        #
        messagePanel = tk.Text(parent)
        messagePanel.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        parent.add(galleryPanel)
        parent.add(messagePanel)
        pass

    def cleanup(self):
        logger.info('Quit gui')
        
