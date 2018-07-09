import robotModel
import resources.analyzer as analyzer
import multiprocessing
import time
#import qi

"""
Robot controller has two modes of configuration
1: robot with no memory
2: robot with memory
the controller has a main loop that handles the data, and analysis throgh the analayzer
and according to the results, sets the behavior for the robot (Robot Model)

"""
class Controller(object):
    def __init__(self, ProjectHandler = None,
                       settings= { 'IpRobot': "192.168.1.2",
                                    'mode'  : 1,
                                    'port'   : 9559,
                                    'name'   : 'Palin',
                                    'UseSpanish': True,
                                    'MotivationTime':1*60,
                                    'BorgTime':2*60,
                                    'useMemory': False,
                                    'UserProfile':{ 'name': "jonathan",
                                                    'age' : 26,
                                                    'alarm2': 150,
                                                    'alarm1': 130,
                                                    'borg_threshold':7,
                                                    'weight': 80,
                                                    'last_measure': {}
                                                   }
                                  },
                        db = None
                ):
        #load settings
        print settings
        self.settings = settings
        self.PH = ProjectHandler
        self.db = db
        #create event handlers
        #session init
        self.onStart = multiprocessing.Event()
        #shutdown session
        self.onShutdown = multiprocessing.Event()
        #provide motivation
        self.onMotivation = multiprocessing.Event() #?
        #on borg request
        self.onBorgRequest = multiprocessing.Event()
        #when borg as been submited
        self.onBorgScale = multiprocessing.Event() #?
        #ask for borg confirmation
        self.onBorgConfirm = multiprocessing.Event()
        #sensor data received
        self.onSensorData = multiprocessing.Event()
        #when the robot asks to the patient if evereything is ok
        self.onAlert = multiprocessing.Event()
        #when call staff is required
        self.onCallStaff = multiprocessing.Event()
        #
        self.onWarning =multiprocessing.Event()
        #
        self.onEmergency = multiprocessing.Event()
        #on cooldown
        self.onCooldown = multiprocessing.Event()
        #events to be passed to the robot model as they are trigger with ashync tasks
        self.Events = {"onMotivation": self.onMotivation,
                       "onBorgScale" : self.onBorgScale
                       }
        #create communication resources
        self.GetSensorData, self.LoadSensorData = multiprocessing.Pipe()
        self.GetBorg, self.LoadBorg = multiprocessing.Pipe()
        #set loop timing = 1 second
        self.ts = 1
        #create process
        self.MainProcess = multiprocessing.Process(target = self.process)

    #launch process method
    def launch(self):
        self.MainProcess.start()

    #process to run in a separate process
    def process(self):
        #creates data alzer
        self.analyzer = analyzer.Analyzer(self.settings['UserProfile'])
        #create robot model
        self.robot = robotModel.Robot(controller = self, settings = self.settings, db = self.db)
        #init behavior
        if not self.settings['useMemory']:
            self.robot.start_behavior()
        else:
            announce = self.robot.dialogs.sentenceAnnounce.replace("XX",str(5))
            announce = announce.replace("YY", str(1))
            text_to_say = self.robot.MemoryRobot.checkAbsence() + self.robot.MemoryRobot.checkPreviousSessionAlerts(announce,5,1)

        #enter to the main programm loop
        while not self.onShutdown.is_set():
            """
            REQUEST DATA
            emitting signals:
                *onCallStaff
                *onAlert
            """
            #if data available read data
            if self.onSensorData.is_set():
                #receive data from pipe
                d = self.GetSensorData.recv()
                #clear the event handler
                self.onSensorData.clear()
                #pass the data to the analyzer obejct
                self.analyzer.load_data(d = d)
                #check the hr 0: no problem, 1: first alarm, 2: second alarm
                r = self.analyzer.check_hr()
                #according to the analysis result some events are set
                #if set alert
                print "dta analysis result: " + str(r)

                if r == 2 :
                    #set events
                    self.onCallStaff.set()
                    #call the medical staff
                    self.robot.alertHr2()

                elif r == 1:
                    #set events
                    self.onAlert.set()
                    #ask to the patient if everything is ok
                    self.robot.alertHr1()
            """
            REQUEST BORG
            emitting signals:
                *onAlert
                *onBorgConfirm
            """
            #if borg data available
            if self.onBorgScale.is_set():
                #receive borg data
                b = self.GetBorg.recv()
                print("borg scale: " + str(b))
                #clear event handler
                self.onBorgScale.clear()
                #pass the data to the analyzer
                self.analyzer.load_borg(b = b)
                #check analysis results
                r = self.analyzer.check_borg()
                print "borg analysis result: " + str(r)
                #decide according to the results
                if r == 0:
                    #say thanks for the value
                    self.robot.thanks_borg()
                #
                elif r == 1:
                    #set event
                    self.onAlert.set()
                    #patient is feeling too tired
                    self.robot.alertFatigue()
                #
                elif r == 2:
                    #set event to request again the borg scale
                    self.onBorgConfirm.set()
                    #ask for borg confirmation
                    self.robot.ask_borg_again()

            #listen for events
            if self.onCallStaff.is_set():
                #set call staff behavior
                self.robot.callMedicalStaff()


            #listen for cooldown event
            if self.onCooldown.is_set():
                self.onCooldown.clear()
                self.robot.cooldown()




            time.sleep(self.ts)

        print("robot process finished")
        #shutdown the robot
        self.robot.shutdown()
        #wait a considerable time for the robot shutdown
        time.sleep(3)

    #method to send data from exterior (GUI) to the controller
    def send_data(self, d):
        if not self.onSensorData.is_set():
            #load data into the send pipe
            self.LoadSensorData.send(d)
            #trigger the event for data available
            self.onSensorData.set()

    #method to send borg value from GUI to the robot
    def send_borg(self, b):
        #load data into the send pipe
        self.LoadBorg.send(b)
        #trigger the event for data available
        self.onBorgScale.set()

    # shutdown method to finish all processes
    def shutdown(self):
        print("shutdown method")
        #set the shutdown event to go out of the main loop
        self.onShutdown.set()


if __name__ == '__main__':
    c = Controller()
    c.launch()
    t = 0
    for i in range(30):
        print("main")
        c.send_data(t)
        t = t + 1
        time.sleep(2)

    c.shutdown()
    time.sleep(2)
    print("going out main")
