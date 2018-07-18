import time
import numpy as np

class Analyzer(object):
    def __init__(self, profile = { 'name'          : "jonathan",
                                   'age'           : 26,
                                   'alarm1'        : 30,
                                   'alarm2'        : 40,
                                   'borg_threshold':11,
                                   'weight'        : 80,
                                   'last_measure'  : {}
                                 }):
        #load the user's profile to be analized
        self.profile = profile
        #creates the data buffer
        self.dataBuffer = []
        #borg scale buffer
        self.borgBuffer = []
        #
        self.isBorgConfirmed = False

    #load sensor data to the analyzer buffer
    def load_data(self,d):
        #check buffer size
        if len(self.dataBuffer) < 10:
            self.dataBuffer.append(d)
        else:
            self.dataBuffer = self.dataBuffer[1:]
            self.dataBuffer.append(d)

    #load borg scale value
    def load_borg(self, b):
        self.borgBuffer.append(b)

    #remove last borg request for confirmation
    def clear_borg(self):
        self.borgBuffer = self.borgBuffer[:-1]
        self.isBorgConfirmed = True

    #check borg scale:
    def check_borg(self):
        #check borg level
        if self.borgBuffer[-1] > self.profile['borg_threshold']:
            #check hr level
            print self.borgBuffer
            if len(self.dataBuffer) > 8:
                m = np.mean([ i['ecg'] for i in self.dataBuffer[4:] ])
                if m > self.profile['alarm1']:
                    #patient feeling too tired
                    return 1
                else:
                    #ask again if patient provided the correct value
                    if self.isBorgConfirmed:
                        self.isBorgConfirmed = False
                        return 0
                    else:
                        return 2

        return 0




    #check profile alarms with minimum the last 8 measured values
    def check_hr(self):
        #check if there are at least 8 values in the buffer
        if len(self.dataBuffer) > 8:
            #calculates the average of the hr
            m = np.mean([ i['ecg'] for i in self.dataBuffer])
            #compare second alarm
            if m > self.profile['alarm2']:
                return 2
            #compare first alarm
            elif m > self.profile['alarm1']:
                return 1
            else:
                return 0
        #if there is not enough data in the buffer
        else:
            return 0


if __name__ == '__main__':
    a = Analyzer(profile = { 'name': "jonathan",
                    'age' : 26,
                    'alarm1': 30,
                    'alarm2': 40,
                    'borg_threshold':11,
                    'weight': 80,
                    'last_measure': {}
                   })

    for i in range(20):
        a.load_data(i*5)
        print "checking: " + str(a.check_hr())
        print a.dataBuffer
