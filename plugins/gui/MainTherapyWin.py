# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui


#%% Therapy window
class TherapyWin(QtGui.QMainWindow):
    #set signals
    onBorg         = QtCore.pyqtSignal()
    onBorgReceive  = QtCore.pyqtSignal()
    onSensorUpdate = QtCore.pyqtSignal()
    onAlert        = QtCore.pyqtSignal()
    onThumbs       = QtCore.pyqtSignal()



    def __init__(self, settings = {"mode": 1, "user":"jonathan casas"}, ProjectHandler = None):
        super(TherapyWin,self).__init__()
        #load settings
        self.settings = settings
        self.PH =ProjectHandler
        #get screen size
        self.screen_h = self.PH.settings['res']['width']
        self.screen_v = self.PH.settings['res']['height']
        #set relative size
        self.r_size = 0.7
        #get setup
        self.setupUi(self)
        #self.show()
        #initialize display variables
        self.data_cadence = 0
        self.data_speed = 0
        self.data_imu = 0
        self.data_step_length = 0
        self.data_ecg = 0
        self.borg_data =0


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #Resizing Mainwindow to a percentage of the total...
        self.winsize_h=int(self.screen_h * self.r_size)
        self.winsize_v=int(self.screen_v* self.r_size)
        #
        self.setGeometry(self.screen_h / 2 - (self.winsize_h / 2), self.screen_v / 2 - (self.winsize_v / 2), self.winsize_h, self.winsize_v)
        #Eliminating window's resize options.
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #Defining a font
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(80)
        #%% Background
        self.label_background=QtGui.QLabel(self.centralwidget)
        self.label_background.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background.setPixmap(QtGui.QPixmap(self.PH.paths['img'] + "background.jpg"))
        self.label_background.setScaledContents(True)
        #%% Background cooldown phase
        self.label_background2=QtGui.QLabel(self.centralwidget)
        self.label_background2.setGeometry(QtCore.QRect(0,0,self.winsize_h,self.winsize_v))
        self.label_background2.setPixmap(QtGui.QPixmap(self.PH.paths['img'] + "background_blue.png"))
        self.label_background2.setScaledContents(True)

        #%%LCD Display
        self.time_lcd=QtGui.QLCDNumber(self.centralwidget)
        self.time_lcd.setGeometry(QtCore.QRect(0.375*self.winsize_h,0.87*self.winsize_v,0.1*self.winsize_h,0.05*self.winsize_h))
        self.time_lcd.display("00:00")
        #%%exit button
        self.exit_button = self.create_textured_button([0.95,0.02,0.035,0.035],self.PH.paths['img'] + "exit_icon.png")
        #%% bord_description
        self.borg_description=QtGui.QLabel(self.centralwidget)
        self.borg_description.setGeometry(QtCore.QRect(0.04*self.winsize_h,0.15*self.winsize_v,0.91*self.winsize_h,0.12*self.winsize_h))
        self.borg_description.setPixmap(QtGui.QPixmap(self.PH.paths['img'] + "borg_description.png"))
        self.borg_description.setScaledContents(True)
        #%% borg 6-9 layout
        self.borg69b=self.create_textured_borg([0.04,0.4,0.2,0.2],self.PH.paths['img'] + "borg69b.png",self.PH.paths['img'] + "borg69_lock.png")
        #%% borg 10-13 layout
        self.borg1013b=self.create_textured_borg([0.28,0.4,0.2,0.2],self.PH.paths['img']+"borg1013b.png",self.PH.paths['img'] + "borg1013_lock.png")
        #%% borg 14-17 layout
        self.borg1417b=self.create_textured_borg([0.52,0.4,0.2,0.2],self.PH.paths['img']+"borg1417b.png",self.PH.paths['img'] + "borg1417_lock.png")
        #%% borg 18-20 layout
        self.borg1820b=self.create_textured_borg([0.76,0.4,0.2,0.2],self.PH.paths['img']+"borg1820b.png",self.PH.paths['img'] + "borg1820_lock.png",flag=False)

        #%% dinamic labels layout data display
        self.label_show={}
        self.label_show['label_back']=QtGui.QLabel(self.centralwidget)
        self.label_show['label_back'].setGeometry(int(self.winsize_h*0.65),int(self.winsize_v*0.785),int(self.winsize_h*0.15),int(self.winsize_v*0.2))
        self.label_show['label_back'].setPixmap(QtGui.QPixmap(self.PH.paths['img'] + 'data_icons.png'))
        self.label_show['label_back'].setScaledContents(True)
        self.label_show['widget']=QtGui.QWidget(self.centralwidget)
        self.label_show['widget'].setGeometry(int(self.winsize_h*0.65),int(self.winsize_v*0.785),int(self.winsize_h*0.15),int(self.winsize_v*0.2))
        self.label_show['layout']=QtGui.QVBoxLayout(self.label_show['widget'])
        self.label_show['layout'].setSpacing(0)
        self.label_show['layout'].setMargin(0)
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(80)

        for i in range(6):
            self.label_show['label'+str(i)]=QtGui.QLabel(self.centralwidget)
            self.label_show['label'+str(i)].setFont(font)
            self.label_show['label'+str(i)].setTextFormat(QtCore.Qt.PlainText)
            self.label_show['label'+str(i)].setAlignment(QtCore.Qt.AlignCenter)
            self.label_show['layout'].addWidget(self.label_show['label'+str(i)])
        #%% static labels layout
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(80)
        self.label_names={}

        self.label_names['label_back']=QtGui.QLabel(self.centralwidget)
        self.label_names['label_back'].setGeometry(int(self.winsize_h*0.5),int(self.winsize_v*0.785),int(self.winsize_h*0.15),int(self.winsize_v*0.2))
        self.label_names['label_back'].setPixmap(QtGui.QPixmap(self.PH.paths['img'] + "data_icons.png"))
        self.label_names['label_back'].setScaledContents(True)
        self.label_names['widget']=QtGui.QWidget(self.centralwidget)
        self.label_names['widget'].setGeometry(int(self.winsize_h*0.5),int(self.winsize_v*0.785),int(self.winsize_h*0.15),int(self.winsize_v*0.2))
        self.label_names['layout']=QtGui.QVBoxLayout(self.label_names['widget'])
        self.label_names['layout'].setSpacing(0)
        self.label_names['layout'].setMargin(0)

        names=['Ritmo cardiaco','Pendiente','Velocidad','Cadencia','Ancho de paso',"Escala de Borg"]

        for i in range(6):
            self.label_names['label'+str(i)]=QtGui.QLabel(self.centralwidget)
            self.label_names['label'+str(i)].setFont(font)
            self.label_names['label'+str(i)].setTextFormat(QtCore.Qt.PlainText)
            self.label_names['label'+str(i)].setAlignment(QtCore.Qt.AlignCenter)
            self.label_names['label'+str(i)].setText(names[i])
            self.label_names['layout'].addWidget(self.label_names['label'+str(i)])

        #%% play button
        self.play_button=self.create_textured_button([0.05,0.8,0.1,0.1],self.PH.paths['img'] + "play_icon.png",self.PH.paths['img'] + "play_icon_on.png")
        #%% pause button
        self.pause_button=self.create_textured_button([0.18,0.85,0.07,0.07],self.PH.paths['img'] + "pause_icon.png",self.PH.paths['img'] + "cooldown1.png")
        #%% stop button
        self.stop_button=self.create_textured_button([0.28,0.85,0.07,0.07],self.PH.paths['img'] + "stop_icon.png",self.PH.paths['img'] + "stop_icon_on.png")
        #%%panic button
        self.panic_button=self.create_textured_button([0.85,0.8,0.1,0.1],self.PH.paths['img'] + "panic_icon.png")
        #%%cooldown phase button
        self.cool_button=self.create_textured_button([0.4,0.02,0.2,0.07],self.PH.paths['img'] + "cooldown.png")
        #%%Thumbs up button
        self.thumbsup_button=self.create_textured_button([0.2,0.15,0.2,0.1],self.PH.paths['img'] + "good_button.png")
        #%%Thumbs down button
        self.thumbsdown_button=self.create_textured_button([0.6,0.15,0.2,0.1],self.PH.paths['img'] + "bad_button.png")

        #%% Message label
        self.label_log=QtGui.QLabel(self.centralwidget)
        self.label_log.setGeometry(int(self.winsize_h*0.3),int(self.winsize_v*0.04),int(self.winsize_h*0.4),int(self.winsize_v*0.15))
        self.label_log.setFont(font)
        self.label_log.setTextFormat(QtCore.Qt.PlainText)
        self.label_log.setAlignment(QtCore.Qt.AlignCenter)
        self.label_log.setText("Como te sientes?")
        #%% Validation label
        font1 = QtGui.QFont()
        font1.setFamily("Century")
        font1.setPointSize(7)
        font1.setBold(True)
        font1.setWeight(40)

        #????
        self.label_val = QtGui.QLabel(self.centralwidget)
        self.label_val.setGeometry(int(self.winsize_h*0.6),int(self.winsize_v*0.93),int(self.winsize_h*0.35),int(self.winsize_v*0.1))
        self.label_val.setFont(font)
        self.label_val.setTextFormat(QtCore.Qt.PlainText)
        self.label_val.setAlignment(QtCore.Qt.AlignCenter)
        self.label_val.hide()
        #%% Patient's name label
        self.label_patient_name = QtGui.QLabel(self.centralwidget)
        self.label_patient_name.setGeometry(int(self.winsize_h*0.05),int(self.winsize_v*0),int(self.winsize_h*0.4),int(self.winsize_v*0.125))
        self.label_patient_name.setFont(font)
        self.label_patient_name.setTextFormat(QtCore.Qt.PlainText)
        self.label_patient_name.setText("Paciente Actual: Juan Sebastian\n Lara Ramirez")
        #%%
        MainWindow.setCentralWidget(self.centralwidget)
        #set initial set_initial_state
        self.set_initial_state()
        #set internal signals
        self.set_signals()


    def set_initial_state(self):
        if self.settings['mode'] == 1 or self.settings['mode'] == 2:
            #lock paus ans stop buttons
            self.lock_pause()
            self.lock_stop()
            self.lock_exit()
            #lock borg buttons
            self.lock_borg()
            #lock cooldown
            self.lock_cooldown()
            #lock buttons
            self.lock_thumbs()
            #hide backgorund background_blue
            self.label_background2.hide()

        elif self.settings['mode'] == 0:
            #lock paus ans stop buttons
            self.lock_pause()
            self.lock_stop()
            self.lock_exit()
            #lock borg buttons
            self.lock_borg()
            #lock cooldown
            self.lock_cooldown()
            #lock buttons
            self.lock_thumbs()
            #lock warning button
            self.lock_warning()
            #lock biofeedback display
            self.lock_display()
            #hide backgorund background_blue
            self.label_background2.hide()

    #set signals
    def set_signals(self):
        #start stop signal controller
        self.play_button['button'].clicked.connect(self.lock_play)
        #self.play_button['button'].clicked.connect(self.onBorg.emit)

        #unlock cooldown button
        self.play_button['button'].clicked.connect(self.unlock_pause)
        #cooldown locked
        self.pause_button['button'].clicked.connect(self.lock_pause)
        #unlock stop button
        self.pause_button['button'].clicked.connect(self.set_cooldown_state)
        #
        self.stop_button['button'].clicked.connect(self.unlock_exit)
        #
        self.stop_button['button'].clicked.connect(self.lock_stop)
        #unlock borg when signal triggered
        #unlock thumbs
        self.onThumbs.connect(self.unlock_thumbs)
        #unlock borg
        self.onBorg.connect(self.unlock_borg)
        #connect borg signal button
        self.connect_borg_to_signals()
        #signal to updat eidsplay
        self.onSensorUpdate.connect(self.update_feedback_display)
        #signal to quit the interface
        self.exit_button['button'].clicked.connect(self.close)

        self.send_data()


    def set_patients_name(self, n):
        s = "Paciente Actual: " + n
        self.label_patient_name.setText(s)

    def set_cooldown_state(self):
        self.label_background.hide()
        self.label_background2.show()
        self.unlock_stop()


    def send_data(self, hr = 0, speed = 0, sl = 0, cad =0, imu = 0):
        self.data_ecg = hr
        self.data_cadence = cad
        self.data_imu = imu
        self.data_step_length = sl
        self.data_speed = speed
        #emit signal to update display
        self.onSensorUpdate.emit()

    def update_feedback_display(self):
        if self.settings['mode'] == 0:
            a="{0:.2f}".format(self.data_ecg)+"{0:.2f}".format(self.data_speed)+"{0:.2f}".format(self.data_speed)+"{0:.2f}".format(self.data_imu)
            self.label_val.setText(a)

        elif self.settings['mode'] == 1 or self.settings['mode'] == 2:
            self.label_show['label0'].setText("{0:.2f}".format(self.data_ecg)+" ppm")
            self.label_show['label1'].setText("{0:.2f}".format(self.data_imu)+" deg")
            self.label_show['label2'].setText("{0:.2f}".format(self.data_speed)+" mph")
            self.label_show['label3'].setText("{0:.2f}".format(self.data_cadence)+" Hz")
            self.label_show['label4'].setText("{0:.2f}".format(self.data_step_length)+" m")

    #lock biofeedback display
    def lock_display(self):
        self.label_names['label_back'].hide()
        self.label_names['widget'].hide()

        self.label_show['label_back'].hide()
        self.label_show['widget'].hide()

    #unlock biofeedback display
    def unlock_display(self):
        self.label_names['label_back'].show()
        self.label_names['widget'].show()
        self.label_show['label_back'].show()
        self.label_show['widget'].show()

    #DEPRECATED
    def unlock_cooldown(self):
        self.cool_button['button'].show()
        self.cool_button['label'].show()
    #DEPRECATED
    def lock_cooldown(self):
        self.cool_button['button'].hide()
        self.cool_button['label'].hide()

    #lock play button
    def lock_play(self):
        self.play_button['button'].hide()
        self.play_button['labelon'].hide()
        self.play_button['label'].show()

    #unlock pplay button
    def unlock_play(self):
        self.play_button['button'].show()
        self.play_button['labelon'].show()
        self.play_button['label'].hide()

    #lock pause button
    def lock_pause(self):
        self.pause_button['button'].hide()
        self.pause_button['labelon'].hide()
        self.pause_button['label'].show()

    #unlock pause button
    def unlock_pause(self):
        self.pause_button['button'].show()
        self.pause_button['labelon'].show()
        self.pause_button['label'].hide()

    #lock stop button
    def lock_stop(self):
        self.stop_button['button'].hide()
        self.stop_button['labelon'].hide()
        self.stop_button['label'].show()

    #unlock stop button
    def unlock_stop(self):
        self.stop_button['button'].show()
        self.stop_button['labelon'].show()
        self.stop_button['label'].hide()

    #lock exit button
    def lock_exit(self):
        self.exit_button['button'].hide()
        self.exit_button['label'].hide()

    #unlock exit button
    def unlock_exit(self):
        self.exit_button['button'].show()
        self.exit_button['label'].show()

    #lock borg buttons
    def lock_borg(self):
        self.borg69b['widget'].hide()
        self.borg69b['label_active'].hide()
        self.borg1013b['widget'].hide()
        self.borg1013b['label_active'].hide()
        self.borg1417b['widget'].hide()
        self.borg1417b['label_active'].hide()
        self.borg1820b['widget'].hide()
        self.borg1820b['label_active'].hide()

    #unlock borg buttons
    def unlock_borg(self):
        self.borg69b['widget'].show()
        self.borg69b['label_active'].show()
        self.borg1013b['widget'].show()
        self.borg1013b['label_active'].show()
        self.borg1417b['widget'].show()
        self.borg1417b['label_active'].show()
        self.borg1820b['widget'].show()
        self.borg1820b['label_active'].show()

    #lock answer buttons
    def lock_thumbs(self):
        self.thumbsup_button['label'].setVisible(0)
        self.thumbsup_button['button'].setVisible(0)
        self.thumbsdown_button['label'].setVisible(0)
        self.thumbsdown_button['button'].setVisible(0)
        self.label_log.hide()
        self.borg_description.show()
    #unlock answer buttons
    def unlock_thumbs(self):
        self.thumbsup_button['label'].setVisible(1)
        self.thumbsup_button['button'].setVisible(1)
        self.thumbsdown_button['label'].setVisible(1)
        self.thumbsdown_button['button'].setVisible(1)
        self.label_log.show()
        self.borg_description.hide()
    #lock warning button
    def lock_warning(self):
        self.panic_button['label'].hide()
        self.panic_button['button'].hide()
    #unlock warning button
    def unlock_warning(self):
        self.panic_button['label'].show()
        self.panic_button['button'].show()

    #method to connect all borg scale buttons to their signals
    def connect_borg_to_signals(self):
        for i in range(2):
            for j in range(2):
                self.borg69b['borg'+str(i)+str(j)].clicked.connect(self.acquire_borg_scale)
        for i in range(2):
            for j in range(2):
                self.borg1013b['borg'+str(i)+str(j)].clicked.connect(self.acquire_borg_scale)
        for i in range(2):
            for j in range(2):
                self.borg1417b['borg'+str(i)+str(j)].clicked.connect(self.acquire_borg_scale)
        self.borg1820b['borg00'].clicked.connect(self.acquire_borg_scale)
        self.borg1820b['borg01'].clicked.connect(self.acquire_borg_scale)
        self.borg1820b['borg10'].clicked.connect(self.acquire_borg_scale)


    #get the borg value and set it on display
    def acquire_borg_scale(self):
        button = self.sender()
        self.borg_data = self.borg69b['layout'].indexOf(button)+6
        if self.borg_data < 6:
            self.borg_data=self.borg1013b['layout'].indexOf(button)+10
            if self.borg_data<10:
                self.borg_data=self.borg1417b['layout'].indexOf(button)+14
                if self.borg_data<14:
                    self.borg_data=self.borg1820b['layout'].indexOf(button)+18

        #lock borg buttons
        self.lock_borg()
        #set value on the dislay
        self.label_show['label5'].setText(str(self.borg_data))
        #emit signal
        self.onBorgReceive.emit()


    #create textured borg
    def create_textured_borg(self,relative_geometry,texture_dir,texture_dir2,flag=True):
        directory={}
        directory['geometry']=int(self.winsize_h*relative_geometry[0]),int(self.winsize_v*relative_geometry[1]),int(self.winsize_h*relative_geometry[2]),int(self.winsize_h*relative_geometry[3])
        directory['label_inactive']=QtGui.QLabel(self.centralwidget)
        directory['label_inactive'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
        directory['label_inactive'].setPixmap(QtGui.QPixmap(texture_dir2))
        directory['label_inactive'].setScaledContents(True)
        directory['label_active']=QtGui.QLabel(self.centralwidget)
        directory['label_active'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
        directory['label_active'].setPixmap(QtGui.QPixmap(texture_dir))
        directory['label_active'].setScaledContents(True)
        directory['widget']=QtGui.QWidget(self.centralwidget)
        directory['widget'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
        directory['layout']=QtGui.QGridLayout(directory['widget'])
        directory['layout'].setSpacing(0)
        directory['layout'].setMargin(0)
        if flag:
            for i in range(2):
                for j in range(2):
                    directory['borg'+str(i)+str(j)]=QtGui.QCommandLinkButton(self.centralwidget)
                    directory['borg'+str(i)+str(j)].setIconSize(QtCore.QSize(0, 0))
                    directory['layout'].addWidget(directory['borg'+str(i)+str(j)],i,j)
        else:
            directory['borg00']=QtGui.QCommandLinkButton(self.centralwidget)
            directory['borg00'].setIconSize(QtCore.QSize(0, 0))
            directory['layout'].addWidget(directory['borg00'],0,0)
            directory['borg01']=QtGui.QCommandLinkButton(self.centralwidget)
            directory['borg01'].setIconSize(QtCore.QSize(0, 0))
            directory['layout'].addWidget(directory['borg01'],0,1)
            directory['borg10']=QtGui.QCommandLinkButton(self.centralwidget)
            directory['borg10'].setIconSize(QtCore.QSize(0, 0))
            directory['layout'].addWidget(directory['borg10'],1,0,1,2)
        return directory
        #%% The following method creates a button and its correspondent label texture.

    #create texture button
    def create_textured_button(self,relative_geometry,texture_dir,texture_dir2=None):
        directory={}
        directory['geometry']=int(self.winsize_h*relative_geometry[0]),int(self.winsize_v*relative_geometry[1]),int(self.winsize_h*relative_geometry[2]),int(self.winsize_h*relative_geometry[3])
        directory['label']=QtGui.QLabel(self.centralwidget)
        directory['label'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
        directory['label'].setPixmap(QtGui.QPixmap(texture_dir))
        directory['label'].setScaledContents(True)
        if texture_dir2:
            directory['labelon']=QtGui.QLabel(self.centralwidget)
            directory['labelon'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
            directory['labelon'].setPixmap(QtGui.QPixmap(texture_dir2))
            directory['labelon'].setScaledContents(True)
        directory['button']=QtGui.QCommandLinkButton(self.centralwidget)
        directory['button'].setGeometry(QtCore.QRect(directory['geometry'][0],directory['geometry'][1],directory['geometry'][2],directory['geometry'][3]))
        directory['button'].setIconSize(QtCore.QSize(0, 0))
        return directory


#testt class to recreate controller of this view window
class tester(object):
    def __init__(self):
        self.main = TherapyWin(settings = {"mode":0})
        self.main.onBorgReceive.connect(self.get_borg)


        self.timer = threading.Timer(15, self.main.onBorg.emit)
        #print(self.timer)
        self.timer.start()
        #print(self.timer)
        self.main.stop_button['button'].clicked.connect(self.shutdown)


    def get_borg(self):
        #print "borg received" + str(self.main.borg_data)
        self.restart_timer()

    def restart_timer(self):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(15, self.main.onBorg.emit)
        self.timer.start()

    def shutdown(self):
        if self.timer:
            self.timer.cancel()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    t = tester()
    sys.exit(app.exec_())
