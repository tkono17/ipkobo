import tkinter as tk
from tkinter import ttk
import sddgen
from .guiComponents import *

class ParameterEntry(ttk.Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.buildGui()
    pass

  def buildGui(self):
    # create subcomponents of ParameterEntry
    name = ttk.Entry(self)
    self.name = name
    value = ttk.Entry(self)
    self.value = value
    slider = ttk.Slider(self)
    self.slider = slider
    pass

class MenuBar(tk.Menu):
  def __init__(self, parent):
    super().__init__(parent)
    self.buildGui()
    pass

  def buildGui(self):
    root = self.master.master
    menuBar = self
    root.config(menu=self)
    self.menuBar = menuBar
    # create subcomponents of MenuBar
    File = tk.Menu(menuBar, tearoff=False)
    menuBar.add_cascade(label="File", menu=File)
    self.File = File
    Test = tk.Menu(menuBar, tearoff=False)
    menuBar.add_cascade(label="Test", menu=Test)
    self.Test = Test

    # create subcomponents of File
    File.add_command(label="Open")
    File.add_command(label="Quit")

    # create subcomponents of Test
    Test.add_command(label="Test1")
    Test.add_command(label="Test2")
    pass

class MainWindow(ttk.Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.root = parent
    self.buildGui()
    self.pack(fill=tk.BOTH, expand=True)
    pass

  def buildGui(self):
    # create subcomponents of MainWindow
    menuBar = MenuBar(self)
    self.menuBar = menuBar
    hbox1 = ttk.PanedWindow(self, orient=tk.HORIZONTAL,height=500)
    self.hbox1 = hbox1
    footer = ttk.Label(self,text="Footer")
    self.footer = footer
    hbox1.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    footer.pack(fill=tk.X,side=tk.BOTTOM)

    # create subcomponents of hbox1
    scrollableList = ttk.Frame(hbox1)
    self.scrollableList = scrollableList
    vbox1 = ttk.PanedWindow(hbox1, orient="vertical",width=300)
    self.vbox1 = vbox1
    vbox2 = ttk.PanedWindow(hbox1, orient=tk.VERTICAL)
    self.vbox2 = vbox2
    vbox1.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
    hbox1.add(scrollableList)
    hbox1.add(vbox1)
    hbox1.add(vbox2)

    # create subcomponents of scrollableList
    listPanel = ttk.Treeview(scrollableList)
    self.listPanel = listPanel
    scrollableList.rowconfigure(0, weight=1)
    scrollableList.columnconfigure(0, weight=1)
    sddgen.guitk.addScrollBars(listPanel, scrollableList, True, True)
    listPanel.grid(row=0,column=0,sticky=tk.NSEW)

    # create subcomponents of vbox1
    imagePanel = ttk.Labelframe(vbox1)
    self.imagePanel = imagePanel
    analysisPanel = ttk.Labelframe(vbox1)
    self.analysisPanel = analysisPanel
    imagePanel.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    analysisPanel.pack(fill=tk.X,expand=True)
    vbox1.add(imagePanel)
    vbox1.add(analysisPanel)

    # create subcomponents of imagePanel
    imageCanvasFrame = ttk.Frame(imagePanel)
    self.imageCanvasFrame = imageCanvasFrame
    showButton = ttk.Button(imagePanel)
    self.showButton = showButton
    imageCanvasFrame.pack(fill=tk.BOTH,expand=True)
    showButton.pack(fill=tk.X,expand=False)

    # create subcomponents of imageCanvasFrame
    imageCanvas = tk.Canvas(imageCanvasFrame)
    self.imageCanvas = imageCanvas
    imageCanvasFrame.rowconfigure(0, weight=1)
    imageCanvasFrame.columnconfigure(0, weight=1)
    sddgen.guitk.addScrollBars(imageCanvas, imageCanvasFrame, True, True)
    imageCanvas.grid(row=0,column=0,sticky=tk.NSEW)

    # create subcomponents of analysisPanel
    selection = ttk.Combobox(analysisPanel)
    self.selection = selection
    runButton = ttk.Button(analysisPanel)
    self.runButton = runButton
    propertiesFrame = PropertyGridFrame(analysisPanel)
    self.propertiesFrame = propertiesFrame
    selection.pack(fill=tk.X,anchor=tk.NW)
    runButton.pack(anchor=tk.NW)
    propertiesFrame.pack(fill=tk.X,anchor=tk.NW,expand=True)

    # create subcomponents of vbox2
    gallery = sddgen.guitk.GalleryPanel(vbox2,width=300,style="r.TFrame")
    self.gallery = gallery
    messagePanel = ttk.Frame(vbox2,style="g.TFrame")
    self.messagePanel = messagePanel
    gallery.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    messagePanel.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    vbox2.add(gallery)
    vbox2.add(messagePanel)
    pass

if __name__ == "__main__":
  root = tk.Tk()
  root.title("Ipcat application")
  root.geometry("1000x700")
  style = ttk.Style()
  style.configure("r.TFrame", background="red")
  style.configure("g.TFrame", background="green")
  style.configure("b.TFrame", background="blue")
  mainWindow = MainWindow(root)
  root.mainloop()
