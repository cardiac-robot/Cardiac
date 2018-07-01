import sys
#import os
from PyQt4 import QtGui, QtCore

class LogInWin(QtGui.QMainWindow):
    onEmptyField = QtCore.pyqtSignal()
    onData = QtCore.pyqtSignal()
    onRegistered = QtCore.pyqtSignal()
    onNotRegistered = QtCore.pyqtSignal()

    def __init__(self,ProjectHandler):
        super(LogInWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.65
        self.init_ui()
        self.CloseButton.clicked.connect(self.close_button)


    def init_ui(self):
        self.setWindowTitle('Log In')
        self.winsize_h = int(self.screen_h * self.r_size)
        self.winsize_v = int(self.screen_v * self.r_size)
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2),self.winsize_h, self.winsize_v)

        ## background label
        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap( self.PH.paths["img"] + "LogIn_background.png"))
        self.label_background.setScaledContents(True)

        ## Buttons
        self.submit = QtGui.QCommandLinkButton(self)
        self.submit.setGeometry(self.winsize_h * 0.39, self.winsize_v * 0.65, self.winsize_v * 0.4,self.winsize_h * 0.05)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap( self.PH.paths["img"] + "submit.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.submit.setIcon(icon)
        self.submit.setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.037))

        self.CloseButton = QtGui.QCommandLinkButton(self)
        self.CloseButton.setGeometry(QtCore.QRect(self.winsize_h * 0.95, self.winsize_v * 0.01, self.winsize_v * 0.045, self.winsize_h * 0.03))
        self.CloseButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "exit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.02))

        ## Line Edit
        self.id_text = QtGui.QLineEdit(self)
        self.id_text.setGeometry(QtCore.QRect(self.winsize_h * 0.395, self.winsize_v * 0.49, self.winsize_v * 0.37, self.winsize_h * 0.05))

        self.set_signals()

    def close_button(self):
        self.close()

    def set_signals(self):
        self.submit.clicked.connect(self.submit_button)

    def submit_button(self):
        if not (str(self.id_text.text()) == ""):
            self.id = str(self.id_text.text())
            #self.a = self.id.isalpha()
            #if (self.a == False):
            #    print(self.id)
            print type(self.id)
            self.onData.emit()
        else:
            self.onEmptyField.emit()

        self.close()


def main():
    app = QtGui.QApplication(sys.argv)
    GUI = LogInWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
