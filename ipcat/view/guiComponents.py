#------------------------------------------------------------------------
# ipcat: guiComponents.py
#------------------------------------------------------------------------
import time
import logging
import tkinter as tk
from tkinter import ttk

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------
# FieldEntryPanel
#------------------------------------------------------------------------
class FieldEntryPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.build()
        
    def build(self):
        x1 = ttk.Label(self, text='Name', width=15)
        x2 = ttk.Entry(self, text='Value')
        x1.pack(side=tk.LEFT)
        x2.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def clear(self):
        pass
    pass

class FieldEntry:
    def __init__(self, parameter):
        self.parameter = parameter
        self.name = parameter.name
        self.value = parameter.value
        self.scaleRange = parameter.drange
        self.choices = parameter.choices
        self.dtype = parameter.dtype

    def createVar(self):
        x = tk.StringVar()
        if type(self.value) == type(''):
            x = tk.StringVar(value=self.value)
        elif type(self.value) == type(1):
            x = tk.IntVar(value=self.value)
        elif type(self.value) == type(1.0):
            x = tk.DoubleVar(value=self.value)
        return x

    def useScale(self):
        return (self.scaleRange != None and len(self.scaleRange)==2)

    def useChoices(self):
        return (self.choices != None)
    
    def scaleMin(self):
        x = None
        if self.useScale():
            x = self.scaleRange[0]
        return x
    
    def scaleMax(self):
        x = None
        if self.useScale():
            x = self.scaleRange[1]
        return x
            
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

class PropertyGridFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style='panel.TFrame')
        self.fields = []
        self.fieldVars = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
    def setFields(self, v):
        self.clear()
        self.fields = v
        self.build()

    def addField(self, field):
        self.fields.append(field)

    def build(self):
        n = len(self.fields)
        c1 = ttk.Label(self, text='Field')
        c2 = ttk.Label(self, text='Value')
        c3 = ttk.Label(self, text='Scale/Choice')
        c1.grid(row=0, column=0, sticky=tk.EW)
        c2.grid(row=0, column=1, sticky=tk.EW)
        c3.grid(row=0, column=2, sticky=tk.EW)
        for i, field in enumerate(self.fields):
            irow = i + 1
            valuestr = field.createVar()
            self.fieldVars[field.name] = valuestr
            label = ttk.Label(self, text=field.name)
            value = ttk.Entry(self, textvariable=valuestr)
            print(f'{field.name}, {field.value}')
            slider = None
            if field.useScale():
                xmin = field.scaleMin()
                xmax = field.scaleMax()
                slider = ttk.Scale(self, from_=xmin, to=xmax,
                                   orient=tk.HORIZONTAL,
                                   command=field.parameter.scaleSet)
            elif field.useChoices():
                slider = ttk.Combobox(self, values=field.choices)
                slider.bind('<<ComboboxSelected>>', field.parameter.itemSelected)
            label.grid(row=irow, column=0, sticky=tk.EW)
            value.grid(row=irow, column=1, sticky=tk.EW)
            if slider:
                slider.grid(row=irow, column=2, sticky=tk.EW)

    def clear(self):
        self.fields.clear()
        self.fieldVars.clear()
        for x in self.winfo_children():
            x.destroy()
        
