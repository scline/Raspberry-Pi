#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Python subprogram for local database commands and setup

import sqlite3, sys

# Example JSON
# {'temperature': {'28-041501e81bff': {'fahrenheit': 82.18, 'celsius': 27.88, 'dateime': '2015-07-02 23:48', 'crc error': False, 'description': 'Right Cage'}, '28-031501f5b8ff': {'fahrenheit': 81.5, 'celsius': 27.5, 'dateime': '2015-07-02 23:48', 'crc error': False}, '28-041501e75bff': {'fahrenheit': 82.74, 'celsius': 28.19, 'dateime': '2015-07-02 23:48', 'crc error': False, 'description': 'Middle Cage'}, '28-03150215f2ff': {'fahrenheit': 81.72, 'celsius': 27.63, 'dateime': '2015-07-02 23:48', 'crc error': False}}}


# [dateTime] - [MAC] - [description] - [CRC] - [celsius] - [fahrenheit]
def temperature(db_file, db_table, json):
	# Define commands for sql functions
    db = sqlite3.connect(db_file)
    c = db.cursor() 

    # Create table if it doesn’t already exist
    sql = 'CREATE TABLE IF NOT EXISTS %s (datetime TIMESTAMP, mac TEXT, crc TEXT, celsius REAL, fahrenheit REAL)'  % ( db_table )
    c.execute(sql)

    for mac in json:
        print "MAC = %s" % mac
        for entry in json[mac]:
            print "fahrenheit = %s" % json[mac][entry]['fahrenheit']
            print "fahrenheit = %s" % json[mac][entry]['celsius']
            print "fahrenheit = %s" % json[mac][entry]['datetime']
            print "fahrenheit = %s" % json[mac][entry]['crc error']

    # Insert data
    #sql = "INSERT INTO %s VALUES('', 'mac', 'crc', 2.34, 98.5)" % ( db_table )
    #print sql
    #c.execute(sql)

    # Save data to database
    db.commit()

    # Testing Things 
    sql = "SELECT * FROM %s" % ( db_table )
    c.execute(sql)
    rows = c.fetchall()
    
    for row in rows:
        print row
    
    # Close open connections
    c.close()    

    return 

json = {'temperature': {'28-041501e81bff': {'fahrenheit': 82.18, 'celsius': 27.88, 'dateime': '2015-07-02 23:48', 'crc error': False, 'description': 'Right Cage'}, '28-031501f5b8ff': {'fahrenheit': 81.5, 'celsius': 27.5, 'dateime': '2015-07-02 23:48', 'crc error': False}, '28-041501e75bff': {'fahrenheit': 82.74, 'celsius': 28.19, 'dateime': '2015-07-02 23:48', 'crc error': False, 'description': 'Middle Cage'}, '28-03150215f2ff': {'fahrenheit': 81.72, 'celsius': 27.63, 'dateime': '2015-07-02 23:48', 'crc error': False}}}

temperature("local.db", "temperature", json['temperature'])