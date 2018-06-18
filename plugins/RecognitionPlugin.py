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


    def set_signals(self):
        #start recognition signal(recog button clicked)
        self.RecognitionWin.ControlButtons['StartRecog'].clicked.connect(self.start_recog)
        #When the id has been submitted from the gui
        self.RecognitionWin.onData.connect(self.idReceived)
        #when patient is registered and found in the database
        self.RecognitionWin.onRegistered.connect(self.onRegisteredCallback)
        #on recogntion confirmed and success
        self.RecognitionWin.onSuccess.connect(self.onSuccessCallback)

    def LaunchView(self):
        #deploy resources
        self.deploy_resources()
        #launch view
        self.RecognitionWin.show()
        #print self.PH.GeneralSettings['IpRobot']

    def start_recog(self):
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
            self.RecognitionWin.onConfirm.emit()
        else:
            print "Emiting on failed recognition signal"
            self.RecognitionWin.onFailed.emit()


    def recognition_sucessfull(self):
        print("success in recognition")


    def recognition_fail(self):
        print("recognition failed")
        #make the robot

    def onSuccessCallback(self):

        print "ID ON SUCCESSCALLBACK" + self.id
        #confirm person identity
        self.RecogniserBN.confirmPersonIdentity(p_id = self.id)
        print "SUCCESSSSSSSS!!!!!"
        self.idReceived(id_recog = self.id)
        self.RecognitionWin.onStartTherapy.emit()

    def onRegisteredCallback(self):
        #confirm person identity with the recognized person
        self.RecogniserBN.confirmPersonIdentity(p_id = self.id)




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
            print "CREATE SESSSINNNNNNN"
            self.DB.General.SM.create_session()
            self.id = i
            if EmitOnRegister:
                self.RecognitionWin.onRegistered.emit()
        else:
            self.RecognitionWin.onNotRegistered.emit()

    def shutdown(self):
        self.RecognitionWin.hide()
