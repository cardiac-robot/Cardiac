# -*- coding: utf-8 -*-
"""ROBOT CONTROLLER CODE"""


import qi
import sys
import time


class Robot(object):
    def __init__(self, settings = { 'IpRobot': "192.168.0.100",
                                    'port'   : 9559,
                                    'name'   : 'Palin',
                                    'UseSpanish': True


                                    }
                 ):
        #load settings
        self.settings = settings

        #create Session
        self.session = qi.Session()
        #connect the session to the robot
        self.connect_session()
        #after connecting to the robot, get services and modules
        self.get_services()



    #connect to the robot through session
    def connect_session(self):
        try:
            self.session.connect("tcp://" + self.settings['IpRobot'] + ":" + str(self.settings['port']))
        except RuntimeError:
            logging.debug("Can't connect to Naoqi at ip \"" + self.settings['IpRobot'] + "\" on port " + str(self.settings['port'] +".\n"
                          "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

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

    #set language method
    def setLanguage(self, value):
        self.tts.setLanguage(value)

    #load Dialogs
    #TODO: LOAD Dialogs from files
    def load_dialogs(self):
        print("look in the database to load available dialogs")

if __name__ == '__main__':
    r = Robot()
    print r.settings
