

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


    def create_session(self):
        #get path
        p = self.PH.paths['data']
        #create user folder if not existing
        user_folder = p + "/" + str(self.UserStatus['name'])
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        #create session folder
        folder = user_folder +"/" +str(self.date.year)+'-'+str(self.date.month)+'-'+str(self.date.day)
        if not os.path.exists(folder):
            os.makedirs(folder)
        #create sensor and event files
        self.sensor_name = folder + "/Sensors.csv"
        self.event_name = folder + "/Events.csv"
        #open files
        self.SensorFile = open(self.sensor_name, 'w+')
        self.EventFile = open(self.event_name, 'w+')
        #initialize headers
        self.SensorFile.write('Heartrate;Speed;Cadence;Steplenght;Inclination\n')
        self.EventFile.write('Type;Cause;value;Timestamp\n')
        #close files
        self.SensorFile.close()
        self.EventFile.close()
        #re open as append files
        self.SensorFile = open(self.sensor_name, 'a')
        #self.EventFile = open(event_name, 'a')

    def finish_session(self):
        self.SensorFile.close()
        self.EventFile.close()

    def register_user(self, name = "nd", age = "nd", gender = "nd", height = "nd", crotch= "nd", id_number = 'nd', weight = "nd", disease = "nd" ):
        self.person = {"name"   : name,
                       "gender" : gender,
                       "age"    : age,
                       "height" : height,
                       "weight" : weight,
                       "crotch" : crotch,
                       "disease": disease,
                       "id"     : id_number
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
            path = self.PH.paths['general']
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
        path = self.PH.paths['general']
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
                    print "patient already existing in db"
                    return {"name" : self.person['name'], "registered" : True}

            return {"name" : self.person['name'], "registered" : False}
        else:
            f = open(path + "/Patients.csv", 'w+')
            f.write("Id;Name;Gender;Age;Height;Weight;Crotch;Disease\n")
            f.close()
            return {"name" : self.person['name'], "registered" : False}
