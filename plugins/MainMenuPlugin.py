"""MAIN MENU PLUGIN"""
from PyQt4 import QtGui, QtCore
import gui.MainMenuWin as MainMenuWin


class MainMenuPlugin(object):
    def __init__(self, ProjectHandler, DataHandler):
        #load ProjectHandler settings
        self.PH = ProjectHandler
        #load database manager
        self.DB = DataHandler
        #load gui resource
        self.MainMenuWin = MainMenuWin.MainMenuWin(ProjectHandler = self.PH)



    #
    def LaunchView(self):
        self.MainMenuWin.show()

    def HideView(self):
        self.MainMenuWin.hide()
    #
    def SignInConnect(self, f):
        self.MainMenuWin.controlbuttons_main['sign_in'].clicked.connect(f)
        self.MainMenuWin.controlbuttons_main['sign_in'].clicked.connect(self.HideView)
    #
    def DataConnect(self,f):

        self.MainMenuWin.controlbuttons_main['data'].clicked.connect(f)
        self.MainMenuWin.controlbuttons_main['data'].clicked.connect(self.HideView)

    #
    def SettingsConnect(self,f):
        self.MainMenuWin.controlbuttons_main['settings'].clicked.connect(f)
        self.MainMenuWin.controlbuttons_main['settings'].clicked.connect(self.HideView)
    #
    def LogInConnect(self,f):
        self.MainMenuWin.controlbuttons_main['log_in'].clicked.connect(f)
        self.MainMenuWin.controlbuttons_main['log_in'].clicked.connect(self.HideView)


    def shutdown(self):
        self.MainWindow.close()
