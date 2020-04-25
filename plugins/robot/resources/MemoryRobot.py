# coding: utf-8
"""in the no-robot condition don't run this script"""
import threading
import time
import datetime
import qi
import functools
import sys
import os.path

#sys.path.append(
#     os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
#import db.database as db

# sys.path.insert(0, '../db')
# import database as db
import dialogs
import bisect
import random # for making random choices for choosing the number of sentences between saying patient name in isSayName
random.seed(123456789)

class MemoryRobot(object):

    def __init__(self,
                 session        = None,
                 p_name         = None,
                 useSpanish     = True,
                 ProjectHandler = None,
                 DataHandler    = None,
                 dialogs        = None,
                 settings       = None,
                 controller     = None):

        #set settings
        self.settings = settings
        #controller
        self.controller = controller
        #loaf ProjectHandler
        self.PH = ProjectHandler
        #load datanhandler
        self.DB = DataHandler
        #load dialog manager
        self.dialogs = dialogs
        #micro value
        self.micro = 1000000
        #load custom memory sentences
        #TODO: migrate custom sentences to the dialog manager
        self.loadSentencesForMemoryFeedback(useSpanish)
        #number of sessions of the user
        self.p_num_sessions = 0
        #set person profile
        self.setPerson(self.settings['UserProfile'])
        #say name of the user n times
        self.num_say_name = 0
        
        #counter to say name of the user
        self.say_name_counter = 0

    def set_session(self, s):
        #load session from robot model
        self.session = s
        #get services
        self.get_services()

    #set language method
    def setLanguage(self, value):
        self.tts.setLanguage(value)


    def get_services(self):
        #text to speech module service
        self.tts = self.session.service("ALTextToSpeech")
        #set language
        self.setLanguage('Spanish')
        #animated text to speech service
        self.animatedSpeech = self.session.service("ALAnimatedSpeech")
        #motion service
        self.motion = self.session.service("ALMotion")
        #posture service
        self.posture = self.session.service("ALRobotPosture")
        #behavior manager
        self.behavior = self.session.service("ALBehaviorManager")
        #Memory for touch sensing
        self.memory = self.session.service("ALMemory")
        self.memory.subscribeToEvent("MiddleTactilTouched","ReactToTouch", "onTouched")
        
        #tracker
        self.tracker = self.session.service("ALTracker")
        targetName = "Face"
        faceWidth = 0.1
        self.tracker.registerTarget(targetName, faceWidth)
        self.tracker.track(targetName)
        #names = self.behavior.getInstalledBehaviors()
        #print(names)
    
    def onTouched(self):

        self.tts.say(self.dialogs.sentenceFine)

    def set_routines(self):
        print("settings memory routines")

        motivate = functools.partial(self.motivation)
        self.motivationTask = qi.PeriodicTask()
        self.motivationTask.setCallback(motivate)
        self.motivationTask.setUsPeriod(self.settings['MotivationTime']*self.micro)

        borg = functools.partial(self.ask_borg)
        self.borgTask = qi.PeriodicTask()
        self.borgTask.setCallback(borg)
        self.borgTask.setUsPeriod(self.settings['BorgTime'] * self.micro)


    #start routine method
    def start_routines(self):
        self.motivationTask.start(True)
        self.borgTask.start(True)

    #setop created async routines
    def stop_routines(self):
        self.motivationTask.stop()
        self.borgTask.stop()

    #callback
    def motivation(self):
        print("motivation memory")
        if self.DB:
            self.DB.General.SM.load_event(t ="Motivation", c = "Timeout", v ="None")

        if self.isSayName():
            s = self.dialogs.get_motivation_memory_sentence(s)
            s = s.replace('XX', self.p_first_name)
        else:
            s = self.dialogs.get_motivation_sentence()
        
        self.animatedSpeech.say(s)

    #callback
    def ask_borg(self):
        print("ask borg scale memory")
        if self.controller:
            print('set onBorgRequest event from memory robot')
            self.controller.onBorgRequest.set()
            print self.controller.onBorgRequest.is_set()
        if self.isSayName():
            s = self.dialogs.get_borg_memory_sentence()
            s = s.replace('XX', self.p_first_name)
        else:
            s = self.dialogs.get_borg_sentence()
        self.animatedSpeech.say(s)

    def run_welcome_behavior(self):
        print('run_welcome_behavior_num_sessions')
        print(self.p_num_sessions)
        if self.p_num_sessions == 1:
            s = self.dialogs.WelcomeSentenceMemory
            s = s.replace("XX", self.settings['UserProfile']['name'])
            self.animatedSpeech.say(s)
        
        self.sentence_counter = 1

        announce = self.dialogs.sentenceAnnounce.replace("XX",str(5))
        announce = announce.replace("YY", str(1))
        text_to_say = self.checkAbsence() + self.checkPreviousSessionAlerts(announce,5,1)
        print "TEXT TO SAY...."
        print text_to_say
        self.animatedSpeech.say(text_to_say)

        #start routines
        self.start_routines()

    def posture_correction_behavior(self):
        if self.isSayName():
            s = self.dialogs.get_posture_correction_memory_sentence()
            s = s.replace('XX', self.p_first_name)
        else:
            s = self.dialogs.get_posture_correction_sentence()
        self.animatedSpeech.say(s)

    #TODO: cooldown method



    def say(self, sentence):
        self.tts.setVolume(0.85)
        self.tts.setParameter("speed", 80)
        threading.Thread(target = self.animatedSpeechProxy.say, args=(sentence,self.configuration)).start()

    def loadInfo(self):
        print'###############################'
        print 'loadInfo'
        #self.db_handler = db.DbHandler()
        #p = self.db_handler.get_person_data({"name":self.p_name})
        self.p = self.person
        self.p_gender = str(self.p["gender"])
        self.p_age = int(self.p["age"])
        self.p_height = float(self.p["height"])
        self.p_times = [] # includes the current session
        times = self.DB.General.SM.load_user_times(p = self.PH.paths['current_user'])
        #print'times'
        #print times
        p_datelist = []
        for tt in times:
            # make sure only one session is added per day
            #TODO: uncomment the line below, and comment the rest if there is more than one session per day
            # self.p_times.append([tt.time().strftime('%H:%M:%S'), tt.isoweekday()])
            date_sess = tt.strftime('%Y-%m-%d')
            if date_sess not in p_datelist:
                self.p_times.append([tt.time().strftime('%H:%M:%S'), tt.isoweekday()])
                p_datelist.append(date_sess)

        print 'loadInfo'
        print "##############################"

    def loadSessionData(self):
        #print('#####################################################################################')
        #print "loadSessionData start"
        #print('#####################################################################################')
        s = self.DB.General.SM.get_all_sessions()
        s.sort(key = lambda x: datetime.datetime.strptime(x["date"], '%Y-%m-%d')) #order sessions by date
        '''
        s {"dates:[], "events":[], "sensors":[], "averages":[]}
        '''
        #
        counter = 0
        self.p_dates = [] # includes the current session
        self.p_events = []
        self.p_averages = []
        #
        #print "**********************************************************************"
        #print s
        #print "**********************************************************************"
        
        for ss in s:
            self.p_dates.append(datetime.datetime.strptime(ss["date"], '%Y-%m-%d'))
            s_events = []
            e = ss["events"]
            #s_avg = []
            avrg = {"Speed": 0, "Inclination": 0,"Hr": 0}
            for e_s in e:
                s_events.append(e_s)
                
                if e_s["Type"] == "average":
                    
                    if e_s["Cause"] == 'speed':
                        avrg["Speed"] = e_s['Value']
                    elif e_s["Cause"] == 'hr':
                        avrg["Hr"] = e_s['Value']
                    elif 'incl' in e_s["Cause"]:
                        avrg["Inclination"] = e_s['Value']

            self.p_events.append(s_events)
            



            #a = ss["average"]
            #print "################ ss[average] ##################"
            #print a
            #print "################ ss[average] ##################"
            #for a_s in a:
            #    s_avg.append(a_s)
            self.p_averages.append(avrg)

            counter = counter + 1 


        #print 'date'
        #print(self.p_dates)
        #print 'events'
        #print(self.p_events)
        #print 'averages'
        #print(self.p_averages)


        print "################"
        print "number of sessions " + str(counter)
        print "################"
        self.p_num_sessions = counter
        #print('#####################################################################################')
         #print "loadSessionData finish"
         #print('#####################################################################################')
       
    def setPerson(self, p):
        self.person = p
        self.p_name = str(self.settings['UserProfile']['name'])
        identity_say = self.p_name.split()
        self.p_first_name = str(identity_say[0])
        self.loadInfo()
        self.loadSessionData()

