import time
import sensor
import threading
import random

class Ecg(sensor.Sensor):
    def __init__(self, settings = {"port":'COM8', "sample":1}):
        super(Ecg, self).__init__()
        #load settings
        self.settings = settings

    #overrride function
    #def process(self, req, exit):
    def process(self,req,exit):

        while not exit.is_set():
            if not self.onSleep.is_set():
                ecg_data = 70 + random.randint(0,30)
            else:
                ecg_data = 0

            if req.is_set():
                print("desde ECG OBJECT ecg data requested" + str(ecg_data))
                self.send_data(ecg_data)




if __name__ == '__main__':
    l = Ecg()
    l.launch_process()
    time.sleep(10)
    l.shutdown()
