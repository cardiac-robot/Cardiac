# -*- coding: utf-8 -*-
import gui.RecognitionWin as RecognitionWin
#import BN
import robot.RecognitionMemory as RM
#import ISE
import robot.resources.photo_handler as PHOTO
import time

class RecognitionPlugin(object):
    def __init__(self, ProjectHandler = None, DataHandler = None):
        #load project_Handler
        self.PH = ProjectHandler
        #load database
        self.DB = DataHandler
        #create window
        self.RecognitionWin = RecognitionWin.RecognitionWin(ProjectHandler = self.PH)
        #id variable
        self.id = ""
        self.ExitConnect(f = self.onExitPressed)

    #creates all required objects to perform the recogntion
    def deploy_resources(self):
        #create image sender
        self.ISE = PHOTO.ImageSender(
                                     ip             = self.PH.GeneralSettings['robot']['IpRobot'],
                                     path           = self.PH.GeneralSettings['robot']['nao_image'],
                                     name           = 'took.jpg',
                                     tempPath       = self.PH.paths['recognition'],
                                     ProjectHandler = self.PH)

        #create recogniser bayesian network
        self.RecogniserBN  = RM.RecogniserBN(
                                              image_sender             = self.ISE,
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


        #set signals
        self.set_signals()

    #set required signals to interact with the plugins and resources
    def set_signals(self):
        #start recognition signal(recog button clicked)
        self.RecognitionWin.ControlButtons['StartRecog'].clicked.connect(self.start_recog)
        #When the id has been submitted from the gui
        self.RecognitionWin.onData.connect(self.idReceived)
        #when patient is registered and found in the database
        self.RecognitionWin.onRegistered.connect(self.onRegisteredCallback)
        #on recogntion confirmed and success
        self.RecognitionWin.onSuccess.connect(self.onSuccessCallback)

    #launch resources and shows the gui for recognition
    def LaunchView(self):
        #deploy resources
        self.deploy_resources()
        #launch view
        self.RecognitionWin.show()
        #print self.PH.GeneralSettings['IpRobot']

    #callback function to start recognition process, launched when the start recognition button is pressed
    def start_recog(self):
        self.start_count()
        print("recognition started ")
        #connect to the robot
        self.RecogniserBN.connectToRobot(ip         = self.PH.GeneralSettings['robot']['IpRobot'],
                                         useSpanish = True)

        #init session
        #TODO: revisar función y text to say
        self.RecogniserBN.initSession(isRegistered    = True,
                                      isMemoryRobot   = True,
                                      isAddPersonToDB = False,
                                      isDBinCSV       = False,
                                      personToAdd     = [])
        #take photo
        self.ISE.takePhoto()
        #send photo to the robot
        self.ISE.sendPhoto()
        #start recognition
        self.identity_est = self.RecogniserBN.startRecognition()
        #validation
        if self.identity_est != "0":
            print "Identity: " + self.identity_est
            self.id = self.identity_est
            self.finish_count()
            self.RecognitionWin.onConfirm.emit()
        else:
            print "Emiting on failed recognition signal"
            self.finish_count()
            self.RecognitionWin.onFailed.emit()




    #callback function called when the recognition has been carried out succesfuly
    def onSuccessCallback(self):

        #confirm person identity
        self.RecogniserBN.confirmPersonIdentity(p_id = self.id)
        #call id received function to set the user in the database
        self.idReceived(id_recog = self.id)
        #emit on start therapy
        self.RecognitionWin.onStartTherapy.emit()

    #callback function called when not recognized and need to indicate the id (submit button pressed)
    #and was found in the database
    def onRegisteredCallback(self):
        #confirm person identity with the recognized person
        self.RecogniserBN.confirmPersonIdentity(p_id = self.id)
        #emit on start therapy signal
        self.RecognitionWin.onStartTherapy.emit()

    def start_count(self):
        self.recog_init = time.time()

    def finish_count(self):
        self.recog_end = time.time()
        t = self.recog_end - self.recog_init
        print('###############################################################')
        print('TIEMPO RECONOCIMIENTO')
        print(t)
        print('###############################################################')


    #callback function called when not recognized and need to find patient in the database
    def idReceived(self, id_recog = None):
        #get the label conent
        if not id_recog:
            EmitOnRegister = True
            i = self.RecognitionWin.id
        else:
            EmitOnRegister = False
            i = id_recog
        print i
        #perform the login process
        status = self.DB.General.login(i = i)
        print status
        #get the status after login
        if status["registered"]:
            #if found in db, create session and start
            self.DB.General.SM.create_session()
            #load id
            self.id = i
            #validate both cases of use
            if EmitOnRegister:
                self.RecognitionWin.onRegistered.emit()
        else:
            self.RecognitionWin.onNotRegistered.emit()

    #close window
    def shutdown(self):
        #hide window
        self.RecognitionWin.hide()

    def ExitConnect(self,f):
        self.RecognitionWin.ControlButtons['CloseButton'].clicked.connect(f)

    def onExitPressed(self,f):
        self.RecogniserBN.shutdown()
        self.RecognitionWin.close()
