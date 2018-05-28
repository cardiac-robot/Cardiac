"""PROJECT HANDLER CODE"""
#library to get system utilities
import sys
#library to get os utilities
import os

#project_Handler object: Manages all the information of the project and location
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
        #self.root = self.root.replace("/","\\")
        #flag for settings
        self.OnSettings = False
        #general settings variable
        self.GeneralSettings = {'robot': {'IpRobot'       : "192.168.1.3",
                                          'port'          : 9559,#9559
                                          'mode'          : 1,
                                          'name'          : "Palin",
                                          'UseSpanish'    : True,
                                          'MotivationTime': 1*60,
                                          'BorgTime'      : 2*60,
                                          'useMemory'     : False,
                                          'nao_image'     : '/home/nao/dev/images',
                                          'UserProfile'   : {}
                                         },
                                'ecg'  : {"port" : 'COM8', "sample" : 1},
                                'imu'  : {"port" : 'COM8', "sample" : 1},
                                'laser': {"port" : 'COM8', "sample" : 1, 'crotch': 0.8},
                                'therapy':{'BorgSample' : 20}
                                }
        #paths dcitionary
        self.paths = {
						'db'  			  : '/db',
						'backup'		  : '/db/backup',
						'data'			  : '/db/data',
                        'general'         : '/db/general',
                        'robot_db'        : '/db/robot',
                        'db_lib'          : '/db/lib',
                        'current_user'    : '/',
						'plugin'		  : '/plugins',
						'gui' 			  : '/plugins/gui',
						'img'             : '/plugins/gui/img',
                        'recognition'     : '/db/recognition',
                        'recog_analysis'  : '/db/recognition/AnalysisFolder',
						'sensor_lib'      : '/plugins/lib',
						'robotController' : '/plugins/robot',
                        'robotBehaviors'  : '/plugins/robot/behaviors',
                        'robotResources'  : '/plugins/robot/resources',
                        'utilities'       : '/utilities'
					 }

        #print all info generated
        if log:
            self.print_info()

    #load general settings
    def load_general_settings(self, s):
        self.GeneralSettings['ecg']['sample']    = s['ecg_sample']
        self.GeneralSettings['ecg']['port']      = s['ecg_port']
        self.GeneralSettings['imu']['sample']    = s['imu_sample']
        self.GeneralSettings['imu']['port']      = s['imu_port']
        self.GeneralSettings['laser']['sample']  = s['laser_sample']
        self.GeneralSettings['laser']['port']    = s['laser_port']
        self.GeneralSettings['robot']['IpRobot'] = s['IpRobot']
        self.OnSettings = True

    def set_user_folder(self,f):
        self.paths['current_user'] =f
    #load detailed settings
    def load_advanced_settings(self,s):
        print('advanced settings')

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