#     def getExpectedSession(self, sorted_times, session_date, cur_session, session_day = None, session_index = None):
#         print('---------session day------------------')
#         print session_day
#         print('---------session day------------------')
#         print('---------session index------------------')
#         print session_index
#         print('---------session index------------------')
#         if session_day is None:
#             session_day = session_date.isoweekday()
#         if session_index is None:
#             session_index = sorted_times.index(session_day)
#         if session_index < len(sorted_times) - 1:
#             day_dif = sorted_times[session_index + 1] - session_day
#         else:
#             day_dif = 7 - session_day + sorted_times[0]
#             self.past_holiday.append(self.weekend_word)
#         for x in range(1, day_dif+1):
#             try_date = session_date + datetime.timedelta(days=x)
#             if try_date < cur_session and try_date in self.holidays:
#                 self.past_holiday.append(self.bank_holiday_word)
#         expected_session = session_date + datetime.timedelta(days=day_dif)
#         return expected_session

    def getNumMissedSessions(self, cur_session, last_session, num_session_of_week):
        num_missed_sessions = 0
        if num_session_of_week == 1:
            cur_session_week_num = cur_session.isocalendar()[1]
            last_session_week_num = last_session.isocalendar()[1]
            num_missed_sessions = (cur_session_week_num - last_session_week_num - 1)*2 # TODO: UPDATE HERE IF IT ISN'T 2 SESSIONS PER WEEK
            if cur_session.isoweekday() >= 5 : # if today is friday, then it is the last session of the week, so the patient missed one session. TODO: UPDATE HERE IF THERE IS A SESSION ON SATURDAY OR SUNDAY
                num_missed_sessions += 1
            
        return num_missed_sessions
    
    def getHolidays(self, cur_session, last_session, num_session_of_week):
        past_holiday = []
        for holiday in self.holidays:
            if last_session < holiday < cur_session:
                past_holiday.append(self.bank_holiday_word)
        if num_session_of_week == 1 and cur_session.isoweekday() < 4: # comment on the weekend for monday, tuesday, wednesday (otherwise it would look odd)
            past_holiday.append(self.weekend_word)
        return past_holiday

    def isPatientOnSchedule(self):
        """check if patient is on schedule (came to the previous session)"""
        print('-------------------------isPatientOnSchedule-----------------')
        print('-------------------------P.NUMSESSIONS-----------------')
        print self.p_num_sessions
        print('-------------------------P.Times-----------------')
        print self.p_times

        on_schedule = True

        cur_session = datetime.datetime.now().date()
        cur_session_week_num = cur_session.isocalendar()[1]
        self.num_session_of_week = 1
        counter = 1
        if len(self.p_dates) > 1:
            ch_session = cur_session
            counter = counter + 1
            while counter <= len(self.p_dates):
                prev_session = ch_session
                ch_session = self.p_dates[-1*counter].date()
                if cur_session_week_num == ch_session.isocalendar()[1]: # it is the same week
    #                     if ch_session != prev_session: #this assumes that the session will not be on the same day (but the assumption is removed now)
                    self.num_session_of_week = self.num_session_of_week + 1
                else:
                    break
                counter = counter + 1

        # look at the last session date, look at the current date, compare the current date to the
        # date that the session should have happened, compare the date that should have happened to holiday
        # and find if the patient skipped a day that wasnt a holiday
        if self.p_times > 1 and self.p_num_sessions > 1:
            print('-------------------------isPatientOnSchedule-----------------')
            last_session = self.p_dates[-2].date()
            
            # TODO: NEED TO CHANGE THIS PART SO SAME DAY SESSIONS CAN BE PROCESSED!   
            # sorted_times = sorted(list(set([row[1] for row in self.p_times]))) # get a unique list of sorted days of week for sessions            
            
            self.num_missed_sessions = self.getNumMissedSessions(cur_session, last_session, self.num_session_of_week)
            if self.num_missed_sessions > 0:
                on_schedule = False
            self.past_holiday = self.getHolidays(cur_session, last_session, self.num_session_of_week)
            
            
