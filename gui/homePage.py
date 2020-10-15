from PySide2 import QtCore, QtWidgets, QtGui
import os

class HomePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(10,30,10,10)

        self.projectPicker = QtWidgets.QGridLayout()
        self.projectLabel = QtWidgets.QLabel("Path to folder containing projects:")
        self.projectLabel.setMaximumHeight(50)
        self.projectPath = QtWidgets.QLineEdit(os.getcwd())#TODO get a better default
        self.projectPath.setFixedWidth(500)
        self.projectSelect = QtWidgets.QPushButton("Browse")
        self.projectSelect.setFixedWidth(100)
        self.projectSelect.clicked.connect(self.projectFilePicker)

        self.projectPicker.addWidget(self.projectLabel,0,0)
        self.projectPicker.addWidget(self.projectPath,1,0)
        self.projectPicker.addWidget(self.projectSelect,1,1)
        self.layout.addLayout(self.projectPicker)
        self.layout.setAlignment(self.projectPicker, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.testSuitePicker = QtWidgets.QGridLayout()
        self.testSuiteLabel = QtWidgets.QLabel("Path to folder containing test suite:")
        self.testSuiteLabel.setMaximumHeight(50)
        self.testSuitePath = QtWidgets.QLineEdit(os.getcwd())#TODO get a better default
        self.testSuitePath.setFixedWidth(500)
        self.testSuiteSelect = QtWidgets.QPushButton("Browse")
        self.testSuiteSelect.setFixedWidth(100)
        self.testSuiteSelect.clicked.connect(self.testSuiteFilePicker)
        
        self.testSuitePicker.addWidget(self.testSuiteLabel,0,0)
        self.testSuitePicker.addWidget(self.testSuitePath,1,0)
        self.testSuitePicker.addWidget(self.testSuiteSelect,1,1)
        self.layout.addLayout(self.testSuitePicker)
        self.layout.setAlignment(self.testSuitePicker, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)


        self.runTests = QtWidgets.QPushButton("Run tests")
        self.runTests.setFixedHeight(50)
        self.runTests.setFixedWidth(100)
        self.layout.addWidget(self.runTests)
        self.layout.setAlignment(self.runTests, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)

        self.setLayout(self.layout)

    def projectFilePicker(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setWindowTitle("Select Project Directory")
        dialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
        dialog.setDirectory(self.projectPath.text())

        if dialog.exec_():
            self.projectPath.setText(dialog.selectedFiles()[0])

    def testSuiteFilePicker(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setWindowTitle("Select Test Suite Directory")
        dialog.setOptions(QtWidgets.QFileDialog.ShowDirsOnly)
        dialog.setDirectory(self.testSuitePath.text())

        if dialog.exec_():
            self.testSuitePath.setText(dialog.selectedFiles()[0])
