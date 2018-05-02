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
"""
main therapy controller, receives ProjectHandler and datanhandler
receives a settings dict to set the interface in mode 0: no robot, 1:robot with no memory and 2: personalized robot

creates a qt thread to monitor robot events and sensor manager data acquisition

gets the data from sensor manager and forward it to the data handler and to the robot
"""

class MainTherapyPlugin(object):
    def __init__(self, ProjectHandler = None, DataHandler  = None, settings  ={"mode"      : 0,
                                                                               "BorgSample": 10
                                                                               } ):
        #load controller settings
        self.settings = settings
        #load ProjectHandler settings
        self.PH = ProjectHandler
        #load database manager
        self.DB = DataHandler
        #creates sensor manager resources
        #create sensor manager
        self.SensorManager = M.SensorManager()
        #create sensor monitor thread
        self.SensorMonitorThread = SensorMonitorThread(self)
        #creates robot resources
        self.useRobot= False





    #set signals
    def set_signals(self):
        #set on start clicked signal
        self.View.play_button['button'].clicked.connect(self.onStart)
        #set on cooldown clicked signal

        #set on stop clicked signal
        self.View.stop_button['button'].clicked.connect(self.shutdown)
        #set on alamarms clicked signals

        #set on borg clicked signal
        self.View.onBorgReceive.connect(self.receive_borg)
        #set on everything is alright signal YES

        #set on everything is alright signal NO

    def LaunchView(self):
        #load settings
        mode = self.DB.General.TherapyStatus['mode']
        user = self.DB.General.TherapyStatus['user']

        self.settings['mode'] = mode
        #if no robot condition
        if self.settings['mode'] == 0:
            #set timer for the borgscale
            self.BorgTimer = threading.Timer(self.settings['BorgSample'], self.request_borg)
        #if robot condition
        elif self.settings['mode'] == 1 or self.settings['mode'] ==2:
            self.useRobot = True
            #Create robot controller
            self.robotController = RC.Controller(ProjectHandler = self.PH,
                                                 settings ={ 'IpRobot': "127.0.0.1",
                                                              'mode'  : 1, # no memory
                                                              'port'   : 43472,
                                                              'name'   : 'Palin',
                                                              'UseSpanish': True,
                                                              'MotivationTime':1*60,
                                                              'BorgTime':2*60,
                                                              'useMemory': False,
                                                              'UserProfile':{ 'name': "jonathan",
                                                                              'age' : 26,
                                                                              'alarm2': 100,
                                                                              'alarm1': 80,
                                                                              'borg_threshold':9,
                                                                              'weight': 80,
                                                                              'last_measure': {}
                                                                             }
                                                            }

                                                )
            #create robot monitor thread
            self.RobotMonitorThread = RobotMonitorThread(self)




        ##create view component
        self.View = MainTherapyWin.TherapyWin(settings = {"mode": mode, "user":user}, ProjectHandler = self.PH)
        self.View.set_patients_name(n = user)
        #set interconecting signals
        self.set_signals()
        #show window
        self.View.show()

    def request_borg(self):
        #set event borg request
        print "borg request"
        #request borg to the view
        self.View.onBorg.emit()


    def receive_borg(self):
        #set event borg received

        #read variable from the view
        b = self.View. borg_data
        print "borg: " + str(b)
        #if using robot, send the value
        if self.robotController:
            self.robotController.send_borg(b)
        #restart Timer
        else:
            self.restart_borg_timer()

    def restart_borg_timer(self):
        print self.BorgTimer
        if self.BorgTimer:
            self.BorgTimer.cancel()
        self.BorgTimer = threading.Timer(15, self.View.onBorg.emit)
        self.BorgTimer.start()


    def onStart(self):
        #set start therapy event

        #deploy resources
        self.deploy_resources()



    #deploy all therapy resources
    def deploy_resources(self):
        #sensor manager
        #set sensors
        self.SensorManager.set_sensors()
        #launch sensors
        self.SensorManager.launch_sensors()
        #launch sensor monitor
        self.SensorMonitorThread.start()

        #robot controller
        if self.useRobot:
            #launch robot
            self.robotController.launch()
            #launch robot monitor
            self.RobotMonitorThread.start()
        else:
            #launch borg timer
            self.BorgTimer.start()

    def shutdown(self):

        if self.settings['mode'] == 0:
            #kill timer
            self.BorgTimer.cancel()
        #kill sensor manager
        self.SensorManager.shutdown()
        #kill sensor monitor thread
        self.SensorMonitorThread.shutdown()

        if self.useRobot:
            #kill robot
            self.robotController.shutdown()
            #kill robot monitor thread
            self.RobotMonitorThread.shutdown()

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
            print("robot monitoring loop")

            #if borgscale requested
            if self.c.robotController.onBorgRequest.is_set():
                self.c.request_borg()
                self.c.robotController.onBorgRequest.clear()


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
        self.ts = 4

    def run(self):
        #main monitor loop
        while self.on:
            print("sensor monitoring loop")
            time.sleep(self.ts)

    def shutdown(self):
        self.on = False



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    t = MainTherapyPlugin()
    sys.exit(app.exec_())
