import sys
#import os
from PyQt4 import QtGui, QtCore
#from ProjectHandler import ProjectHandler

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


    def init_ui(self):
        self.setWindowTitle('Log In')
        self.winsize_h = int(self.screen_h * self.r_size)
        self.winsize_v = int(self.screen_v * self.r_size)
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2),self.winsize_h, self.winsize_v)

        self.submit = QtGui.QPushButton('Submit',self)
        self.submit.setGeometry(self.winsize_h*0.39, self.winsize_v*0.45, self.winsize_v*0.4, self.winsize_h*0.08)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.submit.setFont(font)

        ## Labels
        self.id_label = QtGui.QLabel(self)
        self.id_label.setGeometry(QtCore.QRect(self.winsize_h * 0.4, self.winsize_v * 0.3, self.winsize_h * 0.15, self.winsize_v * 0.05))
        self.id_label.setText("ID:")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.id_label.setFont(font)

        ## Line Edit
        self.id_text = QtGui.QLineEdit(self)
        self.id_text.setGeometry(QtCore.QRect(self.winsize_h * 0.45, self.winsize_v * 0.3, self.winsize_h * 0.15, self.winsize_v * 0.05))

        self.set_signals()

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


def main():
    app = QtGui.QApplication(sys.argv)
    GUI = LogInWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
