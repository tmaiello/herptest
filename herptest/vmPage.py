from PySide2 import QtCore, QtWidgets, QtGui
import os, subprocess

class VmPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QGridLayout()

        self.createVMInfoFields()
        self.createFileInfoFields()
        self.createDirInfoFields()
        self.createCmdInfoFields()

        self.generateButton = QtWidgets.QPushButton("Generate Config")
        self.generateButton.setFixedHeight(50)
        self.generateButton.setFixedWidth(100)
        self.generateButton.clicked.connect(self.writeConfig)
        self.layout.addWidget(self.generateButton)

        self.setLayout(self.layout)

    def createVMInfoFields(self):
        self.typeLabel = QtWidgets.QLabel("VM Type:")
        self.typeLabel.setMaximumHeight(30)
        self.layout.addWidget(self.typeLabel, 0, 0)
        self.typeDropdown = QtWidgets.QComboBox()
        self.typeDropdown.addItem("VMWare")
        self.layout.addWidget(self.typeDropdown, 1, 0)

        self.nameLabel = QtWidgets.QLabel("VM Name:")
        self.nameLabel.setMaximumHeight(30)
        self.layout.addWidget(self.nameLabel, 2, 0)
        self.nameField = QtWidgets.QLineEdit("")
        self.nameField.setFixedWidth(500)
        self.layout.addWidget(self.nameField, 3, 0)

        self.snapshotLabel = QtWidgets.QLabel("Snapshot Name:")
        self.snapshotLabel.setMaximumHeight(30)
        self.layout.addWidget(self.snapshotLabel, 4, 0)
        self.snapshotField = QtWidgets.QLineEdit("")
        self.snapshotField.setFixedWidth(500)
        self.layout.addWidget(self.snapshotField, 5, 0)

        self.ipLabel = QtWidgets.QLabel("VM IP Address:")
        self.ipLabel.setMaximumHeight(30)
        self.layout.addWidget(self.ipLabel, 6, 0)
        self.ipField = QtWidgets.QLineEdit("")
        self.ipField.setFixedWidth(500)
        self.layout.addWidget(self.ipField, 7, 0)

        self.portLabel = QtWidgets.QLabel("VM Port:")
        self.portLabel.setMaximumHeight(30)
        self.layout.addWidget(self.portLabel, 8, 0)
        self.portField = QtWidgets.QLineEdit("")
        self.portField.setFixedWidth(50)
        self.layout.addWidget(self.portField, 9, 0)

        self.userLabel = QtWidgets.QLabel("Username:")
        self.userLabel.setMaximumHeight(30)
        self.layout.addWidget(self.userLabel, 10, 0)
        self.userField = QtWidgets.QLineEdit("")
        self.userField.setFixedWidth(500)
        self.layout.addWidget(self.userField, 11, 0)

        self.passwordLabel = QtWidgets.QLabel("Password:")
        self.passwordLabel.setMaximumHeight(30)
        self.layout.addWidget(self.passwordLabel, 12, 0)
        self.passwordField = QtWidgets.QLineEdit("")
        self.passwordField.setFixedWidth(500)
        self.layout.addWidget(self.passwordField, 13, 0)

        self.bootLabel = QtWidgets.QLabel("VM Boot Time (in seconds):")
        self.bootLabel.setMaximumHeight(30)
        self.layout.addWidget(self.bootLabel, 14, 0)
        self.bootField = QtWidgets.QLineEdit("70")
        self.bootField.setFixedWidth(50)
        self.layout.addWidget(self.bootField, 15, 0)

    def createFileInfoFields(self):
        self.stagingLabel = QtWidgets.QLabel("Staging Files:")
        self.stagingLabel.setMaximumHeight(30)
        self.layout.addWidget(self.stagingLabel, 16, 0)
        self.stagingField = QtWidgets.QLineEdit("Enter as comma separated list")
        self.stagingField.setFixedWidth(500)
        self.layout.addWidget(self.stagingField, 17, 0)

        self.payloadLabel = QtWidgets.QLabel("Payload Files:")
        self.payloadLabel.setMaximumHeight(30)
        self.layout.addWidget(self.payloadLabel, 18, 0)
        self.payloadField = QtWidgets.QLineEdit("Enter as comma separated list")
        self.payloadField.setFixedWidth(500)
        self.layout.addWidget(self.payloadField, 19, 0)

        self.resultLabel = QtWidgets.QLabel("Result Files:")
        self.resultLabel.setMaximumHeight(30)
        self.layout.addWidget(self.resultLabel, 20, 0)
        self.resultField = QtWidgets.QLineEdit("Enter as comma separated list")
        self.resultField.setFixedWidth(500)
        self.layout.addWidget(self.resultField, 21, 0)

    def createDirInfoFields(self):
        self.stagdirLabel = QtWidgets.QLabel("Staging Directory:")
        self.stagdirLabel.setMaximumHeight(30)
        self.layout.addWidget(self.stagdirLabel, 0, 1)
        self.stagdirField = QtWidgets.QLineEdit("")
        self.stagdirField.setFixedWidth(500)
        self.layout.addWidget(self.stagdirField, 1, 1)

        self.paydirLabel = QtWidgets.QLabel("Payload Directory (Test Suite Directory):")
        self.paydirLabel.setMaximumHeight(30)
        self.layout.addWidget(self.paydirLabel, 2, 1)
        self.paydirField = QtWidgets.QLineEdit("")
        self.paydirField.setFixedWidth(500)
        self.layout.addWidget(self.paydirField, 3, 1)

        self.resultdirLabel = QtWidgets.QLabel("Results Directory:")
        self.resultdirLabel.setMaximumHeight(30)
        self.layout.addWidget(self.resultdirLabel, 4, 1)
        self.resultdirField = QtWidgets.QLineEdit("")
        self.resultdirField.setFixedWidth(500)
        self.layout.addWidget(self.resultdirField, 5, 1)

        self.remdirLabel = QtWidgets.QLabel("Remote Project Directory:")
        self.remdirLabel.setMaximumHeight(30)
        self.layout.addWidget(self.remdirLabel, 6, 1)
        self.remdirField = QtWidgets.QLineEdit("")
        self.remdirField.setFixedWidth(500)
        self.layout.addWidget(self.remdirField, 7, 1)

        self.remstagdirLabel = QtWidgets.QLabel("Remote Staging Directory:")
        self.remstagdirLabel.setMaximumHeight(30)
        self.layout.addWidget(self.remstagdirLabel, 8, 1)
        self.remstagdirField = QtWidgets.QLineEdit("")
        self.remstagdirField.setFixedWidth(500)
        self.layout.addWidget(self.remstagdirField, 9, 1)

        self.rempaydirLabel = QtWidgets.QLabel("Remote Payload Directory:")
        self.rempaydirLabel.setMaximumHeight(30)
        self.layout.addWidget(self.rempaydirLabel, 10, 1)
        self.rempaydirField = QtWidgets.QLineEdit("")
        self.rempaydirField.setFixedWidth(500)
        self.layout.addWidget(self.rempaydirField, 11, 1)

        self.remresdirLabel = QtWidgets.QLabel("Remote Results Directory:")
        self.remresdirLabel.setMaximumHeight(30)
        self.layout.addWidget(self.remresdirLabel, 12, 1)
        self.remresdirField = QtWidgets.QLineEdit("")
        self.remresdirField.setFixedWidth(500)
        self.layout.addWidget(self.remresdirField, 13, 1)

    def createCmdInfoFields(self):
        self.buildLabel = QtWidgets.QLabel("Build Command:")
        self.buildLabel.setMaximumHeight(30)
        self.layout.addWidget(self.buildLabel, 14, 1)
        self.buildField = QtWidgets.QLineEdit("")
        self.buildField.setFixedWidth(500)
        self.layout.addWidget(self.buildField, 15, 1)

        self.stageLabel = QtWidgets.QLabel("Stage Command:")
        self.stageLabel.setMaximumHeight(30)
        self.layout.addWidget(self.stageLabel, 16, 1)
        self.stageField = QtWidgets.QLineEdit("")
        self.stageField.setFixedWidth(500)
        self.layout.addWidget(self.stageField, 17, 1)

    def writeConfig(self):
        # Get the current directory
        cur_dir = os.getcwd()

        # Change the directory to the root of the test suite
        os.chdir(self.paydirField.text())

        # Write the config variables to config.py
        with open("config.py", "a+") as file:
            content = "build.vm.is_vm = True\n"
            content += "build.vm.type = \"" + self.typeDropdown.currentText() + "\"\n"
            content += "build.vm.name = \"" + self.nameField.text() + "\"\n"
            content += "build.vm.snapshot = \"" + self.snapshotField.text() + "\"\n"
            content += "build.vm.ip = \"" + self.ipField.text() + "\"\n"
            content += "build.vm.port = \"" + self.portField.text() + "\"\n"
            content += "build.vm.user = \"" + self.userField.text() + "\"\n"
            content += "build.vm.passwd = \"" + self.passwordField.text() + "\"\n"
            content += "build.vm.boot_time = " + self.bootField.text() + "\n"
            
            # The files are entered as a comma list, so split the string
            content += self.splitString(self.stagingField.text(), "staging")
            content += self.splitString(self.payloadField.text(), "payload")
            content += self.splitString(self.resultField.text(), "result")

            content += "build.vm.staging_dir = \"" + self.stagdirField.text() + "\"\n"
            content += "build.vm.payload_dir = \"" + self.paydirField.text() + "\"\n"
            content += "build.vm.result_dir = \"" + self.resultdirField.text() + "\"\n"
            content += "build.vm.build_cmd = \"" + self.buildField.text() + "\"\n"
            content += "build.vm.stage_cmd = \"" + self.stageField.text() + "\"\n"
            content += "build.vm.remote_proj_dir = \"" + self.remdirField.text() + "\"\n"
            content += "build.vm.remote_staging_dir = \"" + self.remstagdirField.text() + "\"\n"
            content += "build.vm.remote_payload_dir = \"" + self.rempaydirField.text() + "\"\n"
            content += "build.vm.remote_result_dir = \"" + self.remresdirField.text() + "\"\n"
            file.write(content)
        
        # Execute the build on command prompt
        subprocess.Popen(['cmd.exe', '/C', 'herp', '.', '.\Projects'])

        # Change back to the initial directory
        os.chdir(cur_dir)
    
    def splitString(self, string, dirType):
        # Remove any spaces
        staging = string.replace(' ','')

        # Split on commas
        l = staging.split(',')

        content = ""
        content += "build.vm." + dirType + "_files = ["
        i = 0

        # Iterate over every file, adding it to the string formatted correctly
        for f in l:
            content += "\"" + f + "\""
            if i == len(l) - 1:
                content += "]\n"
            else:
                content += ", "
                i += 1
        return content
