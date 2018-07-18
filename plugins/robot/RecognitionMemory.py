
# coding: utf-8
import numpy as np
import sys
# sys.path.insert(0, '../../db')
# sys.path.insert(0, '../../cam')

import os
import os.path
import shutil

#sys.path.append(os.path.abspath(os.path.join('..\..\..\CRRobot', 'db')))
#sys.path.append(os.path.abspath(os.path.join('..\..\..\CRRobot', 'cam')))

#print os.path.abspath(os.path.join('..\..\..\CRRobot\db', 'database'))
#from pylab import *
import matplotlib.pyplot as plt
import pyAgrum as gum
import pyAgrum.lib.notebook as gnb

# from scipy.stats import norm

import qi

import pandas

import math

import glob

#import db.database as db  # from ../../db folder

#import photo_handler # from ../../cam folder

# import database as db  # from ../../db folder

# import photo_handler # from ../../cam folder

from datetime import datetime

import csv

import ast

import time

import threading

import logging

import random # for making random choices for the phrases

import json

from collections import OrderedDict

import functools

from multiprocessing.dummy import Pool as ThreadPool

"""in the no-robot condition don't run this script"""
class RecogniserBN:
    def __init__(self,
                 image_sender             = None,
                 testMode                 = True,
                 recog_file               = "RecogniserBN.bif",
                 csv_file                 = "RecogniserBN.csv",
                 initial_recognition_file = "InitialRecognition.csv",
                 analysis_file            = "AnalysisFolder/Analysis.json",
                 db_file                  = "db.csv",
                 comparison_file          = "AnalysisFolder/Comparison.csv",
                 ProjectHandler           = None,
                 DataHandler              = None

                 ):

        self.PH = ProjectHandler
        self.DB = DataHandler
        np.set_printoptions(threshold=np.nan)
        print('PATH LINE 75 RECOGNITIONMEMORY.PY')
        print(os.path.dirname(__file__))
        self.useSpanish = False
        self.isImageFromTablet = False
        self.ise = image_sender

        self.recog_file = recog_file
        self.csv_file = csv_file
        self.initial_recognition_file = initial_recognition_file
        self.analysis_file = analysis_file
        self.db_file = db_file
        self.comparison_file = comparison_file

        self.node_names = ["I", "F", "G", "A", "H", "T"]
        self.prob_threshold = 0.000001 # the probability below 0.000001 is regarded as 0.000001
        self.init_min_threshold = 0.000001
        self.max_threshold = 0.99
        self.face_recognition_rate = 0.9
        self.gender_recognition_rate = self.max_threshold
        self.conf_threshold = 1 - self.max_threshold #the recognition confidence below 0.01 is regarded as 0.01 and all the probabilities are equal
        # TODO: determine weights
        self.weights = [1.0, 0.35, 0.15, 0.16, 0.23] # FOUND MANUALLY (by setting the minimum weights that allow the recognition test cases to be true)
        # [face_weight, gender_weight, age_weight, height_weight, time_weight]
#         self.weights = [0.94, 0.03, 0.0, 0.09, 0.24]
        self.conf_min_identity = 0.25 # minimum confidence of the identity recognition

        self.g_labels = ["Female", "Male"]

        self.unknown_var = "0"

        self.age_min = 0
        self.age_max = 75
#         self.stddev_age = 2
        z_age = self.normppf(self.max_threshold + (1-self.max_threshold)/2.0)
        self.stddev_age = 0.5/z_age

        self.height_min = 50 # TODO: LOOK AT THIS
        self.height_max = 240 # TODO: LOOK AT THIS
        self.stddev_height = 5 # TODO: LOOK AT THIS
        self.height_curve_interval = 47 # TODO: change this if stddev_height changes

        self.period = 5 # time is checked every 5 minutes
        self.stddev_time = 15/self.period # 15 minutes
        self.time_min = 0
        self.time_max = (7*24*60/self.period) -1 # 7(days)*24(hours)*60(minutes)/self.period ( = num_time_slots)

        # TODO: change this if stddev_time or period changes
        if self.period == 1:
            self.time_curve_interval = 135
        else:
            self.time_curve_interval = 135/self.period + 2

