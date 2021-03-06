#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Python subprogram for local database commands and setup

import sqlite3, sys

# Example JSON
# {'temperature': {'28-041501e81bff': {'fahrenheit': 82.18, 'celsius': 27.88, 'datetime': '2015-07-02 23:48', 'crc error': False, 'description': 'Right Cage'}, '28-031501f5b8ff': {'fahrenheit': 81.5, 'celsius': 27.5, 'datetime': '2015-07-02 23:48', 'crc error': False}, '28-041501e75bff': {'fahrenheit': 82.74, 'celsius': 28.19, 'datetime': '2015-07-02 23:48', 'crc error': False, 'description': 'Middle Cage'}, '28-03150215f2ff': {'fahrenheit': 81.72, 'celsius': 27.63, 'datetime': '2015-07-02 23:48', 'crc error': False}}}

# Define commands for sql functions

def main(db_file, db_table):
	# Define command shortcuts
	db = sqlite3.connect(db_file)
	c = db.cursor()

	# Testing Things 
	sql = "SELECT * FROM %s" % ( db_table )
	c.execute(sql)
	rows = c.fetchall()

	for row in rows:
		print row

	return

def get_sql(db_file, db_table, sql):
	# SELECT * FROM temperature 
	# WHERE datetime in (
	# SELECT MAX(datetime) as datetime
	# FROM temperature
	# GROUP BY mac);

	return

def temperature(db_file, db_table, json):
	# Define command shortcuts
	db = sqlite3.connect(db_file)
	c = db.cursor()

	# Create table if it doesnt already exist, add unique clause to mac and datetime
	sql = 'CREATE TABLE IF NOT EXISTS %s (datetime TIMESTAMP, mac TEXT, crc TEXT, celsius REAL, fahrenheit REAL, PRIMARY KEY (datetime, mac), UNIQUE (datetime, mac) ON CONFLICT REPLACE)'  % ( db_table )
	c.execute(sql)

	for mac in json:
		# Format JSON and insert into db
		sql = "INSERT INTO %s VALUES('%s', '%s', '%s', %.2f, %.2f)" % (db_table, json[mac]['datetime'], mac, json[mac]['crc error'], json[mac]['celsius'], json[mac]['fahrenheit'])
		c.execute(sql)

	# Save data to database
	db.commit()

	# Testing Things 
	sql = "SELECT * FROM %s" % ( db_table )
	c.execute(sql)
	rows = c.fetchall()

	#for row in rows:
	#	print row

	# Close open connections
	c.close()    

	return 

# Start program
if __name__ == '__main__':
	main("test", "temperature")
	sys.exit(0)
