#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Python subprogram for local database commands and setup

import sqlite3, sys
from datetime import date, datetime # now = datetime.now()

# [dateTime] - [MAC] - [description] - [CRC] - [celsius] - [fahrenheit]
def temperature(db_file, db_table, json_blob):
	# Define commands for sql functions
    db = sqlite3.connect(db_file)
    c = db.cursor() 

    # Create table if it doesn’t already exist
    sql = 'CREATE TABLE IF NOT EXISTS %s (datetime TIMESTAMP, mac TEXT, crc TEXT, celsius REAL, fahrenheit REAL)'  % ( db_table )
    print sql
    c.execute(sql)

    # Insert data
    sql = "INSERT INTO %s VALUES('%s', 'mac', 'crc', 2.34, 98.5)" % ( db_table, str(datetime.now()) )
    print sql
    c.execute(sql)

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

sql_temperature("local.db", "temperature", "nothing")