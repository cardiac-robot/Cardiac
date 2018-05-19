# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore

class RecognitionWin(QtGui.QMainWindow):
    #signals
    onSuccess       = QtCore.pyqtSignal()
    onFailed        = QtCore.pyqtSignal()
    onRepeat        = QtCore.pyqtSignal()
    onData          = QtCore.pyqtSignal()
    onEmptyField    = QtCore.pyqtSignal()
    onConfirm       = QtCore.pyqtSignal()
    onRegistered    = QtCore.pyqtSignal()
    onNotRegistered = QtCore.pyqtSignal()

    def __init__(self, ProjectHandler):
        super(RecognitionWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        self.init_ui()
        #id variable
        self.id = ""

    def init_ui(self):
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)

        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)

        self.ControlButtons = {}
        #start recog button
        self.ControlButtons['StartRecog'] =  QtGui.QPushButton('Start Recognition',self)
        self.ControlButtons['StartRecog'].setGeometry(QtCore.QRect(self.winsize_v*0.11, self.winsize_h*0.1, self.winsize_v*0.5, self.winsize_h*0.3))
        #buttons for identity validation
        self.ControlButtons['Yes'] =  QtGui.QPushButton('SI',self)
        self.ControlButtons['Yes'].setGeometry(QtCore.QRect(self.winsize_v*0.8, self.winsize_h*0.4, self.winsize_v*0.2, self.winsize_h*0.1))
        self.ControlButtons['No'] =  QtGui.QPushButton('NO',self)
        self.ControlButtons['No'].setGeometry(QtCore.QRect(self.winsize_v*1.2, self.winsize_h*0.4, self.winsize_v*0.2, self.winsize_h*0.1))
        #id submit button
        self.ControlButtons['submit'] = QtGui.QPushButton('Submit',self)
        self.ControlButtons['submit'].setGeometry(self.winsize_h*0.39, self.winsize_v*0.45, self.winsize_v*0.4, self.winsize_h*0.08)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ControlButtons['submit'].setFont(font)
        ## Labels
        self.id_label = QtGui.QLabel(self)
        self.id_label.setGeometry(QtCore.QRect(self.winsize_h * 0.4, self.winsize_v * 0.3, self.winsize_h * 0.15, self.winsize_v * 0.05))
        self.id_label.setText("ID:")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.id_label.setFont(font)

        #Line Edit
        self.id_text = QtGui.QLineEdit(self)
        self.id_text.setGeometry(QtCore.QRect(self.winsize_h * 0.45, self.winsize_v * 0.3, self.winsize_h * 0.15, self.winsize_v * 0.05))

        self.set_initial_state()

        self. set_signals()

    def set_signals(self):
        self.ControlButtons['StartRecog'].clicked.connect(self.lock_recog_button)
        self.ControlButtons['submit'].clicked.connect(self.submit_button)
        self.ControlButtons['No'].clicked.connect(self.unlock_id_request)
        self.ControlButtons['Yes'].clicked.connect(self.onSuccess.emit)
        self.onConfirm.connect(self.unlock_confirmation)

    def set_initial_state(self):
        self.ControlButtons['StartRecog'].show()
        self.lock_confirmation()
        self.lock_id_request()

    def lock_recog_button(self):
        self.ControlButtons['StartRecog'].hide()

    def unlock_recog_button(self):
        self.ControlButtons['StartRecog'].show()

    def lock_confirmation(self):
        self.ControlButtons['Yes'].hide()
        self.ControlButtons['No'].hide()

    def unlock_confirmation(self):
        self.ControlButtons['Yes'].show()
        self.ControlButtons['No'].show()

    def lock_id_request(self):
        self.ControlButtons['submit'].hide()
        self.id_label.hide()
        self.id_text.hide()

    def unlock_id_request(self):
        self.ControlButtons['submit'].show()
        self.id_label.show()
        self.id_text.show()

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
    class ProjectHandler(object):
        def __init__(self):
            res = {'width': 1920, 'height': 1080}
            s = 'linux2'
            self.settings = {'res': res, 'sys': s}


    app = QtGui.QApplication(sys.argv)
    ProjectHandler = ProjectHandler()
    GUI = RecognitionWin(ProjectHandler = ProjectHandler)
    GUI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
