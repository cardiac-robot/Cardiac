import src.Imu as Imu
import src.Laser as Laser
import src.Ecg as Ecg
import threading
import time
import random

class SensorManager(object):
    def __init__(self):
        #sensor control variable
        self.IMU =False
        self.LASER = False
        self.ECG =False
        #data variable
        self.data = {
                     "ecg": 0,
                     "laser": {"speed": 0.0, "cadence": 0.0, "steplenght":0.0},
                     "imu": 0.0
                    }

    #activate sensors
    def set_sensors(self, ecg =False, imu = False, laser = False):
        self.IMU = imu
        self.LASER = laser
        self.ECG = ecg
        if self.IMU:
            self.imu = Imu.Imu()

        if self.ECG:
            self.ecg = Ecg.Ecg()

        if self.LASER:
            self.laser = Laser.Laser()

    #sleep sensors
    def sleep_sensors(self, ecg = False, imu = False, laser = False):
        if ecg and self.ECG:
            self.ecg.Sleep()
        if imu and self.IMU:
            self.imu.Sleep()
        if laser and self.LASER:
            self.laser.Sleep()

    #wake up sensors
    def wakeUp_sensors(self, ecg = False, imu = False, laser = False):
        if ecg and self.ECG:
            self.ecg.WakeUp()
        if imu and self.IMU:
            self.imu.WakeUp()
        if laser and self.LASER:
            self.laser.WakeUp()

    #start running all sensor processes
    def launch_sensors(self):

        if self.IMU:
            self.imu.launch_process()

        if self.ECG:
            self.ecg.launch_process()

        if self.LASER:
            self.laser.launch_process()

    #read sensor data and update data variable
    def update_data(self):
        if self.IMU:
            imu_data = self.imu.read_data()
        else:
            imu_data  = 1.5 + random.randint(0,2)

        if self.ECG:
            ecg_data = self.ecg.read_data()
        else:
            ecg_data = 70 + random.randint(0,30)

        if self.LASER:
            laser_data = self.laser.read_data()
        else:
            laser_data = {"speed": 4.1 + + random.randint(0,2), "cadence": 0.8, "steplenght":0.5}

        self.data['imu'] = imu_data
        self.data['laser'] = laser_data
        self.data['ecg'] = ecg_data

    #print data
    def print_data(self):
        print("DATA FROM MANAGER: " + str(self.data))

    #stop data capture process
    def shutdown(self):

        if self.IMU:
            self.imu.shutdown()

        if self.LASER:
            self.laser.shutdown()

        if self.ECG:
            self.ecg.shutdown()

if __name__ == '__main__':
    sm = SensorManager()
    sm.set_sensors()
    sm.launch_sensors()
    for i in range(4):
        sm.update_data()
        time.sleep(2)
    sm.shutdown()
