"""SETTINGS PLUGIN"""
import gui.SettingsWin as SettingsWin
import robot.RecognitionMemory as RM
import os
import shutil

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
        self.ExitConnect(f = self.onExitPressed)

    #method to connect all signals
    def set_signals(self):
        self.SettingsWin.onData.connect(self.onDataReceived)
        self.SettingsWin.onEmptyField.connect(self.onEmptyData)
        self.CancelConnect(f = self.onCancelPressed)
        self.clearMemoryBNConnect(f = self.onClearMemoryBN)
        self.clearDatabaseConnect(f = self.onClearDatabase)

    #launch view interface
    def LaunchView(self):
        self.SettingsWin.show()

    #callback function when onData signal is emitted
    def onDataReceived(self):
        #get settings from the window
        s = self.SettingsWin.inf_settings
        #load general settings to the ProjectHandler
        self.PH.load_general_settings(s = s)
        print"SS"

    #callback function when onEmptyField signal is emitted
    def onEmptyData(self):
        print("empty field")

    #method to provide the connect mechanism to the cancel button
    def CancelConnect(self, f):
        self.SettingsWin.ControlButtons['cancel'].clicked.connect(f)

    def clearDatabaseConnect(self, f):
        self.SettingsWin.ControlButtons['clear_db'].clicked.connect(f)
    #method to provide the connect mechanism to the clearMemoryBN button
    def clearMemoryBNConnect(self, f):
        self.SettingsWin.ControlButtons['clearMemoryBN'].clicked.connect(f)
    #callback function when cancel button has been pressed
    def onCancelPressed(self):
        print("cancel")
        self.SettingsWin.close()

    def onClearDatabase(self):
        self.DB.General.clear_database(mem = False, gen = True)


    def onClearMemoryBN(self):
        '''
        self.BN = RM.RecogniserBN(
                                      image_sender             = None,
                                      testMode                 = False,
                                      recog_file               = self.PH.paths['recognition']    + "/RecogniserBN.bif",
                                      csv_file                 = self.PH.paths['recognition']    + "/RecogniserBN.csv",
                                      initial_recognition_file = self.PH.paths['recognition']    + "/InitialRecognition.csv",
                                      analysis_file            = self.PH.paths['recog_analysis'] + "/Analysis.json",
                                      db_file                  = self.PH.paths['recognition']    + "/db.csv",
                                      comparison_file          = self.PH.paths['recog_analysis'] + "/Comparison.csv",
                                      ProjectHandler           = self.PH,
                                      DataHandler              = self.DB
                                  )
        '''
        self.BN = RM.RecogniserBN()
        self.BN.CardiacSetVariables(
                                              ProjectHandler = self.PH,
                                              DataHandler    = self.DB,
                                              PhotoHandler   = None
                                              )
        #set path files
        self.BN.CardiacSetFilePaths()

        self.BN.resetFiles()
        #remove pictures
        path = self.PH.paths['recog_img']
        if os.path.exists(path):
            for f in os.listdir(path):
                print f
                f = os.path.join(path,f)
                os.remove(f)

        print('Memory files reset')



    #method to hide the window
    def HideView(self):
        self.SettingsWin.hide()

    #method to close the window
    def shutdown(self):
        self.SettingsWin.close()

    def ExitConnect(self,f):
        self.SettingsWin.CloseButton.clicked.connect(f)

    def onExitPressed(self,f):
        self.SettingsWin.close()
