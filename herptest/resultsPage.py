from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess, csv, math
import numpy as np


class ResultsTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        QtCore.QAbstractTableModel.__init__(self)
        self.loadData(data)

    def loadData(self, data):
        if len(data) > 1:
            self.headers = data[0]
            self.dataDict = data[1:]
        else:
            self.headers = ["No Data"]
            self.dataDict = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.dataDict)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.headers)

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        else:
            return "{}".format(section)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == QtCore.Qt.DisplayRole:
            return self.dataDict[row][column]

        elif role == QtCore.Qt.BackgroundRole:
            return QtGui.QColor(QtCore.Qt.white)
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignRight

        return None

class StatsModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None):
        QtCore.QAbstractTableModel.__init__(self)
        self.calculateStats(data)
        self.headers = ["Test Statistics", ""]

    def calculateStats(self, data):
        self.dataDict = []
        if len(data) > 1:
            scores = [float(entry[2]) for entry in data[1:]]    
            self.dataDict.append(["Mean score", np.mean(scores)])
            self.dataDict.append(["Median score", np.median(scores)])
            self.dataDict.append(["Q1", np.percentile(scores, 25)])
            self.dataDict.append(["Q3", np.percentile(scores, 50)])
            self.dataDict.append(["Standard Deviation", np.std(scores)])
            for item in self.dataDict:
                item[1] = "{:.2f}".format(item[1])
        else:
            self.dataDict.append(["No Data", ""])

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.dataDict)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None
        if orientation == QtCore.Qt.Horizontal:
            return self.headers[section]
        else:
            return ""

    def data(self, index, role=QtCore.Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == QtCore.Qt.DisplayRole:
            return self.dataDict[row][column]

        elif role == QtCore.Qt.BackgroundRole:
            return QtGui.QColor(QtCore.Qt.white)
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignRight

        return None

class ResultsPage(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        

        data = []

        self.model = ResultsTableModel(data)
        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.model)

        self.horizontalHeader = self.tableView.horizontalHeader()
        self.verticalHeader = self.tableView.verticalHeader()
        self.horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalHeader.setStretchLastSection(True)

        self.statsModel = StatsModel(data)
        self.statsView = QtWidgets.QTableView()
        self.statsView.setModel(self.statsModel)

        self.statsHeader = self.statsView.horizontalHeader()
        self.statsHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tableView)
        self.layout.addWidget(self.statsView)

        self.setLayout(self.layout)
    



    def loadResults(self, resultsPath, raiseFunc, raiseArgs):
        #TODO: load data here

        data = []
        with open(resultsPath, newline='') as resultsFile:
            fileReader = csv.reader(resultsFile, delimiter=',')
            for row in fileReader:
                data.append(row)



        self.model = ResultsTableModel(data)
        self.tableView.setModel(self.model)

        self.statsModel = StatsModel(data)
        self.statsView.setModel(self.statsModel)
        

        raiseFunc(raiseArgs)

