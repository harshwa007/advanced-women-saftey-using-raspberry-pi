import serial
import time 
import string
import pynmea2  
ct=0
while True:
    ser=serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
    dataout =pynmea2.NMEAStreamReader() 
    newdata=ser.readline()
    #print(newdata)
    if '$GPRMC' in str(newdata):
        print(newdata.decode('utf-8'))
        newmsg=pynmea2.parse(newdata.decode('utf-8'))  
        lat2=newmsg.latitude 
        lng2=newmsg.longitude 
        gps1 = "Latitude=" + str(lat2) + "and Longitude=" +str(lng2) 
        print(gps1)
    time.sleep(1)
    ct+=1
    if ct==10:
        break