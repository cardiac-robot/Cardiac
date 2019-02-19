# -*- coding: utf-8 -*-
import gui.RecognitionWin as RecognitionWin
#import BN
import robot.RecognitionMemory as RM
#import ISE
import robot.resources.photo_handler as PHOTO
import time
import datetime
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
        

    #launch resources and shows the gui for recognition
    def LaunchView(self):
        #deploy resources
        self.deploy_resources()
        #launch view
        self.RecognitionWin.show()
        #print self.PH.GeneralSettings['IpRobot']


    #creates all required objects to perform the recogntion
    def deploy_resources(self):

        #set on database the memory mode
        self.DB.set_memory(True)
        #create image sender
        self.ISE = PHOTO.ImageSender(
                                     ip             = self.PH.GeneralSettings['robot']['IpRobot'],
                                     path           = self.PH.GeneralSettings['robot']['nao_image'],
                                     name           = 'took.jpg',
                                     tempPath       = self.PH.paths['recognition'],
                                     ProjectHandler = self.PH
                                     )

        #create recogniser bayesian network
        self.RecogniserBN = RM.RecogniserBN()
        #set custom variables and parameters
        self.RecogniserBN.CardiacSetVariables(
                                              ProjectHandler = self.PH,
                                              DataHandler    = self.DB,
                                              PhotoHandler   = self.ISE
                                              )
        #set path files
        self.RecogniserBN.CardiacSetFilePaths()
        #set signals
        self.set_signals()


    #set required signals to interact with the plugins and resources
    def set_signals(self): 
        #start recognition signal(recog button clicked)
        self.RecognitionWin.ControlButtons['StartRecog'].clicked.connect(self.start_recog)
        #When the id has been submitted from the RecognitionWin view
        self.RecognitionWin.onData.connect(self.idReceived)
        #when patient is registered and found in the database
        self.RecognitionWin.onRegistered.connect(self.onRegisteredCallback)
        #on recogntion confirmed and success
        self.RecognitionWin.onSuccess.connect(self.onSuccessCallback)
        #when exit button is pressed
        self.ExitConnect(f = self.onExitPressed)



    #callback function to start recognition process, launched when the start recognition button is pressed
    def start_recog(self):
        #start recognition time counter
        self.start_count()
        #log the recognition
        print("recognition started ")
        #connect to the robot
        self.RecogniserBN.connectToRobot(ip         = self.PH.GeneralSettings['robot']['IpRobot'],
                                         useSpanish = True,
                                         imagePath  = "/home/nao/dev/images/nao_image.jpg")
        #set SessionConst session
        self.RecogniserBN.setSessionConstant(isDBinCSV = True)
        #set SessionVar session
        self.RecogniserBN.setSessionVar()
        #log paths to verify file locations
        self.RecogniserBN.CardiacPrintPaths()
        #take photo
        self.ISE.takePhoto()
        #send photo to the robot
        res = self.ISE.sendPhoto()
        #TODO:validate res from image transfering
        print "after ise from RecognitionPlugin"
        #start recognition
        self.identity_est = self.RecogniserBN.startRecognition()
        print self.identity_est
        #validation of the recognition
        if self.identity_est =="":
            #if none recognized
            #take photo
            self.ISE.takePhoto()
            #send photo to the robot
            res = self.ISE.sendPhoto()
            #TODO:validate res from image transfering

            #start recognition
            self.identity_est = self.RecogniserBN.startRecognition()

        elif self.identity_est != "0":
            #if someone is recognized
            #log the identity
            print "Identity: " + self.identity_est
            self.RecognitionWin.id_text2.setText('ID:'+ self.identity_est)
            #load identity
            self.id = self.identity_est
            #finish recognition count
            self.finish_count()
            #emit confirmation signal
            self.RecognitionWin.onConfirm.emit()
        else:
            print "Emiting on failed recognition signal"
            #finish confirmation signal
            self.finish_count()
            #emit fail recognition signal
            self.RecognitionWin.onFailed.emit()




    #callback function called when the recognition has been carried out succesfuly
    def onSuccessCallback(self):
        #confirm person identity
        self.RecogniserBN.confirmPersonIdentity(p_id = self.id)
        #call id received function to set the user in the database
        self.idReceived(id_recog = self.id)
        #save BN
        self.RecogniserBN.saveBN()
        #save face detection DB
        self.RecogniserBN.saveFaceDetectionDB(recog_folder = self.PH.paths['recognition'])
        #emit on start therapy
        self.RecognitionWin.onStartTherapy.emit()

    #callback function called when not recognized and need to indicate the id (submit button pressed)
    #and was found in the database
    def onRegisteredCallback(self):

        #confirm person identity with the recognized person
        print "confirmPersonIdentity"
        self.RecogniserBN.confirmPersonIdentity(p_id = self.id)
        #save BN
        print "saveBN"
        self.RecogniserBN.saveBN()
        #save face detection DB
        print "saveFaceDetectionDB"
        self.RecogniserBN.saveFaceDetectionDB(recog_folder = self.PH.paths['recognition'])
        #emit on start therapy signal
        print "emitting onStartTherapy"
        self.RecognitionWin.onStartTherapy.emit()

    #callback function called when not registered user has been detected
    def onNotRegisteredCallback(self):
        print"OnNorregisteredCallback"
        #self.id = self.DB.General.SM.UserStatus['id']
        self.person = self.DB.General.SM.person
        print "person: "+ str(self.person)
        t = datetime.datetime.now()
        #set incoming time 
        times = [str(t.hour)+":"+str(t.minute)+":"+str(t.second),str(t.weekday() + 1)]
        #set user information
        p = [self.person['id'], self.person['name'], self.person['gender'],int(self.person['age']), float(self.person['height']), [times]]
        #set person to add on the BN
        print "setPersonToAdd"
        self.RecogniserBN.setPersonToAdd(personToAdd = p)
        #confirm identity on the BN
        print "confirmPersonIdentity"
        self.RecogniserBN.confirmPersonIdentity(p_id = self.person['id'])
        #save BN
        print "saveBN"
        self.RecogniserBN.saveBN()
        #save face detection DB
        print "saveFaceDetectionDB"
        self.RecogniserBN.saveFaceDetectionDB(recog_folder = self.PH.paths['recognition'])
        #emit signal to start therapy
        print "emitting onStartTherapy"
        self.RecognitionWin.onStartTherapy.emit()

    #callback function called when not recognized and need to find patient in the database
    def idReceived(self, id_recog = None):
        #set true on the database to memory mode
        self.DB.set_memory(True)
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


    #method to record recognition time
    def start_count(self):
        self.recog_init = time.time()


    #method to finish recognition time recording
    def finish_count(self):
        self.recog_end = time.time()
        t = self.recog_end - self.recog_init
        print('###############################################################')
        print('TIEMPO RECONOCIMIENTO')
        print(t)
        print('###############################################################')


    #close window
    def shutdown(self):
        #hide window
        self.RecognitionWin.hide()

    #function to connect to the close button signal
    def ExitConnect(self,f):
        self.RecognitionWin.ControlButtons['CloseButton'].clicked.connect(f)

    #callback function when exit button is pressed
    def onExitPressed(self,f):
        self.RecogniserBN.shutdown()
        self.RecognitionWin.close()
