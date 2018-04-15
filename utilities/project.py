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
        #paths dcitionary
        self.paths = {
						'db'  			  : '/db',
						'backup'		  : '/db/backup',
						'data'			  : '/db/data',
                        'general'         : '/db/general',
                        'robot_db'        : '/db/robot',
                        'db_lib'          : '/db/lib',
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
