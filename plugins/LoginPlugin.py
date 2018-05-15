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

    def set_signals(self):
        self.LogInWin.onData.connect(self.idReceived)


    def idReceived(self):
        i = self.LogInWin.id

        status = self.DB.General.login(i = i)
        #print status
        if status["registered"]:
            self.DB.General.SM.create_session()
            self.LogInWin.onRegistered.emit()
        else:
            self.LogInWin.onNotRegistered.emit()
