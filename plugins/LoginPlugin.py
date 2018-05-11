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
        p = {"name"   : "",
             "gender" : "",
                       "age"    : "",
                       "height" : "",
                       "weight" : "",
                       "crotch" : "",
                       "disease": "",
                       "id"     : i
                       }
        self.DB.General.SM.set_person(p  = p)
        #self.DB.General.SM.set_User(US  =)
        status = self.DB.General.SM.check_user()
        self.DB.General.SM.set_User(US  = status)
        if status["registered"]:
            self.LoginWin.onRegistered.emit()
        else:
            self.LoginWin.onNotRegistered.emit()
