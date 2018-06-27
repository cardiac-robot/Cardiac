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
        self.CloseButton.clicked.connect(self.close_button)
        #self.cancel.clicked.connect(self.cancel_button)

    def init_ui(self):
        self.setWindowTitle('Setting')
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)
        #buttons dict
        self.ControlButtons = {}
        #apply changes button
        self.ControlButtons['apply'] = QtGui.QPushButton(self)
        self.ControlButtons['apply'].setGeometry(QtCore.QRect(self.winsize_v*0.51, self.winsize_h*0.38, self.winsize_v*0.33, self.winsize_h*0.08))
        self.ControlButtons['apply'].setText("Apply")
        #cancel button
        self.ControlButtons['cancel'] = QtGui.QPushButton(self)
        self.ControlButtons['cancel'].setGeometry(QtCore.QRect(self.winsize_v*0.951, self.winsize_h*0.38, self.winsize_v*0.33, self.winsize_h*0.08))
        self.ControlButtons['cancel'].setText("Cancel")

        self.CloseButton = QtGui.QCommandLinkButton(self)
        self.CloseButton.setGeometry(QtCore.QRect(self.winsize_h * 0.95, self.winsize_v * 0.01, self.winsize_v * 0.045, self.winsize_h * 0.03))
        self.CloseButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "exit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(self.winsize_v * 0.3, self.winsize_h * 0.14))
        #LABELS
        #port label
        self.port = QtGui.QLabel(self)
        self.port.setGeometry(QtCore.QRect(self.winsize_h*0.351, self.winsize_v*0.1, self.winsize_v*0.1, self.winsize_h*0.1))
        self.port.setText("Port:")

        self.sample = QtGui.QLabel(self)
        self.sample.setGeometry(QtCore.QRect(self.winsize_h*0.61, self.winsize_v*0.1, self.winsize_v*0.1, self.winsize_h*0.1))
        self.sample.setText("Sample:")

        self.laser = QtGui.QLabel(self)
        self.laser.setGeometry(QtCore.QRect(self.winsize_h*0.21, self.winsize_v*0.2, self.winsize_v*0.1, self.winsize_h*0.1))
        self.laser.setText("Laser:")

        self.imu = QtGui.QLabel(self)
        self.imu.setGeometry(QtCore.QRect(self.winsize_h*0.21, self.winsize_v*0.3, self.winsize_v*0.1, self.winsize_h*0.1))
        self.imu.setText("imu:")

        self.ecg = QtGui.QLabel(self)
        self.ecg.setGeometry(QtCore.QRect(self.winsize_h*0.21, self.winsize_v*0.4, self.winsize_v*0.1, self.winsize_h*0.1))
        self.ecg.setText("ECG:")

        self.ip = QtGui.QLabel(self)
        self.ip.setGeometry(QtCore.QRect(self.winsize_h*0.351, self.winsize_v*0.5, self.winsize_v*0.1, self.winsize_h*0.1))
        self.ip.setText("IP Robot:")

        self.laser_port = QtGui.QLineEdit(self)
        self.laser_port.setGeometry(QtCore.QRect(self.winsize_h*0.31, self.winsize_v*0.26, self.winsize_h*0.15, self.winsize_v*0.05))

        self.imu_port = QtGui.QLineEdit(self)
        self.imu_port.setGeometry(QtCore.QRect(self.winsize_h*0.31, self.winsize_v*0.36, self.winsize_h*0.15, self.winsize_v*0.05))

        self.ecg_port = QtGui.QLineEdit(self)
        self.ecg_port.setGeometry(QtCore.QRect(self.winsize_h*0.31, self.winsize_v*0.46, self.winsize_h*0.15, self.winsize_v*0.05))

        self.laser_sample = QtGui.QLineEdit(self)
        self.laser_sample.setGeometry(QtCore.QRect(self.winsize_h*0.551, self.winsize_v*0.26, self.winsize_h*0.15, self.winsize_v*0.05))

        self.imu_sample = QtGui.QLineEdit(self)
        self.imu_sample.setGeometry(QtCore.QRect(self.winsize_h*0.551, self.winsize_v*0.36, self.winsize_h*0.15, self.winsize_v*0.05))

        self.ecg_sample = QtGui.QLineEdit(self)
        self.ecg_sample.setGeometry(QtCore.QRect(self.winsize_h*0.551, self.winsize_v*0.46, self.winsize_h*0.15, self.winsize_v*0.05))

        self.id_robot = QtGui.QLineEdit(self)
        self.id_robot.setGeometry(QtCore.QRect(self.winsize_h*0.421, self.winsize_v*0.56, self.winsize_h*0.15, self.winsize_v*0.05))

        #set internal signals
        self.set_signals()

    def close_button(self):
        self.close()
        
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
