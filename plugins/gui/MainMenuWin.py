"""MAIN MENU GUI CODE"""
# -*- coding: utf-8 -*-import sys
import sys

from PyQt4 import QtGui, QtCore

from PyQt4.QtCore import*

from PyQt4.QtGui import*

import ctypes

class MainMenuWin(QtGui.QMainWindow):

    def __init__(self, project_Handler):
        super(MainMenuWin,self).__init__()
        self.project_Handler=project_Handler

        self.init_ui()

        ##Signals
        self.set_signals()


    def init_ui(self):
        #-------main config-------
        #Window title
        self.setWindowTitle("Main Menu Window")
        #Window size
        self.user32=ctypes.windll.user32
        self.screensize=self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1),
        #Resizing MainWindoe to a percentage of the total
        self.winsize_h=int(self.screensize[0])
        self.winsize_v=int(self.screensize[1])
        self.resize(self.winsize_h,self.winsize_v)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #setting backgroung image
        self.label_background=QtGui.QLabel(self)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.project_Handler.paths["img"]+ "/Window.png"))
        self.label_background.setScaledContents(True)
        #----------------------------------
        #-----------Buttons config----------
        #setting background user image
        self.start=QtGui.QLabel(self)
        self.start.setGeometry(QtCore.QRect(self.winsize_h*0.15,self.winsize_v*0.08,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon3=QtGui.QPixmap(self.project_Handler.paths["img"]+"/userbutton.png")
        Icon_resize3= Icon3.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.start.setPixmap(Icon_resize3)

        #setting background new user image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.40,self.winsize_v*0.08,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/newuserbutton.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting background start image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.65,self.winsize_v*0.08,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/startbutton.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting background stadistic image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.15,self.winsize_v*0.50,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/stadistbutt.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting background settings image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.40,self.winsize_v*0.50,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/settingsbutton.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting background new user image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.65,self.winsize_v*0.50,self.winsize_h*0.21 ,self.winsize_h*0.21))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/button.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.21 ,self.winsize_h*0.21,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)

        #setting background close image
        self.stop=QtGui.QLabel(self)
        self.stop.setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        Icon4=QtGui.QPixmap(self.project_Handler.paths["img"]+"/closebtn.png")
        Icon_resize5= Icon4.scaled(self.winsize_h*0.038 ,self.winsize_h*0.038,QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
        self.stop.setPixmap(Icon_resize5)


        self.controlButtons = {}
        #register button
        self.controlButtons['register'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['register'].setGeometry(QtCore.QRect(self.winsize_h*0.15,self.winsize_v*0.08,self.winsize_h*0.19 ,self.winsize_h*0.21))
        self.controlButtons['register'].setIconSize(QSize(0,0))
        #new register button
        self.controlButtons['newregister'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['newregister'].setGeometry(QtCore.QRect(self.winsize_h*0.40,self.winsize_v*0.08,self.winsize_h*0.19 ,self.winsize_h*0.21))
        self.controlButtons['newregister'].setIconSize(QSize(0,0))
        #start button
        self.controlButtons['start'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['start'].setGeometry(QtCore.QRect(self.winsize_h*0.65,self.winsize_v*0.08,self.winsize_h*0.19 ,self.winsize_h*0.21))
        self.controlButtons['start'].setIconSize(QSize(0,0))
        #stadistic button
        self.controlButtons['stadistic'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['stadistic'].setGeometry(QtCore.QRect(self.winsize_h*0.15,self.winsize_v*0.50,self.winsize_h*0.19 ,self.winsize_h*0.21))
        self.controlButtons['stadistic'].setIconSize(QSize(0,0))
        #setting button
        self.controlButtons['setting'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['setting'].setGeometry(QtCore.QRect(self.winsize_h*0.40,self.winsize_v*0.50,self.winsize_h*0.19 ,self.winsize_h*0.21))
        self.controlButtons['setting'].setIconSize(QSize(0,0))
        #setting button
        self.controlButtons['butt'] =QtGui.QCommandLinkButton(self)
        self.controlButtons['butt'].setGeometry(QtCore.QRect(self.winsize_h*0.65,self.winsize_v*0.50,self.winsize_h*0.19 ,self.winsize_h*0.21))
        self.controlButtons['butt'].setIconSize(QSize(0,0))


        #Close button
        self.controlButtons['close'] = QtGui.QCommandLinkButton(self)
        self.controlButtons['close'].setGeometry(QtCore.QRect(self.winsize_h*0.943,self.winsize_v*0.02,self.winsize_h*0.038 ,self.winsize_h*0.038))
        self.controlButtons['close'].setIconSize(QSize(0,0))


    #------------------------------------SIGNAL METHODS------------------------------------------------------------------------------
    def connectStartButton(self,f):
        self.controlButtons['start'].clicked.connect(f)
    def connectStopButton(self, f):
        self.controlButtons['stop'].clicked.connect(f)
    def connectNewRegisterButton(self, f):
        self.controlButtons['newregister'].clicked.connect(f)

    def connectCloseButton(self):
        self.controlButtons['close'].clicked.connect(self.close)

    def set_signals(self):
        self.connectCloseButton()




#def main():
    #app=QtGui.QApplication(sys.argv)
    #GUI=MainMenuWin()
    #sys.exit(app.exec_())
#A=main()

if __name__ == '__main__':
    app=QtGui.QApplication(sys.argv)
    GUI=MainMenuWin()
    sys.exit(app.exec_())
