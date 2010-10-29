
import roslib; roslib.load_manifest('sr_control_gui')

from PyQt4 import QtCore, QtGui, Qt
import rospy

import paramiko
import subprocess
import socket
import time

class RunCommand(Qt.QThread):
    def __init__(self, command, final_status, library):
        Qt.QThread.__init__(self)
        self.command = command
        self.ip = library.ip
        self.library = library
        self.final_status = final_status
    
    def run(self):
        #TODO run the command
        if self.command != "":
            if self.library.is_local:
                self.run_local_command()
            elif self.final_status == "get_status":
                #the get status command is a ros command run locally
                self.run_local_command()
            else:
                self.run_ssh_command()
    
    def run_local_command(self):
        process = subprocess.Popen(self.command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        if self.final_status == "get_status":
            output = output.split('\n')
            
            all_name_found = True
            for name in self.library.list_of_nodes:
                name_found = False
                for line in output:
                    if name in output:
                        name_found = True
                        #remove the line from the output
                        output.pop(output.index(name))
                        break
                if not name_found:
                    all_name_found = False
                    break
            if all_name_found:
                self.library.status = "started"
            else:
                if "starting" != self.library.status:
                    self.library.status = "stopped"
            
        else:
            self.library.status = self.final_status

    def run_ssh_command(self):
        self.ssh_client.connect(self.library.ip,
                                username=self.library.login,
                                password=self.library.password)
        
class Library(object):
    def __init__(self, name="", list_of_nodes=[], start_cmd="", stop_cmd="", status_cmd="", root_path=""):
        self.name = name
        self.ip = ""
        self.hostname = ""
        self.status = ""
        self.login = ""
        self.password = ""
        self.icon_local_path = root_path + '/src/sr_control_gui/images/icons/local.png'
        self.icon_remote_path = root_path + '/src/sr_control_gui/images/icons/remote.png'
        self.icon_library_path = root_path + '/src/sr_control_gui/images/icons/ros.jpg'
        self.is_local = True
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.list_of_nodes = list_of_nodes
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
        self.status_cmd = status_cmd
        self.thread_start = RunCommand(self.start_cmd, "started", self)
        self.thread_status = RunCommand(self.status_cmd, "get_status", self)
        self.thread_stop = RunCommand(self.stop_cmd, "stopped", self)
        self.set_local_ip()
    
    def set_local_ip(self):
        ip = socket.gethostbyname(socket.gethostname())
        self.set_ip(ip)
        self.is_local = True
    
    def set_ip(self, ip, login="", password=""):
        try:
            socket.inet_aton(ip)
        except socket.error:
            # not a valid ip
            return - 1
        self.ip = ip
        try:
            self.hostname = socket.gethostbyaddr(str(ip))[0]
            if self.hostname != socket.gethostbyname(socket.gethostname()):
                self.login = login
                self.password = password
                self.is_local = False
            else:
                self.is_local = True
        except:
            self.hostname = ""

    def get_status(self):
        if not self.thread_status.isRunning():
            self.thread_status.start()

    def start(self):
        self.status = "starting"
        self.thread_start.start()

    def stop(self):
        self.status = "stopping"
        self.thread_stop.start()
    
    
    def test_login_pwd(self, login, pwd):
        try:
            self.ssh_client.connect(self.ip, username=login, password=pwd)
        except:
            print "Error: ", sys.exc_info()[0]
            return False
        self.ssh_client.close()
        return True

class RobotAndLibrariesBackend(object):
    def __init__(self):
        self.libraries = {}
        
    def add_library(self, name, list_of_nodes=[], start_cmd="", stop_cmd="", status_cmd="", root_path=""):
        lib = Library(name=name, list_of_nodes=list_of_nodes, start_cmd=start_cmd,
                      stop_cmd=stop_cmd, status_cmd=status_cmd, root_path=root_path)
        self.libraries[name] = lib
        
    
