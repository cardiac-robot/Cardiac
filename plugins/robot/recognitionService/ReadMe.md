README FOR RECOGNITION MEMORY:


** On the robot:

RecognitionService should be uploaded to the robot through Choregraphe:

In Choregraphe 2.4: File->Open Project choose CRRobot/recognitionService/recognition-service.pml

Connect to the robot. Go to the Robot Applications view, and click "Package and install current project to the robot" button (in the shape of Nao head with an arrow)


Send the loadCustomFaceLibrary.py file to the robot:
 
 $ cd CRRobot/recognitionService/scripts/

 $ scp loadCustomFaceLibrary.py nao@IP_ADDRESS_ROBOT:/home/nao/dev/lib/

add the library libfacedetection_2_4_2_25_nao.so under the same folder
Link to get the library: http://protolab.aldebaran.com:9000/protolab/facedetection_custom/tree/master
Modify autoload.ini file in the robot /home/nao/naoqi/preferences/ and 
under the [python] line add the path to this python file

Example:
...
[python]
#the/full/path/to/your/python_module.py   # load python_module.py
/home/nao/dev/lib/loadCustomFaceLibrary.py

...

This will exit the current face detection library and load the custom library at startup.

Connect to the robot:

 $ ssh nao@IP_ADDRESS_ROBOT

 $ qicli call ALFaceDetection.clearDatabase

** On the tablet:

Install pandas: (Needs Numpy)

 $ sudo pip install pandas

Install pyAgrum:

 $ sudo pip install pyagrum


Start the MongoDB.

 $ sudo service mongod start

Run testIntegration.py file to see if the code is working. Use that file to integrate the memory into the system. 


TherapyMemory is already integrated within robotController.py so there is no need to run it.