# # # # #         self.l_labels = ["Kitchen", "Office"]

        self.identity_est = ""
        self.recog_results = []
        self.isRegistered = True
        self.isMemoryRobot = True
        self.isMemoryOnRobot = False
        self.areParametersLearned = False
        self.isBNLoaded = False
        self.isDBinCSV = False
        self.isUnknownCondition = False
        self.nonweighted_evidence = []
        self.ie = None


        self.isMultipleRecognitions = False
        self.num_mult_recognitions = 3
        self.mult_recognitions_list = []
        self.ie_list = []
        self.recog_results_list = []
        self.analysis_data_list = []

        self.testMode = testMode

        """
        Nodes explained:

        Identity: "1", "2", "3".., "0" (for "unknown")
        Range variable because it is easier to change the number of states of the node as the database grows

        Face: "1"'s face, "2"'s face, "3"'s face.., "0" (for "unknown")
        See "Identity" variable explanation

        Gender: Labelized variable. Female (0 in Naoqi), Male (1 in Naoqi)

        Age: Range variable in [0, 75] (because Naoqi age detection is in the range of [0,75] ) P(A|I) = Gaussian curve

        Height: Range variable [50, 240] P(H|I) = Gaussian curve

        Location: Range variable (can be changed to labelized variable).
        Kitchen, bedroom, living room, office (the places can change depending on the experiment)
        !!!!!NOTE_COLOMBIA: Not used as the location is the same!!!!!

        Time: Range variable P(T|I) = Gaussian curve

        In RecogniserBN.csv: Field 'R' is used to identify the registering. If the person is registering for the first
        time the value is 1, otherwise 0.
        """

        self.robot_ip = "192.168.1.32"
        # self.connectToRobot(self.robot_ip)

    def connectToRobot(self, ip, port=9559, useSpanish = True, isImageFromTablet = True):
        print'1.1'
        self.robot_ip = ip
        self.robot_port = port
        self.session = qi.Session()
        self.PH.set_robot_session(self.session)

        try:

            self.session.connect("tcp://" + ip + ":" + str(port))

        except RuntimeError:
            logging.debug("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

        self.animatedSpeechProxy = self.session.service("ALAnimatedSpeech")

        self.tts = self.session.service("ALTextToSpeech")

        self.configuration = {"bodyLanguageMode":"contextual"}
        self.useSpanish = useSpanish
        self.face_service = self.session.service("ALFaceDetection")
        self.people_service = self.session.service("ALPeoplePerception")
        self.memory_service = self.session.service("ALMemory")
        self.recog_service = self.session.service("RecognitionService")
        self.isImageFromTablet = isImageFromTablet
        self.recog_service.initSystem(self.useSpanish,self.isImageFromTablet,"") # initialize the robot breathing, height offset, and language
        print'1.5'

    def setWeights(self, face_weight, gender_weight, age_weight, height_weight, time_weight):
        self.weights = [face_weight, gender_weight, age_weight, height_weight, time_weight]

    def setFaceRecognitionRate(self, face_rate):
        self.face_recognition_rate = face_rate

    def setGenderRecognitionRate(self, gender_rate):
        self.gender_recognition_rate = gender_rate

    def updateFaceRecognitionRate(self):
        self.face_recognition_rate = self.face_recognition_rate

    def subscribeToRecognitionResultsUpdated(self):
        self.recognitionResultsUpdatedEvent = "RecognitionResultsUpdated"
        self.recognitionResultsUpdated = self.memory_service.subscriber(self.recognitionResultsUpdatedEvent)
        print self.recognitionResultsUpdated
        self.idRecognitionResultsUpdated = self.recognitionResultsUpdated.signal.connect(functools.partial(self.onRecognitionResultsUpdated, self.recognitionResultsUpdatedEvent))
        print self.idRecognitionResultsUpdated
        self.recog_service.subscribeToPeopleDetected()

    def onRecognitionResultsUpdated(self, strVarName, value):
        self.recognitionResultsUpdated.signal.disconnect(self.idRecognitionResultsUpdated)
        self.recognitionResultsUpdated = None
        self.idRecognitionResultsUpdated = -1
        self.recog_temp = value
        print"setting the recogntion event"
        self.event_recog.set()

    def recognisePerson(self, num_recog = None):
        print 'recognisePerson 233'

        if self.recog_results_from_file is None:
            if self.isMultipleRecognitions:
                print'1'
                self.recog_service.setImagePathMult(num_recog)
            self.recog_service.subscribeToPeopleDetected()
            print'2'
            self.event_recog = threading.Event()
            self.subscribeToRecognitionResultsUpdated()
            print'3'
            self.event_recog.wait()
            print "4 after event recog"
            recog_results = self.recog_temp
            print'after wait 246'
        else:
            if self.isMultipleRecognitions:
                recog_results = self.recog_results_from_file[num_recog]
            else:
                recog_results = self.recog_results_from_file
        print '4'
        return recog_results

    def learnPerson(self, isRegistered, p_id):
        self.p_id = p_id
        if isRegistered:
            if self.isMultipleRecognitions:
                # Parallel learning takes longer than sequential learning
#                 pool = ThreadPool(self.num_mult_recognitions)
#                 joint_results = pool.map(self.threadedLearnPerson, [i for i in range(0, self.num_mult_recognitions)])
#                 pool.close()
#                 pool.join()
#                 print "time to learn parallel: " + str(time.time() - p_start_time)

                for num_recog in range(0, self.num_mult_recognitions):
                    self.recog_service.setImagePathMult(num_recog)
                    learn_face_success = self.recog_service.addPictureToPerson(p_id)
#                     if learn_face_success:
                    # the image was analysed and the results were included in the network so it should be saved even if the learn_face_success is False
                    print('saveImageToTablet 271')
                    self.saveImageToTablet(p_id, num_recog = num_recog)

            else:
                learn_face_success = self.recog_service.addPictureToPerson(p_id)
#                 if learn_face_success:
                # the image was analysed and the results were included in the network so it should be saved even if the learn_face_success is False
                print('saveImageToTablet 278')
                self.saveImageToTablet(p_id)
        elif not self.isMemoryOnRobot:
            if self.isMultipleRecognitions:
                for num_recog in range(0, self.num_mult_recognitions):
                    self.recog_service.setImagePathMult(num_recog)
                    if self.isMemoryOnRobot:
                        learn_face_success = self.recog_service.registerPersonOnRobot(p_id)
                        if num_recog == 0:
                            counter = 1
                            while not learn_face_success and counter < 3:
                                # TODO: take picture
                                learn_face_success = self.recog_service.registerPersonOnRobot(p_id)
                    else:
                        learn_face_success = self.recog_service.registerPerson(p_id)
                        if num_recog == 0:
                            counter = 1
                            while not learn_face_success and counter < 3:
                                # TODO: take picture
                                learn_face_success = self.recog_service.registerPerson(p_id)
                    print('saveImageToTablet 298')
                    self.saveImageToTablet(p_id, num_recog = num_recog)
            else:
                if self.isMemoryOnRobot:
                    learn_face_success = self.recog_service.registerPersonOnRobot(p_id)
                    if num_recog == 0:
                        counter = 1
                        while not learn_face_success and counter < 3:
                            learn_face_success = self.recog_service.registerPersonOnRobot(p_id)
                else:
                    print '*'*30
                    print 'ID RECOGMEMORY'
                    print p_id
                    print '*'*30
                    learn_face_success = self.recog_service.registerPerson(p_id)
                    counter = 1
                    while not learn_face_success and counter < 3:
                        # take another picture from tablet and send to robot
                        # TODO: try this!
                        self.ise.takePhoto()
                        time.sleep(1)
                        self.ise.sendPhoto()
                        learn_face_success = self.recog_service.registerPerson(p_id)
                print('saveImageToTablet 321')
                self.saveImageToTablet(p_id)

    def threadedLearnPerson(self, num_recog):
        self.recog_service.setImagePathMult(num_recog)
        learn_face_success = self.recog_service.addPictureToPerson(self.p_id)
#        if learn_face_success:
        # the image was analysed and the results were included in the network so it should be saved even if the learn_face_success is False
        print('saveImageToTablet 329')
        self.saveImageToTablet(self.p_id, num_recog = num_recog)
        return learn_face_success

    def setFilePaths(self, recog_folder):
        self.recog_file = recog_folder + self.recog_file
        self.csv_file = recog_folder + self.csv_file
        self.initial_recognition_file = recog_folder + self.initial_recognition_file
        self.analysis_file = recog_folder + self.analysis_file
        self.db_file = recog_folder + self.db_file
        self.comparison_file = recog_folder + self.comparison_file

    def learnParameters(self, csv_file, initial_recognition_file):
        # TODO: add location ast.literal_eval and append it to df when L (location) is used!

        df=pandas.read_csv(csv_file, dtype={"I": object}, converters={"F": ast.literal_eval, "G": ast.literal_eval, "A": ast.literal_eval, "H": ast.literal_eval})
        estimates_df = pandas.read_csv(initial_recognition_file, usecols=['F'], converters={"F": ast.literal_eval})
        self.df_orig = df.copy()
        self.df_I = set(df['I'].values.tolist())
        accuracy_db = 2.0 # in recognition the confidence can be 1.0, hence I use 2.0 to differentiate from recognition
        index_unknown = self.i_labels.index(self.unknown_var)
        for counter in range(0, len(self.i_labels)):
            if counter != index_unknown:
#                 li_f = [math.pow(self.init_min_threshold,self.weights[0]) for x in range(0, len(self.i_labels))]
#                 li_f[counter] = math.pow(1.0, self.weights[0])
                li_f = [math.pow((1 - self.face_recognition_rate)/(len(self.i_labels)-1),self.weights[0]) for x in range(0, len(self.i_labels))]
                li_f[counter] = math.pow(self.face_recognition_rate, self.weights[0])

#                 li_f[counter] = math.pow(1 - ((len(self.i_labels)-1)*math.pow(self.init_min_threshold,self.weights[0])),self.weights[0])
                li_f = self.normalise(li_f)

                accuracy = 1.0
                list_f = [[self.i_labels[x],li_f[x]] for x in range(0, len(self.i_labels))]
                list_f = [accuracy, list_f]

#                 li_g = [math.pow(self.init_min_threshold, self.weights[1]), math.pow(self.init_min_threshold, self.weights[1])]
#                 if self.genders[counter] == self.g_labels[0]:
#                     li_g[0] = math.pow(1-self.init_min_threshold, self.weights[1])
#                 else:
#                     li_g[1] = math.pow(1-self.init_min_threshold, self.weights[1])

                li_g = [math.pow(1 - self.gender_recognition_rate, self.weights[1]), math.pow(1 - self.gender_recognition_rate, self.weights[1])]
                if self.genders[counter] == self.g_labels[0]:
                    li_g[0] = math.pow(self.gender_recognition_rate, self.weights[1])
                else:
                    li_g[1] = math.pow(self.gender_recognition_rate, self.weights[1])
                li_g = self.normalise(li_g)
                list_g = [[self.g_labels[x],li_g[x]] for x in range(0, len(self.g_labels))]

                # only add one entry for the first time of a person (the remaining times are added later in computeRangeCPTfromDF)
                df = df.append(pandas.DataFrame.from_items([('I', [self.i_labels[counter]]),
                                                                ('F', [list_f]),
                                                                ('G', [list_g]),
                                                                ('A', [[self.ages[counter], accuracy_db]]),
                                                                ('H', [[self.heights[counter], accuracy_db]]),
                                                                ('T', [self.findTimeSlot(self.times[counter][0])]),
                                                                ('R', [0])]), ignore_index=True)
#         print df
        self.addUnknownLikelihood(self.r_bn)
        self.updateUnknownLikelihood(df, estimates_df, self.r_bn)
        for name_param in ["I","F","G"]:
            self.computeLabelizedCPTfromDF(self.r_bn, df, name_param)
        for name_param in ["A","H","T"]:
            self.computeRangeCPTfromDF(self.r_bn, df, name_param)

        self.areParametersLearned = True


    def computeLabelizedCPTfromDF(self, bn, df, name_param):
        """Compute the CPT of variable "name_param" in the BN bn from the database df"""
        id_v=bn.idFromName(name_param)
        index_unknown = self.i_labels.index(self.unknown_var)

        if name_param == "I":
            bn.cpt(id_v)[:] = self.updatePriorI()
        else:
            group_v = df.loc[:,['I',name_param]].groupby('I')
            for counter in range(0,len(self.i_labels)):
                if counter != index_unknown:
                    total_prob = []
                    gr = group_v.get_group(self.i_labels[counter])
                    for g_counter in range(0, len(gr)):
                        l_val = gr.iloc[g_counter,1]
                        prob_values = self.computeProbValues(name_param, l_val)

                        if g_counter == 0:
                            total_prob = prob_values[:]
                        else:
                            total_prob = [x + y for x, y in zip(total_prob, prob_values)]

                    total_prob = self.normalise(total_prob)

                    bn.cpt(id_v)[{'I':self.i_labels[counter]}] = total_prob[:]

    def computeRangeCPTfromDF(self, bn, df, name_param):
        """Compute the CPT of variable "name_param" in the BN bn from the database df (using soft evidence)"""
        id_v=bn.idFromName(name_param)
        index_unknown = self.i_labels.index(self.unknown_var)

        if name_param == "A":
            min_value = self.age_min
            max_value = self.age_max
        elif name_param == "H":
            min_value = self.height_min
            max_value = self.height_max
        elif name_param == "T":
            min_value = self.time_min
            max_value = self.time_max
        # TODO: change age curve calculation such that it is faster (look at T or H calculations)
        # (THINK ABOUT THE SIZE OF THE LIST -CURVE- WHICH COULD DETERMINE THE curve_interval)

        group_v = df.loc[:,['I',name_param]].groupby('I')
        for counter in range(0,len(self.i_labels)):
            if counter != index_unknown:
                gr = group_v.get_group(self.i_labels[counter])
                curve_total_pdf = []
                for g_counter in range(0, len(gr)):
                    l_val = gr.iloc[g_counter,1]
                    curve_pdf = self.computeProbValues(name_param, l_val)

                    if g_counter == 0:
                        curve_total_pdf = curve_pdf[:]
                    else:
                        curve_total_pdf = [x + y for x, y in zip(curve_total_pdf, curve_pdf)]

                if name_param == "T":
                    # add the remaining times in the database to the curve (when creating df, only the first time in the times of the person was added, so that
                    # the data is not repeated for face, age, gender, and height (which would bias the network). This way, I only add the remaining times to the time curve only
                    for t_counter in range(1, len(self.times[counter])): # start from self.times[counter][1] as 0 is used

                        curve_pdf = self.computeProbValues(name_param, self.findTimeSlot(self.times[counter][t_counter]))

                        curve_total_pdf = [x + y for x, y in zip(curve_total_pdf, curve_pdf)]
                curve_total_pdf = self.normalise(curve_total_pdf)
                bn.cpt(id_v)[{'I':self.i_labels[counter]}] = curve_total_pdf[:]
    #             plt.plot(range(min_value, max_value + 1),curve_total_pdf, label=self.i_labels[counter])

#         print name_param
#         plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
#         plt.show()

    def computeProbValues(self, name_param, l_val):
        if name_param == "F":
            w_i = 0
        elif name_param == "G":
            w_i = 1
        elif name_param == "A":
            w_i = 2
            stddev_v = self.stddev_age
            min_value = self.age_min
            max_value = self.age_max
        elif name_param == "H":
            w_i = 3
            stddev_v = self.stddev_height
            min_value = self.height_min
            max_value = self.height_max
            curve_interval = self.height_curve_interval
            # TODO: change this if things change (this is for making the code more time-efficient,
            # otherwise it takes very long to calculate pdf of each curve and add them up)
            curve_pdf_base = [0.06309573444801932 for x in range(min_value, max_value + 1)]
            curve_pdf_peak = [0.07268099908987054, 0.08701495407943342, 0.10334573211826904, 0.1217634209854823,
                              0.14232027702569458, 0.1650221966252439, 0.18982070900788367, 0.21660599021810098,
                              0.24520141868038245, 0.27536018101928744, 0.30676438883374674, 0.33902708124030684,
                              0.37169736560460764, 0.4042687945841943, 0.4361908992560245, 0.46688360643780863,
                              0.49575407629856555, 0.5222153182250288, 0.5457057929976087, 0.5657091007749367,
                              0.58177279787487, 0.5935253879830573, 0.6006905979161397, 0.6030981722463664,
                              0.6006905979161397, 0.5935253879830573, 0.58177279787487, 0.5657091007749367,
                              0.5457057929976087, 0.5222153182250288, 0.49575407629856555, 0.46688360643780863,
                              0.4361908992560245, 0.4042687945841943, 0.37169736560460764, 0.33902708124030684,
                              0.30676438883374674, 0.27536018101928744, 0.24520141868038245, 0.21660599021810098,
                              0.18982070900788367, 0.1650221966252439, 0.14232027702569458, 0.1217634209854823,
                              0.10334573211826904, 0.08701495407943342, 0.07268099908987054]
        elif name_param == "T":
            w_i = 4
            stddev_v = self.stddev_time
            min_value = self.time_min
            max_value = self.time_max
            curve_interval = self.time_curve_interval
            # TODO: change this if things change (this is for making the code more time-efficient,
            # otherwise it takes very long to calculate pdf of each curve and add them up)
            curve_pdf_base = [1.5848931924611124e-05 for x in range(min_value, max_value + 1)]
            curve_pdf_peak = [3.2797713065777e-05, 0.0001088922421767441, 0.00033078542438542475, 0.0009193731900581618,
                              0.0023379399468789253, 0.005439649461045743, 0.011579892363179918, 0.02255455054751459,
                              0.04019387502618488, 0.06553625561683843, 0.09776860472013102, 0.1334483646647943,
                              0.16665683928175243, 0.19042723955981805, 0.19908156626677875, 0.19042723955981805,
                              0.16665683928175243, 0.1334483646647943, 0.09776860472013102, 0.06553625561683843,
                              0.04019387502618488, 0.02255455054751459, 0.011579892363179918, 0.005439649461045743,
                              0.0023379399468789253, 0.0009193731900581618, 0.00033078542438542475, 0.0001088922421767441,
                              3.2797713065777e-05]

        prob_values = []
        prob = 1.0
        if name_param == "F":
            prob_values = self.setFaceProbabilities(l_val, self.weights[w_i])

        elif name_param == "G":
            for gender_counter in range(0, len(self.g_labels)):
                fr = l_val[gender_counter][1]
                if fr > self.max_threshold:
                    fr = self.max_threshold
                elif fr < 1 - self.max_threshold:
                    fr = 1 - self.max_threshold
#                 if fr < self.prob_threshold:
#                     fr = self.prob_threshold
                prob_values.append(math.pow(fr,self.weights[w_i]))
        else:
            if name_param == "T":
                mean_v = int(l_val)
            else:
                mean_v = int(l_val[0])
                prob = float(l_val[1])
                if name_param == "A":
                    if prob > self.max_threshold and prob <= 1.0:
                        prob = self.max_threshold

                    if prob >= self.conf_threshold and prob <= self.max_threshold:
#                         z= norm.ppf(prob + (1-prob)/2.0)
                        z = self.normppf(prob + (1-prob)/2.0)
                        stddev_v = 0.5/z
                    else:
                        stddev_v = self.stddev_age

            if prob < self.conf_threshold:
                # uniform distribution
                j_pdf = 1.0/(max_value - min_value + 1)
                prob_values = [j_pdf for x in range(min_value, max_value + 1)]
            else:
                # TODO: uncomment this when the weights are set (check and change the curve_pdf_peak and curve_pdf_base first)
#                 if name_param == "A":
#                     curve = norm(loc=mean_v,scale=stddev_v)  #Gaussian curve with mean at age of person and stddev of 2 years
                for j in range(min_value, max_value + 1):
#                         j_pdf = curve.pdf(j)
                    j_pdf = self.normpdf(j, mean_v, stddev_v)
                    if j_pdf < self.prob_threshold:
                        j_pdf = self.prob_threshold
                    prob_values.append(math.pow(j_pdf,self.weights[w_i]))
#                 else:
#                     prob_values = curve_pdf_base[:]
#                     counter_tt = 0
#                     while counter_tt <= (curve_interval -1)/2 and mean_v - counter_tt >= min_value:
#                         prob_values[mean_v - counter_tt - min_value] = curve_pdf_peak[(curve_interval -1)/2 - counter_tt]
#                         counter_tt += 1

#                     counter_tt = 1
#                     while counter_tt <= (curve_interval -1)/2 and mean_v + counter_tt <= max_value:
#                         prob_values[mean_v + counter_tt - min_value] = curve_pdf_peak[(curve_interval -1)/2 + counter_tt]
#                         counter_tt += 1
        prob_values = self.normalise(prob_values)
        return prob_values

    def loadBN(self, recog_file, csv_file, initial_recognition_file):
        # load previous BN from file or create a new BN if the file doesn't exist
        print 'enter loadBN'
        self.isBNLoaded = True
        self.areParametersLearned = False
        self.recog_file = recog_file
        self.csv_file = csv_file
        if self.isDBinCSV:
            self.loadDB()
            #self.loadDBFromCSV(self.db_file)
        else:
            self.loadDB()
        self.num_recognitions = sum(1 for line in open(csv_file)) - 1

        if os.path.isfile(recog_file):
            self.r_bn = gum.loadBN(recog_file)
            #         gnb.showBN(self.r_bn)
            self.loadVariables()
            self.setNumOccurrences(csv_file)
            print '.....................'
        elif self.num_people > 1:
            self.r_bn=gum.BayesNet('RecogniserBN')
            self.addNodes()
            self.addArcs()
            self.setNumOccurrences(csv_file)
            self.addCpts(csv_file, initial_recognition_file)

    def loadVariables(self):
        self.I = self.r_bn.idFromName("I")
        self.F = self.r_bn.idFromName("F")
        self.G = self.r_bn.idFromName("G")
        self.A = self.r_bn.idFromName("A")
        self.H = self.r_bn.idFromName("H")
        self.T = self.r_bn.idFromName("T")
# #         self.L = self.r_bn.idFromName("L")

    def updateProbabilities(self, p_id, ie):
        """Update P(I), P(F|I), P(G|I), P(A|I), P(H|I), P(T|I) in the network, before saving the network"""
        if p_id == self.unknown_var:
            iter_list = [self.node_names[1]]
        else:
            iter_list = self.node_names[1:]

        self.r_bn.cpt(self.I)[:] = self.updatePriorI()
        occur = self.num_occurrences[self.i_labels.index(p_id)] + 1 # occurrence in the database is added to the number of occurrences
        for counter in range(0, len(iter_list)):
            name_param = iter_list[counter]
            id_v = self.r_bn.idFromName(name_param)

            prev_prob_norm = self.r_bn.cpt(id_v)[{'I':p_id}][:]
            prev_prob = [i*occur for i in prev_prob_norm]

            l_val = self.nonweighted_evidence[counter]
            prob_values = self.computeProbValues(name_param, l_val)

            total_prob = [x + y for x, y in zip(prev_prob, prob_values)]
            norm_total_prob = self.normalise(total_prob)

            self.r_bn.cpt(id_v)[{'I':p_id}] = norm_total_prob[:]
        self.num_occurrences[self.i_labels.index(p_id)] += 1

    def priorIOccurrences(self, p_id = None):
        """NOT USED!! Reason: when I use this P(I=i) = num_times_i_seen/num_recognitions,
        the network is biased towards the people seen. So it is better to use equal values for P(I=i) = 1/len(database)"""
        prob_values = self.num_occurrences[:]
        if p_id is None:
            if sum(self.num_occurrences) == 0:
                prob_values = [1/len(self.i_labels) for i in range(0,len(self.i_labels))]
            else:
                for i_count in range(0, len(self.i_labels)):
                    if self.num_occurrences[i_count] == 0:
                        prob_values[i_count] = self.init_min_threshold
            prob_values = [i/float(self.num_recognitions) for i in prob_values]
        else:
            index_name = self.i_labels.index(p_id)
            if sum(self.num_occurrences) == 0:
                prob_values = [self.init_min_threshold for i in range(0,len(self.i_labels))]
                prob_values[index_name] = 1
            else:
                for i_count in range(0, len(self.i_labels)):
                    if i_count ==  index_name:
                        prob_values[i_count] += 1
                    elif self.num_occurrences[i_count] == 0:
                        prob_values[i_count] = self.init_min_threshold

            prob_values = [i/float(self.num_recognitions + 1) for i in prob_values]
        prob_norm = self.normalise(prob_values)
        return prob_norm

    def priorISequentialUpdating(self):
        """NOT USED!! Reason: Biases network towards people met before.
        According to Sequential Bayesian updating, posterior of the previous calculation can be used as the prior"""
        return self.ie.posterior(self.I)[:]

    def priorIEqualProbabilities(self):
        return [1.0/len(self.i_labels) for i in range(0, len(self.i_labels))]

    def updatePriorI(self, p_id = None):
#         updated_priors = self.priorISequentialUpdating()
#         updated_priors = self.priorIOccurrences(p_id)
        updated_priors = self.priorIEqualProbabilities()
        return updated_priors

    def saveBN(self, recog_file, p_id, ie, num_recog = None):
        # save BN before closing the system
        self.recog_file = recog_file
        self.updateProbabilities(p_id, ie)
        if self.isMultipleRecognitions:
            if num_recog == self.num_mult_recognitions - 1:
                gum.saveBN(self.r_bn, recog_file)
        else:
            gum.saveBN(self.r_bn, recog_file)

    def updateData(self, person):
#         person[0] = person[0].replace(" ","_")
        print('updateData 694 RecognitionMemory.py')
        print(person)
        self.i_labels.append(str(person[0]))
        self.names.append(person[1])
        self.genders.append(person[2])
        self.ages.append(person[3])
        self.heights.append(person[4])
        times_patients = []
        if self.isDBinCSV:
            for tt in person[5]:
                times_patients.append(tt[:2])
        else:
            for tt in person[5]:
                times_patients.append([tt.time().strftime('%H:%M:%S'), tt.isoweekday()])
        self.times.append(times_patients)
        self.num_people += 1

    def loadDummyData(self):
        self.i_labels = ["1","2","3"]
        self.names = ["Jane","James","John"]
        self.genders = ["Female","Male","Male"]
        self.ages = [25,25,25]
        self.heights = [168, 168, 168]
        self.times =[[["11:00:00",1]], [["11:00:00",1]], [["11:00:00",1], ["12:00:00",3]]]
        self.num_people = 3

    def addUnknown(self):
        self.i_labels.insert(0, self.unknown_var)
        self.names.insert(0, "unknown")
        self.genders.insert(0, "not-known")
        self.ages.insert(0, 35)
        self.heights.insert(0, 165)
        self.times.insert(0, [["00:00:00",1]])

    def addUnknownLikelihood(self, bn):
        # P(F|I)  : unknown is more likely to be unknown than anyone (however, this should change according to the result of inference)
        # P(F=self.unknown_var|I=self.unknown_var) = 0.5, P(F!=self.unknown_var|I=self.unknown_var) = 0.5/(self.num_people - 1)
        # self.num_people also includes self.unknown_var, whereas I need to divide it by the number of people in the database
        counter = self.i_labels.index(self.unknown_var)
#         li_f = [ math.pow(self.init_min_threshold,self.weights[0]) for x in range(0, len(self.i_labels))]
#         li_f[counter] = math.pow(1.0, self.weights[0])
#         li_f[counter] = math.pow(1 - ((len(self.i_labels)-1)*math.pow(self.init_min_threshold,self.weights[0])),self.weights[0])

        # TODO: decide what to do with this
#         li_f = [ 0.5/(self.num_people-1) for x in range(0, len(self.i_labels))]
#         li_f[counter] = 0.5

        li_f = [math.pow((1 - self.face_recognition_rate)/(len(self.i_labels)-1),self.weights[0]) for x in range(0, len(self.i_labels))]
        li_f[counter] = math.pow(self.face_recognition_rate, self.weights[0])

        bn.cpt(self.F)[{'I':self.unknown_var}] = self.normalise(li_f)

        # P(G|I) : Equally likely to be male or female
        bn.cpt(self.G)[{'I':self.unknown_var}] = [0.5, 0.5]

        # P(A|I) : Uniform distribution for unknown age
        bn.cpt(self.A)[{'I':self.unknown_var}] = self.uniformDistribution(self.age_min, self.age_max)

        # P(H|I) : Uniform distribution for unknown height
        bn.cpt(self.H)[{'I':self.unknown_var}] = self.uniformDistribution(self.height_min, self.height_max)

        # P(T|I) : Uniform distribution for any time
        bn.cpt(self.T)[{'I':self.unknown_var}] = self.uniformDistribution(self.time_min, self.time_max)

    def updateUnknownLikelihood(self, df, estimates_df, bn):

        indices_unknown = list(np.where(df["R"] == 1)[0])
        if indices_unknown:
            estimates_list = estimates_df['F'].values.tolist()

            total_prob = bn.cpt(self.F)[{'I':self.unknown_var}][:]
            for g_counter in indices_unknown:
                l_val = estimates_list[g_counter]
                prob_values = self.setFaceProbabilities(l_val, self.weights[0])
                total_prob = [x + y for x, y in zip(total_prob, prob_values)]

            total_prob = self.normalise(total_prob)

            bn.cpt(self.F)[{'I':self.unknown_var}] = total_prob[:]

    def loadDB(self):
        print 'loadDB enter'
        self.i_labels = []
        self.names = []
        self.genders = []
        self.ages = []
        self.heights = []
        self.times =[]
#         self.loadDummyData()
        p = self.DB.General.get_all_patients()
        #db_handler = db.DbHandler(testMode = self.testMode)
        #p = db_handler.get_all_patients()
        counter_p = 0
        for a in p:
#             name_person = str(a["name"])
#             name_person = name_person.replace(" ","_")
#             self.i_labels.append(name_person)
            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            #print(a.get('id_number'))
            #print(a
            self.i_labels.append(str(a[0]))
            self.names.append(str(a[1]))
            self.genders.append(str(a[2]))
            self.ages.append(int(a[3]))
            self.heights.append(float(a[4]))

        print 'calling addUnknown'
        all_times = self.DB.General.get_all_times()
        for key in all_times:
            times_patients = []
            user_times = all_times[key]
            if user_times:
                times_patients = [[i.time().strftime('%H:%M:%S'), i.isoweekday()] for i in user_times]
                self.times.append(times_patients)

        """for tt in a["times"]:
            times_patients.append([tt.time().strftime('%H:%M:%S'), tt.isoweekday()])
        self.times.append(times_patients)"""

        counter_p = counter_p + 1
        print "labels from loadDB"
        print self.i_labels
        print"TIMES from loadDB"
        for i in self.times:
            print i
        print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        self.addUnknown()

        self.num_people = len(self.i_labels)

#         self.printDB()

    def loadDBFromCSV(self, csv_file):
        db_df = pandas.read_csv(csv_file, dtype={"id": object}, converters={"times": ast.literal_eval})
#         self.i_labels = db_df['name'].values.tolist()
        self.i_labels = db_df['id'].values.tolist()
        self.names = db_df['name'].values.tolist()
        self.genders = db_df['gender'].values.tolist()
        self.ages = db_df['age'].values.tolist()
        self.heights = db_df['height'].values.tolist()
        self.times = []
        ti = db_df['times'].values.tolist()
        for t in ti:
            times_patients = []
            for tt in t:
                times_patients.append(tt[:2])
            self.times.append(times_patients)

        self.addUnknown()

        self.num_people = len(self.i_labels)

    def addNodes(self):

        # Identity node
        self.identity = gum.LabelizedVariable("I","Identity",0)
        for counter in range(0, len(self.i_labels)):
            self.identity.addLabel(self.i_labels[counter])
        self.I = self.r_bn.add(self.identity)

        # Face node
        self.face = gum.LabelizedVariable("F","Face",0)
        for counter in range(0, len(self.i_labels)):
            self.face.addLabel(self.i_labels[counter])
        self.F = self.r_bn.add(self.face)

        # Gender node
        self.gender = gum.LabelizedVariable("G","Gender",0)
        for counter in range(0, len(self.g_labels)):
            self.gender.addLabel(self.g_labels[counter])
        self.G = self.r_bn.add(self.gender)

        # Age node
        self.age = gum.RangeVariable("A","Age",self.age_min,self.age_max)
        self.A = self.r_bn.add(self.age)

        # Height node
        self.height = gum.RangeVariable("H","Height",self.height_min,self.height_max)
        self.H = self.r_bn.add(self.height)

        # Time node
        self.time_of_day = gum.RangeVariable("T","Time",self.time_min,self.time_max)
        self.T = self.r_bn.add(self.time_of_day)

#         gnb.showBN(self.r_bn)

# # # # #         # Location node
# # # # #         self.location = gum.LabelizedVariable("L","Location",0)
# # # # #         for counter in range(0, len(self.l_labels)):
# # # # #             self.location.addLabel(self.l_labels[counter])
# # # # #         self.L = self.r_bn.add(self.location)


    def addArcs(self):
        self.r_bn.addArc(self.I,self.F)
        self.r_bn.addArc(self.I,self.G)
        self.r_bn.addArc(self.I,self.A)
        self.r_bn.addArc(self.I,self.H)
        self.r_bn.addArc(self.I,self.T)
# #  #       self.r_bn.addArc(self.T,self.L)
# #  #       self.r_bn.addArc(self.I,self.L)

    def findTimeSlot(self, p_time):
        print "from findTimeSlot"
        print p_time
        tp = p_time[0].split(":")
        time_slot = (int(p_time[1])-1)*24*60/self.period + int(tp[0])*60/self.period + int(tp[1])/self.period
        return time_slot

    def addCpts(self, csv_file, initial_recognition_file):
        start_time = time.time()
        if self.num_recognitions > 0:
            self.learnParameters(csv_file, initial_recognition_clear
            )
        else:
            # P(I)
            self.r_bn.cpt(self.I).fillWith(1).normalize()
            index_unknown = self.i_labels.index(self.unknown_var)
            # P(F|I), P(G|I), P(A|I), P(H|I), P(T|I)
            for counter in range(0, len(self.i_labels)):
                if counter == index_unknown:
                    self.addUnknownLikelihood(self.r_bn)
                else:
                    print "counter from addCpts"
                    print counter
                    self.addLikelihoods(counter)
        print "time passed for learning: " + str(time.time() - start_time)

    def addLikelihoods(self, counter):
        """Start with equal probabilities for identities, i.e. P(I=i) = 1/num_people_db. For P(F=j|I=i) = self.prob_threshold for j!=i
        and 1-(num_people_db-1)*self.prob_threshold) if j=i"""

        # P(F|I)

#         li_f = [ math.pow(self.init_min_threshold,self.weights[0]) for x in range(0, len(self.i_labels))]
#         li_f[counter] = math.pow(1.0, self.weights[0])

#         li_f[counter] = math.pow(1 - ((len(self.i_labels)-1)*math.pow(self.init_min_threshold,self.weights[0])),self.weights[0])

        li_f = [math.pow((1 - self.face_recognition_rate)/(len(self.i_labels)-1),self.weights[0]) for x in range(0, len(self.i_labels))]
        li_f[counter] = math.pow(self.face_recognition_rate, self.weights[0])

        li_f = self.normalise(li_f)
        # what it does: self.r_bn.cpt(self.I)[{'F':0}]=1 SAME THING AS: self.r_bn.cpt(self.I)[{'F':self.unknown_var}]=[0.5,0.5]
        self.r_bn.cpt(self.F)[{'I':self.i_labels[counter]}] = li_f[:]

        # P(G|I)
#         li_g = [math.pow(self.init_min_threshold, self.weights[1]), math.pow(self.init_min_threshold, self.weights[1])]
#         if self.genders[counter] == self.g_labels[0]:
#             li_g[0] = math.pow(1-self.init_min_threshold, self.weights[1])
#         else:
#             li_g[1] = math.pow(1-self.init_min_threshold, self.weights[1])

        li_g = [math.pow(1 - self.gender_recognition_rate, self.weights[1]), math.pow(1 - self.gender_recognition_rate, self.weights[1])]
        if self.genders[counter] == self.g_labels[0]:
            li_g[0] = math.pow(self.gender_recognition_rate, self.weights[1])
        else:
            li_g[1] = math.pow(self.gender_recognition_rate, self.weights[1])
        li_g = self.normalise(li_g)
        self.r_bn.cpt(self.G)[{'I':self.i_labels[counter]}] = li_g[:]

        # P(A|I)
        print('COUNTER: .........................')
        print self.ages[counter]
        age_curve_pdf = self.getCurve(mean = self.ages[counter], stddev = self.stddev_age, min_value = self.age_min, max_value = self.age_max, weight = self.weights[2])
        self.r_bn.cpt(self.A)[{'I':self.i_labels[counter]}] = age_curve_pdf[:]

        # P(H|I)
        height_curve_pdf = self.getCurve(mean = self.heights[counter], stddev = self.stddev_height, min_value = self.height_min, max_value = self.height_max, weight = self.weights[3])
        self.r_bn.cpt(self.H)[{'I':self.i_labels[counter]}] = height_curve_pdf[:]

        # P(T|I)
        time_curve_total_pdf = []
        print"before for"
        print counter
        print "#####end####"
        for t_counter in range(0, len(self.times[counter])):
            print "t_counter from addLikelihoods"
            print t_counter
            print "self.times"
            print self.times[counter][t_counter]
            print "counter"
            print counter
            print "#####"
            mean = self.findTimeSlot(self.times[counter][t_counter])
            print mean
            print "-------"
            time_curve_pdf = self.getCurve(mean = mean , stddev = self.stddev_time, min_value = self.time_min, max_value = self.time_max, weight = self.weights[4])
            if t_counter == 0:
                time_curve_total_pdf = time_curve_pdf[:]
            else:
                time_curve_total_pdf = [x + y for x, y in zip(time_curve_total_pdf, time_curve_pdf)]
        time_curve_total_pdf = self.normalise(time_curve_total_pdf)
        self.r_bn.cpt(self.T)[{'I':self.i_labels[counter]}] = time_curve_total_pdf[:]

    def setFaceProbabilities(self, face_values, weight, isNormalisationOn = True):
        accuracy_face = face_values[0]
        face_similarities = []
        if len(face_values[1]) > 0:
            face_similarities = face_values[1][:]

        if len(face_similarities) == 0:
            face_similarities.append([self.unknown_var, 1.0])
        elif not (self.unknown_var in (x[0] for x in face_similarities)):
            max_similarity = max(face_similarities, key=lambda x: x[1])[1] # maximum similarity score in the face recognition
            face_similarities.append([self.unknown_var, 1.0 - max_similarity]) # the similarity score of unknown is 1-max_similarity

        r_results_names = []
        for counter in range(0, len(face_similarities)):
            r_results_names.append(face_similarities[counter][0])

        r_results_index = []
        for counter in range(0, len(self.i_labels)):
            if self.i_labels[counter] in r_results_names:
                r_results_index.append(r_results_names.index(self.i_labels[counter]))
            else:
                # if the person in database is not in face recognition database yet (did not have his/her first session yet)
                r_results_index.append(-1)

        face_result = []
        for counter in range(0, len(self.i_labels)):
            # values are normalised when using this method
            if r_results_index[counter] == -1:
                fr = self.prob_threshold
            else:
                fr = face_similarities[r_results_index[counter]][1]
                if fr < self.prob_threshold:
                    fr = self.prob_threshold
#             face_result.append(math.pow(fr,accuracy_face))
            accur = math.pow(fr,accuracy_face)
            face_result.append(math.pow(accur, weight))
        if isNormalisationOn:
            face_result = self.normalise(face_result)
        return face_result

    def setGenderProbabilities(self, gender_values, weight):
        gr = gender_values[1]

        # TODO: think about this!
        if gr > self.max_threshold:
            gr = self.max_threshold
#         if gr >= 1.0 - self.prob_threshold:
#             gr = 1 - self.prob_threshold
        gr_comp = 1 - gr

        gr_comp = math.pow(gr_comp, weight)
        gr = math.pow(gr, weight)
        sum_gr = gr + gr_comp
        if gender_values[0] == self.g_labels[0]:
            gender_result = [gr/sum_gr, gr_comp/sum_gr]
        else:
            gender_result = [gr_comp/sum_gr, gr/sum_gr]
        return gender_result

    def getNonweightedEvidenceResult(self):
        # P(e|F)
        face_result = self.setFaceProbabilities(self.recog_results[0], 1.0)

        # P(e|G)
        gender_result = self.setGenderProbabilities(self.recog_results[1], 1.0)

        # P(e|A)
        age_result = self.getCurve(conf = self.recog_results[2][1], mean = self.recog_results[2][0], min_value = self.age_min, max_value = self.age_max, weight = 1.0)

        # P(e|H)
        height_result = self.getCurve(conf = self.recog_results[3][1], mean = self.recog_results[3][0], stddev = self.stddev_height, min_value = self.height_min, max_value = self.height_max, weight = 1.0)

        # P(e|T)
        # todo: check time curve!
        time_result = self.getCurve(mean = self.findTimeSlot(self.recog_results[4]), stddev = self.stddev_time, min_value = self.time_min, max_value = self.time_max, weight = 1.0)

        return [face_result, gender_result, age_result, height_result, time_result]

    def setEvidence(self, recog_results, param_weights = None):
        """Call this function for self.num_people >=2 (when BN is created)"""
        # self.printPriors()

        if param_weights is None:
            param_weights = self.weights

        # P(e|F)
        face_result = self.setFaceProbabilities(recog_results[0], param_weights[0])

        # P(e|G)
        gender_result = self.setGenderProbabilities(recog_results[1], param_weights[1])

        # P(e|A)
        age_result = self.getCurve(conf = recog_results[2][1], mean = recog_results[2][0], min_value = self.age_min, max_value = self.age_max, weight = param_weights[2])

        # P(e|H)
        height_result = self.getCurve(conf = recog_results[3][1], mean = recog_results[3][0], stddev = self.stddev_height, min_value = self.height_min, max_value = self.height_max, weight = param_weights[3])

        # P(e|T)
        # todo: check time curve!
        time_result = self.getCurve(mean = self.findTimeSlot(recog_results[4]), stddev = self.stddev_time, min_value = self.time_min, max_value = self.time_max, weight = param_weights[4])


#         self.printEvidence(face_result, gender_result, age_result, height_result, time_result)

#         gnb.showInference(self.r_bn,evs={"F":face_result, "G":gender_result, "A":age_result, "H":height_result, "T":time_result})

        ie = gum.LazyPropagation(self.r_bn)
        ie.setEvidence({"F":face_result, "G":gender_result, "A":age_result, "H":height_result, "T":time_result})
        ie.makeInference()

#         self.printInference(ie)

        return ie

    def getPosteriorIUsingCalculatedEvidence(self, bn, evidence):
        ie = gum.LazyPropagation(bn)
        ie.setEvidence({"F":evidence[0], "G":evidence[1], "A":evidence[2], "H":evidence[3], "T":evidence[4]})
        ie.makeInference()
        post_I = ie.posterior(self.I)[:]
#         i_post = np.array(post_I)
#         i_max_cpt = np.max(ie.posterior(self.I)[:])
#         identity_est = self.i_labels[np.argmax(ie.posterior(self.I)[:])]
#         if np.isclose(i_post, i_max_cpt).all() or i_max_cpt < self.conf_min_identity or len(i_post[i_post>=i_max_cpt]) > 1:
#             i_post[0] += 1.0
#             post_I = self.normalise(i_post)
        return post_I

    def getEstimatedProbabilities(self):
        """If the results is unknown because of an unknown condition (see recognise function), increase the probability of unknown and normalise"""
        if self.num_people > 1:
            post_I = self.identity_prob_list
    #         if self.isUnknownCondition:
    #             post_I[0] += 1.0
    #             post_I = self.normalise(post_I)
        else:
            post_I = [1.0] # unknown
        return post_I

    def fillNonweightedEvidence(self, recog_results):

        # SOFT EVIDENCE:
        print "RECOG_RESULTS 1139"
        print type(recog_results)
        face_est = recog_results[0][:]

        gender_val = recog_results[1][:]

        if gender_val[0] == self.g_labels[0]:
            gender_est = [[self.g_labels[0], gender_val[1]],[self.g_labels[1], 1- gender_val[1]]]
        else:
            gender_est = [[self.g_labels[0], 1- gender_val[1]],[self.g_labels[1], gender_val[1]]]
        age_est = recog_results[2][:]
        height_est = recog_results[3][:]
        time_cur= recog_results[4][:]
        time_est = self.findTimeSlot(time_cur) #hard evidence for time

        return [face_est, gender_est, age_est, height_est, time_est]

        # HARD EVIDENCE:
#         face_est = recog_results[0][1][0][0]
#         gender_est = recog_results[1][0]
#         age_est = recog_results[2][0]
#         height_est = recog_results[3][0]
#         time_cur= recog_results[4]
#         time_est = self.findTimeSlot(time_cur)

    def saveCSV(self, csv_file, identity_real):
        self.csv_file = csv_file
        r = 0 # is not registering
        if not self.isRegistered:
            r = 1 # is registering

        df = pandas.DataFrame.from_items([('I', [identity_real]),
                                          ('F', [self.nonweighted_evidence[0]]),
                                          ('G', [self.nonweighted_evidence[1]]),
                                          ('A', [self.nonweighted_evidence[2]]),
                                          ('H', [self.nonweighted_evidence[3]]),
                                          ('T', [self.nonweighted_evidence[4]]),
                                          ('R', [r])])
        with open(csv_file, 'a') as fd:
            df.to_csv(fd, index=False, header=False)

    def saveEstimatedResultCSV(self, initial_recognition_file, recog_results, identity_est):
        self.initial_recognition_file = initial_recognition_file

        gender_val = recog_results[1][:]
        if gender_val[0] == self.g_labels[0]:
            gender_est = [[self.g_labels[0], gender_val[1]],[self.g_labels[1], 1- gender_val[1]]]
        else:
            gender_est = [[self.g_labels[0], 1- gender_val[1]],[self.g_labels[1], gender_val[1]]]

        time_cur= recog_results[4][:]
        time_est = self.findTimeSlot(time_cur) #hard evidence for time

        df = pandas.DataFrame.from_items([('I_est', [identity_est]),
                                          ('F', [recog_results[0][:]]),
                                          ('G', [gender_est]),
                                          ('A', [recog_results[2][:]]),
                                          ('H', [recog_results[3][:]]),
                                          ('T', [time_est])])
        with open(initial_recognition_file, 'a') as fd:
            df.to_csv(fd, index=False, header=False)

    def saveComparisonCSV(self, comparison_file, identity_real, identity_est, posterior_average, calc_time):
        self.comparison_file = comparison_file
        r = 0 # is not registering
        if not self.isRegistered:
            r = 1 # is registering

        df = pandas.DataFrame.from_items([('I_real', [identity_real]),
                                          ('I_est', [identity_est]),
                                          ('I_prob', [posterior_average]),
                                          ('Calc_time', [calc_time]),
                                          ('R', [r])])
        with open(comparison_file, 'a') as fd:
            df.to_csv(fd, index=False, header=False)

    def saveDBToCSV(self, db_file, person):
        df = pandas.DataFrame.from_items([('id', [person[0]]),
                                          ('name', [person[1]]),
                                          ('gender', [person[2]]),
                                          ('age', [person[3]]),
                                          ('height', [person[4]]),
                                          ('times', [person[5]])])
        with open(db_file, 'a') as fd:
            df.to_csv(fd, index=False, header=False)

    def getAnalysisData(self, recog_results, identity_real, ie):
        i_post = ie.posterior(self.I)[:]
        i_max_cpt = np.max(ie.posterior(self.I)[:])
        identity_est = self.i_labels[np.argmax(ie.posterior(self.I)[:])]
        isclose_ar = np.isclose(i_post, i_max_cpt)
        if np.isclose(i_post, i_max_cpt).all():
            # if all states are equally likely then the person is unknown
            identity_est = "unknown-equal"
        elif len(isclose_ar[isclose_ar==True]) > 1:
            # if maximum appears more than one time in the array
            identity_est = "unknown-max-equal"
        elif i_max_cpt < self.conf_min_identity:
             # if maximum confidence is lower than self.conf_min_identity
            identity_est = "unknown-low"
        date_today = recog_results[4][2]+" "+ recog_results[4][3] +" "+ recog_results[4][4] +" "+ recog_results[4][0]

        print "getAnalysisData 1240"
        a =  str(recog_results[4][2])
        b =  str(recog_results[4][3])
        c =  str(recog_results[4][4])
        d =  str(recog_results[4][0])
        print a, b,c,d
        #date_today = str(date_today)
        da = a+" "+b+" "+c+" "+d

        print da
        #date_now = str(datetime.strptime(da, "%d %B %Y %H:%M:%S"))
        date_now = str(datetime.now())
        data = OrderedDict([("Date", date_now),
                ("Database", self.i_labels),
                ("I_real", identity_real),
                ("I_est", [identity_est, i_max_cpt]),
                ("I_cpt", self.r_bn.cpt(self.I)[:].tolist()),
                ("I_posterior", ie.posterior(self.I)[:].tolist()),
                ("F_est", recog_results[0]),
                ("F_cpt", self.r_bn.cpt(self.F)[:].tolist()),
                ("F_posterior", ie.posterior(self.F)[:].tolist()),
                ("G_est", recog_results[1]),
                ("G_cpt", self.r_bn.cpt(self.G)[:].tolist()),
                ("G_posterior", ie.posterior(self.G)[:].tolist()),
                ("A_est", recog_results[2]),
                ("A_cpt", self.r_bn.cpt(self.A)[:].tolist()),
                ("A_posterior", ie.posterior(self.A)[:].tolist()),
                ("H_est", recog_results[3]),
                ("H_cpt", self.r_bn.cpt(self.H)[:].tolist()),
                ("H_posterior", ie.posterior(self.H)[:].tolist()),
                ("T_est", recog_results[4]),
                ("T_cpt", self.r_bn.cpt(self.T)[:].tolist()),
                ("T_posterior", ie.posterior(self.T)[:].tolist())])
        return data

    def saveAnalysisToDB(self, recog_results, identity_real, ie):
        """Call this file for self.num_people >= 2"""
        data = self.getAnalysisData(recog_results, identity_real, ie)
        print "RECOGNITION DATA 1279"
        print data['Database']
        #db_handler = db.DbHandler()
        #db_handler.save_recognition_data(data)

    def saveAnalysisToJson(self, recog_results, identity_real, ie, isPrevSavedToAnalysis, num_recog = None):
        """Call this file for self.num_people >= 2"""

        a = []
        if self.isMultipleRecognitions and num_recog < self.num_mult_recognitions - 1:
            self.analysis_data_list.append(self.getAnalysisData(recog_results, identity_real, ie))
        else:
            if self.isMultipleRecognitions:
                self.analysis_data_list.append(self.getAnalysisData(recog_results, identity_real, ie))
                a = self.analysis_data_list
                if self.num_recognitions > 0:
                    num_file = self.num_recognitions/self.num_mult_recognitions
                else:
                    num_file = self.num_recognitions
            else:
                dt = self.getAnalysisData(recog_results, identity_real, ie)
                a.append(dt)
                num_file = self.num_recognitions

            if isPrevSavedToAnalysis:
                fname = self.analysis_file.replace(".json","") + str(num_file) + "_2.json"
            else:
                fname = self.analysis_file.replace(".json","") + str(num_file) + ".json"
    #         if not os.path.isfile(fname):
            with open(fname, mode='w') as f:
                f.write(json.dumps(a, ensure_ascii=False, indent=2))
    #         else:
    #             with open(fname) as feedsjson:
    #                 feeds = json.load(feedsjson, object_pairs_hook=OrderedDict)

    #             feeds.append(data)
    #             with open(fname, mode='w') as f:
    #                 f.write(json.dumps(feeds, ensure_ascii=False, indent=2))


    def updateNodes(self, p_id):
        """Call the function when a new person added is to the db
        CPT is a property of the BN and not the variable, therefore,
        to add a new state to a node, it is necessary to copy the previous CPT,
        change it accordingly (normalize it, or change it?),
        erase the node, redefine the node
        (e.g. self.face = gum.LabelizedVariable("F","Face",num_people)),
        add the changed node back to the BN, add the arcs, and add the changed CPT to it
        change the CPT of the child nodes
        """
        # Update the face recognition rate depending on the function of change depending on the number of people in the db
        prev_face_recog_rate = self.face_recognition_rate
        self.updateFaceRecognitionRate()

        # Copy CPTs
        cpts = []
        for counter in range(0,self.r_bn.size()):
            nod = self.r_bn.idFromName(self.node_names[counter])
            cpts.append(self.r_bn.cpt(nod)[:])

        # Erase I and F
        self.r_bn.erase(self.I)
        self.r_bn.erase(self.F)

        # Change and add nodes
        # Face node
        self.face = gum.LabelizedVariable("F","Face",0)
        for counter in range(0, len(self.i_labels)):
            self.face.addLabel(self.i_labels[counter])
        self.F = self.r_bn.add(self.face)

        # Identity node
        self.identity = gum.LabelizedVariable("I","Identity",0)
        for counter in range(0, len(self.i_labels)):
            self.identity.addLabel(self.i_labels[counter])
        self.I = self.r_bn.add(self.identity)

        self.addArcs()

        # Change CPT
        updated_cpt_I = []
        for counter in range(0, len(self.i_labels)):
            if counter < len(self.i_labels) - 1:
#                 updated_cpt_F = np.append(cpts[1][counter], [self.init_min_threshold])
                if self.num_occurrences[counter] == 0:
                    for ff in range(0, len(self.i_labels)-1):
                        if np.isclose(cpts[1][counter][ff], (1-prev_face_recog_rate)/(len(self.i_labels)-2)):
                            cpts[1][counter][ff] = (1-self.face_recognition_rate)/(len(self.i_labels)-1)
                    updated_cpt_F = cpts[1][counter][:]
                else:
                    occur = self.num_occurrences[counter] + 1
                    updated_cpt_F = [i*occur for i in cpts[1][counter]]
                updated_cpt_F = np.append(updated_cpt_F, [(1-self.face_recognition_rate)/(len(self.i_labels)-1)])
                updated_cpt_F = self.normalise(updated_cpt_F)
                self.r_bn.cpt(self.F)[{'I':self.i_labels[counter]}] = updated_cpt_F[:]

                self.r_bn.cpt(self.G)[{'I':self.i_labels[counter]}] = cpts[2][counter][:]
                self.r_bn.cpt(self.A)[{'I':self.i_labels[counter]}] = cpts[3][counter][:]
                self.r_bn.cpt(self.H)[{'I':self.i_labels[counter]}] = cpts[4][counter][:]
                self.r_bn.cpt(self.T)[{'I':self.i_labels[counter]}] = cpts[5][counter][:]
            else:
                self.addLikelihoods(counter)

        self.r_bn.cpt(self.I)[:] = self.updatePriorI(p_id)

        ie = gum.LazyPropagation(self.r_bn)
        ie.makeInference()

#     def addPersonToBN(self, person, isDBinCSV = False):
    def addPersonToBN(self, person):
        """get from input (for adding people into db) (person = ["1", Jane", "Female", 26, 175, [arrayOfTimesOfSessionsInDateTimeFormat]])"""
        print('addPersonToBN 1332')
        print(person)
        if not self.isBNLoaded:
            self.loadBN(self.recog_file, self.csv_file, self.initial_recognition_file)
#         person[0] = person[0].replace(" ","_")
        if person[0] in self.i_labels:
            logging.debug("The patient is already in the database.")
        else:
            self.updateData(person)
            if self.isDBinCSV:
                self.saveDBToCSV(self.db_file, person)

        if self.num_people == 2:
            self.r_bn=gum.BayesNet('RecogniserBN')
            self.addNodes()
            self.addArcs()
            self.setNumOccurrences(self.csv_file)
            self.addCpts(self.csv_file, self.initial_recognition_file)
        elif self.num_people > 2:
            if self.r_bn.variableFromName("I").toLabelizedVar().isLabel(person[0]):
                logging.debug("The patient is already in the network.")
            else:
                self.updateNodes(person[0])
                self.num_occurrences.append(0)

    def saveImageToTablet(self, p_id, num_recog=None):
        # TODO: check with windows (/ might need to be \ instead)
        #cur_dir = os.path.dirname(os.path.realpath(__file__))
        #temp_dir = os.path.abspath(os.path.join(cur_dir, '../..', 'cam')) + "/"
        image_dir = self.PH.paths['recog_img']
        print 'GET IMAGE PATH'
        temp_image = self.ise.get_image_path()
        print temp_image
        if self.isMultipleRecognitions:
            match_name = image_dir + p_id + "*-0.jpg"
            num_matches = len(glob.glob(match_name)) + 1
            orig_matches = num_matches
            to_rep = str(num_recog) + ".jpg"
            temp_image = self.imagePath.replace(".jpg", to_rep)
            counter = 0
            for i in range(0,4):
                if num_matches/10 != 0:
                    num_matches = num_matches/10
                    counter += 1
                else:
                    counter += 1
                    break
            print('image_dir: ' + image_dir)
            #rint('image_dir: ' + image_dir)
            save_name = image_dir + p_id + "_" + (str(0)*(4-counter)) + str(orig_matches) + "-" + str(num_recog) +".jpg"
            os.rename(temp_image,save_name)
        else:
            match_name = image_dir + p_id + "*.jpg"
            num_matches = len(glob.glob(match_name)) + 1
            orig_matches = num_matches
            counter = 0
            for i in range(0,4):
                if num_matches/10 != 0:
                    num_matches = num_matches/10
                    counter += 1
                else:
                    counter += 1
                    break
            save_name = image_dir + "/" + p_id + "_" + (str(0)*(4-counter)) + str(orig_matches) + ".jpg"
            print('Os rename ' +  temp_image + ' ' + save_name)
            os.rename(temp_image,save_name)

    def setPersonIdentityMult(self, isRegistered = True, p_id = None, recog_results_from_file = None):
        isPrevSavedToAnalysis = False
        if p_id is None:
            p_id = self.identity_est
        if self.isAlreadyRegistered(p_id):
            self.patientAlreadyRegistered = True
            if not isRegistered:
                logging.debug("The patient is already registered.")
        else:
            self.patientAlreadyRegistered = False
            if isRegistered:
                isRegistered = False
                self.isRegistered = False
        if not isRegistered:
            if self.patientAlreadyRegistered:
                self.learnPerson(self.patientAlreadyRegistered, p_id)
            else:
                if self.num_people > 1:
                    for num_recog in range(0, self.num_mult_recognitions):
                        self.nonweighted_evidence = self.mult_recognitions_list[num_recog]
                        self.updateProbabilities(self.unknown_var, self.ie_list[num_recog])
                self.learnPerson(self.patientAlreadyRegistered, p_id)

            if self.num_people > 1:
                start_time = time.time()
                self.analysis_data_list = []
                for num_recog in range(0, self.num_mult_recognitions):
#                     self.saveAnalysisToDB(self.recog_results_list[num_recog], p_id, self.ie_list[num_recog])
                    self.saveAnalysisToJson(self.recog_results_list[num_recog], p_id, self.ie_list[num_recog], isPrevSavedToAnalysis, num_recog = num_recog)
                isPrevSavedToAnalysis = True
                print "save analysis to db time: " + str(time.time() - start_time)
            if self.isAddPersonToDB:
                self.addPersonToBN(self.personToAdd)
            if recog_results_from_file is None:
                p_start_time = time.time()
                pool = ThreadPool(self.num_mult_recognitions)
                joint_results = pool.map(self.threadedNoEstRecognisePerson, [i for i in range(0, self.num_mult_recognitions)])
                pool.close()
                pool.join()
                self.recog_results_list = [i[0] for i in joint_results]
                self.mult_recognitions_list = [i[1] for i in joint_results]
                self.ie_list = [i[2] for i in joint_results]
                print "time for parallel nonregistered recog:" + str(time.time() - p_start_time)

            else:
                self.mult_recognitions_list = []
                self.recog_results_list = []
                for num_recog in range(0, self.num_mult_recognitions):
                    self.recog_results = self.recognisePerson(num_recog = num_recog)
                    self.mult_recognitions_list.append(self.fillNonweightedEvidence(self.recog_results))
                    self.recog_results_list.append(self.recog_results)
        else:
            self.learnPerson(isRegistered, p_id)
        if self.num_people < 2:
            for num_recog in range(0, self.num_mult_recognitions):
                self.nonweighted_evidence = self.mult_recognitions_list[num_recog]
                self.saveCSV(self.csv_file, p_id)
        else:
            if not isRegistered and recog_results_from_file is not None:
                # get the inference from the final recognition
                self.ie_list = []
                for num_recog in range(0, self.num_mult_recognitions):
                    self.ie = self.setEvidence(self.recog_results_list[num_recog])
                    # TODO: check if I can update likelihoods using posteriors for I = p_id using setEvidence({"I":p_id})!!!
#                     print "before setting identity real posteriors"
#                     self.printInference(self.ie)

#                     self.ie.setEvidence({"I":p_id})
#                     self.ie.makeInference()

#                     print "after setting identity real posteriors"
#                     self.printInference(self.ie)
                    self.ie_list.append(self.ie)

            self.analysis_data_list = []
            for num_recog in range(0, self.num_mult_recognitions):
                self.nonweighted_evidence = self.mult_recognitions_list[num_recog]
                self.recog_results = self.recog_results_list[num_recog]
                self.ie = self.ie_list[num_recog]
                self.saveCSV(self.csv_file, p_id)
                self.saveBN(self.recog_file, p_id, self.ie, num_recog)
#                 self.saveAnalysisToDB(self.recog_results, p_id, self.ie)
                self.saveAnalysisToJson(self.recog_results, p_id, self.ie, isPrevSavedToAnalysis, num_recog = num_recog)
        return self.names[self.i_labels.index(p_id)]
#         return p_id

    def setPersonToAdd(self, personToAdd):
        self.isAddPersonToDB = True
        self.personToAdd = personToAdd
        self.printDB()

    def setPersonIdentity(self, isRegistered = True, p_id = None, recog_results_from_file = None):

    	    self.recog_results_from_file = recog_results_from_file
            if self.isMultipleRecognitions:
                return self.setPersonIdentityMult(isRegistered, p_id, recog_results_from_file)

            isPrevSavedToAnalysis = False
            if p_id is None:
                p_id = self.identity_est
            if self.isAlreadyRegistered(p_id):
                self.patientAlreadyRegistered = True
                if not isRegistered:
                    logging.debug("The patient is already registered line 1504.")
            else:
                self.patientAlreadyRegistered = False
                if isRegistered:
                    isRegistered = False
                    self.isRegistered = False

            if not isRegistered:
                if self.patientAlreadyRegistered:
                    self.learnPerson(self.patientAlreadyRegistered, p_id)
                else:
                    if self.num_people > 1:
                        self.updateProbabilities(self.unknown_var, self.ie)

                    self.learnPerson(self.patientAlreadyRegistered, p_id)

                if self.num_people > 1:
                    start_time = time.time()
                    self.saveAnalysisToDB(self.recog_results, p_id, self.ie)
    #                 self.saveAnalysisToJson(self.recog_results, p_id, self.ie, isPrevSavedToAnalysis)
                    isPrevSavedToAnalysis = True
                    print "save analysis to db time: " + str(time.time() - start_time)
                if self.isAddPersonToDB:
                    self.addPersonToBN(self.personToAdd)
                self.recog_results = self.recognisePerson()
                self.nonweighted_evidence = self.fillNonweightedEvidence(self.recog_results)
            else:
                 self.learnPerson(isRegistered, p_id)
            if self.num_people < 2:
                self.saveCSV(self.csv_file, p_id)
            else:
                if not isRegistered:
                    # get the inference from the final recognition
                    self.ie = self.setEvidence(self.recog_results)

                # TODO: check if I can update likelihoods using posteriors for I = p_id using setEvidence({"I":p_id})!!!
    #             print "before setting identity real posteriors"
    #             self.printInference(self.ie)

    #             self.ie.setEvidence({"I":p_id})
    #             self.ie.makeInference()

    #             print "after setting identity real posteriors"
    #             self.printInference(self.ie)
                self.saveCSV(self.csv_file, p_id)
                self.saveBN(self.recog_file, p_id, self.ie)
                start_time = time.time()
                self.saveAnalysisToDB(self.recog_results, p_id, self.ie)
    #             self.saveAnalysisToJson(self.recog_results, p_id, self.ie, isPrevSavedToAnalysis)
                print "save analysis to db time: " + str(time.time() - start_time)
            return self.names[self.i_labels.index(p_id)]
    #         return p_id

    def threadedNoEstRecognisePerson(self, num_recog):
        recog_results = self.recognisePerson(num_recog)
        mult_recognitions = self.fillNonweightedEvidence(recog_results)
        ie = None
        if self.num_people > 1:
            ie = self.setEvidence(recog_results)
        return [recog_results, mult_recognitions, ie]

    def threadedRecognisePerson(self, num_recog):
        recog_results = self.recognisePerson(num_recog)
        mult_recognitions = self.fillNonweightedEvidence(recog_results)
        ie = None
        if self.num_people > 1:
            ie = self.setEvidence(recog_results)
            i_post = np.array(ie.posterior(self.I)[:])
            identity_est = self.getEstimatedIdentity(i_post)
        else:
            identity_est = self.getEstimatedIdentity()
        return [recog_results, mult_recognitions, ie, identity_est]

    def recognise(self, isRegistered = True, recog_results_from_file = None):
        """isRegistered = False if register button is pressed"""
        print 'recognise enter'
        self.recog_results = []
        self.recog_results_from_file = recog_results_from_file
        if not self.isBNLoaded:
            self.loadBN(self.recog_file, self.csv_file, self.initial_recognition_file)

        if self.isMultipleRecognitions:
            print('is MultipleRecognition 1563')
            self.mult_recognitions_list = []
            self.recog_results_list = []
            self.ie_list = []
            if self.recog_results_from_file is None:
                # do parallel
                p_start_time = time.time()
                pool = ThreadPool(self.num_mult_recognitions)
                joint_results = pool.map(self.threadedRecognisePerson, [i for i in range(0, self.num_mult_recognitions)])
                pool.close()
                pool.join()
                self.recog_results_list = [i[0] for i in joint_results]
                self.mult_recognitions_list = [i[1] for i in joint_results]
                self.ie_list = [i[2] for i in joint_results]
                self.identity_est_list = [i[3] for i in joint_results]
                for num_recog in range(0, self.num_mult_recognitions):
                    self.saveEstimatedResultCSV(self.initial_recognition_file, self.recog_results_list[num_recog], self.identity_est_list[num_recog])

            else:
                #do sequential
                for num_recog in range(0, self.num_mult_recognitions):
                    self.recog_results = self.recognisePerson(num_recog)
                    self.mult_recognitions_list.append(self.fillNonweightedEvidence(self.recog_results))
                    self.recog_results_list.append(self.recog_results)
                    if self.num_people > 1:
                        self.ie = self.setEvidence(self.recog_results)
                        self.ie_list.append(self.ie)
                        i_post = np.array(self.ie.posterior(self.I)[:])
                        self.identity_est = self.getEstimatedIdentity(i_post)
                    else:
                        self.identity_est = self.getEstimatedIdentity()
                    self.saveEstimatedResultCSV(self.initial_recognition_file, self.recog_results, self.identity_est)

            if self.num_people > 1:
                for r in range(0, self.num_mult_recognitions):
                    if r== 0:
                        ie_avg = self.ie_list[r].posterior(self.I)[:]
                    else:
                        temp_p = self.ie_list[r].posterior(self.I)[:]
                        ie_avg = [x + y for x, y in zip(ie_avg, temp_p)]
                self.identity_prob_list = self.normalise(ie_avg)
                print "ie_avg:" + str(self.identity_prob_list)
                self.identity_est = self.getEstimatedIdentity(self.identity_prob_list)
            else:
                self.identity_est = self.getEstimatedIdentity()
                self.identity_prob_list = [1.0] # for unknown
        else:
            print('is not  MultipleRecognition 1674')
            self.recog_results = self.recognisePerson()
            print self.recog_results
            print('after recognized person 1677')
            self.nonweighted_evidence = self.fillNonweightedEvidence(self.recog_results)
            if self.num_people > 1:
                self.ie = self.setEvidence(self.recog_results)
                self.identity_prob_list = np.array(self.ie.posterior(self.I)[:])
                self.identity_est = self.getEstimatedIdentity(self.identity_prob_list)
            else:
                print(' 1626')
                self.identity_est = self.getEstimatedIdentity()
                self.identity_prob_list = [1.0] # for unknown
            self.saveEstimatedResultCSV(self.initial_recognition_file, self.recog_results, self.identity_est)
        return self.identity_est

#     def getEstimatedIdentity(self, recog_results, i_post = None):
    def getEstimatedIdentity(self, i_post = None):
        identity_est = ""
        self.isUnknownCondition = False
        if self.num_people > 1:
            i_max_cpt = np.max(i_post)
            identity_est = self.i_labels[np.argmax(i_post)]
            isclose_ar = np.isclose(i_post, i_max_cpt)
            if i_max_cpt < self.conf_min_identity or len(isclose_ar[isclose_ar==True]) > 1:
                print "unknown condition"
                self.isUnknownCondition = True
                # if all states are equally likely or if maximum confidence is lower than self.conf_min_identity then person is unknown
                identity_est = self.unknown_var
        else:
#             if recog_results[0][1]:
#                 if recog_results[0][1][0][1] > self.conf_min_identity:
#                     identity_est = recog_results[0][1][0][0]
            identity_est = self.unknown_var
#             if identity_est == "":
#                 identity_est = self.unknown_var
        identity_est = str(identity_est)
        return identity_est

    def initSession(self, isRegistered = True, isMemoryRobot = True, isAddPersonToDB = False, isDBinCSV = False, personToAdd = []):
        self.start_recog_time = time.time()
        self.isRegistered = isRegistered
        self.isMemoryRobot = isMemoryRobot
        self.isAddPersonToDB = isAddPersonToDB
        self.isDBinCSV = isDBinCSV
        self.personToAdd = personToAdd

        self.df_I = []
        self.loadSentencesForRecognition()
        self.isBNLoaded = False
        textToSay = self.lookAtTablet
        if isMemoryRobot and isRegistered:
            textToSay += self.pleasePhrase
        else:
            textToSay += self.enterName
        print '4.1'
        self.say(textToSay)
        #i = self.recog_service.get_image_path()
        #print i
        print '4.2'
        # print textToSay

    def initSessionNoPhrase(self, isRegistered = True, isMemoryRobot = True, isAddPersonToDB = False, isDBinCSV = False, personToAdd = []):
        self.start_recog_time = time.time()
        self.isRegistered = isRegistered
        self.isMemoryRobot = isMemoryRobot
        self.isAddPersonToDB = isAddPersonToDB
        self.isDBinCSV = isDBinCSV
        self.personToAdd = personToAdd
        self.df_I = []

    def startRecognition(self, recog_results_from_file = None):
        """call initSession and take picture before calling this function"""
        print 'startRecognition enter'
        identity_est = self.recognise(isRegistered = self.isRegistered, recog_results_from_file = recog_results_from_file)
        print 'xxidentity estx'
        print identity_est
        if self.isMemoryRobot and self.isRegistered:
            if identity_est == self.unknown_var:
                textToSay = self.unknownPerson
            else:
                identity_say = self.names[self.i_labels.index(identity_est)].split()
#                 identity_say = identity_est.split("_") #TODO: change split character if necessary
                textToSay = self.askForIdentityConfirmal.replace("XX", str(identity_say[0]))
            print 'textToSay: ' + textToSay
            self.say(textToSay)
        # print textToSay
        self.identity_est = identity_est
        return identity_est

    def setNumOccurrences(self, csv_file):
        self.num_occurrences = [0 for i in range(0, len(self.i_labels))]
        df_names_registering = pandas.read_csv(csv_file, usecols=["I", "R"], dtype={"I": object})
        occurrences = df_names_registering.I.value_counts()
        num_unknown_occurrences = df_names_registering.R.values.sum()
        for val, cnt in occurrences.iteritems():
            print 'wwwwwwwwwwwwwwwwwwwwwwwww'
            print(self.i_labels)
            print val
            print 'wwwwwwwwwwwwwwwwwwwwwwwww'
            index_name = self.i_labels.index(val)
            self.num_occurrences[index_name] = cnt
        self.num_occurrences[self.i_labels.index(self.unknown_var)] = num_unknown_occurrences

    def isAlreadyRegistered(self, p_id):
        if not self.df_I:
            self.df_I = set(pandas.read_csv(self.csv_file, usecols=["I"], dtype={"I": object}).I.tolist())
        return p_id in self.df_I

    def confirmPersonIdentity(self, p_id = None, recog_results_from_file = None):
        """call startRecognition before calling this function, and then ask for name from the person"""

        # TODO: add more phrases for the welcome, and I am sorry phrases
        name = self.setPersonIdentity(isRegistered = self.isRegistered, p_id = p_id, recog_results_from_file = recog_results_from_file)
        if self.isMemoryRobot:
            identity_say = name.split() #TODO: change split character if necessary
            if p_id is not None:
                if self.isRegistered:
                    falseRecognitionSentence = random.choice(self.falseRecognition)
                    textToSay = falseRecognitionSentence.replace("XX", str(identity_say[0]))
                else:
                    if self.patientAlreadyRegistered:
                        textToSay = self.falseRegistration.replace("XX", str(identity_say[0]))
                    else:
                        textToSay = self.registrationPhrase.replace("XX", str(identity_say[0]))
            else:
                correctRecognition = random.choice(self.correctRecognition)
                textToSay = correctRecognition.replace("XX", str(identity_say[0]))

            self.say(textToSay)
            # print textToSay
        calc_time = time.time() - self.start_recog_time
        if p_id is None:
            identity_real = self.identity_est
        else:
            identity_real = p_id
        self.saveComparisonCSV(self.comparison_file, identity_real, self.identity_est, self.identity_prob_list, calc_time)

    def loadSentencesForRecognition(self):
        # TODO: Change enter name to choose name (in Spanish as well)
        if self.useSpanish:
            self.lookAtTablet = "Hola, podrias mirar la pantalla "
            self.pleasePhrase = "por favor?"
            self.enterName = "e ingresar tu nombre por favor?"
            self.unknownPerson = "Oh lo siento mucho, No pude reconocer quien eres! Podrias ingresar tu nombre en la pantalla por favor?"
            self.askForIdentityConfirmal = "Hola XX, es bueno verte de nuevo ! Podrias confirmar que eres tu?"
            self.falseRecognition = ["Ah, por supuesto, me disculpo! Parece que mis ojos me estan fallando... Bienvenido de nuevo XX!", "Te ves diferente hoy, es un nuevo corte?"]
            self.registrationPhrase = "Hola XX, encantado de conocerte"
            self.falseRegistration = "Ya te había visto antes! Es un gusto verte de nuevo XX!"
            self.correctRecognition = ["Sabia que eras tu, solo queria estar seguro", "Te ves bien hoy XX!"]
        else:
            self.lookAtTablet = "Hello there, could you look at the tablet "
            self.pleasePhrase = "please?"
            self.enterName = "and enter your id please?"
            self.unknownPerson = "Oh I'm sorry, I couldn't recognise who you are! Could you enter your id on the tablet please?"
            self.askForIdentityConfirmal = "Hello XX, it is nice to see you again! Could you confirm that it is you please?"
            self.falseRecognition = ["Ah, of course, my apologies! My eyes seem to fail me.. Welcome back XX!", "You look different today XX, is it a new haircut?"]
            self.registrationPhrase = "Hello XX, nice to meet you!"
            self.falseRegistration = "But we have met before! Nice to see you again XX!"
            self.correctRecognition = ["I knew it was you, just wanted to be sure!", "You look very good today XX!"]

    def say(self, sentence):
        self.tts.setVolume(0.85)
        self.tts.setParameter("speed", 80)
#        threading.Thread(target = self.animatedSpeechProxy.say, args=(sentence,self.configuration)).start()
        self.tts.say(sentence)

    def resetFiles(self):
        if os.path.isfile(self.recog_file):
            os.remove(self.recog_file)
        if os.path.isfile(self.csv_file):
            os.remove(self.csv_file)
        with open(self.csv_file, 'wb') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["I", "F", "G", "A", "H", "T", "R"])
        if os.path.isfile(self.initial_recognition_file):
            os.remove(self.initial_recognition_file)
        with open(self.initial_recognition_file, 'wb') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["I_est", "F", "G", "A", "H", "T"])
