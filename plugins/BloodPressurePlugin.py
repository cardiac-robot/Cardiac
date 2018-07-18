import gui.BloodPressureWin as BloodPressureWin


class BloodPressurePlugin(object):
    def __init__(self, ProjectHandler, DataHandler):
        #project_Handler
        self.PH = ProjectHandler
        #datanhandler
        self.DB = DataHandler
        #create view
        self.View = BloodPressureWin.BloodPressureWin(ProjectHandler = self.PH)
        #set set_signals
        self.set_signals()
        #self.ExitConnect(f = self.onExitPressed)
        #mode
        self.mode = None


    def set_signals(self):
        self.View.onValue.connect(self.get_blood_pressure)

    def get_blood_pressure(self):
        #store the value in the event file
        self.DB.General.SM.load_event(t ="BloodPressure", c = self.Mode, v = self.View.bp)
        if self.Mode == "initial":
            self.View.onStartTherapy.emit()

        elif self.Mode == "final":
            self.View.onFinishTherapy.emit()

        self.View.close()

    def LaunchView(self):
        self.View.show()

    def set_mode(self, mode = None):
        self.Mode = mode

    def shutdown(self):
        self.View.close()

    """
    def ExitConnect(self,f):
        self.BloodPressureWin.exit_button.clicked.connect(f)

    def onExitPressed(self,f):
        self.BloodPressureWin.close()
    """
    



