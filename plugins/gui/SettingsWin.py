import sys
#import os
from PyQt4 import QtGui, QtCore
#from PyQt4.QtCore import*
#from PyQt4.QtGui import*
#from ProjectHandler import ProjectHandler

class SettingsWin(QtGui.QMainWindow):
    #set signals
    onEmptyField = QtCore.pyqtSignal()
    onData       = QtCore.pyqtSignal()

    def __init__(self,ProjectHandler):
        super(SettingsWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        self.init_ui()
        #settings dict
        self.inf_settings = {"imu_port"    : None,
                             "imu_sample"  : None,
                             "laser_port"  : None,
                             "laser_sample": None,
                             "ecg_port"    : None,
                             "ecg_sample"  : None,
                             "IpRobot"     : None}

    def init_ui(self):
        self.setWindowTitle('Setting')
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)
        ## background label
        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.PH.paths["img"] + "Settings_background.png"))
        self.label_background.setScaledContents(True)
        #buttons dict
        self.ControlButtons = {}
        #apply changes button
        self.ControlButtons['apply'] = QtGui.QCommandLinkButton(self)
        self.ControlButtons['apply'].setGeometry(QtCore.QRect(self.winsize_h*0.75, self.winsize_v*0.85, self.winsize_v*0.17, self.winsize_h*0.05))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "aply_settings.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['apply'].setIcon(icon)
        self.ControlButtons['apply'].setIconSize(QtCore.QSize(self.winsize_v * 0.16, self.winsize_h * 0.04))

        #cancel button
        self.ControlButtons['cancel'] = QtGui.QCommandLinkButton(self)
        self.ControlButtons['cancel'].setGeometry(QtCore.QRect(self.winsize_h*0.85, self.winsize_v*0.85, self.winsize_v*0.17, self.winsize_h*0.05))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "cancel_settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['cancel'].setIcon(icon)
        self.ControlButtons['cancel'].setIconSize(QtCore.QSize(self.winsize_v * 0.16, self.winsize_h * 0.04))

        #memory button
        self.ControlButtons['clearMemoryBN'] =  QtGui.QCommandLinkButton(self)
        self.ControlButtons['clearMemoryBN'].setGeometry(QtCore.QRect(self.winsize_h*0.65, self.winsize_v*0.85, self.winsize_v*0.17, self.winsize_h*0.05))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "cancel_settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['clearMemoryBN'].setIcon(icon)
        self.ControlButtons['clearMemoryBN'].setIconSize(QtCore.QSize(self.winsize_v * 0.16, self.winsize_h * 0.04))

        #clear db button
        #memory button
        self.ControlButtons['clear_db'] =  QtGui.QCommandLinkButton(self)
        self.ControlButtons['clear_db'].setGeometry(QtCore.QRect(self.winsize_h*0.55, self.winsize_v*0.85, self.winsize_v*0.17, self.winsize_h*0.05))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "cancel_settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['clear_db'].setIcon(icon)
        self.ControlButtons['clear_db'].setIconSize(QtCore.QSize(self.winsize_v * 0.16, self.winsize_h * 0.04))

        # close button
        self.CloseButton = QtGui.QCommandLinkButton(self)
        self.CloseButton.setGeometry(QtCore.QRect(self.winsize_h * 0.95, self.winsize_v * 0.01, self.winsize_v * 0.045, self.winsize_h * 0.03))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "exit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.02))
        #
        self.laser_port = QtGui.QLineEdit(self)
        self.laser_port.setGeometry(QtCore.QRect(self.winsize_h * 0.33, self.winsize_v * 0.47, self.winsize_h * 0.1, self.winsize_v * 0.04))

        self.imu_port = QtGui.QLineEdit(self)
        self.imu_port.setGeometry(QtCore.QRect(self.winsize_h * 0.67, self.winsize_v * 0.255, self.winsize_h * 0.1, self.winsize_v * 0.04))

        self.ecg_port = QtGui.QLineEdit(self)
        self.ecg_port.setGeometry(QtCore.QRect(self.winsize_h * 0.6, self.winsize_v * 0.61, self.winsize_h * 0.1, self.winsize_v * 0.04))

        self.laser_sample = QtGui.QLineEdit(self)
        self.laser_sample.setGeometry(QtCore.QRect(self.winsize_h * 0.33, self.winsize_v * 0.53, self.winsize_h * 0.1, self.winsize_v * 0.04))

        self.imu_sample = QtGui.QLineEdit(self)
        self.imu_sample.setGeometry(QtCore.QRect(self.winsize_h * 0.67, self.winsize_v * 0.32, self.winsize_h * 0.1, self.winsize_v * 0.04))

        self.ecg_sample = QtGui.QLineEdit(self)
        self.ecg_sample.setGeometry(QtCore.QRect(self.winsize_h * 0.6, self.winsize_v * 0.66, self.winsize_h * 0.1, self.winsize_v * 0.04))

        self.id_robot = QtGui.QLineEdit(self)
        self.id_robot.setGeometry(QtCore.QRect(self.winsize_h * 0.285, self.winsize_v * 0.32, self.winsize_h * 0.12, self.winsize_v * 0.04))

        #set internal signals
        self.set_signals()

    #set internal signals method
    def set_signals(self):
        self.ControlButtons['apply'].clicked.connect(self.apply_button)
        self.onData.connect(self.close)

    #method called when apply button is pressed
    def apply_button(self):
        if not (self.laser_port.text() == '') and not (self.imu_port.text() == '') and not (self.ecg_port.text() == '') and not (self.laser_sample.text() == '') and not (self.imu_sample.text() == '') and not (self.ecg_sample.text() == '') and not (self.id_robot.text() == ''):
            self.inf_settings['laser_port'] = str(self.laser_port.text())
            self.inf_settings['imu_port'] = str(self.imu_port.text())
            self.inf_settings['ecg_port'] = str(self.ecg_port.text())
            self.inf_settings['laser_sample'] = str(self.laser_sample.text())
            self.inf_settings['imu_sample'] = str(self.imu_sample.text())
            self.inf_settings['ecg_sample'] = str(self.ecg_sample.text())
            self.inf_settings['IpRobot'] = str(self.id_robot.text())
            #emit signal on data received
            self.onData.emit()
        else:
            #emit signal on empty field left
            self.onEmptyField.emit()



def main():
    app = QtGui.QApplication(sys.argv)
    GUI = SettingsWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
