import plugins.robot.robotController as RC
import db.database as database
import utilities.project as PJ
import plugins.lib.Manager as M
import time
import random

if __name__ == '__main__':
    ph = PJ.ProjectHandler(log =True)
    db = database.database(ProjectHandler = ph)
    man = M.SensorManager()
    man.set_sensors()#if no parameters all are false
    man.launch_sensors()
    #register user to open a session
    db.General.SM.register_user(id_number = "1031137220",name ="alfonso casas", age =46, gender = "F", height = 1.69, disease = "cvd")
    db.General.SM.load_event(t = "init",c = "none", v = "nd")

    c = RC.Controller(ProjectHandler = ph , db = db)
    t = 0
    c.launch()
    bo = 0
    for i in range(150):
        print("main")

        man.update_data()
        db.General.SM.load_sensor_data(hr = man.data['ecg'],
                                       speed = man.data['laser']['speed'],
                                       cadence= man.data['laser']['cadence'],
                                       sl = man.data['laser']['steplenght'],
                                       inclination = man.data['imu'])
        c.send_data(man.data)
        if bo < 20:
            bo = bo +1
        else:
            bo = 0
            c.send_borg(8 + random.randint(0,4))


        time.sleep(1)

    c.shutdown()
    man.shutdown()
    db.General.SM.load_event(t ="end", c ="none", v = "nd")
    db.General.SM.finish_session()
    time.sleep(5)
    print("going out main")
