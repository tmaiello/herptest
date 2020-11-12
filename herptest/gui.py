import sys
import time, random, pathlib
from PySide2 import QtCore, QtWidgets, QtGui
from . import homePage, testSuiteCreator, resultsPage, vmPage


        
def initWindow():

    window = QtWidgets.QMainWindow()
    
    tabContainer =  QtWidgets.QTabWidget()

    tabContainer.addTab(homePage.HomePage(), "Run PengTest")
    homePageInst = tabContainer.widget(0)
    tabContainer.addTab(testSuiteCreator.TestSuiteCreator(), "Create Test Suite")
    testSuiteCreatorInst = tabContainer.widget(1)
    tabContainer.addTab(resultsPage.ResultsPage(), "Test Results")
    resultsPageInst = tabContainer.widget(2)
    tabContainer.addTab(vmPage.VmPage(), "VM Config")
    vmPageInst = tabContainer.widget(3)

    #give the home page the funcion to call when the SHOW RESULTS button is clicked
    #pass the function to set the results page as active to the results page so data can load first
    homePageInst.setResultsFunction(resultsPageInst.loadResults, (tabContainer.setCurrentWidget, resultsPageInst))


    tabList = ["ELMA Config", "Canvas CSV Upload"]
    for t in tabList:
        tabContainer.addTab(QtWidgets.QLabel("    " + t + " - Coming soon!"), t)

    window.setCentralWidget(tabContainer)
    window.setWindowTitle("PengTest")    
    window.resize(800, 600)
    
    createStatusBar(window)
    return window

def createSplash():
    loadingTips = ["Water is wet", "Slack > Teams"]

    splashLoc = str(pathlib.Path(__file__).parent.absolute()) + "/pengSplash.png"
    splash = QtWidgets.QSplashScreen(pixmap = QtGui.QPixmap(splashLoc))
    splash.showMessage('<h2> Tip: ' + random.choice(loadingTips) + "</h2>", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtGui.QColor(20,20,20))
    return splash

def createStatusBar(window):
    status = QtWidgets.QStatusBar()
    statusMessage = QtWidgets.QLabel("PengTest - GUI is currently in Alpha. Please support the development of PengTest!")
    status.addWidget(statusMessage)
    status.setStyleSheet("background-color: #fcfc9f")
    window.setStatusBar(status)

def main():
    app = QtWidgets.QApplication([])
    window = initWindow()

    if len(sys.argv) > 1 and sys.argv[1] == "--no-splash":
        window.show()
    else:
        splash = createSplash()
        splash.show()
        time.sleep(2.5)
        window.show()
        splash.finish(window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()