from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess
import numpy as np

class CanvasUploader(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel("upload time"))


        
        self.setLayout(self.layout)
    



   

