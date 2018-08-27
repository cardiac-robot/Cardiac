

import sys
from PyQt4 import QtGui, QtCore




class MainMenuWin(QtGui.QMainWindow):
    def __init__(self,ProjectHandler):
        super(MainMenuWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        self.init_ui()
        self.CloseButton.clicked.connect(self.close_button)

    def init_ui(self):
        self.setWindowTitle('Main Menu')
        #
        self.winsize_h = int(self.screen_h * self.r_size)
        self.winsize_v = int(self.screen_v* self.r_size)
        #
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)
        #
        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap( self.PH.paths["img"] + "background_MainMenu2.png"))
        self.label_background.setScaledContents(True)
        #
        self.controlbuttons_main = {}
        #
        self.controlbuttons_main['log_in'] = QtGui.QCommandLinkButton(self)
        self.controlbuttons_main["log_in"].setGeometry(self.winsize_h * 0.13, self.winsize_v * 0.2,self.winsize_v * 0.4, self.winsize_h * 0.06)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "login_icon.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.controlbuttons_main['log_in'].setIcon(icon)
        self.controlbuttons_main['log_in'].setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.045))
        #
        self.controlbuttons_main['sign_in'] = QtGui.QCommandLinkButton(self)
        self.controlbuttons_main["sign_in"].setGeometry(self.winsize_h * 0.13, self.winsize_v * 0.35,self.winsize_v * 0.4, self.winsize_h * 0.06)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "register_icon.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.controlbuttons_main["sign_in"].setIcon(icon)
        self.controlbuttons_main["sign_in"].setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.045))
        #
        self.controlbuttons_main['data'] = QtGui.QCommandLinkButton(self)
        self.controlbuttons_main["data"].setGeometry(self.winsize_h*0.13, self.winsize_v*0.5, self.winsize_v*0.4, self.winsize_h*0.06)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "data_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.controlbuttons_main["data"].setIcon(icon)
        self.controlbuttons_main["data"].setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.045))
        #
        self.controlbuttons_main['settings'] = QtGui.QCommandLinkButton(self)
        self.controlbuttons_main["settings"].setGeometry(self.winsize_h * 0.13, self.winsize_v * 0.65,self.winsize_v * 0.4, self.winsize_h * 0.06)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "settings_icon.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.controlbuttons_main["settings"].setIcon(icon)
        self.controlbuttons_main["settings"].setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.045))
        #
        self.CloseButton = QtGui.QCommandLinkButton(self)
        self.CloseButton.setGeometry(QtCore.QRect(self.winsize_h * 0.95, self.winsize_v * 0.01, self.winsize_v * 0.045, self.winsize_h * 0.03))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "exit_icon.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(self.winsize_v * 0.04, self.winsize_h * 0.02))

    def close_button(self):
        self.close()
def main():
    app = QtGui.QApplication(sys.argv)
    GUI = MainMenuWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
