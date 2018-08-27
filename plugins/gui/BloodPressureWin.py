# -*- coding: utf-8 -
from PyQt4 import QtCore, QtGui

#%% Therapy window
class BloodPressureWin(QtGui.QMainWindow):
    onValue         = QtCore.pyqtSignal()
    onStartTherapy  = QtCore.pyqtSignal()
    onFinishTherapy = QtCore.pyqtSignal()

    def __init__(self, ProjectHandler):
        super(BloodPressureWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        self.init_ui(self)

        self.bp = {}


    def init_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #Resizing Mainwindow to a percentage of the total...
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)
        #Eliminating window's resize options.
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #%% Background
        self.label_background=QtGui.QLabel(self.centralwidget)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.PH.paths['img'] + "background_pressure.png"))
        self.label_background.setScaledContents(True)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(80)
        self.systolic_spin=QtGui.QSpinBox(self.centralwidget)
        self.systolic_spin.setFont(font)
        self.systolic_spin.setGeometry(QtCore.QRect(int(self.winsize_h*0.2),int(self.winsize_v*0.4),int(self.winsize_h*0.1),int(self.winsize_v*0.1)))
        self.systolic_spin.setRange(0,300)
        self.systolic_spin.setValue(90)
        self.diastolic_spin=QtGui.QSpinBox(self.centralwidget)
        self.diastolic_spin.setFont(font)
        self.diastolic_spin.setGeometry(QtCore.QRect(int(self.winsize_h*0.7),int(self.winsize_v*0.4),int(self.winsize_h*0.1),int(self.winsize_v*0.1)))
        self.diastolic_spin.setRange(0,300)
        self.diastolic_spin.setValue(60)
        #%%
        self.acquire_button=self.create_textured_button([0.4,0.6,0.2,0.2], self.PH.paths['img'] + "submit_icon2.png")
        #%%exit button
        self.exit_button=self.create_textured_button([0.95,0.02,0.035,0.035], self.PH.paths['img'] + "exit_icon.png")
        #%%
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #%% The following method creates a button and its correspondent label texture.
        #run signals
        self.set_signals()

    def set_signals(self):
        self.acquire_button['button'].clicked.connect(self.get_value)

    def create_textured_button(self,relative_geometry,texture_dir):
        directory={}
        directory['geometry']=int(self.winsize_h*relative_geometry[0]),int(self.winsize_v*relative_geometry[1]),int(self.winsize_h*relative_geometry[2]),int(self.winsize_h*relative_geometry[3])
        directory['label']=QtGui.QLabel(self.centralwidget)
        directory['label'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
        directory['label'].setPixmap(QtGui.QPixmap(texture_dir))
        directory['label'].setScaledContents(True)
        directory['button']=QtGui.QCommandLinkButton(self.centralwidget)
        directory['button'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
        directory['button'].setIconSize(QtCore.QSize(0, 0))
        return directory

    def get_value(self):
        self.bp = {'systolic': self.systolic_spin.value(), 'diastolic' : self.diastolic_spin.value()}
        self.onValue.emit()

    def close_connect(self, f):
        self.exit_button['button'].clicked.connect(f)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("(MainWindow", "CardiacSAR"))
