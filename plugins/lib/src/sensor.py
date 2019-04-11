import multiprocessing
import threading
import time
import sys

class Sensor(object):
    def __init__(self):
        #Create event handler for data request
        self.onRequest = multiprocessing.Event()
        #on sleep event
        self.onSleep = multiprocessing.Event()
        #create event handler to finish the process
        self.onShutdown = multiprocessing.Event()
        #create Pipe
        self.PipeGet, self.PipeLoad = multiprocessing.Pipe()
        #data variable
        self.data_to_send = 0

    #launch measurement process
    def launch_process(self):
        self.p = multiprocessing.Process(target = self.process,args = (self.onRequest,self.onShutdown,))
        #self.p = threading.Thread(target = self.process,args = (self.onRequest,self.onShutdown,))        
        self.p.start()

    def launch_thread(self):
        self.p = threading.Thread(target = self.process,args = (self.onRequest,self.onShutdown,))
        self.p.start()

    #send data
    def send_data(self, d):
        self.PipeLoad.send(d)

    #returns data readed from process
    def read_data(self):
        self.onRequest.set()
        d = self.PipeGet.recv()
        self.onRequest.clear()
        #print "data received" + str(d)
        return d

    def Sleep(self):
        #set signal
        self.onSleep.set()

    def WakeUp(self):
        #clear sleep signal
        self.onSleep.clear()

    def PrintData(self, data):
        print(data)
        sys.stdout.flush()    


    #trigger the event to stop the process
    def shutdown(self):
        self.onShutdown.set()
        time.sleep(2)

    #process to overrride
    def process(self, req, exit):
        t = 0
        while not exit.is_set():
            if not self.onSleep.is_set():
                t = t + 1
                print ("running process " + str(t))
                if req.is_set():
                    print("data requested" + str(t))
                    self.send_data(t)
                time.sleep(0.1)
            else:
                self.send_data(0)



        print("going out of process...")


if __name__ == '__main__':
    s = Sensor()
    s.launch_thread()
    for i in range(15):
        s.read_data()
        time.sleep(1)

    s.shutdown()
    time.sleep(2)
