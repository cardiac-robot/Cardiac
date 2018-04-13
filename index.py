"""INDEX FILE CARDIAC APPLICATION"""
#library to get system utilities
import sys
#
import utilities.project as pj
#OS system verification
s = sys.platform

#windows 32 bits case
if s == 'win32':
    print 'application running in windows 32 bits'
    #import ctypes to get screen resolution
    import ctypes
    #get resolution
    user32=ctypes.windll.user32
    resolution = user32.GetSysftemMetrics(0), user32.GetSystemMetrics(1)
    res = {'width': resolution[0], 'height': resolution[1]}
    print res

#linux case
elif s == 'linux2':
    print 'application running in Linux'
    #import subprocess to get screen resolution
    import subprocess
    #get resolution
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    res = {'width': resolution[0], 'height': resolution[1]}
    print res

#other platform not supported
else:
    print 'No supported system'
    #finish the program safe
    sys.exit(0)


#proect handler load, paths
ph = pj.ProjectHandler()
