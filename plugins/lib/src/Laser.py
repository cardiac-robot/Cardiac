import time
import sensor
import threading
import random
import serial

class Laser(sensor.Sensor):
    def __init__(self, settings = {"port":'COM8', "sample":1, "crotch":0.68}):
        super(Laser, self).__init__()
        #load settings
        print settings
        self.settings = settings

        self.serial_pi = serial.Serial(port = self.settings['port'],baudrate=115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
        #self.go_on = True
        #self.__pause = True
        self.Ts = self.settings['sample']
        self.data = []
        self.lrf_h = 0.3
        self.crotch = self.settings['crotch']

    #overrride function
    #def process(self, req, exit):
    def process(self,req,exit):

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
                self.crotch = float(self.crotch)
                sl = float(sl)
                sl=sl*self.crotch/(self.crotch-self.lrf_h)
                self.data = [float(cad)*sl, cad, str(sl)]
                self.data = {"speed": float(cad)*sl, "cadence": cad, "steplenght":str(sl)}
                time.sleep(self.Ts)
            else:
                self.data = {"speed": 0.0, "cadence": 0.0, "steplenght":0.0}




            if req.is_set():
                #print("laser data requested" + str(laser_data))
                self.send_data(self.data)



if __name__ == '__main__':
    l = Laser()
    l.launch_process()
    time.sleep(10)
    l.shutdown()
