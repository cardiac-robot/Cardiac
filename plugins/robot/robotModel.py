# -*- coding: utf-8 -*-
"""ROBOT CONTROLLER CODE"""


import qi
import sys
import time
import functools
import resources.dialogs as dialogs
import threading
import resources.MemoryRobot as RMEM

class Robot(object):
    def __init__(self, settings = { 'IpRobot': "192.168.0.100",
                                    'port'   : 9559,
                                    'name'   : 'Palin',
                                    'UseSpanish': True,
                                    'MotivationTime':5,
                                    'BorgTime': 3,
                                    'useMemory': False
                                    },
                        db = None,
                        controller = None,
                 ):
        #load robot controller
        self.controller = controller
        #load settings
        self.settings = settings
        #load event handler
        self.db = db
        #resources
        self.dialogs = dialogs.Dialogs()
        #micro second
        self.micro = 1000000
        # number of alerts in the session
        self.num_alerts = 0
        if self.settings['useMemory']:
            print "creating robot memory from model"
            self.MemoryRobot = RMEM.MemoryRobot(ProjectHandler = self.controller.PH,
                                                settings       = self.controller.settings,
                                                DataHandler    = self.controller.DB,
                                                dialogs        = self.dialogs,
                                                controller     = self.controller)

                #launch_robot
        self.launch_robot()



    #launch the main robot utilities
    def launch_robot(self):
        #load dialogs
        self.dialogs.load_dialogs()
        #create Session
        print "CREATES SESSION FOM ROBOT MODEL"
        self.session = qi.Session()
        #connect the session to the robot
        self.connect_session()
        #after connecting to the robot, get services and modules
        #self.session = self.controller.PH.get_robot_session()


        #set routines

        #pass session to the memory
        print "launch robot"
        if self.settings['useMemory']:
            print("setting the session to the MemoryRobot")
            self.MemoryRobot.set_session(self.session)
            self.MemoryRobot.get_services()
            self.MemoryRobot.set_routines()
            print('memory robot launched')
        else:
            print('##############GET SERVICES ###############################')
            self.get_services()
            self.set_routines()
#----------------------------Setup and initialization Methods--------------------------
    #load Dialogs
    #TODO: LOAD Dialogs from files


    #connect to the robot through session
    def connect_session(self):
        print self.settings['IpRobot']
        print "tcp://" + self.settings['IpRobot'] + ":" + str(self.settings['port'])

        ip = self.settings['IpRobot']
        port = str(self.settings['port'])

        self.session.connect("tcp://" + ip + ":" + str(port))

        print("After connection")

    #get all module services
    def get_services(self):
        #text to speech module service
        self.tts = self.session.service("ALTextToSpeech")
        #set language
        self.setLanguage('Spanish')
        #animated text to speech service
        self.animatedSpeech = self.session.service("ALAnimatedSpeech")
        #motion service
        self.motion = self.session.service("ALMotion")
        #posture service
        self.posture = self.session.service("ALRobotPosture")
        #behavior manager
        self.behavior = self.session.service("ALBehaviorManager")
        #memory for events of touch sensing
        self.memory = self.session.service("ALMemory")
        self.memory.subscribeToEvent("MiddleTactilTouched","ReactToTouch", "onTouched")
        #tracker
        self.tracker = self.session.service("ALTracker")
        targetName = "Face"
        faceWidth = 0.1
        self.tracker.registerTarget(targetName, faceWidth)
        self.tracker.track(targetName)
        #names = self.behavior.getInstalledBehaviors()
        #print(names)

    def onTouched(self):

        if self.settings['useMemory']:
            s = self.dialogs.sentenceFine
            if self.MemoryRobot.isSayName():
                s = self.MemoryRobot.addNameToSentence(s)
                
            self.MemoryRobot.tts.say(s)
        else:
            self.tts.say(self.dialogs.sentenceFine)


    #set language method
    def setLanguage(self, value):
        self.tts.setLanguage(value)

    #routines setup and deploy
    def set_routines(self):
        print("setting routines")
        #set motivation routine
        motivate = functools.partial(self.motivation)
        self.motivationTask = qi.PeriodicTask()
        self.motivationTask.setCallback(motivate)
        self.motivationTask.setUsPeriod(self.settings['MotivationTime'] * self.micro)

        #set borg request routine
        borg = functools.partial(self.ask_borg)
        self.borgTask = qi.PeriodicTask()
        self.borgTask.setCallback(borg)
        self.borgTask.setUsPeriod(self.settings['BorgTime'] * self.micro)

    #start routine method
    def start_routines(self):
        self.motivationTask.start(True)
        self.borgTask.start(True)

    #setop created async routines
    def stop_routines(self):
        self.motivationTask.stop()
        self.borgTask.stop()
   
    def add_alert_count(self):
        self.num_alerts += 1

