"""INDEX FILE CARDIAC APPLICATION"""
#library to get system utilities
import sys
#import PyQt4 gui library
from PyQt4 import QtCore, QtGui
#import local lib to load the project_Handler
import utilities.project as PJ
import plugins.MainPlugin as MP
#import data handler and database
import db.database as database


if __name__ == '__main__':
    #OS system verification
    s = sys.platform

    #windows 32 bits case
    if s == 'win32':
        #import ctypes to get screen resolution
        import ctypes
        #get resolution
        user32=ctypes.windll.user32
        resolution = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        res = {'width': 2.0*int(resolution[0]), 'height': 1.8*int(resolution[1])}

    #linux case
    elif s == 'linux2':
        #import subprocess to get screen resolution
        import subprocess
        #get resolution
        output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
        resolution = output.split()[0].split(b'x')
        res = {'width': int(resolution[0]), 'height': int(resolution[1])}
        print type(res['width'])

    #other platform not supported
    else:
        print 'No supported system'
        #finish the program safe
        sys.exit(0)

    #create settings sdictionary to pass it to de the project handler
    settings = {'res': res, 'sys': s}
    #project handler load, paths
    ph = PJ.ProjectHandler(settings = settings , log = True)
    #database creation
    db = database.database(ProjectHandler = ph)
    #launch entry point of the interface
    app = QtGui.QApplication(sys.argv)
    main = MP.MainPlugin(ProjectHandler = ph, DataHandler = db)

    print"going out"
    sys.exit(app.exec_())
