#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This python script is created for the Rasberry Pi utalizing the DHT22 temperature sensor
# ref: https://github.com/adafruit/Adafruit_Python_DHT

import time, json, sys, os, Adafruit_DHT

# Main process
def main():
    # Prep json variable
    data = {}

    # Move to config eventually
    sensor = Adafruit_DHT.DHT22
    pin = 4

    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    humidity, celsius = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and celsius is not None:
        # Some conversion for fehrenheit
        fahrenheit = 9.0/5.0 * celsius + 32

        # Manually assign good CRC
        crc_error = "false"
    else:
        # Failed to get pull, zero-ize data and flag CRC
        fahrenheit = 0
        crc_error = "true"
        humidity = 0
        celsius = 0

    # Return as dictionary, will be formating this in JSON
    return({'dht22': {'celsius': round(celsius,2), 'fahrenheit' : round(fahrenheit,2), 'humidity' : round(humidity,2), 'crc error' : crc_error, 'datetime': time.strftime("%Y-%m-%d %H:%M")} })

# Start program
if __name__ == '__main__':
    main()
    sys.exit(0)