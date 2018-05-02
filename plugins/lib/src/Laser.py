import time
import sensor
import threading


class Laser(sensor.Sensor):
    def __init__(self, settings = {"port":'COM8', "sample":1, "crotch":0.68}):
        super(Laser, self).__init__()
        #load settings
        self.settings = settings

    #overrride function
    #def process(self, req, exit):





if __name__ == '__main__':
    l = Laser()
    l.launch_process()
    time.sleep(10)
    l.shutdown()
