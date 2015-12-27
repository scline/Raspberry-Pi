#!/usr/bin/env python
#-*- coding: UTF-8 -*-
#
# This tracks the number of rotations of the hedgehog wheel. Like an odomiter, writes results to file
# so other processes can read. Output should be JSON

import time, json, sys, os
import RPi.GPIO as io
io.setmode(io.BCM)

# PIN of magnetic sensor
magnetic_pin = 27
readout_file = "/opt/sensor_api/data/odometer.json"

# Required to read sensor state
io.setup(magnetic_pin, io.IN, pull_up_down=io.PUD_UP)

# Variable to track sensor state
state = 0

# Radius of the wheel in meters
radius = 0.1397

# Distance Calculations
distance = 2*3.1416*radius

while True:
	# Variable to count rounds, import if old counter exsists
	if os.path.isfile(readout_file): 
		json_dump = open(readout_file).read()
		json_data = json.loads(json_dump)
		counter = json_data["odometer"]["count"]	
	else:
		counter = 0

	# Connected state
	if io.input(magnetic_pin):
	
		if state == 1:
			counter = counter + 1
			
			# Update local file for counter
			target = open(readout_file, 'w')
			target.write('''{ "odometer": { "count": %i, "distance": { "meters": %i, "miles": %.2f  } } }''' % ( counter, counter*distance, counter*distance*0.00062137 ))
			target.close()

			#print '''{ "odometer": { "count": %i, "distance": { "meters": %i, "miles": %.2f  } } }''' % ( counter, counter*distance, counter*distance*0.00062137 )
			

		state = 0

	# Disconnected state
	else:
		state = 1

	# Performs checks every 0.01 seconds
	time.sleep(0.01)

