# -*- coding: utf-8 -*-
"""DATABASE CODE"""
"""
General database: Stores basic information of the system, patients registered and data recorded

General ./
         /Patients.csv
         /SensorSettings.csv
Data./
    ./PatientName/Date/Sensors.csv
    ./PatientName/Date/Events.csv


Robot:Stores the information related to the recognitions, speech and dialog available to the robot

Robot ./
      ./Recognition
      ./Dialogs.csv
"""
import lib.SessionManager as SM
import os
class database(object):
    def __init__(self, ProjectHandler = None):
        print("database created and launched")
        #load project handler
        self.PH = ProjectHandler
        #create general data manager
        self.General = General(ProjectHandler = self.PH)
        #create Robot data manager


class General(object):
    def __init__(self, ProjectHandler = None):
        #load project handler
        self.PH = ProjectHandler
        #User status create
        self.UserStatus = {"name" : "no data", "registered" : False}
        #create session data manager
        self.SM = SM.SessionManager(ProjectHandler = self.PH, UserStatus = self.UserStatus)
        #therapy status
        self.TherapyStatus = {"user": "none", "mode":0}

    #register user in db
    def register(self, user = None):
        self.UserStatus = self.SM.register_user(id_number = user['id'],
                                                name      = user['name'],
                                                age       = user['age'],
                                                gender    = "F",
                                                height    = user['height'],
                                                disease   = user ['patology'],
                                                crotch    = user['height_c'],
                                                weight    = user['weight'])
        self.TherapyStatus['user'] = self.UserStatus['name']
    #set modality for the therapy win
    def set_modality(self, d):
        self.TherapyStatus['mode'] = d

    #get last theray settings from db
    def get_therapy_settings(self):
        path = self.PH.paths['general']
        #read threapy settings files
        f = open(path + "/TherapySettings.csv", 'r')
        lines = f.readlines()
        settings  = lines[1].split(';')
        s = {'ImuPort': settings[0],
             'LaserPort': settings[1],
             'EcgPort': settings[2],
             'ImuSample':float(settings[3]),
             'LaserSample':float(settings[4]),
             'EcgSample': float(settings[5]),
             'IpRobot': settings[6],
             'Modality': int(settings[7])
             }

        self.TherapyStatus['mode'] = s['Modality']
        return s


if __name__=='__main__':

    class ProjectHandler(object):
        def __init__(self, settings = {
                                       'res': {'width': 1920, 'height': 1080},
                                       'sys': 'linux'
                                      },
                            log = True
                    ):

            #load settings
            self.settings = settings
            #get root directory
            self.root = os.getcwd()
            #paths dcitionary
            self.paths = {
    						'db'  			  : './',
    						'backup'		  : '/backup',
    						'data'			  : '/data',
                            'general'         : '/general',
                            'robot_db'        : '/robot',
                            'db_lib'          : '/lib',
    						'plugin'		  : '/plugins',
    						'gui' 			  : '/plugins/gui',
    						'img'             : '/plugins/gui/img',
    						'sensor_lib'      : '/plugins/lib',
    						'robotController' : '/plugins/robot',
                            'robotBehaviors'  : '/plugins/robot/behaviors',
                            'robotResources'  : '/plugins/robot/resources',
                            'utilities'       : '/utilities'
    					 }

            #print all info generated
            if log:
                self.print_info()

        #method that prints all the info and paths generated in the object
        def print_info(self):

            print('-------------------------------------------------')
            print('SYSTEM:')
            print(self.settings['sys'])
            print('-------------------------------------------------')
            print('Screen resolution')
            print(self.settings['res'])
            print('-------------------------------------------------')
            print('-----------setting directory address-------------')
            for i in self.paths:
    			print(i +" directory: "+ self.root +self.paths[i])
    			self.paths[i] = self.root + self.paths[i]
            print('-------------------------------------------------')

    ph = ProjectHandler()

    G = database(ProjectHandler = ph)
    a = G.General.get_therapy_settings()
    print a

    G.General.SM.register_user(id_number = "1031137220",name ="alfonso casas", age =46, gender= "F", height = 1.69, disease = "cvd")
    G.General.SM.load_event(t = "init",c = "none", v = "nd")
    G.General.SM.load_sensor_data(hr = 75, speed = 3.4, cadence= 0.8, sl = 1.0, inclination = 2.5)
    G.General.SM.load_sensor_data(hr = 75, speed = 3.4, cadence= 0.8, sl = 1.0, inclination = 2.5)
    G.General.SM.load_sensor_data(hr = 75, speed = 3.4, cadence= 0.8, sl = 1.0, inclination = 2.5)
    G.General.SM.load_sensor_data(hr = 75, speed = 3.4, cadence= 0.8, sl = 1.0, inclination = 2.5)
    G.General.SM.load_sensor_data(hr = 75, speed = 3.4, cadence= 0.8, sl = 1.0, inclination = 2.5)
    G.General.SM.load_event(t = "end",c = "none", v = "nd")
    G.General.SM.finish_session()