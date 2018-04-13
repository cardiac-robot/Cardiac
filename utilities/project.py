"""PROJECT HANDLER CODE"""
import sys

import os

class ProjectHandler(object):
    def __init__(self):
        #get root directory
        self.root = os.getcwd()
        #paths dcitionary
        self.paths = {
						'db'  			  : '/db',
						'backup'		  : '/db/backup',
						'data'			  : '/db/data',
						'plugin'		  : '/plugins',
						'gui' 			  : '/plugins/gui',
						'img'             : '/plugins/gui/img',
						'sensorLib'       : '/plugins/lib',
						'robotController' : '/plugins/robot',
                        'robotBehaviors'  : '/plugins/robot/behaviors',
                        'robotResources'  : '/plugins/robot/resources',
                        'utilities'       : '/utilities'
					 }

        print('-----------setting directory address-------------')
        for i in self.paths:
			print(i +" directory: "+ self.root +self.paths[i])
			self.paths[i] = self.root + self.paths[i]
        print('-------------------------------------------------')
