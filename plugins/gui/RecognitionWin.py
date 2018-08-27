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
    onStartTherapy  = QtCore.pyqtSignal()

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

        ## background label
        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.PH.paths["img"] + "Blue_background.png"))
        self.label_background.setScaledContents(True)


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
        # close button
        self.ControlButtons['CloseButton'] = QtGui.QCommandLinkButton(self)
        self.ControlButtons['CloseButton'].setGeometry(QtCore.QRect(self.winsize_h * 0.95, self.winsize_v * 0.01, self.winsize_v * 0.045, self.winsize_h * 0.03))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "exit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ControlButtons['CloseButton'].setIcon(icon)
        self.ControlButtons['CloseButton'].setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.02))

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

        #call initial state method
        self.set_initial_state()
        #set internal signals
        self. set_signals()


    #internal signal method
    def set_signals(self):
        #lock button when pressed
        self.ControlButtons['StartRecog'].clicked.connect(self.lock_recog_button)
        #connect to callback function, submit_button to validate data submitted
        self.ControlButtons['submit'].clicked.connect(self.submit_button)
        #connect to callback function to unlock request widget
        self.ControlButtons['No'].clicked.connect(self.unlock_id_request)
        #connect to emit onSuccess signal when yes is pressed
        self.ControlButtons['Yes'].clicked.connect(self.onSuccess.emit)
        #connect to unlock confirmation widget
        self.onConfirm.connect(self.unlock_confirmation)
        #connect to unlock id request when recognition has failed
        self.onFailed.connect(self.unlock_id_request)

    #set the initial window configuration state
    def set_initial_state(self):
        #display recognition button
        self.ControlButtons['StartRecog'].show()
        #lock confirmation buttons
        self.lock_confirmation()
        #lock id requests
        self.lock_id_request()

    #widget control function
    def lock_recog_button(self):
        self.ControlButtons['StartRecog'].hide()

    #widget control function
    def unlock_recog_button(self):
        self.ControlButtons['StartRecog'].show()

    #widget control function
    def lock_confirmation(self):
        self.ControlButtons['Yes'].hide()
        self.ControlButtons['No'].hide()

    #widget control function
    def unlock_confirmation(self):
        self.ControlButtons['Yes'].show()
        self.ControlButtons['No'].show()

    #widget control function
    def lock_id_request(self):
        self.ControlButtons['submit'].hide()
        self.id_label.hide()
        self.id_text.hide()

    #widget control function
    def unlock_id_request(self):
        self.ControlButtons['submit'].show()
        self.id_label.show()
        self.id_text.show()

    #callback function for id validation
    def submit_button(self):
        #validate empty field
        if not (str(self.id_text.text()) == ""):
            self.id = str(self.id_text.text())
            print type(self.id)
            self.onData.emit()
            self.hide()
        else:
            self.onEmptyField.emit()






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
