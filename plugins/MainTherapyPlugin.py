"""MAIN THERAPY PLUGIN"""
from PyQt4 import QtCore, QtGui
import time
import threading
#import robot controller module
import robot.robotController as RC
#import sensor manager module
import lib.Manager as M
#import view component
import gui.MainTherapyWin as MainTherapyWin
#import child plugins
import BloodPressurePlugin
import EndQuestionPlugin

import lib.estimateGaze as eG
"""
main therapy controller, receives ProjectHandler and datanhandler
receives a settings dict to set the interface in mode 0: no robot, 1:robot with no memory and 2: personalized robot

creates a qt thread to monitor robot events and sensor manager data acquisition

gets the data from sensor manager and forward it to the data handler and to the robot
"""

class MainTherapyPlugin(object):
    def __init__(self, ProjectHandler = None, DataHandler  = None, settings  ={"mode"      : 0,
                                                                               "BorgSample": 10,
                                                                               "useCamera" : True
                                                                               } ):
        #load controller settings
        self.settings = settings
        #load ProjectHandler settings
        self.PH = ProjectHandler
        #load database manager
        self.DB = DataHandler
        #creates robot resources
        self.useRobot= False
        #create child plugins
        #blood pressure plugin
        self.BloodPressurePlugin = BloodPressurePlugin.BloodPressurePlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #end questionnaire plugin
        self.EndQuestionPlugin = EndQuestionPlugin.EndQuestionPlugin(ProjectHandler = self.PH, DataHandler = self.DB)

        self.cooldownGaze = 55

    #set signals
    def set_signals(self):
        #blood pressure plugin
        self.BloodPressurePlugin.View.onStartTherapy.connect(self.View.show)
        #connect the end questionnaire to the on finishTherapy signal
        self.BloodPressurePlugin.View.onFinishTherapy.connect(self.EndQuestionPlugin.LaunchView)
        #connect shutdown method when blood pressure close_connect is emmited
        self.EndQuestionPlugin.View.exit_button['button'].clicked.connect(self.close)
        #self.BloodPressurePlugin.View.close_connect(self.shutdown)
        #set on start clicked signal
        self.View.play_button['button'].clicked.connect(self.onStart)
        #set on cooldown clicked signal
        self.View.pause_button['button'].clicked.connect(self.onCooldown)
        #set on stop clicked signal
        self.View.stop_button['button'].clicked.connect(self.shutdown)
        
        self.View.exit_button['button'].clicked.connect(self.launch_final_bpm)
        #set on alamarms clicked signals

        #set on borg clicked signal
        self.View.onBorgReceive.connect(self.receive_borg)
        #set on everything is alright signal YES

        #set on everything is alright signal NO
        
        #robot signals



    def LaunchView(self):
        #load settings
        mode = self.DB.General.TherapyStatus['mode']
        user = self.DB.General.TherapyStatus['user']
        #creates sensor manager resources
        #get crotch for laser settings
        self.PH.GeneralSettings['laser']['crotch'] = self.DB.General.SM.person['crotch']
        #create sensor manager
        self.SensorManager = M.SensorManager(imu   = self.PH.GeneralSettings['imu'],
                                             ecg   = self.PH.GeneralSettings['ecg'],
                                             laser = self.PH.GeneralSettings['laser'])
        #create sensor monitor thread
        self.SensorMonitorThread = SensorMonitorThread(self)

        self.settings['mode'] = mode
        #if no robot condition
        if self.settings['mode'] == 0:
            #set timer for the borgscale
            self.BorgTimer = threading.Timer(self.PH.GeneralSettings['therapy']['BorgSample'], self.request_borg)
        
        #if robot condition
        elif self.settings['mode'] == 1 or self.settings['mode'] ==2:
            print("USERROBOT = TRUE")
            self.useRobot = True
            if self.settings['mode'] == 2:
                print("USE MEMORY 0 TRUE")
                self.useMemory = True
                self.PH.GeneralSettings['robot']['useMemory'] = self.useMemory
            #get user profile
            self.PH.GeneralSettings['robot']['UserProfile'] = self.DB.General.SM.person
            #Create robot controller
            self.robotController = RC.Controller(ProjectHandler = self.PH,
                                                 settings       = self.PH.GeneralSettings['robot'],
                                                 DataHandler    = self.DB
                                                )
            #create robot monitor thread
            self.RobotMonitorThread = RobotMonitorThread(self)


        #create timer display thread
        self.TimerDisplayThread = TimerDisplayThread(self)


        ##create view component
        self.View = MainTherapyWin.TherapyWin(settings = {"mode": mode, "user":user}, ProjectHandler = self.PH)
        self.View.set_patients_name(n = user)
        #set interconecting signals
        self.set_signals()

        #launch blood pressure
        self.BloodPressurePlugin.set_mode(mode = "initial")
        self.BloodPressurePlugin.LaunchView()



        #self.View.show()

    #Emit signal to request the borg scale
    def request_borg(self):
        #set request borg event
        self.DB.General.SM.load_event(t = "BorgRequest", c = "Timeout", v ="none")
        #set event borg request
        print "borg request"
        #request borg to the view
        self.View.onBorg.emit()

    #request borg confirm
    def request_borg_confirm(self):
        self.DB.General.SM.load_event(t = "BorgConfirm", c = "Timeout", v ="none")
        self.View.onBorg.emit()

    #receive borg from the interface and forward it to the event handler and robot
    def receive_borg(self):
        #read variable from the view
        b = self.View.borg_data
        #set event borg received
        self.DB.General.SM.load_event(t ="BorgReceive", c = "Clicked", v = str(b))
        print "borg: " + str(b)
        #if using robot, send the value
        if self.useRobot:
            self.robotController.send_borg(b)
        #restart Timer
        else:
            self.restart_borg_timer()

    #restart timer in no robot condition
    def restart_borg_timer(self):

        if self.BorgTimer:
            self.BorgTimer.cancel()
        self.BorgTimer = threading.Timer(15, self.request_borg)
        self.BorgTimer.start()

    #callback method to run when start button is clicked
    def onStart(self):
        #set start therapy event
        self.DB.General.SM.load_event(t ="StartRecording", c ="None", v = "None")
        #deploy resources
        self.deploy_resources()



    #deploy all therapy resources
    def deploy_resources(self):
        #sensor manager
        #set sensors
        self.SensorManager.set_sensors(ecg = True, imu = True, laser = False)
        #launch sensors
        self.SensorManager.launch_sensors()
        #launch timer
        self.TimerDisplayThread.start()
        #launch sensor monitor
        self.SensorMonitorThread.start()
        #robot controller
        if self.useRobot:
            #launch robot
            print "deploy resources launch"
            self.robotController.launch()
            print("robotController lounchjed from MainTherapypluWin")
            #launch robot monitor
            self.RobotMonitorThread.start()
        else:
            #launch borg timer
            self.BorgTimer.start()
        
        #use camera for gaze estimation
        if self.settings['useCamera']:
            self.headEstimator = eG.GetGaze(controller = self)
            self.headThread=threading.Thread(target=self.headEstimator.start)
            self.lowGazeCounter = 0
            self.lowGazeRequested = True
            self.lowGazeFeedback = True
            self.timerGaze = threading.Timer(self.cooldownGaze, self.resetGaze)

            self.headThread.start()
            self.timerGaze.start()

        




    def resetGaze(self):
        self.lowGazeRequested = False

    #request look
    def requestLook(self):
        self.DB.General.SM.load_event(t ="RequestLook", c ="None", v = "None")
        if self.useRobot:
            self.robotController.correct_posture()
            #self.say(self.sentenceRequestLookForward,self.requestLookForwardProvided)



