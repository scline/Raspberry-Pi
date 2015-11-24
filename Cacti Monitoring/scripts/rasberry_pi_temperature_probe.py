#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Script to pull temperature data from Rasberry Pi probe via API call, this is for cacti monitoring system use only.

import sys, urllib, json

# Script expects one argument, the hostname of the temperature probe for API calls
# python script.py hostname

# API endpoint ip or hostname
HOST = sys.argv[1]

# Cacti commands
# index - list the mac address of each temperature probe
# num_indexes - how manny mac addresses are present in the api call
CMD = sys.argv[2]

# Define Variables
api_data = {}

# Main program run
def main():
	# Load data via API call, store in variable
	api_data = api_call(HOST)

	# If Cacti is requesting index, run the following
	if (CMD == 'index'):
		index(api_data)

	# If cacti is requesting num_index, run the following
	if (CMD == 'num_indexes'):
		num_indexes(api_data)

	if (CMD == 'get'):
		# rasberry_pi_temperature_probe.py 192.168.200.31 get fahrenheit 28-041501e81bff
		get(api_data, sys.argv[3], sys.argv[4])

	if CMD == 'query' and len(sys.argv) > 3:
		query(api_data, sys.argv[3])
	return

# num_indexes - how manny mac addresses are present in the api call
def num_indexes(api_data):
	# Get number of indexes (probe mac addresses)
	print len(api_data['temperature'])

	return 

# index - list the mac address of each temperature probe
def index(api_data):
	# List mac address values for temperature probes, used as index
	for index in api_data['temperature']:
		print index

	return

# get - Pulls variables based on mac/index
def get(api_data, var, index):
	# List mac address values for temperature probes
	print "%s" % ( api_data['temperature'][index][var])

	return

# get - Pulls variables based on mac/index
def query(api_data, var):
	if var == 'index':
		# Lists output of "index:index" for cacti to record index value and order
		for index in api_data['temperature']:
			print "%s|%s" % ( index, index )
	else:
		# Lists output of "index:value" for cacti to record a value related to an index
		for index in api_data['temperature']:
			print "%s|%s" %( index, api_data['temperature'][index][var] )

	return

def api_call(HOST):
	# Get json data from API call, ref http://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
	url = "http://%s/api/temperature/get_cached" % ( HOST )
	response = urllib.urlopen(url);

	# Store json data into variable
	data = json.loads(response.read())

	return data

# Start program
if __name__ == '__main__':
	main()
	sys.exit(0)