#----------------------------------------------------------------------
#----------------------------Behavior Methods--------------------------
    #start behavior method
    def start_behavior(self):
        if self.db:
            self.db.General.SM.load_event(t ="RobotWelcome", c ="Start", v="WelcomeSentence")

        #make the robot stand up

        #run behavior   cardio-7fad01
        #self.run_welcome_behavior()
        if self.settings['useMemory']:
            self.MemoryRobot.motion.wakeUp()
            #threading.Thread(target = self.MemoryRobot.run_welcome_behavior).start()
            self.MemoryRobot.run_welcome_behavior()
	    #TODO: checkPreviousSessionAlerts(begin), checkProgress(end)
        else:
            self.motion.wakeUp()
            threading.Thread(target = self.run_welcome_behavior).start()


    #behavior fucntion
    def run_welcome_behavior(self):
        #run behavior manager
        if self.settings['useMemory']:
            self.MemoryRobot.run_welcome_behavior()
        else:
            self.behavior.runBehavior("cardio-7fad01/Welcome")
        #start asyncronic routines
        self.start_routines()

    #method to run with the ashyncronic task
    def motivation(self):
        if self.db:
            self.db.General.SM.load_event(t ="Motivation", c = "Timeout", v ="None")
        #request the dialog manager the random motivation sentence
        s = self.dialogs.get_motivation_sentence()
        #self.tts.say(s)
        self.run_motivation_behavior()
        #threading.Thread(target = self.run_motivation_behavior).start()

    def run_motivation_behavior(self):
        self.behavior.runBehavior('motivation-f4819c/motivation1')

    #borg scale request behavior
    def ask_borg(self):
        if self.controller:
            self.controller.onBorgRequest.set()
        #event loaded in the theray plugin
        #if self.db:
        #    self.db.General.SM.load_event(t ="BorgRequest", c = "Timeout", v ="none")
        #request the dialog mnager the random borg sentence
        s = self.dialogs.get_borg_sentence()
        self.animatedSpeech.say(s)

    def correct_posture(self):
        if self.settings['useMemory']:
            self.MemoryRobot.posture_correction_behavior()

        else:
            s = self.dialogs.get_posture_correction_sentence()
            self.animatedSpeech.say(s)


    #alert fatigue
    def alertFatigue(self):
        if self.db:
            self.db.General.SM.load_event(t ="alarm_fatigue", c = "timeout", v ="none")

        #set alarm  event
        if self.settings['useMemory']:
            s = self.dialogs.sentenceWarning
            if self.MemoryRobot.isSayName():
                s = self.MemoryRobot.addNameToSentence(s)
            self.MemoryRobot.tts.say(s)
            self.add_alert_count()

        else:
            self.tts.say(self.dialogs.sentenceWarning)

    #borg scale receive
    def thanks_borg(self):
        if self.settings['useMemory']:
            s = self.dialogs.get_borg_receive()
            if self.MemoryRobot.isSayName():
                s = self.MemoryRobot.addNameToSentence(s)
            self.MemoryRobot.animatedSpeech.say(s)
        else:
            s = self.dialogs.get_borg_receive()
            self.animatedSpeech.say(s)

    #thumbs receive
    def thanks_thumbs(self):
        if self.settings['useMemory']:
            s = self.dialogs.sentence_fine()
            if self.MemoryRobot.isSayName():
                s = self.MemoryRobot.addNameToSentence(s)
            self.MemoryRobot.animatedSpeech.say(s)
        else:
            s = self.dialogs.sentence_fine()
            self.animatedSpeech.say(s)

   #ask borg again behavior
    def ask_borg_again(self):

        if self.settings['useMemory']:
            s = self.dialogs.ask_borg_again()
            if self.MemoryRobot.isSayName():
                s = self.MemoryRobot.addNameToSentence(s)
            self.MemoryRobot.tts.say(s)
        else:
            s = self.dialogs.ask_borg_again()
            self.tts.say(s)



    #alert 1 behavior
    def alertHr1(self):
        if self.db:
            self.db.General.SM.load_event(t = "Alert1", c = "HighHr", v = "None")

        if self.settings['useMemory']:
            s = self.dialogs.sentenceWarning
            if self.MemoryRobot.isSayName():
                s = self.MemoryRobot.addNameToSentence(s)
            
            self.MemoryRobot.tts.say(s)
            self.add_alert_count()
            
            #self.motion.rest()
            
        else:
           self.tts.say(self.dialogs.sentenceWarning)
           #self.motion.rest()

    #alert 2 behavior
    #TODO: set redundancy control
    def alertHr2(self):
        if self.db:
            self.db.General.SM.load_event(t = "Alert2", c = "HighHr", v = "none")
            
        if self.settings['useMemory']:
            s = self.dialogs.sentenceAlertHR
            if self.MemoryRobot.isSayName():
                s = self.dialogs.sentenceAlertHRMemory
                s = s.replace('XX', self.MemoryRobot.p_first_name)
            
            self.MemoryRobot.tts.say(s)
            self.add_alert_count()
            m = self.dialogs.get_CallStaff_sentence()
            self.MemoryRobot.behavior.runBehavior(m)
            #self.MemoryRobot.memory.subscribeToEvent("MiddleTactilTouched","ReactToTouch", "onTouched")

            #self.motion.rest()
            
        else:
           self.tts.say(self.dialogs.sentenceAlertHR)
           m = self.dialogs.get_CallStaff_sentence()
           self.behavior.runBehavior(m)
           #self.memory.subscribeToEvent("MiddleTactilTouched","ReactToTouch", "onTouched")
           #self.motion.rest()

    #call doctor behavior
    def callMedicalStaff(self):
        print("call doctor behavior")
        if self.db:
            self.db.General.SM.load_event(t = "CallMedicalStaff", c = "HighHr", v = "none")

        s = self.dialogs.sentenceWarning
        if self.settings['useMemory'] and self.MemoryRobot.isSayName():
            s = self.MemoryRobot.addNameToSentence(s)
            self.add_alert_count()
            
        self.tts.say(s)

    #cooldown behavior
    def cooldown(self):
        if self.settings['useMemory']:
            s = self.dialogs.cooldownSentence
            if self.MemoryRobot.isSayName():
                s = self.MemoryRobot.addNameToSentence(s)
            self.MemoryRobot.animatedSpeech.say(s)
            self.MemoryRobot.stop_routines()
        else:
            self.animatedSpeech.say(self.dialogs.cooldownSentence)
            self.stop_routines()

#------------------------------------------------------------------------

    #shutdown method, stop routines and get to rest position
    def shutdown(self):
        if self.settings['useMemory']:
            s = self.MemoryRobot.end_of_session_announcement + self.MemoryRobot.checkProgress(self.num_alerts) + self.MemoryRobot.fill_questionnaire
            self.num_alerts = 0
            self.MemoryRobot.animatedSpeech.say(s)
            self.MemoryRobot.motion.rest()
        else:
            self.animatedSpeech.say(self.dialogs.ByeSentence)
            self.motion.rest()


if __name__ == '__main__':
    r = Robot()
    print r.settings
