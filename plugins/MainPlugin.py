"""MAIN PLUGIN CODE"""
#import standart libs
import threading
import time
#import GUI library
from PyQt4 import QtGui, QtCore
#import gui component for the plugin
import gui.WelcomeWin as WelcomeWin
#import plugins
import MainMenuPlugin
import ModalityPlugin
import RegisterPlugin
import SettingsPlugin
import MainTherapyPlugin

class MainPlugin(object):
    def __init__(self, ProjectHandler = None, DataHandler = None):
        #load project handler and system settings
        self.PH = ProjectHandler
        #create database
        self.DB = DataHandler
        #launch presentation window
        self.WelcomeWin = WelcomeWin.WelcomeWin(ProjectHandler = self.PH)
        #show the window
        self.WelcomeWin.show()
        #create menu plugin
        self.MainMenuPlugin = MainMenuPlugin.MainMenuPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create register plugin
        self.RegisterPlugin = RegisterPlugin.RegisterPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create settings plugin
        self.SettingsPlugin = SettingsPlugin.SettingsPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create modality plugin
        self.ModalityPlugin = ModalityPlugin.ModalityPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create therapy plugin
        self.MainTherapyPlugin  = MainTherapyPlugin.MainTherapyPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #count_down
        threading.Thread(target = self.count_down).start()
        #create database object




    #count_down to start the application
    def count_down(self, t = 1):
        cont = 6
        while cont:
            cont = cont -1
            print cont
            time.sleep(t)
        self.WelcomeWin.hide()
        time.sleep(5)
        self.shutdown()

    def shutdown(self):
        self.WelcomeWin.close()
