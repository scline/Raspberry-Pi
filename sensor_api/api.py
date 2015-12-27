#!flask/bin/python
 
# This application is for a Rasberry Pi web server that responds with stats via API calls
# Later this may have some sort of GUI to make things pretty...
#
# Last Update by Sean Cline (smcline06@gmail.com)
# Date: 06/23/2015

import ConfigParser, json
from flask import Flask, request, jsonify
from lib import ds18b20, sql

CONFIG_FILE = "/opt/sensor_api/config/api.conf"

# Load config file and store section in dictionary format
def loadconfig(section):
	config = ConfigParser.ConfigParser()
	config.read(CONFIG_FILE)

	return config._sections[section]

# Define the flask application
app = Flask(__name__)

# Load flask webserver settings for listening port and IP
config_section_webserver = loadconfig('WEBSERVER')

# Define empty JSON
json_data = {}

# Root URL call, point to some homepage
@app.route('/')
def index():
	return "Index Page, or something :)"

# Gets temperature data and displays data as JSON
@app.route('/api/temperature/get', methods=['GET'])
def temperature_get():
	# Load configuration settings
	config_section_temperature = loadconfig('TEMPERATURE')

	# Define JSON key
	json_data['temperature'] = ds18b20.main()

	# Add JSON value for temperature probe description if defined in config file
	for key in config_section_temperature.keys():
		if key is not "__name__":
			try:
				# Errors if key does not exsist
				json_data['temperature'][key].update({"description":config_section_temperature.get(key)})
			except:
				# Ignore and move on
				pass

	# Load cache file data
	config_section_temperature = loadconfig('TEMPERATURE')
	temperature_file = config_section_temperature.get('file')

	# Write output to file
	with open(temperature_file , 'w') as outfile:
		json.dump(json_data, outfile)

	# Defined in ds18b20.py script
	return jsonify(json_data), 200

# Gets temperature data and displays data as JSON, this is pulled from a cached file for quicker polling
@app.route('/api/temperature/get_cached', methods=['GET'])
def temperature_get_cached():

	config_section_temperature = loadconfig('TEMPERATURE')
	temperature_file = config_section_temperature.get('file')

	json_dump = open(temperature_file).read()
	json_data = json.loads(json_dump)

	# Defined in ds18b20.py script
	return jsonify(json_data), 200

# Gets temperature data and displays data as JSON and store in local SQL databace
@app.route('/api/temperature/set', methods=['GET'])
def temperature_set():
	# Load  database configuration settings
	config_section_db = loadconfig('DB')

	# Load configuration settings
	config_section_temperature = loadconfig('TEMPERATURE')

	# Get temperature data from hardware probes, store in json 
	json_data['temperature'] = ds18b20.main()

	# Add JSON value for temperature probe description if defined in config file
	for key in config_section_temperature.keys():
		if key is not "__name__":
			try:
				# Errors if key does not exsist
				json_data['temperature'][key].update({"description":config_section_temperature.get(key)})
			except:
				# Ignore and move on
				pass

	# Pull db name and table name from config file, sql.py will create files if non exsist.
	db_database = config_section_db.get('database_name')
	db_table = config_section_db.get('table_name')

	sql.temperature(db_database, db_table, json_data['temperature'])

	# Defined in ds18b20.py script
	return jsonify(json_data), 200

# Gets odometer data and displays data as JSON
@app.route('/api/odometer/get', methods=['GET'])
def odometer_get():
	# Load configuration settings
	config_section_odometer = loadconfig('ODOMETER')
	odometer_file = config_section_odometer.get('file')

	json_dump = open(odometer_file).read()
	json_data = json.loads(json_dump)

	# Defined in ds18b20.py script
	return jsonify(json_data), 200

# Start program
if __name__ == '__main__':
	app.run(host=config_section_webserver.get('host'), port=int(config_section_webserver.get('port')), debug=True)
