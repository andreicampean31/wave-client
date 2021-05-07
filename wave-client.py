import threading
from threading import Thread
import time
from serial import Serial
import RPi.GPIO as GPIO
from datetime import datetime
import urllib.request

class input_sensor:
    def __init__(self, input_pin):
        self.pin = input_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_sensor(self):
        if(GPIO.input(self.pin) == True):
            time.sleep(1)
            if(GPIO.input(self.pin) != True):
                return "1 " 
            else:
                return "0! "
        else:
            return "0 "



class barcode_scanner:
    def __init__(self):
        port = '/dev/ttyACM0'
        baud = 9600
        self.serial_port = serial.Serial(port, baud)
        self.thread_running = True
        self.exit_event = threading.Event()
        self.reading = ''
        url = 'http://localhost/'
        

    def insert_DB(self, prezenta_obiect):
        while self.thread_running:
            if(prezenta_obiect == "0 "):
                
                print(prezenta_obiect + self.reading)
            else:
                print(prezenta_obiect + self.reading)
            time.sleep(1)


    def take_input(self, ser):
        self.reading = ser.readline().decode("utf-8")

    def run(self, prezenta_obiect):
        self.thread_running = True
        t1 = Thread(target=self.insert_DB, args=[prezenta_obiect])
        t2 = Thread(target=self.take_input, args=[self.serial_port])
        t1.start()
        t2.start()
        t2.join()  # interpreter will wait until your process get completed or terminated
        self.thread_running = False


        # print('The end')

x = barcode_scanner()
y = input_sensor(12)
while 1:
    x.run(y.read_sensor())
    time.sleep(1)