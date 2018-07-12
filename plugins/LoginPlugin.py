import gui.LogInWin as LogInWin

class LoginPlugin(object):
    def __init__(self, ProjectHandler = None, DataHandler = None):
        #load ProjectHandler
        self.PH = ProjectHandler
        #load DataHandler
        self.DB = DataHandler
        #create view
        self.LogInWin = LogInWin.LogInWin(ProjectHandler = self.PH)
        self.set_signals()

    def LaunchView(self):
        self.LogInWin.show()
        #validate if settings were modified
        if not self.PH.OnSettings:
            print "load settings from file"

    def set_signals(self):
        self.LogInWin.onData.connect(self.idReceived)


    def idReceived(self):
        #get the label conent
        i = self.LogInWin.id
        #perform the login process
        status = self.DB.General.login(i = i)
        #get the status after login
        if status["registered"]:
            #if found in db, create session and start
            self.DB.General.SM.create_session()
            self.LogInWin.onRegistered.emit()
        else:
            self.LogInWin.onNotRegistered.emit()

    def ExitConnect(self,f):
        self.LogInWin.CloseButton.clicked.connect(f)
