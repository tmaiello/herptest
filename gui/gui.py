import sys
import time, random
from PySide2 import QtCore, QtWidgets, QtGui
from homePage import HomePage

def createSplash():
    loadingTips = ["Water is wet", "Slack > Teams"]
    splash = QtWidgets.QSplashScreen(pixmap = QtGui.QPixmap("pengSplash.png"))
    splash.showMessage('<h2> Tip: ' + random.choice(loadingTips) + "</h2>", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtGui.QColor(20,20,20))
    return splash

def main():
    app = QtWidgets.QApplication([])

    window = QtWidgets.QMainWindow()
    
    tabContainer =  QtWidgets.QTabWidget()

    tabContainer.addTab(HomePage(), "Run PengTest")

    tabList = ["Create Test Suite", "Test Results", "ELMA Config"]
    for t in tabList:
        tabContainer.addTab(QtWidgets.QLabel("    " + t + " - Coming soon!"), t)




    window.setCentralWidget(tabContainer)
    window.setWindowTitle("HerpTest")

    status = QtWidgets.QStatusBar()
    status.showMessage("HerpTest is currently in Alpha. Please support the development of HerpTest!")
    status.setStyleSheet("background-color: #fcfc9f")
    window.setStatusBar(status)
    
    window.resize(800, 600)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--no-splash":
        window.show()
    else:
        splash = createSplash()
        splash.show()
        time.sleep(2)
        window.show()
        splash.finish(window)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()