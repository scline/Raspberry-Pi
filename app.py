#!flask/bin/python
 
# This application is for a Rasberry Pi web server that responds with stats via API calls
# Later this may have some sort of GUI to make things pretty...
#
# Last Update by Sean Cline (smcline06@gmail.com)
# Date: 06/23/2015

import ConfigParser, sqlite3, dallas, json, sql
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
@app.route('/api/temperature/get', methods=['GET'])
def temperature_get():
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

# Gets temperature data and displays data as JSON
@app.route('/api/temperature/set', methods=['GET'])
def temperature_set():
	# Load  database configuration settings
	config_section_db = loadconfig('DB')

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

	db_database = config_section_db.get('database_name')
	db_table = config_section_db.get('table_name')

	print json_data
	temperature(db_database, db_table, json_data)

	# Defined in dallas.py script
	return jsonify(json_data)
	#return json.dumps(config_section_temperature)

def temperature(db_file, db_table, json):
	# Define commands for sql functions
	db = sqlite3.connect(db_file)
	c = db.cursor() 

	# Create table if it doesnt already exist
	sql = 'CREATE TABLE IF NOT EXISTS %s (datetime TIMESTAMP, mac TEXT, crc TEXT, celsius REAL, fahrenheit REAL)'  % ( db_table )
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

	for row in rows:
		print row

	# Close open connections
	c.close()    

	return 

# Start program
if __name__ == '__main__':
	app.run(host=config_section_webserver.get('host'), port=int(config_section_webserver.get('port')), debug=True)