#             if last_session_day in sorted_times:
#                 print('checkAbsence compare first if')
#                 last_session_index = sorted_times.index(last_session_day)
#                 expected_session = self.getExpectedSession(sorted_times, last_session, cur_session, last_session_day, last_session_index)
#             else:
#                 print('checkAbsence compare second if')
#                 last_session_index = bisect.bisect(sorted_times, last_session_day)
#                 expected_session = self.getExpectedSession(sorted_times, last_session, cur_session, last_session_day, last_session_index-1)
#             if cur_session > expected_session:
#                 self.missed_sessions.append(expected_session)
#                 missed = cur_session - expected_session
#                 while missed.days > 0:
#                     expected_session = self.getExpectedSession(sorted_times, expected_session, cur_session)
#                     print expected_session
#                     if cur_session > expected_session:
#                         if expected_session not in self.holidays:
#                             self.missed_sessions.append(expected_session)
#                             missed = cur_session - expected_session
#                     else:
#                         break
#             
#                 on_schedule = False
#             elif cur_session < expected_session:
#                 self.came_early = True

#             self.lastSessionOfWeek = False
#             if self.num_session_of_week == len(sorted_times) and cur_session.isoweekday() == sorted_times[self.num_session_of_week-1]:
#                 self.lastSessionOfWeek = True
#             print self.num_session_of_week
#             print on_schedule

        return on_schedule

    def checkAbsence(self):
        text_to_say = ""
        print('-------------------------------------------CHECK Absence number sesio----------------------')
        print(self.p_num_sessions)
        print('-------------------------------------------CHECK Absence number sesio----------------------')
        if self.p_num_sessions == 1:
            print "this is the first session"
            return text_to_say
        self.past_holiday = []
        self.came_early = False
        self.on_schedule = self.isPatientOnSchedule()
        if not self.on_schedule:
            if self.num_missed_sessions == 1:
