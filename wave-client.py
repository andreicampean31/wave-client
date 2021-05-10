import RPi.GPIO as GPIO
import serial
import time
import urllib.request
import concurrent.futures

class SendData:
    def __init__(self, input_pins, port, baud_rate, url):
        self.pins = input_pins
        self.domain_url = url
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.cod_activ = {
            'L1': '',
            'L2': '',
            'L3': ''
        }
        #port = port #'/dev/ttyACM0'
        #baud = baud_rate #9600
        self.serial = serial.Serial(port, baud_rate)
        self.barcode_data = {
            'id_linie': '',
            'cod_placa': ''
        }

    def readSensorInput(self, input_pin):
        if GPIO.input(input_pin):
            time.sleep(0.1)
            return "lipsa"
        else:
            time.sleep(0.1)
            if(GPIO.input(input_pin)):
                return "obiect"
            else:
                return "stationare"

    def splitBarcode(self, barcode):
        i=5
        cod_placa = ''
        while i<len(barcode):
            cod_placa = cod_placa + barcode[i]
            i+=1
        data = {
            'id_linie': barcode[1],
            'cod_placa': cod_placa
        }    
        return data
        
    def readBarcode(self):
        barcode_read = self.serial.readline().decode("utf-8")
        self.barcode_data = self.splitBarcode(barcode_read)
        if self.barcode_data['id_linie'] == '1':
            self.cod_activ['L1'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '2':
            self.cod_activ['L2'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '3':
            self.cod_activ['L3'] = self.barcode_data['cod_placa']

    
    def sendDataToWeb(self):
        if(self.serial.inWaiting()>0):
            self.readBarcode()
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            t1 = executor.submit(self.readSensorInput, self.pins[0])
            t2 = executor.submit(self.readSensorInput, self.pins[1])
            #t3 = executor.submit(self.readSensorInput, self.pins[2])

        sending_data = {
            'L1': {
                'prezenta_obiect': t1.result(),
                'cod_placa': self.cod_activ['L1'],
                'id_linie': '1'
            },
            'L2': {
                'prezenta_obiect': t2.result(),
                'cod_placa': self.cod_activ['L2'],
                'id_linie': '2'
            } 
            #'L3': t3.result()
        }
        
        print(self.barcode_data)
        #print(self.cod_activ)
        for i in sending_data:
            print(sending_data[i])

        for i in sending_data:
            if sending_data[i]['prezenta_obiect'] == 'obiect':
                url =  self.domain_url + sending_data[i]['id_linie'] + '&' + sending_data[i]['cod_placa']
                print(url)
                urllib.request.urlopen(url)

x = SendData([11,12], '/dev/ttyACM0', 9600, 'http://192.168.1.4:8000/insert_data/')
while 1:
    x.sendDataToWeb()