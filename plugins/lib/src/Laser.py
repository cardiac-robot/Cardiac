import time
import sensor
import threading
import random

class Laser(sensor.Sensor):
    def __init__(self, settings = {"port":'COM8', "sample":1, "crotch":0.68}):
        super(Laser, self).__init__()
        #load settings
        self.settings = settings

    #overrride function
    #def process(self, req, exit):
    def process(self,req,exit):

        while not exit.is_set():
            if not self.onSleep.is_set():
                laser_data = {"speed": 4.1  + random.randint(0,2), "cadence": 0.8, "steplenght":0.5}

            else:
                laser_data = {"speed": 0.0, "cadence": 0.0, "steplenght":0.0}

            if req.is_set():
                #print("laser data requested" + str(laser_data))
                self.send_data(laser_data)



if __name__ == '__main__':
    l = Laser()
    l.launch_process()
    time.sleep(10)
    l.shutdown()
