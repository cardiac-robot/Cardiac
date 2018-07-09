# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:56:16 2017

@author: cardio
"""
import sys
import os
import socket
import cv2
import threading
import logging
import time

logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] (%(threadName)-9s) %(message)s',)

class ImageSender(object):
    def __init__(self,
                 ip = '192.168.1.7',
                 path = '//home//nao//dev//images//',
                 name = 'took.jpg',
                 tempPath = '//',
                 ProjectHandler = None):
        #load ProjectHandler
        self.PH = ProjectHandler
        #
        self.imgToSend = None
        self.imgName = name
        self.destIp = ip
        self.destPath = path
        self.tempPath = self.PH.paths['recognition']
        self.local = self.tempPath + "/took.jpg"


    #
    def takePhoto(self):
        self.cam = cv2.VideoCapture(0)
        if self.cam.isOpened():
            s,img = self.cam.read()
            if s:
                cv2.namedWindow("cam-test",cv2.WINDOW_AUTOSIZE)
                cv2.imshow("cam-test",img)
                time.sleep(5)
                cv2.destroyWindow("cam-test")
                cv2.imwrite(self.local,img) #save image

            self.cam.release()
    #
    def sendPhoto(self):
        if self.PH.settings['sys'] == "win32":
            os.system('pscp .\\' + self.local + ' nao@' + self.destIp + '://home//nao//dev//images//nao_image.jpg')
        elif self.PH.settings['sys'] == "linux2":
            print "pscp -pw bmd " + self.imgName + " nao@" + self.destIp + ":/home/nao/dev/images/nao_image.jpg"
            os.system("pscp -pw bmd " + self.local + " nao@" + self.destIp + ":/home/nao/dev/images/nao_image.jpg")

    #
    def get_image_path(self):
        print('from scripts')
        print self.local
        return self.local


'''
ImageServer Object:

This object inherits the Thread class and runs a socket server that takes the photo to the patient
and sends it through the socket to the client socket.
'''

class ImageServer(threading.Thread):
    def __init__(self,  file_name = "nao_image.jpg", file_path = "/home/nao/dev/images/"):
        super(ImageServer, self).__init__(group = None, target = None, name = "ImageServer-Thread", verbose = None)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.port = 8888
        self.BUFF = 1000000
        self.get_ip()
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        self.go_on = True
        self.file_path = file_path
        self.file_name = self.file_path + file_name



    def run(self):
        while self.go_on:
            logging.debug("Waiting on connection....")
            self.sc, address = self.socket.accept()
            logging.debug("Client connected with Address: ")
            logging.debug(address)
            code = self.sc.recv(100)
            if code == "1":
                logging.debug("shutdown server")
                self.sc.close()
                break
            if code == "0":
                self.img = self.sc.recv(self.BUFF)
                if self.img:
                    self.file = open(self.file_name, 'wb')
                    self.file.write(self.img)
                    self.file.close()
                else:
                    logging.debug("no image")
                    self.file.close()

        logging.debug("out")

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            self.ip = s.getsockname()[0]
            logging.debug(self.ip)
            s.close()
        except:
            logging.debug("cannot connect... localhost ip assigned")
            self.ip = "127.0.0.1"




    def shutdown(self):
        self.go_on = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.ip,self.port))
            self.s.send("1")
            self.socket.close()
        except:
            self.socket.close()

'''
ImageClient:
This class inherits the thread class and stablish a connection with the server running on the tablet on the interface side.
This recieves the picture and save it on the specified file
'''
class ImageClient(threading.Thread):
    def __init__(self, server_ip = "192.168.1.3"):
        super(ImageClient, self).__init__(group = None, target = None, name = "ImageClient-Thread", verbose = None)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.port = 8888
        self.server_ip = server_ip



        self.attempts = 2

    def run(self):
        keepTrying = True
        cont = 0
        while keepTrying:
            try:
                self.socket.connect((self.server_ip, self.port))
                self.socket.send("0")

                self.captureRoutine()
                #self.img = self.socket.recv(self.BUFF)

                keepTrying = False
            except:
                cont += 1
                logging.debug("connection to the server could not be established, attempt: " + str(cont))
                time.sleep(0.5)
                if cont > self.attempts:
                    cont = 0
                    keepTrying = False
                    logging.debug("going out")

        logging.debug("out")

    def captureRoutine(self):
        self.cam = cv2.VideoCapture(0)
        if self.cam.isOpened():
            s,img = self.cam.read()
            if s:
                cv2.namedWindow("cam-test",cv2.WINDOW_AUTOSIZE)
                cv2.imshow("cam-test",img)
                time.sleep(5)
                cv2.destroyWindow("cam-test")
                cv2.imwrite("temp.jpg",img) #save image
                f = open("temp.jpg",'rb').read()
                self.socket.send(f)
                #f.close()
                self.socket.close()

            self.cam.release()

'''
Main function example
'''
def main():
    #creation of the server
    s = ImageServer(file_path = "")
    #creation of the client
    c = ImageClient()
    #launch the server and starts listening to incomming client request
    s.start()
    time.sleep(5)
    #send the request to the server
    for i in range(2):

        c.start()
        time.sleep(10)
        c = ImageClient()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        s.shutdown()
if __name__ == '__main__':
    main()
