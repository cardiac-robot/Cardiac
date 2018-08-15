import sys

from PyQt4 import QtGui, QtCore


class RegisterWin(QtGui.QMainWindow):
    #set signals
    onEmptyField       = QtCore.pyqtSignal()
    onData             = QtCore.pyqtSignal()
    onAlreadyRegistered = QtCore.pyqtSignal()
    onNotRegistered    = QtCore.pyqtSignal()

    def __init__(self,ProjectHandler):
        super(RegisterWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        self.init_ui()
        #info variable
        self.info_reg = {}

    def init_ui(self):
        self.setWindowTitle('Sign in')

        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtGui.QWidget(self)
        self.resize(self.winsize_h,self.winsize_v)
        #self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)

        ## Background label
        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap( self.PH.paths["img"] + "Register_background.png"))
        self.label_background.setScaledContents(True)

        ## Buttons
        self.controlbuttons_reg = {}

        self.controlbuttons_reg['submit'] = QtGui.QCommandLinkButton(self)
        self.controlbuttons_reg["submit"].setGeometry(self.winsize_h * 0.65, self.winsize_v * 0.82,self.winsize_v * 0.27, self.winsize_h * 0.06)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "submit_register.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.controlbuttons_reg['submit'].setIcon(icon)
        self.controlbuttons_reg['submit'].setIconSize(QtCore.QSize(self.winsize_v * 0.25, self.winsize_h * 0.05))

        self.controlbuttons_reg['Cancel'] = QtGui.QCommandLinkButton(self)
        self.controlbuttons_reg["Cancel"].setGeometry(self.winsize_h * 0.78, self.winsize_v * 0.82,self.winsize_v * 0.25, self.winsize_h * 0.06)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "cancel_reg.png"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.controlbuttons_reg['Cancel'].setIcon(icon)
        self.controlbuttons_reg['Cancel'].setIconSize(QtCore.QSize(self.winsize_v * 0.25, self.winsize_h * 0.05))

        self.CloseButton = QtGui.QCommandLinkButton(self)
        self.CloseButton.setGeometry(QtCore.QRect(self.winsize_h * 0.95, self.winsize_v * 0.01, self.winsize_v * 0.045, self.winsize_h * 0.03))
        self.CloseButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.PH.paths["img"] + "exit_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CloseButton.setIcon(icon)
        self.CloseButton.setIconSize(QtCore.QSize(self.winsize_v * 0.4, self.winsize_h * 0.02))


        ## Line Edit
        self.controllabels = {}
        self.controllabels['name'] = QtGui.QLineEdit(self)
        self.controllabels['name'].setGeometry(QtCore.QRect(self.winsize_h * 0.62, self.winsize_v * 0.23, self.winsize_v * 0.575, self.winsize_h * 0.03))

        self.controllabels['age'] = QtGui.QLineEdit(self)
        self.controllabels['age'].setGeometry(QtCore.QRect(self.winsize_h * 0.62, self.winsize_v * 0.36, self.winsize_v * 0.1, self.winsize_h * 0.03))

        self.controllabels['height'] = QtGui.QLineEdit(self)
        self.controllabels['height'].setGeometry(QtCore.QRect(self.winsize_h * 0.62, self.winsize_v * 0.62, self.winsize_v * 0.1, self.winsize_h * 0.03))

        self.controllabels['weight'] = QtGui.QLineEdit(self)
        self.controllabels['weight'].setGeometry(QtCore.QRect(self.winsize_h * 0.8, self.winsize_v * 0.62, self.winsize_v * 0.1, self.winsize_h * 0.03))

        self.controllabels['height_c'] = QtGui.QLineEdit(self)
        self.controllabels['height_c'].setGeometry(QtCore.QRect(self.winsize_h * 0.62, self.winsize_v * 0.75, self.winsize_v * 0.1, self.winsize_h * 0.029))

        self.controllabels['id'] = QtGui.QLineEdit(self)
        self.controllabels['id'].setGeometry(QtCore.QRect(self.winsize_h * 0.8, self.winsize_v * 0.36, self.winsize_v * 0.25, self.winsize_h * 0.029))

        self.controllabels['patology'] = QtGui.QLineEdit(self)
        self.controllabels['patology'].setGeometry(QtCore.QRect(self.winsize_h * 0.8, self.winsize_v * 0.75, self.winsize_v * 0.25, self.winsize_h * 0.029))

        self.female = QtGui.QRadioButton(self)
        self.female.setGeometry(QtCore.QRect(self.winsize_h * 0.62, self.winsize_v * 0.49, self.winsize_v * 0.21, self.winsize_h * 0.032))
        self.female.setText("Femenino")

        self.male = QtGui.QRadioButton(self)
        self.male.setGeometry(QtCore.QRect(self.winsize_h * 0.75, self.winsize_v * 0.49, self.winsize_v * 0.21, self.winsize_h * 0.032))
        self.male.setText("Masculino")

        #set internal signals
        self.set_signals()


    def set_signals(self):
        self.controlbuttons_reg['submit'].clicked.connect(self.submit_button)


    def submit_button(self):
        if not(self.controllabels['name'].text() =="")and not(self.controllabels['age'].text() =="") and not(self.controllabels['height'].text() =="") and not(self.controllabels['weight'].text() =="") and not(self.controllabels['height_c'].text() =="") and not(self.controllabels['id'].text() =="")and not(self.controllabels['patology'].text() ==""):
            if(" " in str(self.controllabels['name'].text())== True ) and (str(self.controllabels['name'].text()).isdigit() == False) and (str(self.controllabels['age'].text()).isdigit() == True) and (str(self.controllabels['height'].text()).isdigit() == True) and (str(self.controllabels['weight'].text()).isdigit() == True) and (str(self.controllabels['height_c'].text()).isdigit() == True) and (str(self.controllabels['id'].text()).isdigit() == True) and (str(self.controllabels['patology'].text()).isalpha() == True):
                self.info_reg['name'] = str(self.controllabels['name'].text())
                self.info_reg['age'] = str(self.controllabels['age'].text())
                self.info_reg['height'] = str(self.controllabels['height'].text())
                self.info_reg['weight'] = str(self.controllabels['weight'].text())
                self.info_reg['height_c'] = str(self.controllabels['height_c'].text())
                self.info_reg['id'] = str(self.controllabels['id'].text())
                self.info_reg['patology'] = str(self.controllabels['patology'].text())
                self.onData.emit()
                print(self.info_reg)


        if not (str(self.controllabels['name'].text()).isalpha() == True) and not (self.controllabels['name'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Ingrese solo letras nombre')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['age'].text()).isdigit() == True) and not(self.controllabels['age'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Ingrese solo numeros')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['height'].text()).isdigit() == True) and not(self.controllabels['height'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Ingrese solo numeros')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['weight'].text()).isdigit() == True) and not(self.controllabels['weight'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Ingrese solo numeros')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['height_c'].text()).isdigit() == True)and not(self.controllabels['height_c'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Ingrese solo numeros')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['id'].text()).isdigit() == True) and not (self.controllabels['id'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Ingrese solo numeros')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()


        if not (str(self.controllabels['patology'].text()).isalpha() == True) and not (self.controllabels['patology'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('Ingrese solo letras')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        else:
            self.onEmptyField.emit()





def main():
    app = QtGui.QApplication(sys.argv)
    GUI = RegisterWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
