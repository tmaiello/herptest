from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess

class ResultsPage(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(10,30,10,10)

        self.layout.addWidget(QtWidgets.QLabel("Test results go here"))


        self.setLayout(self.layout)
    
    def loadResults(self, raiseFunc, raiseArgs):
        #TODO: load data here

        raiseFunc(raiseArgs)

