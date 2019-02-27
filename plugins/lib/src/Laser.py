import time
import sensor
import threading
import random
import serial
import sys
#import laser.leg_detector as LD

class Laser(sensor.Sensor):
    def __init__(self, settings = {"port":'COM9', "sample":1, "crotch":0.68}):
        super(Laser, self).__init__()
        #load settings
        self.laser_height = 0.3
        #print settings
        self.settings = settings   

        #self.serial_pi = serial.Serial(port = self.settings['port'],baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
        #self.go_on = True
        #self.__pause = True
        #self.leg_detector = LD.LegDetector(port = self.settings['port'])
        self.Ts = self.settings['sample']
        self.data = {"speed": 1, "cadence": 1, "steplenght": 1}
        self.lrf_h = 0.3
        self.crotch = self.settings['crotch']
        #print "end init...."
    #overrride function
    #def process(self, req, exit):

    def process_deprecated(self,req,exit):
        #print'started laser process'
        
        self.serial_pi = serial.Serial(port = self.settings['port'],baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
        while not exit.is_set():
            if not self.onSleep.is_set():
                
                self.leg_detector.leg_detection_process()
                data  = self.leg_detector.get_processed_data()
                cad   = float(data['cadence'])
                cad   = cad/2

                sl    = float(data['ldd'] * self.crotch / (self.crotch - self.laser_height))
                sl = sl /1000

                speed = float(sl * cad)
                speed = speed * 5.76

                self.data = {"speed": speed, "cadence": cad, "steplenght": sl}

                print self.data
                if req.is_set():
                    #print self.data
                    self.send_data([ self.data['cadence'], self.data['steplenght'], self.data['speed'] ])



    def process(self,req,exit):
        
        self.serial_pi = serial.Serial(port = self.settings['port'],baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
        
        while not exit.is_set():
            if not self.onSleep.is_set():
                #laser_data = {"speed": 4.1  + random.randint(0,2), "cadence": 0.8, "steplenght":0.5}
                #Escribir byte de inicio
                self.serial_pi.write(chr(0x55))
                #adquirir respuesta
                pong = self.serial_pi.read(1)
                if not pong:
                    continue
                val=ord(pong)
                #si el resultado es 0x0A, significa que la raspberry recibio el mensaje
                if val!=0x0A:
                    time.sleep(0.05)
                    continue
                #pedir la longitud de la velocidad
                val=ord(self.serial_pi.read(1))
                #adquirir los datos de la velocidad
                vel=self.serial_pi.read(val)
                #pedir la longitud de la cadencia
                val=ord(self.serial_pi.read(1))
                #adquirir los datos de la cadencia
                cad=self.serial_pi.read(val)
                #pedir la longitud de la longitud de paso
                val=ord(self.serial_pi.read(1))
                #adquirir los datos de longitud de paso
                sl=self.serial_pi.read(val)
                #mostrar los datos en consola...
                    
                vel = float(vel)
                cad = float(cad)
                sl  = float(sl)


                self.crotch = float(self.crotch)
                sl  = sl/1000
                cad = cad/2
                sl = float(sl)
                sl=sl*self.crotch/(self.crotch-self.lrf_h)
                self.data = [float(cad)*sl, cad, str(sl)]
                self.data = {"speed": float(cad)*sl, "cadence": cad, "steplenght":str(sl)}
                
                
                if req.is_set():
                    #print self.data
                    self.send_data([ self.data['cadence'], self.data['steplenght'], self.data['speed'] ])
                time.sleep(self.Ts)
            else:
                self.data = {"speed": 0.0, "cadence": 0.0, "steplenght":0.0}



        self.serial_pi.close()
            #if req.is_set():
              #print("laser data requested" + str(laser_data))
                #self.send_data(self.data)



if __name__ == '__main__':
    l = Laser()
    l.WakeUp()
    print 'launch process from main'
    l.launch_process()
    time.sleep(2)
    print l.read_data()
    time.sleep(1)
    print l.read_data()
    time.sleep(1)
    print l.read_data()
    time.sleep(1)
    print l.read_data()
    time.sleep(1)
    print l.read_data()

    print"end....."
    l.shutdown()