#         if os.path.isfile(self.db_file):
#             os.remove(self.db_file)
#         with open(self.db_file, 'wb') as outcsv:
#             writer = csv.writer(outcsv)
#             writer.writerow(["id", "name", "gender", "age", "height", "times"])
        analysis_dir = self.analysis_file.replace("/Analysis.json","")
        if os.path.isdir(analysis_dir):
            shutil.rmtree(analysis_dir)
        os.makedirs(analysis_dir)
        with open(self.comparison_file, 'wb') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(["I_real", "I_est", "I_prob", "Calc_time", "R"])

    """Print functions:"""
    def printPriors(self):
        print "priors:"
        print "I:"
        print self.r_bn.cpt(self.I)[:]
        print "F:"
        print self.r_bn.cpt(self.F)[:]
        print "G:"
        print self.r_bn.cpt(self.G)[:]
        print "A:"
        for counter in range(0,len(self.i_labels)):
            plt.plot(range(self.age_min, self.age_max + 1),self.r_bn.cpt(self.A)[{'I':self.i_labels[counter]}], label=self.i_labels[counter])
        plt.show()
        print "H:"
        for counter in range(0,len(self.i_labels)):
            plt.plot(range(self.height_min, self.height_max + 1),self.r_bn.cpt(self.H)[{'I':self.i_labels[counter]}], label=self.i_labels[counter])
        plt.show()
        print "T:"
        for counter in range(0,len(self.i_labels)):
            plt.plot(range(self.time_min, self.time_max + 1),self.r_bn.cpt(self.T)[{'I':self.i_labels[counter]}], label=self.i_labels[counter])
        plt.show()

    def printEvidence(self, face_result, gender_result, age_result, height_result, time_result):
        print "face weighted evidence"
        print face_result

        print "gender weighted evidence"
        print gender_result

        print "age weighted evidence"
        plt.plot(range(self.age_min, self.age_max+1),age_result)
        plt.show()

        print "height weighted evidence"
        plt.plot(range(self.height_min, self.height_max+1),height_result)
        plt.show()

        print "time weighted evidence"
        plt.plot(range(self.time_min, self.time_max+1),time_result)
        plt.show()

    def printInference(self, ie):
        print "ie.posterior(self.I):"
        print ie.posterior(self.I)
        print "ie.posterior(self.F):"
        print ie.posterior(self.F)
        print "ie.posterior(self.G):"
        print ie.posterior(self.G)
        print "ie.posterior(self.A):"
        plt.plot(range(self.age_min, self.age_max+1),ie.posterior(self.A)[:])
        plt.show()
        print "ie.posterior(self.H):"
        plt.plot(range(self.height_min, self.height_max+1),ie.posterior(self.H)[:])
        plt.show()
        print "ie.posterior(self.T):"
        plt.plot(range(self.time_min, self.time_max+1),ie.posterior(self.T)[:])
        plt.show()

    def printDB(self):
        print "database:"
        print "self.i_labels: " + str(self.i_labels)
        print "self.genders: "  + str(self.genders)
        print "self.ages: " + str(self.ages)
        print "self.heights: " + str(self.heights)
        print "self.times: " + str(self.times)
        print "self.num_people: " + str(self.num_people)

    """Math functions:"""
    def uniformDistribution(self, min_value, max_value):
        uni_value = 1.0/(max_value - min_value + 1)
        return [uni_value for x in range(min_value, max_value + 1)]

    def getCurve(self, conf = 1.0, mean = 0.0, stddev = 0.0, min_value = 0, max_value = 0, weight = 1.0):
        curve = []
        if conf > self.max_threshold:
            conf = self.max_threshold # decrease the prob. to get a Gaussian distribution

        if np.isclose(stddev, 0.0) and conf >= self.conf_threshold:
            # applicable to age only
            stddev = 0.5/self.normppf(conf + (1-conf)/2.0)

        if conf < self.conf_threshold:
            # uniform distribution
            curve = self.uniformDistribution(min_value, max_value)
        else:
            # Gaussian distribution
