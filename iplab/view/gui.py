import tkinter as tk
from tkinter import ttk
import sddgen
from .guiComponents import addScrollBars, GalleryPanel

class ParameterEntry(ttk.Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.buildGui()
    pass

  def buildGui(self):
    # create subcomponents of ParameterEntry
    self.name = ttk.Entry(self)
    self.value = ttk.Entry(self)
    self.slider = ttk.Slider(self)
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
    self.File = tk.Menu(menuBar, tearoff=False)
    self.Test = tk.Menu(menuBar, tearoff=False)
    menuBar.add_cascade(label="File", menu=self.File)
    menuBar.add_cascade(label="Test", self.menu=Test)

    # create subcomponents of File
    self.File.add_command(label="Open")
    self.File.add_command(label="Quit")

    # create subcomponents of Test
    self.Test.add_command(label="Test1")
    self.Test.add_command(label="Test2")
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
    self.menuBar = MenuBar(self)
    self.hbox1 = ttk.PanedWindow(self, orient=tk.HORIZONTAL,height=500)
    self.footer = ttk.Label(self,text="Footer")
    self.hbox1.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    self.footer.pack(fill=tk.X,side=tk.BOTTOM)

    # create subcomponents of hbox1
    self.scrollableList = ttk.Frame(hbox1)
    self.vbox1 = ttk.PanedWindow(hbox1, orient="vertical",width=300)
    self.vbox2 = ttk.PanedWindow(hbox1, orient=tk.VERTICAL)
    self.vbox1.pack(fill=tk.BOTH,side=tk.LEFT,expand=True)
    self.hbox1.add(self.scrollableList)
    self.hbox1.add(self.vbox1)
    self.hbox1.add(self.vbox2)

    # create subcomponents of scrollableList
    self.listPanel = ttk.Treeview(self.scrollableList)
    self.scrollableList.rowconfigure(0, weight=1)
    self.scrollableList.columnconfigure(0, weight=1)
    addScrollBars(self.listPanel, self.scrollableList, True, True)
    self.listPanel.grid(row=0,column=0,sticky=tk.NSEW)

    # create subcomponents of vbox1
    self.imagePanel = ttk.Labelframe(vbox1)
    self.eanalysisPanel = ttk.Labelframe(vbox1)
    self.imagePanel.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    self.analysisPanel.pack(fill=tk.X,expand=True)
    self.vbox1.add(self.imagePanel)
    self.vbox1.add(self.analysisPanel)

    # create subcomponents of imagePanel
    self.imageCanvasFrame = ttk.Frame(imagePanel)
    self.showButton = ttk.Button(imagePanel)
    self.imageCanvasFrame.pack(fill=tk.BOTH,expand=True)
    self.showButton.pack(fill=tk.X,expand=False)

    # create subcomponents of imageCanvasFrame
    self.imageCanvas = tk.Canvas(self.imageCanvasFrame)
    self.imageCanvasFrame.rowconfigure(0, weight=1)
    self.imageCanvasFrame.columnconfigure(0, weight=1)
    addScrollBars(self.imageCanvas, self.imageCanvasFrame, True, True)
    self.imageCanvas.grid(row=0,column=0,sticky=tk.NSEW)

    # create subcomponents of analysisPanel
    self.selection = ttk.Combobox(self.analysisPanel)
    self.runButton = ttk.Button(self.analysisPanel)
    self.propertiesFrame = PropertyGridFrame(self.analysisPanel)
    self.selection.pack(fill=tk.X,anchor=tk.NW)
    self.runButton.pack(anchor=tk.NW)
    self.propertiesFrame.pack(fill=tk.X,anchor=tk.NW,expand=True)

    # create subcomponents of vbox2
    self.galleary = GalleryPanel(self.vbox2,width=300,style="r.TFrame")
    self.messagePanel = ttk.Frame(self.vbox2,style="g.TFrame")
    self.gallery.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    self.messagePanel.pack(fill=tk.BOTH,side=tk.TOP,expand=True)
    self.vbox2.add(self.gallery)
    self.vbox2.add(self.messagePanel)
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
