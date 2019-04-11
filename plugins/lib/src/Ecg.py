import time
import sensor
import threading
import random
import struct
import serial

class Ecg(sensor.Sensor):
    def __init__(self, settings = {"port":'COM7', "sample":1}):
        super(Ecg, self).__init__()
        #load settings
        print settings
        self.settings = settings

        #defining the serial port that will be used.
        #self.__ser = serial.Serial(self.settings['port'], 115200, timeout=1)
        #Flag used to check the synchronization.
        self.__async = False
        
        self.__data_temp=[]
        #Flag that is used in case of pause.
        self.__pause=True
        self.sample_time= self.settings['sample']
        print("init run")

    def process(self, req, exit):
        
        EcgSensor(port = "COM7")
        

    #overrride function
    #def process(self, req, exit):
    def process_deprecated(self,req,exit):
        #defining the serial port that will be used.
        self.__ser = serial.Serial(self.settings['port'], 115200, timeout=3)
        #Variables used in the zephyr's serial protocol.
        self.__stx = struct.pack("<B", 0x02)
        self.__etx = struct.pack("<B", 0x02)
        self.__rate = struct.pack("<B", 0x26)
        self.__dlc_byte = struct.pack("<B", 55)
        #Array  where the EKG data will be saved.
        self.PrintData("Processs started")
        cont =0
        while not exit.is_set():
            if not self.onSleep.is_set():
                #ECG PROCESS HERE
                try:
                    d = self.__ser.read()
                    print(str(d))
                    if d != self.__stx:
                        if not self.__async:
                            print >>sys.stderr, "Not synched"
                            self.__async = True
                        continue

                    self.__async = False
                    type = self.__ser.read()	# Msg ID
                    if type != self.__rate:
                        print >>sys.stderr, "Unknown message type"
                    dlc = self.__ser.read()	# DLC
                    len, = struct.unpack("<B", dlc)
                    if len != 55:
                        print >>sys.stderr, "Bad DLC"
                    payload = self.__ser.read(len)
                    crc, = struct.unpack("<B", self.__ser.read())
                    end, = struct.unpack("<B", self.__ser.read())
                    sum = 0
                    #print "L: " + str(len)

                    for i in xrange(len):
                        b, = struct.unpack("<B", payload[i])
                        #print "Data: 0x%02x" % b
                        sum = (sum ^ b) & 0xff
                        for j in xrange(8):
                            if sum & 0x01:
                                sum = (sum >> 1) ^ 0x8c
                            else:
                                sum = (sum >> 1)
                    #print "CRC:  0x%02x" % crc
                    if crc != sum:
                        print >>sys.stderr, "Bad CRC: " + str(sum) + " is not " + str(crc)
                    else:
                        pass #print "CRC validated!"
                    if end != 0x03:
                        print >>sys.stderr, "Bad ETX"

                    #Saving data into the backup file.
                    with self.lock:
                        self.__data_temp=list(struct.unpack("<H2sH2sBBB15H6xHHB3x", payload))

                    self.val=reduce(lambda a,b:str(a)+','+str(b),self.__data_temp)+'\n'
                    #self.load_data(self.val)

                    if req.is_set():
                        self.send_data(self.val)
                        
                    time.sleep(self.sample_time)
                except:
                    print("problems with ECG acquisition ")
                    cont += 1
                    if (cont == 5):
                        self.__ser.close()
                        break
                    pass
                    

                    #if req.is_set():
                    #    self.send_data(self.val)

                    #time.sleep(self.sample_time)
                    
                #except:
                #    print("problems with ECG acquisition ")
                #    cont += 1
                #    if (cont == 5):
                #       break
                #   pass
                
            else:
                time.sleep(1)
                ecg_data = 0




if __name__ == '__main__':
    l = Ecg()
    l.launch_thread()
    #l.launch_thread()
    print "process launched"
    for i in range(15):
        print "data"
        d = l.read_data()
        print d
        time.sleep(1)
    print "out"
    l.shutdown()
