

import sys
from PyQt4 import QtGui, QtCore
#from ProjectHandler import ProjectHandler
#from SettingsWin import SettingsWin
#from RegisterWin import RegisterWin
#from ModalityWin import ModalityWin


class MainMenuWin(QtGui.QMainWindow):
    def __init__(self,ProjectHandler):
        super(MainMenuWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.65
        self.init_ui()
        #self.controlbuttons_main['sign_in'].clicked.connect(self.signin_button)
        #self.controlbuttons_main['modalities'].clicked.connect(self.modalities_button)
        #self.controlbuttons_main['settings'].clicked.connect(self.settings_button)

    def init_ui(self):
        self.setWindowTitle('Main Menu')
        #
        self.winsize_h = int(self.screen_h * self.r_size)
        self.winsize_v = int(self.screen_v* self.r_size)
        #
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)
        #
        self.controlbuttons_main = {}
        #
        self.controlbuttons_main['log_in'] = QtGui.QPushButton('Log in',self)
        self.controlbuttons_main["log_in"].setGeometry(self.winsize_v*0.35, self.winsize_h*0.07, self.winsize_v*0.5, self.winsize_h*0.16)
        #
        self.controlbuttons_main['sign_in'] = QtGui.QPushButton('Sign in',self)
        self.controlbuttons_main["sign_in"].setGeometry(self.winsize_v*0.95, self.winsize_h*0.07, self.winsize_v*0.5, self.winsize_h*0.16)
        #
        self.controlbuttons_main['data'] = QtGui.QPushButton('Data',self)
        self.controlbuttons_main["data"].setGeometry(self.winsize_v*0.35, self.winsize_h*0.28, self.winsize_v*0.5, self.winsize_h*0.16)
        #
        self.controlbuttons_main['settings'] = QtGui.QPushButton('Settings',self)
        self.controlbuttons_main["settings"].setGeometry(self.winsize_v*0.95, self.winsize_h*0.28, self.winsize_v*0.5, self.winsize_h*0.16)

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = MainMenuWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
