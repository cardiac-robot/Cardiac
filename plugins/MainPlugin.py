"""MAIN PLUGIN CODE"""
#import standart libs
import threading
import time
#import GUI library
from PyQt4 import QtGui, QtCore
#import gui component for the plugin
import gui.WelcomeWin as WelcomeWin
#import plugins
import MainMenuPlugin
import ModalityPlugin
import RegisterPlugin
import SettingsPlugin
import MainTherapyPlugin
import LoginPlugin



class MainPlugin(object):
    def __init__(self, ProjectHandler = None, DataHandler = None):
        #load project handler and system settings
        self.PH = ProjectHandler
        #load database object
        self.DB = DataHandler
        #launch presentation window
        self.WelcomeWin = WelcomeWin.WelcomeWin(ProjectHandler = self.PH)
        #show the window
        self.WelcomeWin.show()
        #create menu plugin
        self.MainMenuPlugin = MainMenuPlugin.MainMenuPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create register plugin
        self.RegisterPlugin = RegisterPlugin.RegisterPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create settings plugin
        self.SettingsPlugin = SettingsPlugin.SettingsPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create LoginWin
        self.LoginPlugin = LoginPlugin.LoginPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create modality plugin
        self.ModalityPlugin = ModalityPlugin.ModalityPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #create therapy plugin
        self.MainTherapyPlugin  = MainTherapyPlugin.MainTherapyPlugin(ProjectHandler = self.PH, DataHandler = self.DB)
        #set signals
        self.set_signals()
        #count_down in another thread
        threading.Thread(target = self.count_down).start()



    #this function creates all the binds between plugins through signals
    def set_signals(self):
        """
        FIRST STATE: show WelcomeWin during a period of time, after timer has finished, emits signals
        OnCountDownEnd emitted, the MainMenuWin must be displayed
        """
        #hide Welcome window when count_down ended
        self.WelcomeWin.OnCountDownEnd.connect(self.WelcomeWin.hide)
        #launch MainMenu window
        self.WelcomeWin.OnCountDownEnd.connect(self.MainMenuPlugin.LaunchView)
        self.WelcomeWin.OnShutDown.connect(self.shutdown)
        """
        MAIN MENU STATE: The main menu is displayed, all buttons of the main menu must be connected to each window
        [1] Register: SignInConnect must connect the register plugin
        [2] Settings: SettingsConnect must connect the Settings plugin
        [3] Log in: starts the therapy, and call the login window, followed by modality and then therapy plugin
        [4] Data: Data plugin not implemented yet
        """
        #[1] Register plugin connect
        self.MainMenuPlugin.SignInConnect(f = self.RegisterPlugin.LaunchView)
        #[2] SettingsPlugin connect
        self.MainMenuPlugin.SettingsConnect(f = self.SettingsPlugin.LaunchView)
        #[3] Log in plugin connect
        #TODO: to implement LoginWin
        self.MainMenuPlugin.LogInConnect(f =self.LoginPlugin.LaunchView)
        #self.MainMenuPlugin.LogInConnect(f = self.ModalityPlugin.LaunchView)
        #[4] DataPlugin connect
        #TODO: to implement
        #self.MainMenuPlugin.DataConnect(f = self.DataPlugin.LaunchView)
        """
        REGISTER STATE: register functionality defined
        register win has two signals
        [1]CancelConnect: when user cancel the register process, the window should close and reopen the main menu
        [2]onData: when there is data available and the register can be performed, the window should close and reopen the main menu
        """
        #[1] connect cancel button to relaunch the main menu and close the Register window
        self.RegisterPlugin.CancelConnect(f = self.MainMenuPlugin.LaunchView)
        #[2] connect onData signal, when data has been succesfuly filled in the form and ready to use, launch de main menu again
        self.RegisterPlugin.RegisterWin.onData.connect(self.MainMenuPlugin.LaunchView)
        """
        SETTINGS STATE: settings has similar behavior as the Register, has two signals
        [1] CancelConnect: when settings process has been canceled, the window should close and reopen main menu
        [2] onData: when data has been vaildated and the process finished, reopen the main menu
        """
        #[1] connect cancel button to reopen main window
        self.SettingsPlugin.CancelConnect(f = self.MainMenuPlugin.LaunchView)
        #[2] OnData validation signal implementation
        self.SettingsPlugin.SettingsWin.onData.connect(self.MainMenuPlugin.LaunchView)
        """
        LOG IN STATE: the login process should open a LoginWin and have two signals
        [1]onNotRegistered: if not registered, the register window should be displayed and LoginWin closed
        [2]onRegistered: if registered, the ModalityWin should be opened
        """
        #[1] integrate LoginWin
        self.LoginPlugin.LogInWin.onNotRegistered.connect(self.RegisterPlugin.LaunchView)
        #[2]if registered open the modality win
        self.LoginPlugin.LogInWin.onRegistered.connect(self.ModalityPlugin.LaunchView)
        """
        MODALITY STATE: the modality win emit three signals that set the configuration of the MainTherapyPlugin
        [1]onModalitySet: closes the window and launch the MainTherapyPlugin
        """
        #[1]connect MainTherapyPlugin to the onModalitySet signal
        self.ModalityPlugin.ModalityWin.onModalitySet.connect(self.MainTherapyPlugin.LaunchView)
        """
        THERAPY STATE
        """


    #count_down to start the application
    def count_down(self, t = 1):
        cont = 6
        while cont:
            cont = cont -1
            print cont
            time.sleep(t)
        #emit signal when count_down is finished
        self.WelcomeWin.OnCountDownEnd.emit()
        time.sleep(5)
        #emit signal to close the entire system
        self.WelcomeWin.OnShutDown.emit()

    #shutdown plugin
    def shutdown(self):
        self.WelcomeWin.close()
