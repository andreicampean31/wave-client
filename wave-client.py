import RPi.GPIO as GPIO
import serial
import time
import urllib.request
import concurrent.futures
#import I2C_LCD_driver
import sys
import datetime

class SendData:
    def __init__(self, input_pins, port, baud_rate, url):
        self.pins = input_pins
        self.domain_url = url
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
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
        #self.displayL1 = I2C_LCD_driver.lcd()
        #self.displayL1.lcd_clear()
        self.f = open("log.txt", "a")

    def readSensorInput(self, input_pin):
        #time.sleep(0.05)
        if GPIO.input(input_pin):
            time.sleep(5)
            return 1
        #else:
            #time.sleep(0.5)
         #   return "lipsa"

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
        try:
            if(self.serial.inWaiting()>0):
                self.readBarcode()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                t1 = executor.submit(self.readSensorInput, self.pins[0])
                t2 = executor.submit(self.readSensorInput, self.pins[1])
                t3 = executor.submit(self.readSensorInput, self.pins[2])

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
                }, 
                'L3': {
                    'prezenta_obiect': t3.result(),
                    'cod_placa': self.cod_activ['L3'],
                    'id_linie': '3'
                } 
            }
            
            #print(self.barcode_data)
            #print(self.cod_activ)

            #self.displayL1.lcd_clear()
            #self.displayL1.lcd_display_string("Linia 1", 1, 0)
            #self.displayL1.lcd_display_string(sending_data['L1']['cod_placa'], 2, 0)
            #self.displayL1.lcd_clear()
            #time.sleep(1)
            for i in sending_data:          
                if sending_data[i]['cod_placa'] != '':
                    #self.f.write(datetime.datetime.now + " --- " + sending_data[i])
                    
                    if sending_data[i]['prezenta_obiect'] == 1: 
                        print(sending_data[i])
                        #print(sending_data[i])
                        url =  self.domain_url + sending_data[i]['id_linie'] + '&' + sending_data[i]['cod_placa']
                        print(url)
                        #self.f.write(datetime.datetime.now + " --- " + url)
                        urllib.request.urlopen(url)
                        #time.sleep(1)
                else: 
                    #self.displayL1.lcd_clear()
                    #self.displayL1.lcd_display_string("scan barcode", 1, 0)
                    print("scan barcode")
                    #self.f.write(datetime.datetime.now + " --- scan barcode")
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        wait_for_barcode_read = executor.submit(self.readBarcode)
                    #self.displayL1.lcd_clear()
            sending_data['L1']['prezenta_obiect'] = 0
            sending_data['L2']['prezenta_obiect'] = 0
            sending_data['L3']['prezenta_obiect'] = 0
        except KeyboardInterrupt:
            #self.displayL1.lcd_clear()
            sys.exit(0)
            
                    
def main():
    x = SendData([11,12,13], '/dev/ttyACM0', 9600, 'http://192.168.10.80/insert_data/')
    while 1:
        x.sendDataToWeb()

if __name__ == "__main__":
    main()