import src.Imu as Imu
import src.Laser as Laser
#import src.Ecg as Ecg
import src.ecg_sensor as Ecg
import threading
import time
import random

class SensorManager(object):
    def __init__(self, imu   = {"port":'COM4', "sample":1},
                       ecg   = {"port":'COM6', "sample":1},
                       laser = {"port":'COM3', "sample":1, "crotch":0.68}
                ):
        #sensor control variable
        self.settings_imu = imu
        self.settings_ecg = ecg
        self.settings_laser = laser
        #control variables
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
    def set_sensors(self, ecg =True, imu = True, laser = True):
        self.IMU = imu
        self.LASER = laser
        self.ECG = ecg
        if self.IMU:
            self.imu = Imu.Imu(settings = self.settings_imu)

        if self.ECG:
            #self.ecg = Ecg.Ecg(settings = self.settings_ecg)
            self.ecg = Ecg.EcgSensor(port=self.settings_ecg['port'], sample = self.settings_ecg['sample'])

        if self.LASER:
            self.laser = Laser.Laser(settings = self.settings_laser)

    #sleep sensors
    def sleep_sensors(self, ecg = False, imu = False, laser = False):
        if ecg and self.ECG:
            self.ecg.close()
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
            #self.ecg.launch_process()
            self.ecg.start()
            self.ecg.play()

        if self.LASER:
            self.laser.launch_process()

    #read sensor data and update data variable
    def update_data(self):
        print("Update data from SensorManager")
        if self.IMU:
            imu_data = self.imu.read_data()
        else:
            imu_data  = [1.5 + random.randint(0,2), 0, 0]

        if self.ECG:
            #ecg_data = self.ecg.read_data()
            ecg_data = self.ecg.get_data()
            #print('Data ecg from Manager')
            #print(ecg_data)
            if not ecg_data:
                ecg_data = 0

            #ecg_data = float(ecg_data)
            if len(str(ecg_data))> 1:
                ecg_data = ecg_data[5]
                #ecg_data = float(ecg_data)
        else:
            ecg_data = 70 + random.randint(0,30)

        if self.LASER:
            print("#####READING DATA FROM LASER#####")
            laser_data = self.laser.read_data()
            if len(laser_data) == 3:
                laser_data = {"speed": laser_data[2], "cadence": laser_data[0], "steplenght": laser_data[1]}
                print laser_data
            else:
                print("missing data from laser")
                pass 

            print("################################")
        else:
            laser_data = {"speed": 4.1 + + random.randint(0,2), "cadence": 0.8, "steplenght":0.5}

        self.data['imu'] = imu_data[0]
        self.data['laser'] = laser_data
        self.data['ecg'] = ecg_data
        print("#########sensor manager update data##########")
        print self.data
        print("#############################################")
        #self.data = str(self.data)

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
    sm.set_sensors(laser = False, imu = False, ecg = True)
    sm.launch_sensors()
    for i in range(4):
        sm.update_data()
        sm.print_data()
        time.sleep(2)
    sm.shutdown()
