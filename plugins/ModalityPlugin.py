"""MODALITY PLUGIN"""
import gui.ModalityWin as ModalityWin


class ModalityPlugin(object):
    def __init__(self, ProjectHandler, DataHandler):
        #load ProjectHandler settings
        self.PH = ProjectHandler
        #load database manager
        self.DB = DataHandler
        #load gui resource
        self.ModalityWin = ModalityWin.ModalityWin(ProjectHandler = self.PH)
        #set signals
        self.set_signals()
        self.ExitConnect(f = self.onExitPressed)

    #signal connection method
    def set_signals(self):
        #connect to onNoRobot callback function when no robot button is pressed
        self.ModalityWin.ControlButtons['no_robot'].clicked.connect(self.onNoRobot)
        #connect to onRobot callback functin when robot button is ressed
        self.ModalityWin.ControlButtons['robot'].clicked.connect(self.onRobot)
        #connect to onMemoryRobot callback function when robot memory button is pressed
        self.ModalityWin.ControlButtons['robot_memory'].clicked.connect(self.onMemoryRobot)
        #close modality win whe it has been set
        self.ModalityWin.onModalitySet.connect(self.ModalityWin.hide)

    #show the view component
    def LaunchView(self):
        self.ModalityWin.show()

    #callback function when on no robot button clicked
    def onNoRobot(self):
        print("no robot")
        #close Modality window
        self.ModalityWin.close()
        #set modality on the database
        self.DB.General.set_modality(0)
        #emit on modality set signal
        self.ModalityWin.onModalitySet.emit()

    #callback function when on no robot button clicked
    def onRobot(self):
        print("robot")
        #close modality window
        self.ModalityWin.close()
        #set modality on the database
        self.DB.General.set_modality(1)
        #emit on modality set signal
        self.ModalityWin.onModalitySet.emit()

    #callback function when on  memory robot button clicked
    def onMemoryRobot(self):
        print("memory robot")
        #close Modality window
        self.ModalityWin.close()
        #set modality on the database
        self.DB.General.set_modality(2)
        #emit on modality set signal
        self.ModalityWin.onMemory.emit()

    def ExitConnect(self,f):
        self.ModalityWin.CloseButton.clicked.connect(f)

    def onExitPressed(self,f):
        self.ModalityWin.close()

    def shutdown(self):
        self.ModalityWin.hide
        del ModalityWin
        del self
