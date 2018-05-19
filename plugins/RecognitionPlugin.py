import gui.RecognitionWin as RecognitionWin
#import BN
#import ISE
import time

class RecognitionPlugin(object):
    def __init__(self, ProjectHandler = None, DataHandler = None):
        #load project_Handler
        self.PH = ProjectHandler
        self.DB = DataHandler
        #create window
        self.RecognitionWin = RecognitionWin.RecognitionWin(ProjectHandler = self.PH)
        #create recogniser bayesian network

        #create image sender
        #set signals
        self.set_signals()

    def set_signals(self):
        self.RecognitionWin.ControlButtons['StartRecog'].clicked.connect(self.start_recog)
        self.RecognitionWin.onData.connect(self.idReceived)

    def LaunchView(self):
        #launch view
        self.RecognitionWin.show()
        #print self.PH.GeneralSettings['IpRobot']

    def start_recog(self):
        print("recognition started ")
        time.sleep(5)
        self.RecognitionWin.onConfirm.emit()


    def idReceived(self):
        #get the label conent
        i = self.RecognitionWin.id
        #perform the login process
        status = self.DB.General.login(i = i)
        #get the status after login
        if status["registered"]:
            #if found in db, create session and start
            self.DB.General.SM.create_session()
            self.RecognitionWin.onRegistered.emit()
        else:
            self.RecognitionWin.onNotRegistered.emit()
