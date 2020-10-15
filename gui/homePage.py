from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess

class HomePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(10,30,10,10)

        self.createProjectPicker()
        self.createTestSuitePicker()
        self.createTestOutputFields()

        self.setLayout(self.layout)

    def createProjectPicker(self):
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

    def createTestSuitePicker(self):
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

    def createTestOutputFields(self):
        self.outputFields = QtWidgets.QVBoxLayout()
        self.outputLabel = QtWidgets.QLabel("Test Output:")
        self.outputLabel.setMaximumHeight(50)
        self.outputFields.addWidget(self.outputLabel)

        self.outputBox = QtWidgets.QPlainTextEdit()
        self.outputBox.setReadOnly(True)
        self.outputFields.addWidget(self.outputBox)
        
        self.runTests = QtWidgets.QPushButton("Run tests")
        self.runTests.setFixedHeight(50)
        self.runTests.setFixedWidth(100)
        self.runTests.clicked.connect(self.runTestSuite)
        self.outputFields.addWidget(self.runTests)
        self.outputFields.setAlignment(self.runTests, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.layout.addLayout(self.outputFields)

    def runTestSuite(self):
        print("Running test suite from: \n" + self.testSuitePath.text())
        print("on projects from: \n" + self.projectPath.text())

        #TODO: linkage
        command = ['ping', '-c 4', 'python.org']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        self.outputBox.clear()
        self.outputBox.appendPlainText("$ " + " ".join(command))
        self.outputBox.repaint()
        while True:
            output = process.stdout.readline()
            #print(output.strip())
            self.outputBox.appendPlainText(output.strip())
            self.outputBox.repaint()
            # Do something else
            return_code = process.poll()
            if return_code is not None:
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    #print(output.strip())
                    self.outputBox.appendPlainText(output.strip())
                    self.outputBox.repaint()
                break
        