#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example for integration of tablet and RecognitionMemory"""

import RecognitionMemory
from datetime import datetime
import time
import photo_handler as ph

if __name__ == "__main__":
    start_time = time.time()
    ise = ph.ImageSender(ip = '10.30.0.110')
    isSpanish = True
    RB = RecognitionMemory.RecogniserBN(image_sender = ise, testMode = False)
    

    print '1'
    RB.connectToRobot("10.30.0.110", useSpanish=isSpanish)
    print '2'
    isMemoryRobot = True # True if the robot with memory is used (get this from the days maybe?)
    isRegistered = True # False if register button is pressed (i.e. if the person starts the session for the first time)
    isAddPersonToDB = False # True ONLY IF THE EXPERIMENTS ARE ALREADY STARTED, THE BN IS ALREADY CREATED, ONE NEW PERSON IS BEING ADDED!FOR ADDING MULTIPLE PEOPLE AT THE SAME TIME, DELETE RecogniserBN.bif FILE INSTEAD!!!
    person = []
    if isAddPersonToDB:
        cur_date = datetime.now()
        person = ["1031137228", "jonathan casas", "Male", 25, 175, [cur_date]] # TODO: get from the tablet
        isRegistered = False
    print '3'
    # Press either register button (isRegistered = False) or start session button (isRegistered = True)
    RB.initSession(isRegistered = isRegistered, isMemoryRobot = isMemoryRobot, isAddPersonToDB = isAddPersonToDB, personToAdd = person)
    # TODO: take a picture and send to robot!
    print '4'
    ise.takePhoto()
    time.sleep(1)
    ise.sendPhoto()
    print '5'    
    identity_est = RB.startRecognition() # get the estimated identity from the recognition network
    p_id = None
    isRecognitionCorrect = False
    if isMemoryRobot:
        print '6'
        if isRegistered:
            if identity_est != '0':
                # TODO: ask for confirmation of identity_est on the tablet (isRecognitionCorrect = True if confirmed) 
                isRecognitionCorrect = True # True if the name is confirmed by the patient
                
    if isRecognitionCorrect:
        print '7'
        RB.confirmPersonIdentity(p_id = '1031137228') # save the network, analysis data, csv for learning and picture of the person in the tablet
    else:
        if isAddPersonToDB:
            # TODO: add person to DB
            print 'A'
            p_id = '1031137228'
        else:
            print 'B'
            p_id = '1031137228' # TODO: ask for patient name (p_name) on tablet
        print '*'*20
        print 'id'
        print p_id
        print '*'*20
        RB.confirmPersonIdentity(p_id = p_id)
    total_time = time.time() - start_time
    print total_time        
        
    # Start the session!
    
