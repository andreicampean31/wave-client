import serial
import urllib.request

class GetBarcode:
    def __init__(self, port, baud_rate):
        try:
            self.scannerSerial = serial.Serial(port, baud_rate)
            self.cod_activ = {
                'L1': '',
                'L2': '',
                'L3': ''
            }
            self.barcode_data = {
                'id_linie': '',
                'cod_placa': ''
            }
        except:
            print("connect scanner")

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
        barcode_read = self.scannerSerial.readline().decode("utf-8").rstrip()
        self.barcode_data = self.splitBarcode(barcode_read)
        if self.barcode_data['id_linie'] == '1':
            self.cod_activ['L1'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '2':
            self.cod_activ['L2'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '3':
            self.cod_activ['L3'] = self.barcode_data['cod_placa']

    def inUseBarcodes(self):
        try:
            if self.scannerSerial.inWaiting() > 0:
                self.readBarcode()
                #print(self.cod_activ)
            return self.cod_activ
        except:
            print("connect Scanner")
        #else:
         #   return 0



class GetSensorInput:
    def __init__(self, port, baud_rate):
        try:
            self.arduinoSerial = serial.Serial(port, baud_rate)
        except:
            print("connect Arduino")

    def readSensorInput(self):
        try:
            if self.arduinoSerial.inWaiting() > 0:
                switchState_read = self.arduinoSerial.readline().rstrip().decode('utf-8')
                #print(switchState_read)
                return switchState_read
                #if (switchState_read == '1'):
                 #   print('1')
                #elif (switchState_read == '2'):
                 #   print('0')
        except:
            print("connect Arduino")

class SendDataToWeb:
    def __init__(self, url):
        self.domain_url = url
        #self.barcode_missing = GetBarcode('/dev/ttyACM0', 9600)

    def sendData(self, state, barcodes):
        #print(state)
        #print(barcodes)
        if state == '1':
            if barcodes['L1'] != '':
                url = self.domain_url + '1' + '&' + barcodes['L1']
                print(url)
                print(barcodes)
                print("placa pe L1")
                urllib.request.urlopen(url)
            else:
                print("Scan barcode for L1")
        elif state == '2':
            if barcodes['L2'] != '':
                url = self.domain_url + '2' + '&' + barcodes['L2']
                print(url)
                print(barcodes)
                print("placa pe L2")
                urllib.request.urlopen(url)
            else:
                print("Scan barcode for L2")
        elif state == '3':
            if barcodes['L3'] != '':
                url = self.domain_url + '3' + '&' + barcodes['L3']
                print(url)
                print(barcodes)
                print("placa pe L3")
                urllib.request.urlopen(url)
            else:
                print("Scan barcode for L3")

def main():
    barcodeScanner = GetBarcode('/dev/ttyACM0', 9600)
    actualState = GetSensorInput('/dev/ttyUSB0', 9600)
    accessingWeb = SendDataToWeb('http://localhost:8000/wave/insert_data/')

    while 1:
        first_run = 0
        activeBarcodes = barcodeScanner.inUseBarcodes()
        prezenta = actualState.readSensorInput()
        accessingWeb.sendData(prezenta, activeBarcodes)
        #time.sleep(1)

if __name__ == "__main__":
    main()