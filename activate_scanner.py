import subprocess as cmd

print("Conecteaza sacannerul")
x = ''
x = input("Ai conectat scannerul? Daca da apasa pe 1, daca nu te rog sa il conectezi")
while x != '1':
	x = input("Raspuns invalid, incearca din nou:...")

output = cmd.Popen("dmesg | grep ttyACM", shell=True, stdout=cmd.PIPE)
#print(output[1])

output_array = []
for line in output.stdout:
	output_array.append(line)
	#print(line.rstrip())

print(output_array[len(output_array)-1])

last_device = output_array[len(output_array)-1]

port_index = last_device.find(b'ttyACM')
dev_number_index = last_device.find(b'cdc_acm')

port = last_device[port_index:(port_index+7)]
dev_number = last_device[(dev_number_index+8):(dev_number_index+8+5)]

print(dev_number)
print(port)

output = cmd.Popen(b"udevadm info --name=/dev/"+port+b" --attribute-walk", shell=True, stdout=cmd.PIPE)

ok=0
idVendor = b''
idProduct = b''
for line in output.stdout:
#	print(line)

	if line.find(dev_number) > 0:
#		print(dev_number + b":\n")
		if line[-len(dev_number)-3:] == dev_number+b"':\n":
			print("asta e linia")
			ok=1
#			print(line)
	if ok:
		#print(line)
		if line.find(b"idVendor") > 0:
			print(line)
			index = line.find(b'"')
			#print(index)
			if index > 0:
				idVendor = line[index+1:index+5]
			print(idVendor)
		if line.find(b"idProduct") > 0:
			print(line)
			index = line.find(b'"')
			if index > 0:
				idProduct = line[index+1:index+5]
			print(idProduct)
		#print(line)
	if line == b"\n":
		ok=0

f = open("/etc/udev/rules.d/10-usb-serial.rules", "w")

f.write('SUBSYSTEM=="tty", ATTRS{idProduct}=="6001", ATTRS{idVendor}=="0403", SYMLINK+="ttyUSB_ARD"\nSUBSYSTEM=="tty", ATTRS{idProduct}=="'+idProduct.decode("utf-8")+'", ATTRS{idVendor}=="'+idVendor.decode("utf-8")+'", SYMLINK+="ttyACM_BARCODE"')

f.close()

try:
	cmd.Popen("udevadm trigger", shell=True)
	cmd.Popen("ls -l /dev/ttyACM*", shell=True)
	cmd.Popen("ls -l /dev/ttyUSB*", shell=True)
	print("Scanner asociat")
except:
	print("Asociere esuata")

