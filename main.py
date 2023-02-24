from gsm import *
import serial
import http.client as http
import urllib
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(3, False)
# change 1

# GPIO.output(8,False)
# key = 'TOMNWOBTO4BWP8ET'
lrr = []  # array for storing pulse
count = 0  # pulse count
co = 0  # for removing string in serial coming from arduino


def upload_to_ts(val):

    params = urllib.parse.urlencode({'field1': val, 'key': 'TOMNWOBTO4BWP8ET'})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = http.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception:
        print("Connection failed")

    except Keyboardinterrupt:
        print("\nExiting.....")
        exit()


'''
def check_push_button():
    if GPIO.input(5)==0:
        status='true'
    else:
        status='false'
'''
time.sleep(30)
ser = serial.Serial('/dev/ttyACM0', 9600)
print("started")
while True:

    try:
        if GPIO.input(5) == 0:
            GPIO.output(3, True)
            send_alert()
            print("alert send manually")
            time.sleep(50)
            if GPIO.input(5) == 1:
                GPIO.output(3, False)
            GPIO.output(3, False)
            break
        read_serial = ser.readline()
        bpm = read_serial.decode('utf-8').strip()
        co += 1
        if co > 1:
            ss = int(bpm)
            nbpm = ss - 28
            if nbpm > 45 and nbpm < 190:
                print(nbpm)
                lrr.append(nbpm)
                count += 1
                # upload_to_ts(nbpm)
        if count == 20:
            avg_pulse = int(sum(lrr)/len(lrr))
            print("Average pulse rate : ", avg_pulse)
            upload_to_ts(avg_pulse)
            if avg_pulse > 120:
                GPIO.output(3, True)
                time.sleep(10)
                if GPIO.input(5) == 0:
                    GPIO.output(3, False)
                    time.sleep(20)
                else:
                    send_alert()
                    print("Alert send automatically")
                    time.sleep(50)
                    GPIO.output(3, False)
                    break

            count = 0

    except Keyboardinterrupt:
        print("\nExiting.....")
        break
