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
        self.ExitConnect(f = self.onExitPressed)

    #show the view window
    def LaunchView(self):
        self.RegisterWin.show()

    def LaunchViewMemoryMode(self):
        self.onMemory = True
        self.RegisterWin.show()

    def onDataReceived(self):
        print self.RegisterWin.info_reg
        #register the user
        self.DB.General.register(user = self.RegisterWin.info_reg)
        #check the register status
        if self.DB.General.UserStatus['registered']:
            #if patient already found in the database emit signal
            self.RegisterWin.onAlreadyRegistered.emit()
        else:
            if self.onMemory:
                self.RegisterWin.onNotRegistered.emit()

        self.shutdown()


    def onEmptyData(self):
        print("empty field")
        #launch pop up window or label in red

    def CancelConnect(self, f):
        self.RegisterWin.controlbuttons_reg['Cancel'].clicked.connect(f)

    def onCancelPressed(self, f):
        self.RegisterWin.close()

    def ExitConnect(self,f):
        self.RegisterWin.CloseButton.clicked.connect(f)

    def onExitPressed(self,f):
        self.RegisterWin.close()

    def HideView(self):
        self.RegisterWin.hide()

    def shutdown(self):
        self.RegisterWin.close()
