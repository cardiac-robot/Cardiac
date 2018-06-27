import sys

from PyQt4 import QtGui, QtCore


class RegisterWin(QtGui.QMainWindow):
    #set signals
    onEmptyField       = QtCore.pyqtSignal()
    onData             = QtCore.pyqtSignal()
    onAlreadyRegistered = QtCore.pyqtSignal()

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
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)

        self.label_background = QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0, 0, self.winsize_h, self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap( self.PH.paths["img"] + "Register_background.png"))
        self.label_background.setScaledContents(True)

        self.controlbuttons_reg = {}

        self.controlbuttons_reg['submit'] = QtGui.QPushButton('Submit', self)
        self.controlbuttons_reg["submit"].setGeometry(self.winsize_v*0.5, self.winsize_h*0.38, self.winsize_v*0.33, self.winsize_h*0.08)

        self.controlbuttons_reg['Cancel'] = QtGui.QPushButton('Cancel', self)
        self.controlbuttons_reg["Cancel"].setGeometry(self.winsize_v*0.95, self.winsize_h*0.38, self.winsize_v*0.33, self.winsize_h*0.08)

        self.name = QtGui.QLabel(self)
        self.name.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.035, self.winsize_v*0.1, self.winsize_h*0.1))
        self.name.setText('Name:')
        self.age = QtGui.QLabel(self)
        self.age.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.08, self.winsize_v*0.12, self.winsize_h*0.1))
        self.age.setText('Edad:')
        self.gender = QtGui.QLabel(self)
        self.gender.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.115, self.winsize_v*0.1, self.winsize_h*0.1))
        self.gender.setText('Gender:')
        self.height = QtGui.QLabel(self)
        self.height.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.15, self.winsize_v*0.1, self.winsize_h*0.1))
        self.height.setText('Height:')
        self.weight = QtGui.QLabel(self)
        self.weight.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.185, self.winsize_v*0.1, self.winsize_h*0.1))
        self.weight.setText('Weigth:')
        self.height_c = QtGui.QLabel(self)
        self.height_c.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.217, self.winsize_v*0.2, self.winsize_h*0.1))
        self.height_c.setText('Crotch height:')
        self.id = QtGui.QLabel(self)
        self.id.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.25, self.winsize_v*0.1, self.winsize_h*0.1))
        self.id.setText('ID:')
        self.patology = QtGui.QLabel(self)
        self.patology.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.285, self.winsize_v*0.1, self.winsize_h*0.1))
        self.patology.setText('Patology:')

        self.controllabels = {}
        self.controllabels['name'] = QtGui.QLineEdit(self)
        self.controllabels['name'].setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.065, self.winsize_v*0.55, self.winsize_h*0.03))
        self.controllabels['age'] = QtGui.QLineEdit(self)
        self.controllabels['age'].setGeometry(QtCore.QRect(self.winsize_v*0.75, self.winsize_h*0.115, self.winsize_v*0.55, self.winsize_h*0.03))
        self.controllabels['height'] = QtGui.QLineEdit(self)
        self.controllabels['height'].setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.182, self.winsize_v*0.1, self.winsize_h*0.03))
        self.controllabels['weight'] = QtGui.QLineEdit(self)
        self.controllabels['weight'].setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.22, self.winsize_v*0.1, self.winsize_h*0.03))
        self.controllabels['height_c'] = QtGui.QLineEdit(self)
        self.controllabels['height_c'].setGeometry(QtCore.QRect(self.winsize_v*0.75, self.winsize_h*0.255, self.winsize_v*0.1, self.winsize_h*0.029))
        self.controllabels['id'] = QtGui.QLineEdit(self)
        self.controllabels['id'].setGeometry(QtCore.QRect(self.winsize_v*0.65, self.winsize_h*0.285, self.winsize_v*0.25, self.winsize_h*0.03))
        self.controllabels['patology']= QtGui.QLineEdit(self)
        self.controllabels['patology'].setGeometry(QtCore.QRect(self.winsize_v*0.72, self.winsize_h*0.32, self.winsize_v*0.3, self.winsize_h*0.030))

        self.female = QtGui.QRadioButton(self)
        self.female.setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.15, self.winsize_v*0.15, self.winsize_h*0.032))
        self.female.setText("Femenino")
        self.male = QtGui.QRadioButton(self)
        self.male.setGeometry(QtCore.QRect(self.winsize_v*0.85, self.winsize_h*0.15, self.winsize_v*0.15, self.winsize_h*0.032))
        self.male.setText("Masculino")
        #set internal signals
        self.set_signals()


    def set_signals(self):
        self.controlbuttons_reg['submit'].clicked.connect(self.submit_button)


    def submit_button(self):
        if not(self.controllabels['name'].text() =="")and not(self.controllabels['age'].text() =="") and not(self.controllabels['height'].text() =="") and not(self.controllabels['weight'].text() =="") and not(self.controllabels['height_c'].text() =="") and not(self.controllabels['id'].text() =="")and not(self.controllabels['patology'].text() ==""):
            if(str(self.controllabels['name'].text()).isalpha() == True) and (str(self.controllabels['age'].text()).isdigit() == True) and (str(self.controllabels['height'].text()).isdigit() == True) and (str(self.controllabels['weight'].text()).isdigit() == True) and (str(self.controllabels['height_c'].text()).isdigit() == True) and (str(self.controllabels['id'].text()).isdigit() == True) and (str(self.controllabels['patology'].text()).isalpha() == True):
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
            msgBox.setText('You must enter only letters in the name')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['age'].text()).isdigit() == True) and not(self.controllabels['age'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter only numbers in age')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['height'].text()).isdigit() == True) and not(self.controllabels['height'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter only numbers in height')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['weight'].text()).isdigit() == True) and not(self.controllabels['weight'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter only numbers in weight')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['height_c'].text()).isdigit() == True)and not(self.controllabels['height_c'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter only numbers in crotch height')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()

        if not (str(self.controllabels['id'].text()).isdigit() == True) and not (self.controllabels['id'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter only numbers in id')
            msgBox.setWindowTitle('Warning')
            ret = msgBox.exec_()


        if not (str(self.controllabels['patology'].text()).isalpha() == True) and not (self.controllabels['patology'].text() ==""):
            msgBox = QtGui.QMessageBox()
            msgBox.setText('You must enter only letters in patology')
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
