from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess, json

class TestSuiteCreator(QtWidgets.QWidget):

    class TestCase(QtWidgets.QWidget):
        def __init__(self, name, defaultTestValue, defaultMatchType, defaultStartToken, defaultEndToken):
            super().__init__()
            self.layout = QtWidgets.QHBoxLayout()
            self.textBox = QtWidgets.QVBoxLayout()
            self.inputTitle = QtWidgets.QLabel("Enter input for test case (separate inputs with newline):")
            self.inputTitle.setFixedHeight(30)
            self.inputText = QtWidgets.QPlainTextEdit()
            self.textBox.addWidget(self.inputTitle)
            self.textBox.addWidget(self.inputText)
            self.layout.addLayout(self.textBox)
            self.setLayout(self.layout)
            self.name = name
            self.points = defaultTestValue
            self.matchType = defaultMatchType
            self.startToken = defaultStartToken
            self.endToken = defaultEndToken

    def __init__(self, defaultTestValue=10, defaultMatchType=0, defaultStartToken=0, defaultEndToken=0):
        super().__init__()

        self.defaultTestValue = defaultTestValue
        self.defaultMatchType = defaultMatchType
        self.defaultStartToken = defaultStartToken
        self.defaultEndToken = defaultEndToken

        self.containerLayout = QtWidgets.QVBoxLayout()
        self.containerLayout.setContentsMargins(0,0,0,0)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)
        self.createMenuBar()
        self.setActiveLanguage("Python")
        
        self.createTestCaseContainer()
        
        self.generateTestSuiteContainer()

        self.containerLayout.addLayout(self.layout)
        self.createBreadcrumb()
        self.setLayout(self.containerLayout)

    def createBreadcrumb(self):
        self.breadcrumbBar = QtWidgets.QStatusBar()
        self.breadcrumb = QtWidgets.QLabel()

        self.totalPoints = QtWidgets.QLabel()
        self.breadcrumbBar.addPermanentWidget(self.totalPoints)

        self.breadcrumbBar.setStyleSheet("background-color:#dddddd")
        self.breadcrumbBar.setSizeGripEnabled(False)
        self.breadcrumbBar.addWidget(self.breadcrumb)
        self.breadcrumbBar.setFixedHeight(20)
        self.breadcrumbBar.setContentsMargins(5,0,5,0)
        self.containerLayout.addWidget(self.breadcrumbBar)
        self.updateBreadcrumb("No directory selected")
        self.updateTotalPoints()

    def updateBreadcrumb(self, activeDirectory):
        self.activeDirectory = activeDirectory
        self.breadcrumb.setText("Active Test Suite: " + self.activeDirectory)

    def updateTotalPoints(self):
        #make sure that the current test case gets updated, will not call on Add Test Case widget
        if self.testCaseStack.count() != 1:
            self.testCaseStack.widget(self.testCaseStack.currentIndex()).points = self.testCasePoints.value()

        total = 0
        for index in range(0, self.testCaseStack.count()-1):
            total += self.testCaseStack.widget(index).points
        self.totalPoints.setText(str(total) + " Total Points | " + str(self.testCaseStack.count()-1) + " test cases")
        
    def updateMatchType(self, index):
        # match type converted to values used in tests.py on test suite code generation
        self.testCaseStack.widget(self.testCaseStack.currentIndex()).matchType = index
        if index == 1 or index == 2:
            self.startToken.setEnabled(True)
            self.endToken.setEnabled(True)
        else:
            self.startToken.setDisabled(True)
            self.endToken.setDisabled(True)
        

    def updateStartToken(self, token):
        self.testCaseStack.widget(self.testCaseStack.currentIndex()).startToken = token

    def updateEndToken(self, token):
        self.testCaseStack.widget(self.testCaseStack.currentIndex()).endToken = token

    def createMenuBar(self):
        self.menuBar = QtWidgets.QMenuBar()
        self.fileMenu = self.menuBar.addMenu("File")

        self.fileMenuNew = self.fileMenu.addMenu("New Test Suite")
        self.fileMenuNewCPP = self.fileMenuNew.addAction("C++")
        self.fileMenuNewCPP.triggered.connect(lambda: self.newTestSuite("C++"))
        self.fileMenuNewJava = self.fileMenuNew.addAction("Java")
        self.fileMenuNewJava.triggered.connect(lambda: self.newTestSuite("Java"))
        self.fileMenuNewPython = self.fileMenuNew.addAction("Python")
        self.fileMenuNewPython.triggered.connect(lambda: self.newTestSuite("Python"))


        self.fileMenuOpen = self.fileMenu.addAction("Open")
        self.fileMenuOpen.setShortcuts(QtGui.QKeySequence.Open)
        self.fileMenuOpen.triggered.connect(lambda: self.openTestSuite())
        self.fileMenuSave = self.fileMenu.addAction("Save")
        self.fileMenuSave.setShortcuts(QtGui.QKeySequence.Save)
        self.fileMenuSave.triggered.connect(lambda: self.saveTestSuite())
        self.fileMenuSaveAs = self.fileMenu.addAction("Save As")
        self.fileMenuSaveAs.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_S,))
        self.fileMenuSaveAs.triggered.connect(lambda: self.saveTestSuite(saveAs=True))
        self.fileMenuClose = self.fileMenu.addAction("Close")
        self.fileMenuClose.setShortcuts(QtGui.QKeySequence.Close)
        self.fileMenuClose.triggered.connect(lambda: self.closeTestSuite())

        self.editMenu = self.menuBar.addMenu("Edit")
        self.editMenuCut = self.editMenu.addAction("Cut")
        self.editMenuCut.setShortcuts(QtGui.QKeySequence.Cut)
        self.editMenuCut.triggered.connect(lambda: self.handleEditAction("Cut"))
        self.editMenuCopy = self.editMenu.addAction("Copy")
        self.editMenuCopy.setShortcuts(QtGui.QKeySequence.Copy)
        self.editMenuCopy.triggered.connect(lambda: self.handleEditAction("Copy"))
        self.editMenuPaste = self.editMenu.addAction("Paste")
        self.editMenuPaste.setShortcuts(QtGui.QKeySequence.Paste)
        self.editMenuPaste.triggered.connect(lambda: self.handleEditAction("Paste"))

        self.testCaseMenu = self.menuBar.addMenu("Test Cases")
        self.testCaseAdd = self.testCaseMenu.addAction("Add Test Case")
        self.testCaseAdd.triggered.connect(lambda: self.addTestCase())
        self.testCaseRename = self.testCaseMenu.addAction("Rename Test Case")
        self.testCaseRename.triggered.connect(lambda: self.renameTestCase(self.testCaseStack.currentIndex()))
        self.testCaseDelete = self.testCaseMenu.addAction("Delete Test Case")
        self.testCaseDelete.triggered.connect(lambda: self.removeTestCase(self.testCaseStack.currentIndex()))

        self.languageMenu = self.menuBar.addMenu("Language")
        self.languageMenuGroup = QtWidgets.QActionGroup(self.languageMenu)

        self.languageMenuCPP = self.languageMenuGroup.addAction("C++")
        self.languageMenuCPP.setCheckable(True)
        self.languageMenu.addAction(self.languageMenuCPP)
        self.languageMenuJava = self.languageMenuGroup.addAction("Java")
        self.languageMenuJava.setCheckable(True)
        self.languageMenu.addAction(self.languageMenuJava)
        self.languageMenuPython = self.languageMenuGroup.addAction("Python")
        self.languageMenuPython.setCheckable(True)
        self.languageMenu.addAction(self.languageMenuPython)
      
        self.layout.addWidget(self.menuBar)
        self.layout.setAlignment(self.menuBar, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)


    def createTestCaseContainer(self):
        self.testCaseStack =  QtWidgets.QStackedWidget()
        self.testCaseComboBox = QtWidgets.QComboBox()
        self.testCaseComboBox.setFixedWidth(200)
        self.testCaseComboBox.activated[int].connect(self.changeTestCase)
        self.testCaseComboBox.addItem("+ Add Test Case")
        self.nullTestCase = QtWidgets.QLabel('Click "Add Test Case" to get started!')
        self.testCaseStack.addWidget(self.nullTestCase)
        self.layout.setAlignment(self.nullTestCase, QtCore.Qt.AlignCenter)

        self.testCasePointsLabel = QtWidgets.QLabel("Points:")
        self.testCasePointsLabel.setFixedWidth(40)
        self.testCasePoints = QtWidgets.QSpinBox()
        self.testCasePoints.setValue(self.defaultTestValue)
        self.testCasePoints.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.testCasePoints.valueChanged.connect(self.updateTotalPoints)
        self.testCasePoints.setRange(0,999999)
        self.testCasePoints.setFixedWidth(50)
        self.testCasePoints.setDisabled(True)

        self.matchTypeLabel = QtWidgets.QLabel("Match type:")
        self.matchTypeLabel.setFixedWidth(75)
        self.matchTypeComboBox = QtWidgets.QComboBox()
        self.matchTypeComboBox.setFixedWidth(250)
        self.matchTypeComboBox.addItem("Exact Match")
        self.matchTypeComboBox.addItem("Result contains benchmark subset")
        self.matchTypeComboBox.addItem("Result contains benchmark superset")
        self.matchTypeComboBox.activated[int].connect(self.updateMatchType)
        self.matchTypeComboBox.setDisabled(True)

        self.startTokenLabel = QtWidgets.QLabel("Start token:")
        self.startTokenLabel.setFixedWidth(75)
        self.startToken = QtWidgets.QSpinBox()
        self.startToken.setValue(self.defaultStartToken)
        self.startToken.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.startToken.valueChanged.connect(self.updateStartToken)
        self.startToken.setRange(-99999, 99999)
        self.startToken.setFixedWidth(50)
        self.startToken.setDisabled(True)
        
        self.endTokenLabel = QtWidgets.QLabel("End token:")
        self.endTokenLabel.setFixedWidth(70)
        self.endToken = QtWidgets.QSpinBox()
        self.endToken.setValue(self.defaultEndToken)
        self.endToken.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.endToken.valueChanged.connect(self.updateEndToken)
        self.endToken.setRange(-99999, 99999)
        self.endToken.setFixedWidth(50)
        self.endToken.setDisabled(True)

        self.testCaseControls = QtWidgets.QHBoxLayout()
        self.testCaseControls.setContentsMargins(10,20,10,0)
        self.testCaseControls.addWidget(self.testCaseComboBox)
        self.testCaseControls.addSpacing(10)
        self.testCaseControls.addWidget(self.testCasePointsLabel)
        self.testCaseControls.addWidget(self.testCasePoints)
        self.testCaseControls.addSpacing(10)
        self.testCaseControls.addWidget(self.matchTypeLabel)
        self.testCaseControls.addWidget(self.matchTypeComboBox)
        self.testCaseControls.addSpacing(10)
        self.testCaseControls.addWidget(self.startTokenLabel)
        self.testCaseControls.addWidget(self.startToken)
        self.testCaseControls.addWidget(self.endTokenLabel)
        self.testCaseControls.addWidget(self.endToken)

        self.layout.addLayout(self.testCaseControls)

        self.layout.addWidget(self.testCaseStack)

    def generateTestSuiteContainer(self):
        self.generateTestSuiteButton = QtWidgets.QPushButton("Generate Test Suite")
        self.generateTestSuiteButton.setFixedWidth(200)
        self.generateTestSuiteButton.clicked.connect(self.solutionFilePicker)
        self.generateTestSuiteButton.setDisabled(True)
        self.layout.addWidget(self.generateTestSuiteButton)
        self.layout.setAlignment(self.generateTestSuiteButton, QtCore.Qt.AlignRight)
        
    
    def solutionFilePicker(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setWindowTitle("Select Solution Code")
        dialog.setDirectory(os.getcwd()) #TODO get a better default

        if dialog.exec_():
            solutionCodeBaseName = os.path.basename(os.path.normpath(dialog.selectedFiles()[0]))
            self.generateTestSuite(solutionCodeBaseName)

    def generateTestSuite(self, basename):
        data = {}
        data['solution_file'] = basename
        data['test_cases'] = []
        for index in range(0, self.testCaseStack.count()-1):
            testCase = {}
            testCase['test_case_title'] = self.testCaseStack.widget(index).name
            testCase['input_list'] = self.testCaseStack.widget(index).inputText.toPlainText().split("\n")
            testCase['points'] = self.testCaseStack.widget(index).points
            if self.testCaseStack.widget(index).matchType == 2:
                testCase['match_type'] = -1
            else:
                testCase['match_type'] = self.testCaseStack.widget(index).matchType
            testCase['start_token'] = self.testCaseStack.widget(index).startToken
            testCase['end_token'] = self.testCaseStack.widget(index).endToken
            data['test_cases'].append(testCase)
        with open(basename + '_testsuite.json', 'w') as outfile: #TODO figure out where to save this path
            json.dump(data, outfile)

    def changeTestCase(self, index):
        if index == self.testCaseComboBox.count()-1:
            self.addTestCase()
        else:
            self.testCaseComboBox.setCurrentIndex(index)
            self.testCaseStack.setCurrentIndex(index)
            self.testCasePoints.setValue(self.testCaseStack.widget(index).points)
            self.matchTypeComboBox.setCurrentIndex(self.testCaseStack.widget(index).matchType)
            self.startToken.setValue(self.testCaseStack.widget(index).startToken)
            self.endToken.setValue(self.testCaseStack.widget(index).endToken)

    def addTestCase(self):
        dialog, ok = QtWidgets.QInputDialog().getText(self, "Test Case Name", "Enter test case name:", QtWidgets.QLineEdit.Normal) 
        if ok and dialog:
            self.generateTestSuiteButton.setEnabled(True)
            self.testCasePoints.setEnabled(True)
            self.matchTypeComboBox.setEnabled(True)
            self.testCaseStack.insertWidget(self.testCaseStack.count()-1, self.TestCase(dialog, self.defaultTestValue, self.defaultMatchType, self.defaultStartToken, self.defaultEndToken))
            self.testCaseComboBox.insertItem(self.testCaseComboBox.count()-1, dialog)
            self.changeTestCase(self.testCaseStack.count()-2)
            self.updateTotalPoints()
        else:
            #if user cancels, test case switches to last test case -> TODO preserve previous test case instead of defaulting to last?
            if self.testCaseStack.count() > 1:
                self.changeTestCase(self.testCaseStack.count()-2)
            else:
                self.generateTestSuiteButton.setDisabled(True)
                

    def removeTestCase(self, index):

        #TODO add dialog before removing test case for safety

        # prevents deleting Add Test Case item
        if self.testCaseComboBox.count() == 1:
            return

        target = self.testCaseStack.widget(index)
        self.testCaseStack.removeWidget(target)
        self.testCaseComboBox.removeItem(index)
        self.updateTotalPoints()

        if self.testCaseComboBox.count() > 1:
            if self.testCaseComboBox.currentIndex() == self.testCaseComboBox.count()-1:
                self.changeTestCase(self.testCaseComboBox.currentIndex()-1)

            if self.testCaseStack.count() == 2:
                #we just deleted the penultimate real test case, make sure that the remaining one is selected
                self.changeTestCase(0)
        else:
            self.generateTestSuiteButton.setDisabled(True)
            self.testCasePoints.setDisabled(True)
            self.matchTypeComboBox.setDisabled(True)


    def renameTestCase(self, index):

        dialog, ok = QtWidgets.QInputDialog().getText(self, "Rename Test Case", "Enter new name:", QtWidgets.QLineEdit.Normal) 

        if ok and dialog:
            self.testCaseComboBox.setItemText(index, dialog)
            self.testCaseStack.widget(index).name = dialog

    def newTestSuite(self, language):
        print("Creating new test suite for " + language)
        #TODO: linkage

    def setActiveLanguage(self, language):
        if language == "Java":
            self.languageMenuJava.setChecked(True)
        elif language == "Python":
            self.languageMenuPython.setChecked(True)
        elif language == "C++":
            self.languageMenuCPP.setChecked(True)

    def handleEditAction(self, action):
        print("handle action for:" + action)
        #TODO: add implementation for cut, copy, paste

    def openTestSuite(self, path=""):
        print("open test suite")
        #TODO implement opening the test suite
        
        if path == "":
            path = os.getcwd()
            #TODO make this open a file picker instead
        self.updateBreadcrumb(path)

    def saveTestSuite(self, saveAs =False):
        #TODO implement saving test suite
        if(self.testCaseStack.count() == 1):
            #TODO display error message
            return


    def closeTestSuite(self):
        print("close test suite")
        #TODO implement closing test suite and prompting to save if changes have been made
        self.updateBreadcrumb("No directory selected")
