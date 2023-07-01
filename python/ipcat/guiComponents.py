#------------------------------------------------------------------------
# ipcat: GUI components
#------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk

from .common import cdata

#------------------------------------------------------------------------
# AnalysisPanel
#------------------------------------------------------------------------
class AnalysisPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = ttk.Label(self, text='Analysis')
        self.title.pack(side=tk.TOP, fill=tk.X)
        self.selection = ttk.Combobox(self, values=['One', 'Two', 'Three'])
        self.selection.pack(side=tk.TOP, fill=tk.X)
        self.properties = ttk.LabelFrame(self, text='Properties')
        self.properties.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.properties.rowconfigure(0, weight=1)
        self.properties.columnconfigure(0, weight=10)

        self.table = ttk.Treeview(self.properties)
        #self.table = tk.Text(self.properties, height=10)
        self.table.grid(row=0, column=0, sticky=tk.N+tk.EW)
        yscrollbar = ttk.Scrollbar(self.properties,
                                   orient='vertical',
                                   command=self.table.yview)
        self.table['yscrollcommand'] = yscrollbar.set
        yscrollbar.grid(row=0, column=1, sticky=tk.NS)
        xscrollbar = ttk.Scrollbar(self.properties,
                                   orient=tk.HORIZONTAL, 
                                   command=self.table.xview)
        self.table['xscrollcommand'] = xscrollbar.set
        xscrollbar.grid(row=1, column=0, sticky=tk.EW)

#------------------------------------------------------------------------
# FieldEntryPanel
#------------------------------------------------------------------------
class FieldEntryPanel(ttk.Frame):
    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.name = name
        self.value = value
        self.build()
        
    def build(self):
        x1 = ttk.Label(self, text=self.name, width=15)
        x2 = ttk.Entry(self, text=self.value)
        x1.pack(side=tk.LEFT)
        x2.pack(side=tk.LEFT, fill=tk.X, expand=True)
    pass

#------------------------------------------------------------------------
# EntryButtonPanel
#------------------------------------------------------------------------
class EntryButtonPanel(ttk.Frame):
    def __init__(self, parent, buttonText):
        super().__init__(parent)
        self.buttonText = buttonText
        self.build()
        
    def build(self):
        entry = ttk.Entry(self)
        button = ttk.Button(self, self.buttonText, width=20)
        entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button.pack(side=tk.LEFT)
        pass
    pass

class ComboEntryPanel(ttk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.build(text)
        
    def build(self, text):
        cbox = ttk.Combobox(self, width=20)
        entry = ttk.Entry(self, text)
        cbox.pack(side=tk.LEFT)
        entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.comboBox = cbox
        self.entry = entry
        pass
    pass

#------------------------------------------------------------------------
# ImageControlPanel
#------------------------------------------------------------------------
class ImageControlPanel(ttk.Frame):
    def __init__(self, panel, analysis):
        super().__init__(panel, style='P1.TFrame')
        self.analysis = analysis
        self.comboEntries = []
        self.parameters = {}
        self.build()

    def build(self):
        n = self.analysis.nInputImages
        print('ImageControlPanel n = %d' % n)
        self.comboEntries.clear()
        self.parameters.clear()
        #
        if n >= 1 and n <= 10:
            for i in range(n):
                text = ''
                if len(self.analysis.inputImages)>i:
                    text = self.analysis.inputImages[i].name
                x = ComboEntryPanel(self, text)
                x.pack(anchor=tk.NW, fill=tk.X)#, expand=True)
                print('Add combobox')
                self.comboEntries.append(x)
        for k, v in self.analysis.parameters.items():
            x1 = FieldEntryPanel(self, k, str(v))
            x1.pack(side=tk.TOP, fill=tk.X)#, expand=True)
            print('Add parameter field')
            self.parameters[k] = v
        #
        run = ttk.Button(self, text='Run', width=10)
        run.pack(side=tk.LEFT, expand=True)

    pass
