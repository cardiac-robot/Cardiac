# coding=utf-8
import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import*
from PyQt4.QtGui import*
from ProjectHandler import ProjectHandler

class ModalityWin(QtGui.QMainWindow):
    def __init__(self,ProjectHandler):
        super(ModalityWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        self.init_ui()
        self.no_robot.clicked.connect(self.no_robot_button)
        self.robot.clicked.connect(self.robot_button)
        self.robot_memoria.clicked.connect(self.robot_memoria_button)

    def init_ui(self):
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)
        self.no_robot = QtGui.QPushButton('No robot',self)
        self.no_robot.setGeometry(QtCore.QRect(self.winsize_v*0.11, self.winsize_h*0.1, self.winsize_v*0.5, self.winsize_h*0.3))
        self.robot = QtGui.QPushButton('Robot',self)
        self.robot.setGeometry(QtCore.QRect(self.winsize_v*0.63, self.winsize_h*0.1, self.winsize_v*0.5, self.winsize_h*0.3))
        self.robot_memoria = QtGui.QPushButton('Robot with memory',self)
        self.robot_memoria.setGeometry(QtCore.QRect(self.winsize_h*0.648, self.winsize_h*0.1, self.winsize_v*0.5, self.winsize_h*0.3))

    def no_robot_button(self):
        self.close()

    def robot_button(self):
        self.close()

    def robot_memoria_button(self):
        self.close()

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = ModalityWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
