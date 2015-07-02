#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Python subprogram for local database commands and setup

import sqlite3, sys
from datetime import date, datetime # now = datetime.now()

db_file = "local.db"
db_table = "temperature"

# Define commands for sql functions
db = sqlite3.connect(db_file)
c = db.cursor() 

# [dateTime] - [MAC] - [description] - [CRC] - [celsius] - [fahrenheit]
def sql_temperature(db_table, json_blob):
	# Create table if it doesnt already exsist
    sql = 'CREATE TABLE IF NOT EXSISTS ' + db_table + ' (datetime TIMESTAMP, mac TEXT, crc TEXT, celsius REAL, fahrenheit REAL)'
    c.execute(sql)




    c.commit()
    c.close()
    return 

create_table("test", "nothing")