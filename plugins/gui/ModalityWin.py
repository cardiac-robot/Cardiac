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

        self.CloseButton.clicked.connect(self.close_button)
        #self.robot.clicked.connect(self.robot_button)
        #self.robot_memoria.clicked.connect(self.robot_memoria_button)

    def init_ui(self):
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)

        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)

        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.PH.paths["img"] + "background_Modalities.png"))
        self.label_background.setScaledContents(True)

        self.ControlButtons = {}
        # no robot button
        self.ControlButtons['no_robot'] = QtGui.QCommandLinkButton(self)
        self.ControlButtons['no_robot'].setGeometry(QtCore.QRect(self.winsize_h * 0.1, self.winsize_v * 0.15, self.winsize_v * 0.45, self.winsize_h * 0.25))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "no_robot.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['no_robot'].setIcon(icon)
        self.ControlButtons['no_robot'].setIconSize(QtCore.QSize(self.winsize_v * 0.5, self.winsize_h * 0.24))
        # robot no memory button
        self.ControlButtons['robot'] = QtGui.QCommandLinkButton(self)
        self.ControlButtons['robot'].setGeometry(QtCore.QRect(self.winsize_h * 0.37, self.winsize_v * 0.15, self.winsize_v * 0.45, self.winsize_h * 0.25))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "y_robot.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['robot'].setIcon(icon)
        self.ControlButtons['robot'].setIconSize(QtCore.QSize(self.winsize_v * 0.5, self.winsize_h * 0.24))
        # robot with memory button
        self.ControlButtons['robot_memory'] = QtGui.QCommandLinkButton(self)
        self.ControlButtons['robot_memory'].setGeometry(QtCore.QRect(self.winsize_h * 0.63, self.winsize_v * 0.15, self.winsize_v * 0.45, self.winsize_h * 0.25))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "robot_memory.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['robot_memory'].setIcon(icon)
        self.ControlButtons['robot_memory'].setIconSize(QtCore.QSize(self.winsize_v * 0.5, self.winsize_h * 0.24))
        # Close button
        self.CloseButton = QtGui.QCommandLinkButton(self)
        self.CloseButton.setGeometry(QtCore.QRect(self.winsize_h * 0.95, self.winsize_v * 0.01, self.winsize_v * 0.045, self.winsize_h * 0.03))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "exit_icon.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(self.winsize_v * 0.04, self.winsize_h * 0.02))

    def close_button(self):
        self.close()

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
