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


    def set_signals(self):
        self.ModalityWin.ControlButtons['no_robot'].clicked.connect(self.onNoRobot)
        self.ModalityWin.ControlButtons['robot'].clicked.connect(self.onRobot)
        self.ModalityWin.ControlButtons['robot_memory'].clicked.connect(self.onMemoryRobot)
        self.ModalityWin.onModalitySet.connect(self.ModalityWin.hide)

    #show the view component
    def LaunchView(self):
        self.ModalityWin.show()

    #on no robot button clicked
    def onNoRobot(self):
        print("no robot")
        self.DB.General.set_modality(0)
        self.ModalityWin.onModalitySet.emit()

    #on no robot button clicked
    def onRobot(self):
        print("robot")
        self.DB.General.set_modality(1)
        self.ModalityWin.onModalitySet.emit()

    #on no robot button clicked
    def onMemoryRobot(self):
        print("memory robot")
        self.DB.General.set_modality(2)
        self.ModalityWin.onMemory.emit()