#                 day_missed = self.week_days[self.missed_sessions[0].isoweekday() - 1]
#                 text_to_say = self.missing_one_session.replace("XX", str(day_missed))
                text_to_say = self.missing_one_session
            else:
                text_to_say = self.missing_multiple_sessions.replace("XX", str(self.num_missed_sessions))
        elif len(self.past_holiday) > 0:

            if len(self.past_holiday) == 1:
                text_to_say = self.holiday_sentence.replace("XX", self.past_holiday[0])
            else:
                text_to_say = self.holiday_sentence.replace("XX", self.holiday_word)
        else:
            ordinal_day=self.ordinal_num[self.num_session_of_week-1]
            text_to_say = self.session_num_sentence.replace("XX", ordinal_day)
        print text_to_say
        # self.say(text_to_say)
        return text_to_say

    def checkPreviousSessionAlerts(self, announce, targetSpeed, targetSlope):
        text_to_say = ""
        if self.p_num_sessions == 1:
            text_to_say = announce
            return text_to_say
        last_session_events = self.p_events[-1]
        print last_session_events
        # vals = [0,0,0] # [heart_rate_counter, blood_pressure_counter, borg_scale_counter]
        vals = [0,0,0] # [heart_rate_counter, request_look, borg_scale_counter]

        for s in last_session_events:

            if s["Type"] == "Alert1":
                vals[0] += 1

            if s["Type"] == "Alert2":
                vals[0] += 1

            if s["Type"] == "RequestLook":
                vals[1] += 1

            if s["Type"] == "alarm_fatigue":
                vals[2] += 1


            # if s["Type"] == "HighBorg":
            #     vals[2] += 1

            # if s["Type"] == "Emergency":
            #     vals[1] += 1


        if sum(vals) == 0:
            prev_session_announcement = self.good_previous_session_announcement
            end_announcement = self.good_previous_session_motivation
        else:
            max_val = vals.index(max(vals))
            if max_val == 0:
                max_bad_value = self.heart_rate_word
            elif max_val == 1:
                # max_bad_value = self.blood_pressure_word
                max_bad_value = self.posture_word
            else:
                max_bad_value = self.tiredness_word

            if sum(vals) == 1:
                prev_session_announcement = self.bad_previous_session_announcement.replace("XX", max_bad_value)
            else:
                prev_session_announcement = self.bad_previous_session_announcement_multi.replace("XX", max_bad_value)

            end_announcement = self.bad_previous_session_motivation
        print "######################P_averages ################################"
        print self.p_averages
        print "######################LP_averages ################################"
        last_session_avgs = self.p_averages[-1]
        session_announcement = announce
        print "######################LAST SESSION AVGS ################################"
        print last_session_avgs
        print "######################LAST SESSION AVGS ################################"
        # TODO: update it to use the avg session values (last value might be the slow down speed and inclination!!!)
        if targetSpeed == float(last_session_avgs["Speed"]) and targetSlope == float(last_session_avgs["Inclination"]):
            session_announcement += self.session_intensity_same
            self.session_intensity = 0
        elif targetSpeed > float(last_session_avgs["Speed"]) or targetSlope > float(last_session_avgs["Inclination"]):
            session_announcement += self.session_intensity_more
            self.session_intensity = 1
        else:
            session_announcement += self.session_intensity_less
            self.session_intensity = -1

        text_to_say = session_announcement + prev_session_announcement + end_announcement
        print text_to_say
        # self.say(text_to_say)
        return text_to_say

    def checkProgress(self, numAlerts):
        """check progress of the current session compared to the previous one(s) and announce it at the end of the session"""
        
        text_to_say = ""
        if self.p_num_sessions == 1:
            # The robot should not comment on the current session, because there is no previous session! The announce is handled in robotModel.
            return text_to_say

        self.p_events_counts =[]
        for s_events in self.p_events:
            alerts_c = 0
            request_look_c = 0
            # request_distance_c = 0
            alarm_fatigue_c = 0
            for s_e in s_events:
                if "Alert" in s_e["Type"]:
                    alerts_c += 1
                elif s_e["Type"] == "RequestLook":
                    request_look_c += 1
                elif s_e["Type"] == "alarm_fatigue":
                    alarm_fatigue_c += 1
            self.p_events_counts.append([alerts_c, request_look_c, alarm_fatigue_c])

        self.extra_comment = self.session_intensity_comment
        print('...............................checkProgressAlerts.................')
        print(numAlerts)
        print(self.p_events_counts[-1][0])
        print('...............................checkProgressAlerts.................')
        if numAlerts == 0:
            progress_feedback = self.no_alert_feedback
        elif numAlerts == self.p_events_counts[-1][0]:
            progress_feedback = self.equal_alerts_as_previous
        elif numAlerts < self.p_events_counts[-1][0]:
            progress_feedback = self.less_alerts_than_previous
        elif numAlerts > self.p_events_counts[-1][0]:
            progress_feedback = self.more_alerts_than_previous
            self.extra_comment = self.session_intensity_comment_bad
        if self.session_intensity == 1:
            # session intensity higher
            progress_feedback = progress_feedback.replace(" XX", " " + self.extra_comment)
        else:
            progress_feedback = progress_feedback.replace(" XX", "")
        progress_feedback = progress_feedback.replace("YY", self.p_first_name)
        text_to_say = progress_feedback
        print text_to_say
        # self.say(text_to_say)
        return text_to_say

        # TODO: check progress in the overall therapy
        # at every 3-4 sessions, do an overall review.
        # e.g. we are doing good, we had less than XX alerts in average per session in the past YY sessions, and the heart rate is decreasing (ask Monica!)

        # TODO: check avg heart beat/blood pressure/borg scale
        # TODO: ask Monica how they monitor the patient, is it good for the heart beat to decrease, etc.

    def isSayName(self):
        """if true the robot with memory will say the name of the person (in addition to the sentence being said)"""
        if self.num_say_name == 0 or self.sentence_counter == self.num_say_name:
            self.num_say_name = random.randint(2,4)
            self.sentence_counter = 0
            return True
        self.sentence_counter += 1
        return False

    def addNameToSentence(self, sentenceToSay):
        addChar = sentenceToSay[-1]
        sentenceToSay = sentenceToSay.rstrip('!?.')
        sentenceToSay += ", \\pau=200\\ " + self.p_first_name
        if addChar == "!" or addChar == "?" or addChar == ".":
            sentenceToSay += addChar
        return sentenceToSay

    def loadSentencesForMemoryFeedback(self, useSpanish):
        if useSpanish:
            # in Colombia 2017
