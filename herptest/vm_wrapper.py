import virtualbox
import virtualbox.events
import virtualbox.library
from vix import VixHost, VixError, VixJob

import os
import time
from pathlib import Path
from datetime import datetime
import paramiko
import paramiko.ssh_exception
import socket
import subprocess

# TODO - should these be added as a config option?
VM_BOOT_TIME = 70
MAX_RETRIES  = 10
VM_SLEEP_TIME = 10
ADB = "adb"

# Project information
STAGING_FILES = [ "staging.sh", "staging.tgz" ]
# TODO - make sure this is the right name, add as config
PAYLOAD_FILES = [ "processlog.tar.gz", "p1.diff" ]
RESULT_FILES = [ "run.log", "result.log" ]
STAGING_DIR = "staging"
PAYLOAD_DIR = "submissions"
RESULT_DIR = "result"
BUILD_CMD = "build.sh"
STAGE_CMD = "staging.sh"
REM_PROJ_DIR = "/home/reptilian/"
REM_STAGING_DIR = REM_PROJ_DIR
REM_PAYLOAD_DIR = REM_PROJ_DIR + "/payload"
REM_RESULT_DIR = REM_PROJ_DIR + "/result"

# Log information
BUILD_LOG = "build.log"
RUN_LOG = "run.log"
ERR_LOG = ".err"
RESULT_LOG = "result.log"
STAGING_LOG = "staging.log"

