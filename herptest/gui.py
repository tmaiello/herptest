import sys
import time, random
from PySide2 import QtCore, QtWidgets, QtGui
from . import homePage, testSuiteCreator, resultsPage



def createSplash():
    loadingTips = ["Water is wet", "Slack > Teams"]
    splash = QtWidgets.QSplashScreen(pixmap = QtGui.QPixmap("pengSplash.png"))
    splash.showMessage('<h2> Tip: ' + random.choice(loadingTips) + "</h2>", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtGui.QColor(20,20,20))
    return splash

def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    
    tabContainer =  QtWidgets.QTabWidget()

    tabContainer.addTab(homePage.HomePage(), "Run PengTest")
    homePageInst = tabContainer.widget(0)
    tabContainer.addTab(testSuiteCreator.TestSuiteCreator(), "Create Test Suite")
    testSuiteCreatorInst = tabContainer.widget(1)
    tabContainer.addTab(resultsPage.ResultsPage(), "Test Results")
    resultsPageInst = tabContainer.widget(2)

    #give the home page the funcion to call when the SHOW RESULTS button is clicked
    #pass the function to set the results page as active to the results page so data can load first
    homePageInst.setResultsFunction(resultsPageInst.loadResults, (tabContainer.setCurrentWidget, resultsPage))


    tabList = ["ELMA Config"]
    for t in tabList:
        tabContainer.addTab(QtWidgets.QLabel("    " + t + " - Coming soon!"), t)




    window.setCentralWidget(tabContainer)
    window.setWindowTitle("PengTest")

    status = QtWidgets.QStatusBar()
    statusMessage = QtWidgets.QLabel("HerpTest is currently in Alpha. Please support the development of HerpTest!")
    status.addWidget(statusMessage)
    status.setStyleSheet("background-color: #fcfc9f")
    window.setStatusBar(status)
    
    window.resize(800, 600)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--no-splash":
        window.show()
    else:
        splash = createSplash()
        splash.show()
        time.sleep(1)
        window.show()
        splash.finish(window)


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()