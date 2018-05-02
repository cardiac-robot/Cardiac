"""SETTINGS PLUGIN"""
import gui.SettingsWin as SettingsWin

class SettingsPlugin(object):
    def __init__(self, ProjectHandler, DataHandler):
        #load ProjectHandler settings
        self.PH = ProjectHandler
        #load database manager
        self.DB = DataHandler
        #load gui resource
        self.SettingsWin = SettingsWin.SettingsWin(ProjectHandler = self.PH)
        #set singals
        self.set_signals()

    #method to connect all signals
    def set_signals(self):
        self.SettingsWin.onData.connect(self.onDataReceived)
        self.SettingsWin.onEmptyField.connect(self.onEmptyData)
        self.CancelConnect(f = self.onCancelPressed)

    #launch view interface
    def LaunchView(self):
        self.SettingsWin.show()

    #callback function when onData signal is emitted
    def onDataReceived(self):
        print self.SettingsWin.inf_settings

    #callback function when onEmptyField signal is emitted
    def onEmptyData(self):
        print("empty field")

    #method to provide the connect mechanism to the cancel button
    def CancelConnect(self, f):
        self.SettingsWin.ControlButtons['cancel'].clicked.connect(f)

    #callback function when cancel button has been pressed
    def onCancelPressed(self):
        print("cancel")
        self.SettingsWin.close()

    #method to hide the window
    def HideView(self):
        self.SettingsWin.hide()

    #method to close the window
    def shutdown(self):
        self.SettingsWin.close()
