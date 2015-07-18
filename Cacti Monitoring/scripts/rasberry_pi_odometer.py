#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Script to pull temperature data from Rasberry Pi probe via API call, this is for cacti monitoring system use only.

import sys, urllib, json

# Script expects one argument, the hostname of the temperature probe for API calls
# python script.py hostname

# API endpoint ip or hostname
HOST = sys.argv[1]

# Define Variables
api_data = {}

# Main program run
def main():
	# Load data via API call, store in variable
	api_data = api_call(HOST)

	print "count: %s meters: %s miles: %s" % (api_data['odometer']['count'], api_data['odometer']['distance']['meters'], api_data['odometer']['distance']['meters'] )

	return

# num_indexes - how manny mac addresses are present in the api call
def num_indexes(api_data):
	# Get number of indexes (probe mac addresses)
	print len(api_data['temperature'])

	return

def api_call(HOST):
	# Get json data from API call, ref http://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
	url = "http://%s/api/odometer/get" % ( HOST )
	response = urllib.urlopen(url);

	# Store json data into variable
	data = json.loads(response.read())

	return data

# Start program
if __name__ == '__main__':
	main()
	sys.exit(0)