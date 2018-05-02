import sys
import serial
import struct
import time
import threading

class HXM_data(object):

    def __init__(self,serial_port='/dev/rfcomm0',name_csv='datos.csv',time_adq=2):
		#Este objeto permite adquirir datos del dispositivo zephyr-HXM
		#Recibe como argumento una direccion en la cual se encuentra enlazado
		#El puerto bluetooth.
		#Los siguientes atributos representan configuracion de la comunicacion
		#Serial con el dispositivo:
		self.__ser=serial.Serial(serial_port, 115200, timeout=1)
		self.__async=False
		self.__stx = struct.pack("<B", 0x02)
		self.__etx = struct.pack("<B", 0x02)
		self.__rate = struct.pack("<B", 0x26)
		self.__dlc_byte = struct.pack("<B", 55)
		#Bandera que indica si se adquieren datos o no.
		self.acquire_on=True
		#Hilos utilizados, se cierra al asignar False a la bandera anterior
		self.__t1=threading.Thread(target=self.save_data)
		#self.__t2=threading.Thread(target=self.acquire_data)
		#Nombre del archivo donde se guardan los datos temporalmente
		self.__name_csv=name_csv
		#Frecuencia en la que reciben los datos
		self.time_adq=time_adq
		#Inicializacion de las variables
		self.__f2=open(self.__name_csv,'w')
		self.__f2.write("fid, fiv, hid, hiv, batt, hr, hbn, hbts1, hbts2, hbts3, hbts4, hbts5, hbts6, hbts7, hbts8, hbts9, hbts10, hbts11, hbts12, hbts13, hbts14, hbts15, distance, speed, strides")
		self.__f2.close()

    def run_all(self):
		self.__t1.start()
		#self.__t2.start()

    def acquire_data(self):
		#Funcion para extraer los datos del fichero
        self.f1=open(self.__name_csv,'r')
        line =  self.f1.readlines()[-1]
        self.f1.close()
        return line

    def save_data(self):
        while self.acquire_on:
            try:
                d = self.__ser.read()
                print(str(d))
                if d != self.__stx:
                    if not self.__async:
                        print >>sys.stderr, "Not synched"
                        print(":()")
                        self.__async = True
                    continue
                print("pass")
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
                print "L: " + str(len)

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
                    print "CRC validated!"
                if end != 0x03:
                    print >>sys.stderr, "Bad ETX"

                #Guardando datos en fichero
                self.__data_temp=struct.unpack("<H2sH2sBBB15H6xHHB3x", payload)
                self.val=reduce(lambda a,b:str(a)+','+str(b),self.__data_temp)+'\n'
                self.__f2=open(self.__name_csv,'a+')
                self.__f2.write(self.val)
                print('Agregado')
                self.__f2.close()
            except:
                print("problems...")
                pass
#   	     	fid, fiv, hid, hiv, batt, hr, hbn, hbts1, hbts2, hbts3, hbts4, hbts5, hbts6, hbts7, hbts8, hbts9, hbts10, hbts11, hbts12, hbts13, hbts14, hbts15, distance, speed, strides = struct.unpack("<H2sH2sBBB15H6xHHB3x", payload)
if __name__=='__main__':
	a=HXM_data()
	a.run_all()
	try:
		while True:
			time.sleep(0.5)
	except KeyboardInterrupt:
		print("Keyboard interrupt")
		a.acquire_on = False
