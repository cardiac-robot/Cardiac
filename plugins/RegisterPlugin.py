"""REGISTER PLUGIN"""

import gui.RegisterWin as RegisterWin

class RegisterPlugin(object):
    def __init__(self, ProjectHandler, DataHandler):
        #load ProjectHandler settings
        self.PH = ProjectHandler
        #load database manager
        self.DB = DataHandler
        #load gui resource
        self.RegisterWin = RegisterWin.RegisterWin(ProjectHandler = self.PH)
        #set signals
        self.set_signals()



    def set_signals(self):
        self.RegisterWin.onData.connect(self.onDataReceived)
        self.RegisterWin.onEmptyField.connect(self.onEmptyData)
        self.CancelConnect(f = self.onCancelPressed)

    #show the view window
    def LaunchView(self):
        self.RegisterWin.show()

    def onDataReceived(self):
        print self.RegisterWin.info_reg

    def onEmptyData(self):
        print("empty field")

    def CancelConnect(self, f):
        self.RegisterWin.controlbuttons_reg['Cancel'].clicked.connect(f)

    def onCancelPressed(self, f):
        self.RegisterWin.close()

    def HideView(self):
        self.RegisterWin.hide()

    def shutdown(self):
        self.RegisterWin.close()
