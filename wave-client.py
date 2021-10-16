import serial
import urllib.request

class GetBarcode:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate

        if not self.connect_scanner():
            print("trying to connect to barcode scanner...")
            while not self.connect_scanner():
                pass
        print("barcode scanner connected")
        self.cod_activ = {
            'L1': '',
            'L2': '',
            'L3': '',
            'L2A': '',
            'L3A': ''
        }
        self.barcode_data = {
            'id_linie': '',
            'cod_placa': ''
        }
    def connect_scanner(self):
        try:
            self.scannerSerial = serial.Serial(self.port, self.baud_rate)
            return 1
        except:
            return 0
    def splitBarcode(self, barcode):
        i=1
        j=0
        cod_placa = ''
        id_linie = ''
        print(barcode)
        while i<len(barcode):
            if barcode[i] == '-':
                j=1
                i+=1

            if not j:
                id_linie += barcode[i]
            else:
                cod_placa = cod_placa + barcode[i]
            i+=1
        data = {
            'id_linie': id_linie,
            'cod_placa': cod_placa
        }
        print(data)
        return data

    def readBarcode(self):
        try:
            barcode_read = self.scannerSerial.readline().decode("utf-8").rstrip()
        except:
            print("inavlid format")
        self.barcode_data = self.splitBarcode(barcode_read)
        if self.barcode_data['id_linie'] == '1':
            self.cod_activ['L1'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '2':
            self.cod_activ['L2'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '3':
            self.cod_activ['L3'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '2A':
            self.cod_activ['L2A'] = self.barcode_data['cod_placa']
        elif self.barcode_data['id_linie'] == '3A':
            self.cod_activ['L3A'] = self.barcode_data['cod_placa']

    def inUseBarcodes(self):
        try:
            if self.scannerSerial.inWaiting() > 0:
                self.readBarcode()
                print(self.cod_activ)
            return self.cod_activ
        except:
            print("scanner deconnected")
            if self.connect_scanner():
                print("scanner reconnected")
            return self.cod_activ




class GetSensorInput:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        if not self.connect_to_arduino():
            print("trying to connect to arduino...")
            while not self.connect_to_arduino():
                pass
        print("arduino connected")

    def connect_to_arduino(self):
        try:
            self.arduinoSerial = serial.Serial(self.port, self.baud_rate)
            return 1
        except:
            return 0

    def readSensorInput(self):
        try:
            if self.arduinoSerial.inWaiting() > 0:
                switchState_read = self.arduinoSerial.readline().rstrip().decode('utf-8')
                print(switchState_read)
                return switchState_read
        except:
            print("arduino deconnected")
            print("trying to reconnect to arduino ...")
            while not self.connect_to_arduino():
                pass
            print("arduino reconnected")

class SendDataToWeb:
    def __init__(self, url):
        self.domain_url = url
        self.buffer = []
        #self.barcode_missing = GetBarcode('/dev/ttyACM0', 9600)

    def save_to_buffer(self, url):
        self.buffer.append(url)
        return 1

    def upload_buffer(self):
        if self.buffer != []:
            for count,i in enumerate(self.buffer):
                try:
                    urllib.request.urlopen(i)
                    del self.buffer[count]

                except:
                    pass
            if self.buffer == []:
                print("buffer uploaded and cleared")

    def open_url(self, url):
        try:
            urllib.request.urlopen(url)
        except urllib.error.URLError as err:
            print(err)
            if self.save_to_buffer(url):
                print("saved to buffer")

    def sendData(self, state, barcodes):
        #print(state)
        #print(barcodes)
        self.upload_buffer()
        if state != None:
            linie = 'L'+ state

            if barcodes[linie] != '':
                url = self.domain_url + state + '&' + barcodes[linie]
                print(url)
                print(barcodes)
                print("placa pe L" + state)
                self.open_url(url)
            else:
                print("Scan barcode for " + linie)

def main():
    barcodeScanner = GetBarcode('/dev/cu.usbmodemR4319__1', 9600)
    actualState = GetSensorInput('/dev/cu.usbserial-A50285BI', 9600)
    accessingWeb = SendDataToWeb('http://192.168.1.9:80/wave/insert_data/')

    while 1:
        activeBarcodes = barcodeScanner.inUseBarcodes()
        prezenta = actualState.readSensorInput()
        accessingWeb.sendData(prezenta, activeBarcodes)

if __name__ == "__main__":
    main()