#             self.holidays = [datetime.date(2017, 1, 1), datetime.date(2017, 1, 9),
#                              datetime.date(2017, 3, 20), datetime.date(2017, 4, 13),
#                              datetime.date(2017, 4, 14), datetime.date(2017, 5, 1),
#                              datetime.date(2017, 5, 29), datetime.date(2017, 6, 19),
#                              datetime.date(2017, 6, 26), datetime.date(2017, 7, 3),
#                              datetime.date(2017, 7, 20), datetime.date(2017, 8, 7),
#                              datetime.date(2017, 8, 15), datetime.date(2017, 10, 16),
#                              datetime.date(2017, 11, 6), datetime.date(2017, 11, 13),
#                              datetime.date(2017, 11, 13), datetime.date(2017, 12, 8),
#                              datetime.date(2017, 12, 25)]

            self.holidays = [datetime.date(2019, 1, 1), datetime.date(2019, 1, 7),
                             datetime.date(2019, 3, 25), datetime.date(2019, 4, 18),
                             datetime.date(2019, 4, 19), datetime.date(2019, 5, 1),
                             datetime.date(2019, 6, 3), datetime.date(2019, 6, 24),
                             datetime.date(2019, 7, 1), datetime.date(2019, 8, 7),
                             datetime.date(2019, 8, 19), datetime.date(2019, 10, 14),
                             datetime.date(2019, 11, 4), datetime.date(2019, 11, 11),
                             datetime.date(2019, 12, 8), datetime.date(2019, 12, 25),
                             datetime.date(2020, 1, 1), datetime.date(2020, 1, 6),
                             datetime.date(2020, 3, 23), datetime.date(2020, 4, 9),
                             datetime.date(2020, 4, 10), datetime.date(2020, 5, 1),
                             datetime.date(2020, 5, 25), datetime.date(2020, 6, 15),
                             datetime.date(2020, 6, 22), datetime.date(2020, 6, 29),
                             datetime.date(2020, 7, 20), datetime.date(2020, 8, 7),
                             datetime.date(2020, 8, 17), datetime.date(2020, 10, 12),
                             datetime.date(2020, 11, 2), datetime.date(2020, 11, 16),
                             datetime.date(2020, 12, 8), datetime.date(2020, 12, 25)
                             ]
            
            self.missing_one_session = "No viniste a la sesión anterior. Espero que todo este bien! "
            self.missing_multiple_sessions = "No viniste a las últimas XX sesiones. Espero que todo esté bien! "
            self.holiday_sentence = "Espero que hayas tenido XX. "
            self.session_num_sentence = "Esta es la XX sesion de la semana. "

            self.weekend_word = "un buen fin de semana"
            self.bank_holiday_word = "un buen dia festivo"
            self.holiday_word = "unas buenas vacaciones"

            self.ordinal_num = ["primera", "segunda", "tercera", "cuarta", "quinta", "sexta", "séptima", "última"]
            self.week_days = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]

            # Previous session alerts:
            self.good_previous_session_announcement = ""
            self.good_previous_session_motivation = "Estoy seguro que esta sesión será tan buena como la última! "
            self.bad_previous_session_announcement = "En la sesión previa tuviste un problema XX. "
            self.bad_previous_session_announcement_multi = "En la sesión previa tuviste algunos problemas XX. "
            self.bad_previous_session_motivation = "Estoy seguro que todo va a estar bien! "

            self.heart_rate_word = "con la frecuencia cardiaca"
            self.blood_pressure_word = "con la presión sanguínea"
            self.tiredness_word = "de cansancio"
            self.posture_word = "con la postura"

            self.session_intensity_same = " es la misma intensidad que la última vez. "
            self.session_intensity_more = " un poco más intenso que la última vez. "
            self.session_intensity_less = " un poco menos intenso que la última vez. "

            # Progress feedback:
            self.end_of_session_announcement = "Eso ha sido todo por hoy! "
            self.no_alert_feedback = "Súper, no tuvimos problemas en esta sesión XX! Me alegra haberte acompañado, YY! "
            self.equal_alerts_as_previous = "Tuvimos el mismo número de problemas que la última vez XX. La próxima vez lo haremos mejor, YY! "
            self.less_alerts_than_previous = "Tuvimos menos problemas que la última vez XX. Sigamos trabajando así, YY! "
            self.more_alerts_than_previous = "Tuvimos más problemas que la última vez XX. La próxima vez lo haremos mejor, YY! "
            self.session_intensity_comment = "a pesar que la intensidad de la sesión fue más alta"
            self.session_intensity_comment_bad = "pero la intensidad de la sesión fue un poco más alta"
            self.fill_questionnaire = "\\pau=20\\ No olvides ingresar la presión arterial y responder las preguntas al final!"
        else:
            #in UK
            self.holidays = [datetime.date(2017, 1, 2), datetime.date(2017, 4, 14),
                             datetime.date(2017, 4, 17), datetime.date(2017, 5, 1),
                             datetime.date(2017, 5, 29), datetime.date(2017, 6, 28),
                             datetime.date(2017, 12, 25), datetime.date(2017, 12, 26)]

            # Absence sentences:
            self.missing_one_session = "You didn't come to the session last session. I hope everything is alright! "
            self.missing_multiple_sessions = "You didn't come to the last XX sessions. I hope everything is alright! "
            self.holiday_sentence = "I hope you had a nice XX. "
            self.session_num_sentence = "It is the XX session of the week. "

            self.weekend_word = "weekend"
            self.bank_holiday_word = "bank holiday"
            self.holiday_word = "holiday"

            self.ordinal_num = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "last"]
            self.week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

            # Previous session alerts:
            self.good_previous_session_announcement = ""
            self.good_previous_session_motivation = "I'm sure that it will be as good as last time! "
            self.bad_previous_session_announcement = "In the previous session, you experienced a problem with XX. "
            self.bad_previous_session_announcement_multi = "In the previous session, you experienced a few problems with XX. "
            self.bad_previous_session_motivation = "I am sure it will be all fine this time! "

            self.heart_rate_word = "heart rate"
            self.blood_pressure_word = "blood pressure"
            self.tiredness_word = "tiredness"
            self.posture_word = "posture"

            self.session_intensity_same = " same intensity as the last time. "
            self.session_intensity_more = " more intense than the last time. "
            self.session_intensity_less = " less intense than the last time. "

            # Progress feedback at the end of the session:
            self.no_alert_feedback = "Wonderful, we had no problems this session XX! I'm glad to have been here for you, YY! "
            self.equal_alerts_as_previous = "We had same number of problems as last time XX. Next time we will do even better, YY! "
            self.less_alerts_than_previous = "We had less problems this session than the previous one XX. Let's keep up the good work, YY! "
            self.more_alerts_than_previous = "We had more problems this session than the previous one XX. Next time will be better, YY! "
            self.session_intensity_comment = "even though the session intensity was higher"
            self.session_intensity_comment_bad = "but the session intensity was higher"

if __name__ == "__main__":
    useSpanish = True

    targetSpeed = 30
    targetSlope = 3
    sentenceAnnounce = "Today, we are starting with a speed of XX kilometers per second with an inclination of YY"
    if useSpanish:
        sentenceAnnounce = "Hoy, vamos a iniciar con una velocidad de XX metros por segundo con una inclinación de YY"

    MR = MemoryRobot("sergio sierra", useSpanish)

    start_time = time.time()
    MR.checkAbsence()
    MR.checkPreviousSessionAlerts(sentenceAnnounce, targetSpeed, targetSlope)

    numAlerts = 1
    sentenceToSay = "Mereces un aplauso, buen trabajo."
    for i in range(0,50):
        if MR.isSayName():
            sentence_to_say = MR.addNameToSentence(sentenceToSay)
        else:
            sentence_to_say = sentenceToSay
        print sentence_to_say
    MR.checkProgress(numAlerts)
    print time.time() - start_time
