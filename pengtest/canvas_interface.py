from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess
import numpy as np
from . import grade_csv_uploader, canvas, env_dialog

class AbstractCanvasInterface(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.courseDict = None
        self.assignmentDict = {}
        #init trackers, updating this makes it simpler to pass this data to upload
        self.currentCourse = None
        self.currentCourseId = None
        self.currentAssignment = None
        self.assignmentReady = False
        self.canvasEnvMissing = False
        self.setupCanvasInstances()

        if self.canvasEnvMissing:
            #setupCanvasInstances sets this true if there was an issue with setup, show the dialog to fetch the env
            self.envDialog = env_dialog.EnvDialog(lambda: self.handleEnvLoaded())
            self.setLayout(self.envDialog.layout)
        else:
            #canvas env loaded properly, load the UI
            self.createUI()




    def handleEnvLoaded(self):
        #print("callback success")
        
        QtWidgets.QWidget().setLayout(self.layout())
        self.createUI()
        
    

    def createUI(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.title = QtWidgets.QLabel()

        self.containerView = QtWidgets.QTreeView()
        self.showCourses() 
        
        self.containerView.clicked[QtCore.QModelIndex].connect(self.handleSelection)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.containerView)

        self.createControls()

        self.setLayout(self.layout)

    def createControls(self):
        #blank for this generic interface, override this function to add different controls to the bottom third
        pass

    def handleSelection(self, index):
        item = self.activeModel.itemFromIndex(index)
        if item.text().find("<-") != -1:
            #go back to the courses page
            
            self.currentCourse = None
            self.currentAssignment = None
            self.showCourses()
            self.assignmentReady = False
        elif item.text().find("->") != -1:
            #go down a level
            courseNameIndex = self.activeModel.itemFromIndex(index.siblingAtColumn(0))
            self.currentCourse = courseNameIndex.text()
            courseIdIndex = self.activeModel.itemFromIndex(index.siblingAtColumn(1))
            self.currentCourseId = courseIdIndex.text()

            self.showAssignments(courseNameIndex)
        elif self.mode == "assignments":
            assn = self.activeModel.itemFromIndex(index.siblingAtColumn(0)).text()
            if assn.find("<-") == -1:
                self.currentAssignment = assn
                self.assignmentReady = True
            else:
                self.currentAssignment = None
                self.assignmentReady = False
        elif self.mode == "courses":
            self.currentCourse = self.activeModel.itemFromIndex(index.siblingAtColumn(0)).text()
        #print("current course: " + str(self.currentCourse))
        #print("current assignment: " + str(self.currentAssignment))
        self.onSelect()

    def onSelect(self):
        #blank for this generic interface, add any additional tasks to be done when the selection is changed by
        #   overriding this function in an inherited class
        pass


    def setupCanvasInstances(self):
        self.canvasUtil = None
        self.canvasPath = "https://ufl.instructure.com/api/v1"
        self.canvasBasePath = "https://ufl.instructure.com"
        self.dotEnvPath = "canvas.env"
        self.tokenType = "TOKEN"
        try:
            self.canvasUtil = grade_csv_uploader.CanvasUtil(self.canvasPath, self.dotEnvPath, self.tokenType)

            self.canvasWrapper = canvas.CanvasWrapper(self.canvasBasePath, self.dotEnvPath)
        except:
            print("Something went wrong, either the canvas.env does not exist or it does not contain a token with the type TOKEN")
            self.canvasEnvMissing = True

        

    def showCourses(self):
        self.mode = "courses"
        self.title.setText("List of Courses")
        coursesModel = QtGui.QStandardItemModel()
        coursesModel.setHorizontalHeaderLabels(["Course Name", "Course ID", " "])

        if not self.courseDict:
            self.courseDict = self.canvasUtil.get_courses_this_semester() # dictionary with keys:course name, values:course id

        if len(self.courseDict.keys()) == 0:
            #No active courses available
            self.courseDict["No Active Courses Found"] = ""   

        for course in self.courseDict.keys():
            courseName = QtGui.QStandardItem(course)
            courseName.setEditable(False)
            courseId = QtGui.QStandardItem(str(self.courseDict[course]))
            courseId.setEditable(False)
            if courseId.text() == "":
                expandCourse = QtGui.QStandardItem("")
            else:
                expandCourse = QtGui.QStandardItem("Expand ->")
            expandCourse.setEditable(False)
            coursesModel.appendRow([courseName, courseId, expandCourse])
        
        self.coursesActive = True
        self.activeModel = coursesModel
        self.containerView.setModel(self.activeModel)
        for i in range(0,3):
            self.containerView.resizeColumnToContents(i)

    def showAssignments(self, courseItem):
        course = courseItem.text()
        self.mode = "assignments"
        self.title.setText("Assignments for " + course)
        assignmentsModel = QtGui.QStandardItemModel()
        assignmentsModel.setHorizontalHeaderLabels(["Assignment Name", "Assignment ID"])

        
        if course not in self.assignmentDict.keys() or not self.assignmentDict[course]:
            self.assignmentDict[course] = self.canvasUtil.get_assignment_list(self.courseDict[course])
        
        assignments = self.assignmentDict[course]

        backSelect = QtGui.QStandardItem("<- Return to Courses")
        backSelect.setEditable(False)   
        blank = QtGui.QStandardItem("")
        blank.setEditable(False)
        assignmentsModel.appendRow([backSelect, blank])

        if len(assignments.keys()) == 0:
            #no active assignments available
            assignments["No Assignments Found"] = ""  

        for assignment in assignments.keys():
            assignmentName = QtGui.QStandardItem(assignment)
            assignmentName.setEditable(False)
            assignmentId = QtGui.QStandardItem(str(assignments[assignment]))
            assignmentId.setEditable(False)
            assignmentsModel.appendRow([assignmentName, assignmentId])

        self.coursesActive = False
        self.activeModel = assignmentsModel
        self.containerView.setModel(self.activeModel)
        for i in range(0,3):
            self.containerView.resizeColumnToContents(i)