#!flask/bin/python
 
# This application is for a Rasberry Pi web server that responds with stats via API calls
# Later this may have some sort of GUI to make things pretty...
#
# Last Update by Sean Cline (smcline06@gmail.com)
# Date: 06/23/2015

import ConfigParser, dallas, json
from flask import Flask, request, jsonify

CONFIG_FILE = "config/app.conf"

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
@app.route('/api/temperature', methods=['GET'])
def temperature():
	# Load configuration settings
	config_section_temperature = loadconfig('TEMPERATURE')

	# Define JSON key
	json_data['temperature'] = dallas.main()

	# Add JSON value for temperature probe description if defined in config file
	for key in config_section_temperature.keys():
		if key is not "__name__":
			try:
				# Errors if key does not exsist
				json_data['temperature'][key].update({"description":config_section_temperature.get(key)})
			except:
				# Ignore and move on
				pass

	# Defined in dallas.py script
	return jsonify(json_data)
	#return json.dumps(config_section_temperature)

# Start program
if __name__ == '__main__':
	app.run(host=config_section_webserver.get('host'), port=int(config_section_webserver.get('port')), debug=True)