# Headgaze related functions
    def headGaze(self, value):
        if value:
            self.lowGazeCounter += 1
            if self.lowGazeCounter > 5 and not self.lowGazeRequested:
                self.requestLook()
                self.lowGazeRequested = True
                self.lowGazeFeedback = False
                self.timerGaze = threading.Timer(self.cooldownGaze, self.resetGaze)
                self.timerGaze.start()
        else:
            self.lowGazeCounter = 0
            if self.lowGazeRequested and not self.lowGazeFeedback:
                self.feedbackLook()


                self.lowGazeFeedback = True



    #callback method when cooldown is pressed
    def onCooldown(self):
        #set cooldown event
        self.DB.General.SM.load_event(t ="Cooldown", c ="None", v = "None")
        #sleep laser an IMu sensor
        self.SensorManager.sleep_sensors(ecg = False, imu = False, laser = False)
        #if using no robot condition, cancel the timer
        if self.settings['mode'] == 0:
            #kill timer
            self.BorgTimer.cancel()
        if self.useRobot:
            self.robotController.onCooldown.set()

        if self.settings['useCamera']:
            self.headEstimator.stop()
            self.timerGaze.cancel()

    #callback method to close all resources in a safe way
    def shutdown(self):
        #stop timer
        self.TimerDisplayThread.shutdown()
        #stop event
        self.DB.General.SM.load_event(t ="EndRecording", c ="None", v = "None")
        #kill sensor manager
        self.SensorManager.shutdown()
        #kill sensor monitor thread
        self.SensorMonitorThread.shutdown()

        #self.BloodPressurePlugin.shutdown()
        #if using robot, kill all robot resources
        if self.useRobot:
            #kill robot
            self.robotController.shutdown()
            #kill robot monitor thread
            self.RobotMonitorThread.shutdown()
        #finish session
        #self.DB.General.SM.finish_session()

    def close(self):

        self.BloodPressurePlugin.shutdown()
        
        self.DB.General.SM.finish_session()

    def launch_final_bpm(self):
        #set mode
        print("launch_final_bpm")
        self.BloodPressurePlugin.set_mode(mode = "final")
        self.BloodPressurePlugin.LaunchView()

