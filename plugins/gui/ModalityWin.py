# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore

class ModalityWin(QtGui.QMainWindow):

    onModalitySet = QtCore.pyqtSignal()
    onMemory = QtCore.pyqtSignal()

    def __init__(self,ProjectHandler):
        super(ModalityWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        self.init_ui()

        #self.no_robot.clicked.connect(self.no_robot_button)
        #self.robot.clicked.connect(self.robot_button)
        #self.robot_memoria.clicked.connect(self.robot_memoria_button)

    def init_ui(self):
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)

        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)

        self.ControlButtons = {}
        #no robot button
        self.ControlButtons['no_robot'] = QtGui.QPushButton('No robot',self)
        self.ControlButtons['no_robot'].setGeometry(QtCore.QRect(self.winsize_v*0.11, self.winsize_h*0.1, self.winsize_v*0.5, self.winsize_h*0.3))
        #robot no memory button
        self.ControlButtons['robot'] = QtGui.QPushButton('Robot',self)
        self.ControlButtons['robot'].setGeometry(QtCore.QRect(self.winsize_v*0.63, self.winsize_h*0.1, self.winsize_v*0.5, self.winsize_h*0.3))
        #robot with memory button
        self.ControlButtons['robot_memory'] = QtGui.QPushButton('Robot with memory',self)
        self.ControlButtons['robot_memory'].setGeometry(QtCore.QRect(self.winsize_h*0.648, self.winsize_h*0.1, self.winsize_v*0.5, self.winsize_h*0.3))
        #call set internal signals method
        self.set_signals()

    #set internal signals
    def set_signals(self):
        #close the window when any of the modality buttons is pressed
        self.ControlButtons['no_robot'].clicked.connect(self.close)
        self.ControlButtons['robot'].clicked.connect(self.close)
        self.ControlButtons['robot_memory'].clicked.connect(self.close)


def main():
    app = QtGui.QApplication(sys.argv)
    GUI = ModalityWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
