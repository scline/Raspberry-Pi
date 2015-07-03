#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Python subprogram for local database commands and setup

import sqlite3, sys

# Example JSON
# {'temperature': {'28-041501e81bff': {'fahrenheit': 82.18, 'celsius': 27.88, 'datetime': '2015-07-02 23:48', 'crc error': False, 'description': 'Right Cage'}, '28-031501f5b8ff': {'fahrenheit': 81.5, 'celsius': 27.5, 'datetime': '2015-07-02 23:48', 'crc error': False}, '28-041501e75bff': {'fahrenheit': 82.74, 'celsius': 28.19, 'datetime': '2015-07-02 23:48', 'crc error': False, 'description': 'Middle Cage'}, '28-03150215f2ff': {'fahrenheit': 81.72, 'celsius': 27.63, 'datetime': '2015-07-02 23:48', 'crc error': False}}}

db_table = 'temperature'
db_file = 'local.db'
# Define commands for sql functions
db = sqlite3.connect(db_file)
c = db.cursor()

def main():
    # Testing Things 
    sql = "SELECT * FROM %s" % ( db_table )
    c.execute(sql)
    rows = c.fetchall()

    return

# Start program
if __name__ == '__main__':
    main()
    c.close()    
    sys.exit(0)
#temperature("local.db", "temperature", json['temperature'])