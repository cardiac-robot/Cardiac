"""MAIN MENU PLUGIN"""
from PyQt4 import QtGui, QtCore


class MainMenuPlugin(object):
    def __init__(self, ProjectHandler, DataHandler):
        #load ProjectHandler settings
        self.PH = ProjectHandler
        #load database manager
        self.DB = DataHandler
        #load gui resource
