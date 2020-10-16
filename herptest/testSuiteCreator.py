from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess

class TestSuiteCreator(QtWidgets.QWidget):

    class TestCase(QtWidgets.QWidget):
        def __init__(self, name, defaultTestValue):
            super().__init__()
            self.layout = QtWidgets.QHBoxLayout()

            self.left = QtWidgets.QVBoxLayout()
            self.right = QtWidgets.QVBoxLayout()
            self.inputTitle = QtWidgets.QLabel("Enter input for test case:")
            self.inputTitle.setFixedHeight(30)
            self.outputTitle = QtWidgets.QLabel("Enter output for test case:")
            self.outputTitle.setFixedHeight(30)
            self.inputText = QtWidgets.QPlainTextEdit()
            self.outputText = QtWidgets.QPlainTextEdit()
            self.left.addWidget(self.outputTitle)
            self.left.addWidget(self.outputText)
            self.right.addWidget(self.inputTitle)
            self.right.addWidget(self.inputText)

            self.layout.addLayout(self.left)
            self.layout.addLayout(self.right)

            self.setLayout(self.layout)

            self.name = name
            self.points = defaultTestValue

    def __init__(self, defaultTestValue=10):
        super().__init__()

        self.defaultTestValue = defaultTestValue

        self.containerLayout = QtWidgets.QVBoxLayout()
        self.containerLayout.setContentsMargins(0,0,0,0)
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)
        self.createMenuBar()
        self.setActiveLanguage("Python")
        
        self.createTestCaseContainer()

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
        #make sure that the current test case gets updated
        self.testCaseStack.widget(self.testCaseStack.currentIndex()).points = self.testCasePoints.value()

        total = 0
        for index in range(0, self.testCaseStack.count()-1):
            total += self.testCaseStack.widget(index).points
        self.totalPoints.setText(str(total) + " Total Points | " + str(self.testCaseStack.count()-1) + " test cases")
        

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
        self.testCaseComboBox.setFixedWidth(300)
        for i in range(0,3):
            title = "Test Case " + str(i)
            self.testCaseStack.addWidget(self.TestCase(title, self.defaultTestValue))
            self.testCaseComboBox.addItem(title)
        self.testCaseComboBox.activated[int].connect(self.changeTestCase)
        self.testCaseComboBox.addItem("+ Add Test Case")
        self.nullTestCase = QtWidgets.QLabel('Click "Add Test Case" to get started')
        self.testCaseStack.addWidget(self.nullTestCase)
        self.layout.setAlignment(self.nullTestCase, QtCore.Qt.AlignCenter)

        self.testCasePointsLabel = QtWidgets.QLabel("Points:")
        self.testCasePointsLabel.setFixedWidth(50)
        self.testCasePoints = QtWidgets.QSpinBox()
        self.testCasePoints.setValue(self.defaultTestValue)
        self.testCasePoints.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.testCasePoints.valueChanged.connect(self.updateTotalPoints)
        self.testCasePoints.setRange(0,999999)
        self.testCasePoints.setFixedWidth(50)
        self.testCaseRename = QtWidgets.QPushButton("Rename Test Case")
        self.testCaseRename.setFixedWidth(120)
        self.testCaseRename.clicked.connect(lambda: self.renameTestCase(self.testCaseStack.currentIndex()))

        self.testCaseRemove = QtWidgets.QPushButton("Delete Test Case")
        self.testCaseRemove.setFixedWidth(120)
        self.testCaseRemove.clicked.connect(lambda: self.removeTestCase(self.testCaseStack.currentIndex()))


        self.testCaseControls = QtWidgets.QHBoxLayout()
        self.testCaseControls.setContentsMargins(10,20,10,0)
        self.testCaseControls.addWidget(self.testCaseComboBox)
        self.testCaseControls.addSpacing(10)
        self.testCaseControls.addWidget(self.testCasePointsLabel)
        self.testCaseControls.addWidget(self.testCasePoints)
        self.testCaseControls.addSpacing(10)
        self.testCaseControls.addWidget(self.testCaseRename)
        self.testCaseControls.addSpacing(10)
        self.testCaseControls.addWidget(self.testCaseRemove)
        self.testCaseControls.addStretch(10)
        self.layout.addLayout(self.testCaseControls)

        self.layout.addWidget(self.testCaseStack)

    def changeTestCase(self, index):
        if index == self.testCaseComboBox.count()-1:
            self.addTestCase()
        else:
            self.testCaseComboBox.setCurrentIndex(index)
            self.testCaseStack.setCurrentIndex(index)
            self.testCasePoints.setValue(self.testCaseStack.widget(index).points)



    def addTestCase(self):
        self.testCaseRemove.setEnabled(True) #since we keep at least 1 real test case around at all times
        self.testCaseStack.insertWidget(self.testCaseStack.count()-1, self.TestCase("New Test Case", self.defaultTestValue))
        self.testCaseComboBox.insertItem(self.testCaseComboBox.count()-1, "New Test Case")
        self.changeTestCase(self.testCaseStack.count()-2)
        self.updateTotalPoints()


    def removeTestCase(self, index):

        target = self.testCaseStack.widget(index)
        self.testCaseStack.removeWidget(target)
        
        self.testCaseComboBox.removeItem(index)
        self.updateTotalPoints()
        
        if self.testCaseComboBox.currentIndex() == self.testCaseComboBox.count()-1:
            self.changeTestCase(self.testCaseComboBox.currentIndex()-1)


        if self.testCaseStack.count() == 2:
            #we just deleted the penultimate real test case, make sure that the remaining one is selected
            self.changeTestCase(0)

            #also disable deletion until we get 2 real test cases
            self.testCaseRemove.setEnabled(False)


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
        print("save test suite, saveAs= " + str(saveAs))
        #TODO implement saving the test suite

    def closeTestSuite(self):
        print("close test suite")
        #TODO implement closing test suite and prompting to save if changes have been made
        self.updateBreadcrumb("No directory selected")
