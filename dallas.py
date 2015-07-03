# This python script is created for the Rasberry Pi utalizing the DS18B20 temperature sensor
# ref: https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/temperature/

import time, json, sys, os, re

# Main process
def main():
	# Prep json variable
	data = {}

	# Get list of directories in /sys/bus/w1/devices/
	directory_path = "/sys/bus/w1/devices/"
	directory_list = os.listdir(directory_path)

	# Search and pull ony matching "XX-XXXXXXXXXXXX", all characters outside the "-" is expected to be HEX
	for directory in directory_list:
		m = re.search(r"[0-9a-fA-F]{2}-[0-9a-fA-F]{12}", directory)

		# If a match is found, do something
		if m:
			# Temperature is stored in a file we need to read from, "/sys/bus/w1/devices/XX-XXXXXXXXXXXX/w1_slave"
			probe = "%s%s/w1_slave" %(directory_path, directory)
			data[directory] = readtemperature(probe)

	# Format information to JSON for easy consumption
	json_data = json.dumps(data)
	
	return(data)

def readtemperature(probe_file):
	# Open file and read contents, store in variable "text"
	tfile = open(probe_file) 
	text = tfile.read() 
	tfile.close()

	# CRC value is stored on the first line
	firstline = text.split("\n")[0]

	# Temperature value is stored on the second line
	secondline = text.split("\n")[1] 

	# CRC data is stored on the 12th word, "YES" = True while "NO" = False
	if firstline.split(" ")[11] == "YES":
		crc_error = False
	else:
		crc_error = True

	# Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
	temperaturedata = secondline.split(" ")[9] 

	# The first two characters are "t=", so get rid of those and convert the temperature from a string to a number. 
	temperature = float(temperaturedata[2:])

	# Places a decimal place where it belongs, data is in Celcius
	celsius = temperature / 1000 

	# Some conversion for fehrenheit
	fahrenheit = 9.0/5.0 * celsius + 32

	# Return as dictionary, will be formating this in JSON
	return({'celsius': round(celsius,2), 'fahrenheit' : round(fahrenheit,2), 'crc error' : crc_error, 'datetime': time.strftime("%Y-%m-%d %H:%M")})

# Start program
if __name__ == '__main__':
	main()
	sys.exit(0)