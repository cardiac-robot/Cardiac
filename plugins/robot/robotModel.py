# -*- coding: utf-8 -*-
"""ROBOT CONTROLLER CODE"""


import qi
import sys
import time
import functools
import resources.dialogs as dialogs


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
        #launch_robot
        self.launch_robot()

    #launch the main robot utilities
    def launch_robot(self):
        #load dialogs
        self.dialogs.load_dialogs()
        #create Session
        self.session = qi.Session()
        #connect the session to the robot
        self.connect_session()
        #after connecting to the robot, get services and modules
        self.get_services()
        #set routines
        self.set_routines()
#----------------------------Setup and initialization Methods--------------------------
    #load Dialogs
    #TODO: LOAD Dialogs from files


    #connect to the robot through session
    def connect_session(self):
        self.session.connect("tcp://" + self.settings['IpRobot'] + ":" + str(self.settings['port']))


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
        #tracker
        self.tracker = self.session.service("ALTracker")
        targetName = "Face"
        faceWidth = 0.1
        self.tracker.registerTarget(targetName, faceWidth)
        self.tracker.track(targetName)

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

#----------------------------------------------------------------------
#----------------------------Behavior Methods--------------------------
    #start behavior method
    def start_behavior(self):
        if self.db:
            self.db.General.SM.load_event(t ="robot_welcome", c ="start", v="WelcomeSentence")

        #make the robot stand up
        self.motion.wakeUp()
        #say welcome sentence
        self.animatedSpeech.say(self.dialogs.WelcomeSentence)
        #start asyncronic routines
        #self.start_routines()


    #method to run with the ashyncronic task
    def motivation(self):
        if self.db:
            self.db.General.SM.load_event(t ="motivation", c = "timeout", v ="none")
        #request the dialog manager the random motivation sentence
        s = self.dialogs.get_motivation_sentence()
        self.tts.say(s)

    #borg scale request behavior
    def ask_borg(self):
        if self.controller:
            self.controller.onBorgRequest.set()

        if self.db:
            self.db.General.SM.load_event(t ="borg_request", c = "timeout", v ="none")
        #request the dialog mnager the random borg sentence
        s = self.dialogs.get_borg_sentence()
        self.tts.say(s)

    #alert fatigue
    def alertFatigue(self):
        if self.db:
            self.db.General.SM.load_event(t ="alarm_fatigue", c = "timeout", v ="none")
        #set alarm  event
        self.tts.say(self.dialogs.sentenceWarning)

    #borg scale receive
    def thanks_borg(self):
        print("say_ thanks")
        s = self.dialogs.get_borg_receive()
        print s
        self.tts.say(s)

   #ask borg again behavior
    def ask_borg_again(self):

        s = self.dialogs.ask_borg_again()
        self.tts.say(s)

    #alert 1 behavior
    def alertHr1(self):
        if self.db:
            self.db.General.SM.load_event(t = "alert", c = "cause", v = "none")

        print("Alert")
        self.tts.say(self.dialogs.sentenceWarning)
        self.motion.rest()

    #aler 2 behavior
    #TODO: set redundancy control
    def alertHr2(self):
        if self.db:
            self.db.General.SM.load_event(t = "alert", c = "cause", v = "none")

        self.tts.say(self.dialogs.sentenceAlertHR)

    #call doctor behavior
    def callMedicalStaff(self):
        print("call doctor behavior")
        self.tts.say(self.dialogs.sentenceWarning)



#------------------------------------------------------------------------

    #shutdown method, stop routines and get to rest position
    def shutdown(self):
        self.animatedSpeech.say(self.dialogs.ByeSentence)
        self.stop_routines()
        self.motion.rest()


if __name__ == '__main__':
    r = Robot()
    print r.settings
