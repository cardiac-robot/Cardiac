"""MAIN MENU GUI CODE"""
# -*- coding: utf-8 -*-import sys
import sys

from PyQt4 import QtGui, QtCore

from PyQt4.QtCore import*

from PyQt4.QtGui import*

import ctypes

class WelcomeWin(QtGui.QMainWindow):

    def __init__(self, ProjectHandler):
        super(WelcomeWin,self).__init__()
        #load project handler settings
        self.PH = ProjectHandler
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.65
        #init_ui
        self.init_ui()
        ##Signals
        #self.set_signals()



    def init_ui(self):
        #-------main config-------
        #Window title
        self.setWindowTitle("Welcome Window")
        #Resizing MainWindoe to a percentage of the total
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)
        #define position and size of the window
        self.setGeometry(self.screen_h/2 - (self.winsize_h/2) , self.screen_v/2 - (self.winsize_v/2),self.winsize_h, self.winsize_v)
        #self.resize(self.winsize_h,self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #setting backgroung image
        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.PH.paths["img"]+ "/WelcomeWindow.jpg"))
        self.label_background.setScaledContents(True)
        #----------------------------------

    #------------------------------------SIGNAL METHODS------------------------------------------------------------------------------




#def main():
    #app=QtGui.QApplication(sys.argv)
    #GUI=MainMenuWin()
    #sys.exit(app.exec_())
#A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=MainMenuWin()
    sys.exit(app.exec_())