#robot monitor thread
class RobotMonitorThread(QtCore.QThread):
    def __init__(self, controller):
        super(RobotMonitorThread,self).__init__()
        #load controller
        self.c = controller
        self.on = True
        self.ts = 0.5

    def run(self):
        #main monitor loop
        while self.on:
            #if borgscale requested
            if self.c.robotController.onBorgRequest.is_set():
                print('onBorgRequest received ftom RobotMonitorThread')
                self.c.request_borg()
                self.c.robotController.onBorgRequest.clear()

            if self.c.robotController.onBorgConfirm.is_set():
                self.c.request_borg_confirm()
                self.c.robotController.onBorgConfirm.clear()

            time.sleep(self.ts)

    def shutdown(self):
        self.on = False

#sensor monitor thread
class SensorMonitorThread(QtCore.QThread):
    def __init__(self, controller):
        super(SensorMonitorThread,self).__init__()
        #load controller
        self.c = controller
        self.on = True
        self.ts = 1

    def run(self):
        #main monitor loop
        while self.on:
            #update data
            self.c.SensorManager.update_data()
            #self.c.SensorManager.print_data()
            #load data to the database
            self.c.DB.General.SM.load_sensor_data(hr          = self.c.SensorManager.data['ecg'],
                                                speed       = self.c.SensorManager.data['laser']['speed'],
                                                cadence     = self.c.SensorManager.data['laser']['cadence'],
                                                sl          = self.c.SensorManager.data['laser']['steplenght'],
                                                inclination = self.c.SensorManager.data['imu'])
            #if robot, load data to the robot
            if self.c.useRobot:
                self.c.robotController.send_data(self.c.SensorManager.data)
            #load data to the display
            self.c.View.send_data(hr    = self.c.SensorManager.data['ecg'],
                                  speed = self.c.SensorManager.data['laser']['speed'],
                                  sl    = self.c.SensorManager.data['laser']['steplenght'],
                                  cad   = self.c.SensorManager.data['laser']['cadence'],
                                  imu   = self.c.SensorManager.data['imu'])
            #print("sendind data to view")
            #print self.c.SensorManager.data
            time.sleep(self.ts)



    def shutdown(self):
        self.on = False


# timer display thread
class TimerDisplayThread(QtCore.QThread):
    def __init__(self, controller):
        super(TimerDisplayThread,self).__init__()
        #Flags
        self.c = controller
        self.go_on = True
        self.Ts = 1

    def run(self):
        self.time_secs=0
        self.time_mins=0
        while self.go_on:
            self.time_secs=self.time_secs+1
            if self.time_secs>59:
                self.time_secs=0
                self.time_mins=self.time_mins+1

            print(self.time_secs)
            print(self.time_mins)
            fun= lambda time : str(time) if time>9 else '0'+str(time)
            self.c.View.time_lcd.display(fun(self.time_mins)+':'+fun(self.time_secs))

            time.sleep(self.Ts)
    def shutdown(self):
        self.go_on = False





if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    t = MainTherapyPlugin()
    sys.exit(app.exec_())
