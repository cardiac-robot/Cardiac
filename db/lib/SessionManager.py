

import time
import os
import datetime

#OBJECT that handles all the patient data during the session
class SessionManager(object):
    def __init__(self, ProjectHandler = None, UserStatus = None):
        #load project_Handler
        self.PH = ProjectHandler
        #load User status
        self.UserStatus = UserStatus
        #date
        self.date = datetime.datetime.now()
        #
        self.memory = False

    def set_memory_db(self, v = True):
        self.memory = v

    def load_sensor_data(self, hr = 0,speed =0,cadence = 0, sl =0, inclination = 0 ):
        data = str(hr) + ";" + str(speed) + ";" +str(cadence) + ";" +str(sl) + ";" +str(inclination) + ";"+ str(datetime.datetime.now()) +'\n'
        self.SensorFile.write(data)

    def load_event(self, t = "nd", c = "nd", v = "nd"):
        self.EventFile = open(self.event_name, 'a')
        data = str(t) + ";" + str(c) + ";" + str(v) +";"+ str(datetime.datetime.now())+'\n'
        self.EventFile.write(data)
        self.EventFile.close()

    def set_User(self, US):
        #load User status
        self.UserStatus = US


    def get_all_sessions(self):

        path  =  self.PH.paths['current_user']

        sessions = next(os.walk(path))[1]

        session_dict = {"events": [], "average":[],"sensors":[], 'date': []}
        all_sessions = []
        if sessions:
            for s in sessions:
                session_sensor_list = []
                session_event_list = []
                #print s
                string = path + "/" +str(s)
                print string
                sensor_file = open(string + "/Sensors.csv","r")
                se = sensor_file.readlines()[1:]
                se_dict = {"Heartrate":"","Speed":"","Cadence":"","Steplenght":"","Inclination":"","Timestamp":""}
                l = 0
                for l in enumerate(se):
                    d = se[l[0]].strip().split(";")

                    se_dict['Heartrate'] = d[0]
                    se_dict['Speed'] = d[1]
                    se_dict['Cadence'] = d[2]
                    se_dict['Steplenght'] = d[3]
                    se_dict['Inclination'] = d[4]
                    se_dict['Timestamp'] = d[5]
                    session_sensor_list.append(dict(se_dict))

                event_file = open(string + "/Events.csv", "r")
                ev = event_file.readlines()[1:]
                ev_dict = {"Type":"","Cause":"","Value":"","Timestamp":""}
                for l in enumerate(ev):
                    e = ev[l[0]].strip().split(";")

                    ev_dict['Type'] = e[0]
                    ev_dict['Cause'] = e[1]
                    ev_dict['Value'] = e[2]
                    ev_dict['Timestamp'] = e[3]
                    session_event_list.append(dict(ev_dict))

                session_dict['date'] = s

            session_dict['events'] = session_event_list
            session_dict['sensors']= session_sensor_list
            session_dict['average']= {'Speed': 3, 'Inclination': 1}
            all_sessions.append(dict(session_dict))
        else:
            print "0"
            return 0

        print all_sessions
        return all_sessions

    def check_attending_time(self):
        #p = self.RegisterStatus[1]
        p = self.load_user_times()
        isSameTime = False
        period = 5
        stddev_time = 15

        for t in p:
            if self.date.isoweekday() == t.isoweekday():
                ts = self.find_time_slot(t.isoweekday(), t.time().strftime('%H:%M:%S'), period)
                cur_ts = self.find_time_slot(self.date.isoweekday(), self.date.time().strftime('%H:%M:%S'), period)
                if cur_ts >= ts - (stddev_time/period) and cur_ts <= ts + (stddev_time/period):
                    isSameTime = True
                    print "same time"
                    break
        if not isSameTime:
            print "new time "
            #p["times"].append(self.date)
            #result = self.db_handler.update_person_times(p["name"], p["times"])
            #if result:
            #    logging.debug("added a new time for the patient")
            #else:
            #    logging.debug(self.date + ": problem occurred while adding time to patient! Add manually!!!!")


    def load_user_times(self, p):
        #get user path
        #path = self.PH.paths['current_user']
        path = p + "/times.csv"
        if os.path.exists(path):
            #open time files
            f = open(path,'r')
            #read times
            p = f.readlines()
            #eliminate "\n" character
            l = [i.strip() for i in p]
            #remove header
            times = l[1:]
            #convert to datetime format
            t = [datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f') for i in times]
            #return list of time attendance
            return t
        else:
            return 0

    def find_time_slot(self, week_day, p_time, period):
        tp = p_time.split(":")
        time_slot = (int(week_day)-1)*24*60/period + int(tp[0])*60/period + int(tp[1])/period
        return time_slot

    def update_person_times(self):
        #get user path
        path = self.PH.paths['current_user']
        #open file_name
        f = open(path + "/times.csv", "a")
        #write new attendance
        f.write(str(datetime.datetime.now()) + '\n')
        #close files
        f.close()

    def create_session(self):
        #get path
        if not self.memory:
            p = self.PH.paths['data']
        else:
            p = self.PH.paths['memory_data']

        #create user folder if not existing
        user_folder = p + "/" + str(self.UserStatus['id'])
        #load to the project handler
        self.PH.set_user_folder(user_folder)
        #validate paths
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
            self.times_file = open(user_folder + "/times.csv", 'a+')
            self.times_file.write("times\n")
            self.times_file.close()
        #create session folder
        folder = user_folder +"/" +str(self.date.year)+'-'+str(self.date.month)+'-'+str(self.date.day)
        #update current session folder
        self.PH.paths['current_session'] = folder
        #create folder
        if not os.path.exists(folder):
            os.makedirs(folder)
        #create sensor and event files
        self.sensor_name = folder + "/Sensors.csv"
        self.event_name = folder + "/Events.csv"
        #open files
        self.SensorFile = open(self.sensor_name, 'w+')
        self.EventFile = open(self.event_name, 'w+')
        #initialize headers
        self.SensorFile.write('Heartrate;Speed;Cadence;Steplenght;Inclination;Timestamp\n')
        self.EventFile.write('Type;Cause;value;Timestamp\n')
        #close files
        self.SensorFile.close()
        self.EventFile.close()
        #re open as append files
        self.SensorFile = open(self.sensor_name, 'a')
        #self.EventFile = open(event_name, 'a')

    def finish_session(self):
        #close files
        self.SensorFile.close()
        self.EventFile.close()
        #register attending
        self.update_person_times()

    def set_person(self, p):
        self.person = p


    def register_user(self, name = "nd", age = "nd", gender = "nd", height = "nd", crotch= "nd", id_number = 'nd', weight = "nd", disease = "nd" ):
        self.person = {"name"   : name,
                       "gender" : gender,
                       "age"    : age,
                       "height" : height,
                       "weight" : weight,
                       "crotch" : crotch,
                       "disease": disease,
                       "id"     : id_number,
                       'alarm1' : 120,
                       'alarm2' : 150,
                       'borg_threshold': 12
                       }
        print self.person
        #saves user in the db if not exists
        self.save_user()
        #create session for the user
        self.set_User(US = self.UserStatus)
        self.create_session()

        return self.UserStatus


    def save_user(self):
        #verify in database
        self.UserStatus = self.check_user()
        print self.UserStatus
        #saves patient if not exists: returns True if found in database and False otherwise
        if not self.UserStatus['registered']:
            #enters if not registers and perform the register process
            if not self.memory:
                path = self.PH.paths['general']
            else:
                path = self.PH.paths['memory_general']

            if os.path.exists(path + "/Patients.csv"):
                #open file to read an write
                f = open(path + "/Patients.csv", 'a')
                #save new user information
                f.write(self.person['id']          +";"+
                        self.person['name']        +";"+
                        self.person['gender']      +";"+
                        str(self.person['age'])    +";"+
                        str(self.person['height']) +";"+
                        str(self.person['weight']) +";"+
                        str(self.person['crotch']) +";"+
                        self.person['disease']     +'\n'
                        )
                #close the file
                f.close()
            else:
                f = open(path + "/Patients.csv", 'w+')
                f.write("Id;Name;Gender;Age;Height;Weight;Crotch;Disease\n")
                f.close()

                f = open(path + "/Patients.csv", 'a')
                #save new user information
                f.write(self.person['id']          +";"+
                        self.person['name']        +";"+
                        self.person['gender']      +";"+
                        str(self.person['age'])    +";"+
                        str(self.person['height']) +";"+
                        str(self.person['weight']) +";"+
                        str(self.person['crotch']) +";"+
                        self.person['disease']     +'\n'
                        )
                #close the file
                f.close()

    #method to check if user is already on the database
    def check_user(self):
        #load general path
        if not self.memory:
            path = self.PH.paths['general']
        else:
            path = self.PH.paths['memory_general']

        #check if patiens file exits
        if os.path.exists(path + "/Patients.csv"):
            f = open(path + "/Patients.csv", 'r')
            #read all lines of the file and load it into a list
            lines = f.readlines()
            #close file
            f.close()
            #skip the headers
            patients = lines[1:]
            #check patient lists
            for p in patients:
                pl = p.split(";")
                if pl[0] == self.person['id']:
                    #load personf info
                    self.person['name']           = pl[1]
                    self.person['gender']         = pl[2]
                    self.person['age']            = pl[3]
                    self.person['height']         = pl[4]
                    self.person['weight']         = pl[5]
                    self.person['crotch']         = pl[6]
                    self.person['disease']        = pl[7]
                    self.person['alarm1']         = 120
                    self.person['alarm2']         = 150
                    self.person['borg_threshold'] = 12
                    print "patient already existing in db"
                    return {"name" : self.person['name'], "registered" : True, "id" : self.person['id']}

            return {"name" : self.person['name'], "registered" : False, "id" : self.person['id']}
        else:
            f = open(path + "/Patients.csv", 'w+')
            f.write("Id;Name;Gender;Age;Height;Weight;Crotch;Disease\n")
            f.close()
            return {"name" : self.person['name'], "registered" : False, "id" : self.person['id']}
