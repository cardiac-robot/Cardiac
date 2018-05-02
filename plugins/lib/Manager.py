import src.Imu as Imu
import threading
import time
import random

class SensorManager(object):
    def __init__(self):
        #create IMU object

        self.IMU =False
        self.LASER = False
        self.ECG =False
        self.data = {
                     "ecg": 0,
                     "laser": {"speed": 0.0, "cadence": 0.0, "steplenght":0.0},
                     "imu": 0.0
                    }
    def set_sensors(self, ecg =False, imu = False, laser = False):
        if self.IMU:
            self.imu = Imu.Imu()

        if self.ECG:
            print("ecg")

        if self.LASER:
            print("laser")


    def launch_sensors(self):
        if self.IMU:
            self.imu.launch_process()

        if self.ECG:
            print("launch ecg")

        if self.LASER:
            print("launch laser")


    def update_data(self):
        if self.IMU:
            imu_data = self.imu.read_data()
            print "data from manager " +str(imu_data)

        else:
            #print("simulated data")
            imu_data  = 1.5 + random.randint(0,2)


        if self.ECG:
            print("get ecg sensor data")
        else:
            #print("simulated data")
            ecg_data = 70 + random.randint(0,30)

        if self.LASER:
            print("get laser sensor data")
        else:
            #print("simulated data")
            laser_data = {"speed": 4.1 + + random.randint(0,2), "cadence": 0.8, "steplenght":0.5}

        self.data['imu'] = imu_data
        self.data['laser'] = laser_data
        self.data['ecg'] = ecg_data

        print self.data

    def shutdown(self):
        if self.IMU:
            self.imu.shutdown()

if __name__ == '__main__':
    sm = SensorManager()
    sm.set_sensors()
    sm.launch_sensors()
    for i in range(4):
        sm.update_data()
        time.sleep(2)
    sm.shutdown()
