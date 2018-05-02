import multiprocessing
from multiprocessing.managers import BaseManager
import time
import threading
import sys

class SensorManager(object):
    def __init__(self, settings = 0):
        self.settings = settings
        self.sample_time  = 2

    def launch_process(self):
        self.PipeOut, self.PipeIn= multiprocessing.Pipe()
        self.e = multiprocessing.Event()
        self.e1 = multiprocessing.Event()
        self.p = multiprocessing.Process(target = self.process, args = ((self.PipeOut,self.PipeIn),self.e,self.e1,))
        self.p.start()
        self.on = True

        #self.p.join()

    def reader(self):
        while self.on:
            self.e.set()
            self.update_data()
            self.e.clear()
            print "reader " + str(self.settings)
            time.sleep(self.sample_time)
        print("going out reader")

    def shutdown(self):
        self.e1.set()
        self.on = False

    def launch_data_server(self):
        self.ManagerServer = BaseManager(address=('', 50000), authkey=b'abc')
        self.ManagerServer.start()
        #self.ManagerServer.register(self.settings)
        #self.server = self.ManagerServer.get_server()
        #self.server.start()

    def update_data(self):
        self.settings = self.PipeOut.recv()

    def shutdown_server(self):
        self.ManagerServer.shutdown()

    def process(self, pipe, e, e1):
        #self.client = BaseManager(address=('127.0.0.1', 50000), authkey=b'abc')
        #self.client.connect()
        t  = self.settings
        PipeOut,PipeIn = pipe
        while not e1.is_set():
            t = t +1
            print "reducing " +str(t)
            if e.is_set():
                print "send"
                PipeIn.send(t)
            time.sleep(0.5)
        print "going out"



if __name__ == '__main__':
    sm = SensorManager(settings = 10)
    sm.launch_process()
    t = threading.Thread(target = sm.reader)
    t.start()

    print("sss")
    time.sleep(10)
    print("countdown")
    sm.shutdown()
    print("------")
    print sm.on
    time.sleep(5)
    print("chao")
