# Raspberry-Pi Wireless Temperature Sensor
This program exposes two different types of temperature sensors used by the custom [Temperature Hat](https://github.com/scline/Raspberry-Pi-Temperature-Hat) printed circuit board.

## Installation Instructions
### Operating System
The followin instructions are for getting this hat to work using the [Raspbian](https://www.raspbian.org/) Linux Debian based operating system. At the time of writing this we are using the latest version based on kernal 4.1.x. There are manny [online guides](https://www.raspberrypi.org/documentation/installation/installing-images/) how to perform this step.

### System Files

The following change allows the DS18B20 temperature sensor to pull data from GPIO Pin 03 instead of the default GPIO Pin 04. 
Edit "/boot/config.txt" and add the following line
```
dtoverlay=w1-gpio,gpiopin=3
```
In order to load the required modules we need to edit the "/etc/modules" file and add the following lines. Some of these may already exsist.
```
snd-bcm2835
w1-gpio
w1-therm
```
Then reboot the system so the settings take affect.


---NEEDS UPDATING---
You can validate temperature sensors are being read by running "ls /sys/bus/w1/devices/". You should see folders "XX-XXXXXXXXXXXX", one for each temperature sensor. These are also the serial numbers per device.


## API Calls

### http:{ip}/api/temperature/get
Gets all temperature readings from all attached probes. This call takes ~5sec per attached probe.
```
{
  "temperature": {
    "28-031501edd7ff": {
      "celsius": 24.56, 
      "crc error": false, 
      "datetime": "2015-12-26 23:16", 
      "fahrenheit": 76.21
    }
  }
}
```

### http:{ip}/api/temperature/get_cached
Gets all temperature readings the most recent cached data, cached data is created when running the '/api/temperature/get' call. And easy way to always have recent data is to cron a curl command. Cached calls are near-instant. 
```
{
  "temperature": {
    "28-031501edd7ff": {
      "celsius": 24.56, 
      "crc error": false, 
      "datetime": "2015-12-26 23:16", 
      "fahrenheit": 76.21
    }
  }
}

### http:{ip}/api/temperature/set
TBA

### http:{ip}/api/odometer/get
TBA
