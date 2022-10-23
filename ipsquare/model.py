#------------------------------------------------------------------------
# ImageProcessingSquare: model.py
#------------------------------------------------------------------------

from .vmodel import ViewModel

class AppData:
    def __init__(self):
        self.image0 = None
        self.images = []
        self.viewModel = ViewModel()
        pass