#             norm_curve = norm(loc=observed_height,scale=self.stddev_height )
            for j in range(min_value, max_value +1):
#                 j_pdf = norm_curve.pdf(j)
                j_pdf = self.normpdf(j, mean, stddev)
                if j_pdf < self.prob_threshold:
                    j_pdf = self.prob_threshold
                curve.append(math.pow(j_pdf, weight))
#                 curve.append(j_pdf)
            curve = self.normalise(curve)
        return curve

    def normalise(self, array):
        sum_array = sum(array)
        return [float(i) / sum_array for i in array]

    def softmax(self, array):
        array_exp = [math.exp(i) for i in array]
        sum_array_exp = sum(array_exp)
        return [i / sum_array_exp for i in array_exp]

    def normpdf(self, x, loc=0, scale=1):
        """x is the value that pdf wants to be read at, loc is the mean, and scale is the stddev
        From: https://stackoverflow.com/questions/8669235/alternative-for-scipy-stats-norm-pdf"""
        #print "normpdf line 1931 : x: "+ str(x) + " loc: " + str(loc)
        u = float(x-loc) / abs(scale)
        y = np.exp(-u*u/2) / (np.sqrt(2*np.pi) * abs(scale))
        return y

    def normppf(self, y0):
        """From https://stackoverflow.com/questions/41338539/how-to-calculate-a-normal-distribution-percent-point-function-in-python"""

        s2pi = 2.50662827463100050242E0

        P0 = [
            -5.99633501014107895267E1,
            9.80010754185999661536E1,
            -5.66762857469070293439E1,
            1.39312609387279679503E1,
            -1.23916583867381258016E0,
        ]

        Q0 = [
            1,
            1.95448858338141759834E0,
            4.67627912898881538453E0,
            8.63602421390890590575E1,
            -2.25462687854119370527E2,
            2.00260212380060660359E2,
            -8.20372256168333339912E1,
            1.59056225126211695515E1,
            -1.18331621121330003142E0,
        ]

        P1 = [
            4.05544892305962419923E0,
            3.15251094599893866154E1,
            5.71628192246421288162E1,
            4.40805073893200834700E1,
            1.46849561928858024014E1,
            2.18663306850790267539E0,
            -1.40256079171354495875E-1,
            -3.50424626827848203418E-2,
            -8.57456785154685413611E-4,
        ]

        Q1 = [
            1,
            1.57799883256466749731E1,
            4.53907635128879210584E1,
            4.13172038254672030440E1,
            1.50425385692907503408E1,
            2.50464946208309415979E0,
            -1.42182922854787788574E-1,
            -3.80806407691578277194E-2,
            -9.33259480895457427372E-4,
        ]

        P2 = [
            3.23774891776946035970E0,
            6.91522889068984211695E0,
            3.93881025292474443415E0,
            1.33303460815807542389E0,
            2.01485389549179081538E-1,
            1.23716634817820021358E-2,
            3.01581553508235416007E-4,
            2.65806974686737550832E-6,
            6.23974539184983293730E-9,
        ]

        Q2 = [
            1,
            6.02427039364742014255E0,
            3.67983563856160859403E0,
            1.37702099489081330271E0,
            2.16236993594496635890E-1,
            1.34204006088543189037E-2,
            3.28014464682127739104E-4,
            2.89247864745380683936E-6,
            6.79019408009981274425E-9,
        ]
        if y0 <= 0 or y0 >= 1:
            raise ValueError("ndtri(x) needs 0 < x < 1")
        negate = True
        y = y0
        if y > 1.0 - 0.13533528323661269189:
            y = 1.0 - y
            negate = False

        if y > 0.13533528323661269189:
            y = y - 0.5
            y2 = y * y
            x = y + y * (y2 * self.polevl(y2, P0) / self.polevl(y2, Q0))
            x = x * s2pi
            return x

        x = math.sqrt(-2.0 * math.log(y))
        x0 = x - math.log(x) / x

        z = 1.0 / x
        if x < 8.0:
            x1 = z * self.polevl(z, P1) / self.polevl(z, Q1)
        else:
            x1 = z * self.polevl(z, P2) / self.polevl(z, Q2)
        x = x0 - x1
        if negate:
            x = -x

        return x

    def polevl(self, x, coef):
        accum = 0
        for c in coef:
            accum = x * accum + c
        return accum


    def shutdown(self):
        if self.session:
            self.session.close()
if __name__ == "__main__":

    RB = RecogniserBN()