class VmWrapper:
    # TODO - update to only pass cfg.build.vm, then pull vars off that
    def __init__(self, type, name, snapshot, ip, port, user, passwd):
        # Currently only supports VMWare and VirtualBox
        if type == "VMWare" or type == "VirtualBox":
            self._type = type
        else:
            # TODO - make this more robust
            print("Unsupported VM type!")
            return
        self._name = name
        self._snapshot = snapshot
        self._ip = ip
        self._port = port
        self._user = user
        self._passwd = passwd

    # Method to start the VM software, only needs to be done once
    def start_vm(self):
        if self._type == "VMWare":
            # Load VMWare
            print("Starting VM session at " + str(datetime.now()) + "...")
            self.host = VixHost()

            # Using the VM directory, identify the valid VMs and add them to a dictionary {name: file}
            vm_dir = str(Path.home() / "Documents" / "Virtual Machines")
            files = [(root, file) for root, _, flist in os.walk(vm_dir) for file in flist if file.endswith(".vmx")]
            vm_dict = {file.rsplit('.', 1)[0]: os.path.join(root, file) for root, file in files}
            self._vm_file = vm_dict[self._name]
        # else self._type == "VirtualBox":
        #     self.vm = 
    
    # Method to boot up the VM
    def boot_vm(self):
        self.vm = self.host.open_vm(self._vm_file)

        if self._snapshot != None:
            snapshot = self.vm.snapshot_get_named(self._snapshot)
            self.vm.snapshot_revert(snapshot=snapshot)

        self.vm.power_on()
        time.sleep(VM_BOOT_TIME)

    # Method to send the necessary files over to reptilian, make the project, then reboot
    def make_vm(self, target):
        self.boot_vm()
        # Connect to the remote server
        print("Connecting via SSH...")
        ssh = self.loop_for_shell()
        if not ssh:
            print("Error setting up SSH connection! Exiting...");
            self.dirty_shutdown()
            return

        # Run the staging phase.
        print("Setting the stage for the payload...")
        self.run_staging(ssh, target)

        # Run the build phase.
        print("Beginning build cycle...")
        self.run_build(ssh, target)
        ssh.close()

        # Reboot if needed
        print("Shutting down post build...")
        self.graceful_shutdown()

        # TODO - uncomment once testing is able to be performed
        # print("Rebooting post build...")
        # self.vm.power_on()
        # time.sleep(VM_BOOT_TIME)

    # Method to run tests, then shut down the VM once completed
    def run_tests(self, target):
        ssh = self.loop_for_shell()
        if not ssh:
            print("Error setting up SSH connection! Exiting...");
            self.dirty_shutdown()
            return

        # Run the test phase.
        print("Beginning test cycle...")

        # Limit to 2 min test
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(REM_STAGING_DIR + "/" + 'run.sh', timeout=120000)
        time.sleep(2)
        gen_errors = ssh_stderr.readlines()
        print("Tests complete. Fetching results.")
        sftp = ssh.open_sftp()
        for filename in RESULT_FILES:
            print("Getting " + filename + "...")
            try:
                sftp.get(REM_RESULT_DIR + "/" + filename, RESULT_DIR + "/" + target + "/" + filename)
            except:
                print("Error: could not grab " + filename + " for target " + target + ". Skipping.")

        sftp.close()
        self.write_to_file(gen_errors, RESULT_DIR + "/" + target + "/" + RUN_LOG + ERR_LOG)

        ssh.close()

        # Shut down the VM for this target
        print("Shutting down VM...")
        self.dirty_shutdown()
    
    def loop_for_shell(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connected = False
        failures = 0

        while not(connected) and failures < MAX_RETRIES:
            try:
                ssh.connect(self._ip, username=self._user, password=self._passwd, port=self._port)
                connected = True
            except (socket.timeout, paramiko.ssh_exception.SSHException) as err:
                print("Error connecting. Retrying...")
                failures = failures + 1

        if not(connected):
            print("Could not connect to guest: retries exceeded.")
            return None
        return ssh
    
    def dirty_shutdown(self):
        self.vm.power_off(from_guest=False)
        time.sleep(5)
    
    def graceful_shutdown(self):
        # Make sure we are connected with ADB
        subprocess.call([ ADB, "connect", self._name ])
        # Send the shutdown signal via ADB and wait for the machine to finish
        subprocess.call([ ADB, "shell", "su -c 'svc power shutdown'" ])
        time.sleep(VM_SLEEP_TIME)
        self.vm.power_off(from_guest=True)
    
    def write_to_file(self, lines, filename):
        with open(filename, 'w+') as file:
            for line in lines:
                file.write(line + "\n")
            file.close()
    
    def run_staging(self, ssh, target):
        # Make sure the directory is there for staging.
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("mkdir " + REM_STAGING_DIR) # Make staging dir
        build_errors = ssh_stderr.readlines()

        # Push files via SFTP.
        sftp = ssh.open_sftp()

        for filename in STAGING_FILES:
            if not os.path.isfile(STAGING_DIR + "/" + filename):
                print("Error - file " + filename + " does not exist in staging area. Skipping.")
                continue

            print("Pushing " + filename + "...")
            try:
                sftp.put(STAGING_DIR + "/" + filename, REM_STAGING_DIR + "/" + filename)
            except:
                print("Error: could not upload " + filename + ".")
            sftp.close()

            # Run the staging script.
            print("Running staging script...");
            time.sleep(2)

            # Make the script executable
            build_errors.extend(ssh_stderr.readlines())
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("chmod +x " + REM_STAGING_DIR + "/" + STAGE_CMD)
            time.sleep(2)

            # Run the staging script
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(REM_STAGING_DIR + "/" + STAGE_CMD)
            build_errors.extend(ssh_stderr.readlines())
            self.write_to_file(build_errors, RESULT_DIR + "/" + target + "/" + STAGING_LOG + ERR_LOG)
        
    def run_build(self, ssh, target):
        # Push files via SFTP.
        sftp = ssh.open_sftp()

        for filename in PAYLOAD_FILES:
            if not os.path.isfile(PAYLOAD_DIR + "/" + target + "/" + filename):
                print("Error - file " + filename + " does not exist in payload area for target " + target + ". Skipping.")
                continue

            print("Pushing " + filename + "...")
            try:
                sftp.put(PAYLOAD_DIR + "/" + target + "/" + filename, REM_PAYLOAD_DIR + "/" + filename)
            except:
                print("Error: could not upload " + filename + ".")

        # Run the build script; power down when completed.
        print("Executing build....")
        # Limit to 20 min build
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(REM_STAGING_DIR + "/" + BUILD_CMD, timeout=1200000)
        time.sleep(2)
        build_errors = ssh_stderr.readlines()

        print("Build complete. Fetching logs.")
        sftp.get(REM_RESULT_DIR + "/" + BUILD_LOG, RESULT_DIR + "/" + target + "/" + BUILD_LOG)
        sftp.close()
        self.write_to_file(build_errors, RESULT_DIR + "/" + target + "/" + BUILD_LOG + ERR_LOG)
