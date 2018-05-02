import sys

from PyQt4 import QtGui, QtCore

class RegisterWin(QtGui.QMainWindow):
    #set signals
    onEmptyField = QtCore.pyqtSignal()
    onData       = QtCore.pyqtSignal()

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

        self.controlbuttons_reg = {}

        self.controlbuttons_reg['submit'] = QtGui.QPushButton('Submit', self)
        self.controlbuttons_reg["submit"].setGeometry(self.winsize_v*0.5, self.winsize_h*0.38, self.winsize_v*0.33, self.winsize_h*0.08)

        self.controlbuttons_reg['Cancel'] = QtGui.QPushButton('Cancel', self)
        self.controlbuttons_reg["Cancel"].setGeometry(self.winsize_v*0.95, self.winsize_h*0.38, self.winsize_v*0.33, self.winsize_h*0.08)

        self.nombre = QtGui.QLabel(self)
        self.nombre.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.035, self.winsize_v*0.1, self.winsize_h*0.1))
        self.nombre.setText('Name:')
        self.age = QtGui.QLabel(self)
        self.age.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.08, self.winsize_v*0.12, self.winsize_h*0.1))
        self.age.setText('Edad:')
        self.genero = QtGui.QLabel(self)
        self.genero.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.115, self.winsize_v*0.1, self.winsize_h*0.1))
        self.genero.setText('Gender:')
        self.altura = QtGui.QLabel(self)
        self.altura.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.15, self.winsize_v*0.1, self.winsize_h*0.1))
        self.altura.setText('Height:')
        self.peso = QtGui.QLabel(self)
        self.peso.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.185, self.winsize_v*0.1, self.winsize_h*0.1))
        self.peso.setText('Weigth:')
        self.altura_entrepierna = QtGui.QLabel(self)
        self.altura_entrepierna.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.217, self.winsize_v*0.2, self.winsize_h*0.1))
        self.altura_entrepierna.setText('Crotch height:')
        self.cedula = QtGui.QLabel(self)
        self.cedula.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.25, self.winsize_v*0.1, self.winsize_h*0.1))
        self.cedula.setText('ID:')
        self.patologia = QtGui.QLabel(self)
        self.patologia.setGeometry(QtCore.QRect(self.winsize_v*0.6, self.winsize_h*0.285, self.winsize_v*0.1, self.winsize_h*0.1))
        self.patologia.setText('Patology:')

        self.controllabels = {}
        self.controllabels['nombre'] = QtGui.QLineEdit(self)
        self.controllabels['nombre'].setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.065, self.winsize_v*0.55, self.winsize_h*0.03))
        self.controllabels['edad'] = QtGui.QLineEdit(self)
        self.controllabels['edad'].setGeometry(QtCore.QRect(self.winsize_v*0.75, self.winsize_h*0.115, self.winsize_v*0.55, self.winsize_h*0.03))
        self.controllabels['altura'] = QtGui.QLineEdit(self)
        self.controllabels['altura'].setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.182, self.winsize_v*0.1, self.winsize_h*0.03))
        self.controllabels['peso'] = QtGui.QLineEdit(self)
        self.controllabels['peso'].setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.22, self.winsize_v*0.1, self.winsize_h*0.03))
        self.controllabels['al_entrepierna'] = QtGui.QLineEdit(self)
        self.controllabels['al_entrepierna'].setGeometry(QtCore.QRect(self.winsize_v*0.75, self.winsize_h*0.255, self.winsize_v*0.1, self.winsize_h*0.029))
        self.controllabels['cedula'] = QtGui.QLineEdit(self)
        self.controllabels['cedula'].setGeometry(QtCore.QRect(self.winsize_v*0.65, self.winsize_h*0.285, self.winsize_v*0.25, self.winsize_h*0.03))
        self.controllabels['patologia']= QtGui.QLineEdit(self)
        self.controllabels['patologia'].setGeometry(QtCore.QRect(self.winsize_v*0.72, self.winsize_h*0.32, self.winsize_v*0.3, self.winsize_h*0.030))

        self.femenino = QtGui.QRadioButton(self)
        self.femenino.setGeometry(QtCore.QRect(self.winsize_v*0.7, self.winsize_h*0.15, self.winsize_v*0.15, self.winsize_h*0.032))
        self.femenino.setText("Femenino")
        self.masculino = QtGui.QRadioButton(self)
        self.masculino.setGeometry(QtCore.QRect(self.winsize_v*0.85, self.winsize_h*0.15, self.winsize_v*0.15, self.winsize_h*0.032))
        self.masculino.setText("Masculino")

    def submit_button(self):
        if not(self.controllabels['name'].text() =="")and not(self.controllabels['age'].text() =="") and not(self.controllabels['height'].text() =="") and not(self.controllabels['weight'].text() =="") and not(self.controllabels['height_c'].text() =="") and not(self.controllabels['id'].text() =="")and not(self.controllabels['patology'].text() ==""):
            self.info_reg['name'] = str(self.controllabels['nombre'].text())
            self.info_reg['age'] = str(self.controllabels['edad'].text())
            self.info_reg['height'] = str(self.controllabels['altura'].text())
            self.info_reg['weight'] = str(self.controllabels['peso'].text())
            self.info_reg['height_c'] = str(self.controllabels['al_entrepierna'].text())
            self.info_reg['id'] = str(self.controllabels['cedula'].text())
            self.info_reg['patology'] = str(self.controllabels['patologia'].text())
            self.onData.emit()
        else:
            self.onEmptyField.emit()




def main():
    app = QtGui.QApplication(sys.argv)
    GUI = RegisterWin(ProjectHandler())
    GUI.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
