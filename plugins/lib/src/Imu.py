import time
import sensor
import threading
import imu.Lec_imu as Lec_imu
import numpy as np

class Imu(sensor.Sensor):
    def __init__(self, settings = {"port":'/dev/ttyACM0', "sample":1}):
        super(Imu, self).__init__()
        #load settings
        self.settings = settings
        #Default debug provided by InvenSense.
        self.__debug = Lec_imu.debug_packet_viewer()
        #Default acquisition object provided by InvenSense.
        self.__data = Lec_imu.data_packet_viewer()
        #Assigning the private variable that corresponds to the port directory.
        self.__port = self.settings['port']
        self.sample_time = self.settings['sample']
        #Default reader object provided by InvenSense.
        self.__reader = Lec_imu.eMPL_packet_reader(self.__port)
        #Arrays where data will be saved.
        self.angles_data = []
        self.quat_data = []
        self.lock = threading.Lock()
        #Flag that is used in case of pause.
        self.__pause=True

    #overrride function
    #def process(self, req, exit):
    def process(self,req,exit):
        while not exit.is_set():
            if not self.onSleep.is_set():
                try:
                    #Acquiring quaternions from the [__reader] object.
                    p1,p2,p3,p4 = self.__reader.read()
                    if (p1 == None) and (p2 == None) and (p3 == None) and (p4 == None):
                        pass
                    else:
                        #Transforming quaterions into DEG angles.
                        e1,e2,e3 = Lec_imu.ANG_euler(p2,p3,p4,p1)
                        e1 =  e1 * 180/np.pi
                        e2 =  e2 * 180/np.pi
                        e3 =  e3 * 180/np.pi
                        #saving the collected data using the thread's lock.
                        d = [e1,e2,e3]
                        #print(d)
                        if req.is_set():
                            #print("imu data requested" + str(d))
                            self.send_data(d)
                    #self.update_data([e1,e2,e3],[p1,p2,p3,p4])
                    #Coupling the list format (actual data) to the csv file (backup data).
                    #self.val=reduce(lambda a,b:str(a)+','+str(b),self.angles_data)+","+reduce(lambda a,b:str(a)+','+str(b),self.quat_data)+'\n'
                    #Save data into the backup file.
                    #self.load_data(self.val)
                    time.sleep(self.sample_time)
                except:
                    print("problems")
            else:
                self.send_data([0,0,0])
                time.sleep(self.sample_time)

    def reset(self):
        print "reset imu"
        self.onShutdown.set()
        self.__reader = Lec_imu.eMPL_packet_reader(self.__port)
        self.launch_process()


if __name__ == '__main__':
    l = Imu()
    l.launch_process()
    time.sleep(10)
    print("after 10 seconds main")
    l.shutdown()
