# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
#%% Therapy window
class EndQuestionWin(QtGui.QMainWindow):
    onSatisfaction = QtCore.pyqtSignal()
    onMotivation   = QtCore.pyqtSignal()
    onExit         = QtCore.pyqtSignal()
    onData         = QtCore.pyqtSignal()

    def __init__(self, ProjectHandler):
        super(EndQuestionWin, self).__init__()
        self.PH = ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.8
        #get setup
        self.setupUi(self)
        self.data = {"motivation" : None, "satisfaction": None}

        self.isMotivation = False
        self.isSatisfaction = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #Resizing Mainwindow to a percentage of the total...
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)

        MainWindow.resize(self.winsize_h,self.winsize_v)
        #Eliminating window's resize options.
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #%% Background
        self.label_background=QtGui.QLabel(self.centralwidget)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.PH.paths['img'] + "/background2.png"))
        self.label_background.setScaledContents(True)
        #%% first message label
        self.label_msg=QtGui.QLabel(self.centralwidget)
        self.label_msg.setGeometry(QtCore.QRect(int(self.winsize_h*0.1),int(self.winsize_v*0.1),int(self.winsize_h*0.8),int(self.winsize_v*0.1)))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(80)
        self.label_msg.setFont(font)
        self.label_msg.setTextFormat(QtCore.Qt.PlainText)
        self.label_msg.setAlignment(QtCore.Qt.AlignCenter)
        self.label_msg.setText('Que tan motivado te sientes para regresar de nuevo?')
        #%% second message label
        self.label_msg2=QtGui.QLabel(self.centralwidget)
        self.label_msg2.setGeometry(QtCore.QRect(int(self.winsize_h*0.1),int(self.winsize_v*0.5),int(self.winsize_h*0.8),int(self.winsize_v*0.1)))
        self.label_msg2.setFont(font)
        self.label_msg2.setTextFormat(QtCore.Qt.PlainText)
        self.label_msg2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_msg2.setText('Como te sentiste en la sesion?')
        #%%motivation
        self.motivation={}
        self.motivation['label']=QtGui.QLabel(self.centralwidget)
        self.motivation['label'].setGeometry(int(self.winsize_h*0.1),int(self.winsize_v*0.2),int(self.winsize_h*0.8),int(self.winsize_v*0.25))
        self.motivation['label'].setPixmap(QtGui.QPixmap(self.PH.paths['img'] + '/borg10.png'))
        self.motivation['label'].setScaledContents(True)

        self.motivation['label_inactive']=QtGui.QLabel(self.centralwidget)
        self.motivation['label_inactive'].setGeometry(int(self.winsize_h*0.1),int(self.winsize_v*0.2),int(self.winsize_h*0.8),int(self.winsize_v*0.25))
        self.motivation['label_inactive'].setPixmap(QtGui.QPixmap(self.PH.paths['img'] + '/borg10-lock.png'))
        self.motivation['label_inactive'].setScaledContents(True)
        self.motivation['label_inactive'].hide()
        self.motivation['widget']=QtGui.QWidget(self.centralwidget)
        self.motivation['widget'].setGeometry(int(self.winsize_h*0.1),int(self.winsize_v*0.2),int(self.winsize_h*0.8),int(self.winsize_v*0.25))
        self.motivation['layout']=QtGui.QHBoxLayout(self.motivation['widget'])
        self.motivation['layout'].setSpacing(0)
        self.motivation['layout'].setMargin(0)
        for i in range(10):
            self.motivation['borg'+str(i)]=QtGui.QCommandLinkButton(self.centralwidget)
            self.motivation['borg'+str(i)].setIconSize(QtCore.QSize(0, 0))
            self.motivation['borg'+str(i)].clicked.connect(self.acquire_motivation)
            self.motivation['layout'].addWidget(self.motivation['borg'+str(i)])
        #%% satisfaction
        self.satisfaction={}
        self.satisfaction['label']=QtGui.QLabel(self.centralwidget)
        self.satisfaction['label'].setGeometry(int(self.winsize_h*0.1),int(self.winsize_v*0.6),int(self.winsize_h*0.8),int(self.winsize_v*0.25))
        self.satisfaction['label'].setPixmap(QtGui.QPixmap(self.PH.paths['img'] + '/borg10.png'))
        self.satisfaction['label'].setScaledContents(True)
        self.satisfaction['label_inactive']=QtGui.QLabel(self.centralwidget)
        self.satisfaction['label_inactive'].setGeometry(int(self.winsize_h*0.1),int(self.winsize_v*0.6),int(self.winsize_h*0.8),int(self.winsize_v*0.25))
        self.satisfaction['label_inactive'].setPixmap(QtGui.QPixmap(self.PH.paths['img'] + '/borg10-lock.png'))
        self.satisfaction['label_inactive'].setScaledContents(True)
        self.satisfaction['label_inactive'].hide()
        self.satisfaction['widget']=QtGui.QWidget(self.centralwidget)
        self.satisfaction['widget'].setGeometry(int(self.winsize_h*0.1),int(self.winsize_v*0.6),int(self.winsize_h*0.8),int(self.winsize_v*0.25))
        self.satisfaction['layout']=QtGui.QHBoxLayout(self.satisfaction['widget'])
        self.satisfaction['layout'].setSpacing(0)
        self.satisfaction['layout'].setMargin(0)
        for i in range(10):
            self.satisfaction['borg'+str(i)]=QtGui.QCommandLinkButton(self.centralwidget)
            self.satisfaction['borg'+str(i)].setIconSize(QtCore.QSize(0, 0))
            self.satisfaction['borg'+str(i)].clicked.connect(self.acquire_satisfaction)
            self.satisfaction['layout'].addWidget(self.satisfaction['borg'+str(i)])
        #%%exit button
        self.exit_button=self.create_textured_button([0.95,0.02,0.035,0.035], self.PH.paths['img'] + "/exit_icon.png")
        self.exit_button['button'].hide()
        self.exit_button['label'].hide()
        #%%
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.set_signals()
        #%% The following method creates a button and its correspondent label texture.
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


    def set_signals(self):
        self.onExit.connect(self.unlock_exit)
        self.exit_button['button'].clicked.connect(self.close)

    def acquire_satisfaction(self):
        #Get which button emitted the signal
        button = self.sender()
        #Get the index of the button in the motivation layout.
        self.data['satisfaction'] = self.satisfaction['layout'].indexOf(button)
        #Lock the motivation widget.
        self.lock_satisfaction()
        self.isSatisfaction = True
        print self.isSatisfaction
        self.onExit.emit()

    def acquire_motivation(self):
        #Get which button emitted the signal
        button = self.sender()
        #Get the index of the button in the motivation layout.
        self.data['motivation'] = self.motivation['layout'].indexOf(button)
        #Lock the motivation widget.
        self.lock_motivation()
        self.isMotivation = True
        print self.isMotivation
        self.onExit.emit()

    def unlock_exit(self):
        if self.isMotivation and self.isSatisfaction:
            self.exit_button['button'].show()
            print('on Data emit')
            self.onData.emit()

    def lock_motivation(self):
        for i in range(10):
            self.motivation['borg'+str(i)].hide()
        self.motivation['label'].hide()
        self.motivation['label_inactive'].show()
    def unlock_motivation(self):
        for i in range(10):
            self.motivation['borg'+str(i)].show()
        self.motivation['label'].show()
        self.motivation['label_inactive'].hide()
    def lock_satisfaction(self):
        for i in range(10):
            self.satisfaction['borg'+str(i)].hide()
        self.satisfaction['label'].hide()
        self.satisfaction['label_inactive'].show()
    def unlock_satisfaction(self):
        for i in range(10):
            self.satisfaction['borg'+str(i)].show()
        self.satisfaction['label'].show()
        self.satisfaction['label_inactive'].hide()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CardiacSAR"))
